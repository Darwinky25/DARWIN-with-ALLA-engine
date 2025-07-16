# ==============================================================================
# semantic_cascade_engine.py
# ALLA Semantic Cascade Learning System
# 
# Hukum Rantai Makna (Law of Semantic Propagation):
# "Setiap kata adalah simpul makna yang membawa serta semua konsep, relasi, 
#  dan entitas yang saling terhubung dengannya."
# ==============================================================================

import re
import json
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class SemanticNode:
    """Simpul dalam graph semantik."""
    word: str
    word_type: str
    definition: str
    relations: Dict[str, List[str]] = field(default_factory=dict)
    depth: int = 0
    confidence: float = 1.0
    source: str = "user"  # user, internet, cascade

@dataclass
class CascadeResult:
    """Hasil dari proses cascade learning."""
    root_word: str
    total_concepts_learned: int
    new_words: List[str]
    relations_discovered: int
    cascade_depth: int
    learning_tree: Dict[str, List[str]]

class SemanticCascadeEngine:
    """
    Engine yang mengimplementasikan pembelajaran cascade semantic.
    
    Ketika ALLA belajar satu kata, engine ini akan:
    1. Extract semua entitas dan relasi dari definisi
    2. Belajar semua kata baru yang ditemukan
    3. Membangun graph semantik lengkap
    4. Melakukan cascade learning dengan depth limit
    """
    
    def __init__(self, alla_engine, max_depth: int = 3):
        self.alla = alla_engine
        self.max_depth = max_depth
        self.semantic_graph: Dict[str, SemanticNode] = {}
        self.learning_history: List[CascadeResult] = []
        
        # Pattern untuk extract entitas dan relasi
        self.relation_patterns = {
            'is_a': [r'is a (.+)', r'is an (.+)', r'type of (.+)'],
            'has_part': [r'has (.+)', r'contains (.+)', r'consists of (.+)'],
            'does': [r'does (.+)', r'performs (.+)', r'carries out (.+)'],
            'needs': [r'needs (.+)', r'requires (.+)', r'depends on (.+)'],
            'produces': [r'produces (.+)', r'creates (.+)', r'makes (.+)'],
            'found_in': [r'found in (.+)', r'located in (.+)', r'grows in (.+)'],
            'used_for': [r'used for (.+)', r'serves to (.+)', r'helps (.+)'],
            'causes': [r'causes (.+)', r'leads to (.+)', r'results in (.+)'],
            'discovered_by': [r'discovered by (.+)', r'invented by (.+)', r'created by (.+)'],
            'occurs_in': [r'occurs in (.+)', r'happens in (.+)', r'takes place in (.+)']
        }
        
        # Entity extraction patterns
        self.entity_patterns = [
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b',  # Proper nouns
            r'\b([a-z]+(?:tion|ism|ity|ness|ment|ance|ence))\b',  # Abstract nouns
            r'\b([a-z]+(?:ing|ed))\b',  # Verbs
            r'\b([a-z]+(?:ic|al|ous|ful|less|able))\b'  # Adjectives
        ]
    
    def cascade_learn(self, word: str, definition: str, word_type: str, source: str = "user") -> CascadeResult:
        """
        Melakukan cascade learning dari satu kata.
        
        Args:
            word: Kata yang akan dipelajari
            definition: Definisi kata
            word_type: Tipe kata (noun, property, etc.)
            source: Sumber pembelajaran (user, internet, cascade)
            
        Returns:
            CascadeResult dengan detail pembelajaran cascade
        """
        print(f"\n🌊 MEMULAI CASCADE LEARNING untuk '{word}'")
        print(f"   Definisi: {definition}")
        print(f"   Max depth: {self.max_depth}")
        
        # Initialize cascade result
        result = CascadeResult(
            root_word=word,
            total_concepts_learned=0,
            new_words=[],
            relations_discovered=0,
            cascade_depth=0,
            learning_tree={}
        )
        
        # Set untuk tracking kata yang sudah diproses
        processed_words = set()
        
        # Queue untuk breadth-first cascade learning
        learning_queue = [(word, definition, word_type, source, 0)]
        
        while learning_queue and result.cascade_depth < self.max_depth:
            current_word, current_def, current_type, current_source, depth = learning_queue.pop(0)
            
            if current_word in processed_words:
                continue
                
            processed_words.add(current_word)
            result.cascade_depth = max(result.cascade_depth, depth)
            
            print(f"\n  🔍 DEPTH {depth}: Memproses '{current_word}'")
            
            # Extract entities dan relations dari definisi
            entities, relations = self._extract_semantic_content(current_def)
            
            # Buat semantic node
            node = SemanticNode(
                word=current_word,
                word_type=current_type,
                definition=current_def,
                relations=relations,
                depth=depth,
                source=current_source
            )
            
            self.semantic_graph[current_word] = node
            
            # Tambahkan ke ALLA's lexicon jika belum ada
            if not self.alla.lexicon.get_entry(current_word):
                self._add_to_alla_lexicon(current_word, current_type, current_def)
                result.new_words.append(current_word)
                result.total_concepts_learned += 1
                print(f"    ✅ Ditambahkan ke lexicon: {current_word}")
            
            # Count relations
            total_relations = sum(len(rel_list) for rel_list in relations.values())
            result.relations_discovered += total_relations
            
            # Build learning tree
            if current_word not in result.learning_tree:
                result.learning_tree[current_word] = []
            
            # Process discovered entities for next depth level
            if depth < self.max_depth - 1:
                for entity in entities:
                    if entity not in processed_words and len(entity) > 2:  # Skip very short words
                        # Coba dapatkan definisi untuk entity ini
                        entity_def = self._get_entity_definition(entity)
                        if entity_def:
                            entity_type = self._classify_entity_type(entity, entity_def)
                            learning_queue.append((entity, entity_def, entity_type, "cascade", depth + 1))
                            result.learning_tree[current_word].append(entity)
                            print(f"      🔗 Menemukan entitas baru: {entity}")
        
        # Save cascade result
        self.learning_history.append(result)
        
        print(f"\nCASCADE LEARNING COMPLETED!")
        print(f"   Root word: {result.root_word}")
        print(f"   Total konsep dipelajari: {result.total_concepts_learned}")
        print(f"   Kata baru: {len(result.new_words)}")
        print(f"   Relasi ditemukan: {result.relations_discovered}")
        print(f"   Depth tercapai: {result.cascade_depth}")
        
        return result
    
    def _extract_semantic_content(self, definition: str) -> Tuple[List[str], Dict[str, List[str]]]:
        """Extract entities dan relations dari definisi."""
        entities = set()
        relations = {}
        
        definition_lower = definition.lower()
        
        # Extract relations menggunakan patterns
        for relation_type, patterns in self.relation_patterns.items():
            relations[relation_type] = []
            for pattern in patterns:
                matches = re.findall(pattern, definition_lower)
                for match in matches:
                    # Clean up match
                    cleaned = self._clean_extracted_text(match)
                    if cleaned:
                        relations[relation_type].append(cleaned)
                        # Add words from relation as entities
                        entities.update(cleaned.split())
        
        # Extract entities menggunakan patterns
        for pattern in self.entity_patterns:
            matches = re.findall(pattern, definition)
            for match in matches:
                cleaned = self._clean_extracted_text(match)
                if cleaned and len(cleaned) > 2:
                    entities.add(cleaned)
        
        # Extract nouns (simple approach)
        words = re.findall(r'\b[a-z]+\b', definition_lower)
        for word in words:
            if len(word) > 3 and word not in ['that', 'this', 'with', 'from', 'they', 'them', 'their', 'have', 'been', 'were', 'will', 'would', 'could', 'should']:
                entities.add(word)
        
        # Remove relations that are empty
        relations = {k: v for k, v in relations.items() if v}
        
        return list(entities), relations
    
    def _clean_extracted_text(self, text: str) -> str:
        """Bersihkan text yang di-extract."""
        # Remove articles, prepositions, etc.
        stop_words = {'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        words = text.strip().split()
        cleaned_words = [w for w in words if w.lower() not in stop_words]
        return ' '.join(cleaned_words)
    
    def _get_entity_definition(self, entity: str) -> Optional[str]:
        """Dapatkan definisi untuk entity (simplified)."""
        # Check if already in ALLA's lexicon
        existing_entry = self.alla.lexicon.get_entry(entity)
        if existing_entry:
            return existing_entry.meaning_expression
        
        # Try autonomous learning if available
        if hasattr(self.alla, 'autonomous_learning_enabled') and self.alla.autonomous_learning_enabled:
            if hasattr(self.alla, 'attempt_autonomous_learning'):
                success = self.alla.attempt_autonomous_learning(entity, f"cascade learning from semantic analysis")
                if success:
                    new_entry = self.alla.lexicon.get_entry(entity)
                    if new_entry:
                        return new_entry.meaning_expression
        
        # Simplified definitions for common entities
        simple_definitions = {
            'organism': 'a living thing',
            'process': 'a series of actions or steps',
            'energy': 'the ability to do work',
            'light': 'electromagnetic radiation visible to humans',
            'water': 'a clear liquid essential for life',
            'oxygen': 'a gas essential for breathing',
            'carbon': 'a chemical element found in all living things',
            'cell': 'the basic unit of life',
            'plant': 'a living organism that makes its own food',
            'animal': 'a living organism that moves and eats other organisms'
        }
        
        return simple_definitions.get(entity.lower())
    
    def _classify_entity_type(self, entity: str, definition: str) -> str:
        """Klasifikasi tipe entity berdasarkan kata dan definisi."""
        definition_lower = definition.lower()
        entity_lower = entity.lower()
        
        # Social words
        if any(word in definition_lower for word in ['greeting', 'hello', 'goodbye', 'thank', 'please']):
            return 'social'
        
        # Properties/adjectives
        if any(word in definition_lower for word in ['color', 'size', 'quality', 'characteristic']) or entity_lower.endswith(('ful', 'less', 'ous', 'ic', 'al')):
            return 'property'
        
        # Actions/verbs
        if any(word in definition_lower for word in ['action', 'process', 'activity']) or entity_lower.endswith(('ing', 'tion', 'ment')):
            return 'action'
        
        # Relations
        if any(word in definition_lower for word in ['between', 'relationship', 'connection']):
            return 'relation'
        
        # Default to noun
        return 'noun'
    
    def _add_to_alla_lexicon(self, word: str, word_type: str, definition: str):
        """Tambahkan kata ke ALLA's lexicon."""
        try:
            # Generate appropriate expression based on type
            if word_type == 'social':
                expression = f"lambda: '{definition}'"
            elif word_type == 'property':
                expression = f"lambda obj: hasattr(obj, '{word}') or '{word}' in str(obj).lower()"
            elif word_type == 'action':
                expression = f"lambda: 'performing {word}'"
            elif word_type == 'noun':
                expression = f"lambda obj: getattr(obj, 'type', '').lower() == '{word}' or '{word}' in str(obj).lower()"
            else:
                expression = f"lambda: '{definition}'"
            
            # Create meaning function
            meaning_function = eval(expression)
            
            # Create WordEntry
            from alla_engine import WordEntry
            entry = WordEntry(
                word=word,
                word_type=word_type,
                meaning_expression=expression,
                meaning_function=meaning_function
            )
            
            # Add to lexicon
            self.alla.lexicon.add_entry(entry)
            
        except Exception as e:
            print(f"    Warning: Error adding {word} to lexicon: {e}")
    
    def get_semantic_graph_for_word(self, word: str) -> Optional[Dict]:
        """Dapatkan semantic graph untuk kata tertentu."""
        if word not in self.semantic_graph:
            return None
        
        node = self.semantic_graph[word]
        return {
            'word': node.word,
            'type': node.word_type,
            'definition': node.definition,
            'relations': node.relations,
            'depth': node.depth,
            'source': node.source
        }
    
    def get_cascade_statistics(self) -> Dict:
        """Dapatkan statistik cascade learning."""
        if not self.learning_history:
            return {'total_cascades': 0}
        
        total_concepts = sum(result.total_concepts_learned for result in self.learning_history)
        total_relations = sum(result.relations_discovered for result in self.learning_history)
        avg_depth = sum(result.cascade_depth for result in self.learning_history) / len(self.learning_history)
        
        return {
            'total_cascades': len(self.learning_history),
            'total_concepts_learned': total_concepts,
            'total_relations_discovered': total_relations,
            'average_cascade_depth': avg_depth,
            'semantic_graph_size': len(self.semantic_graph),
            'recent_cascades': [result.root_word for result in self.learning_history[-5:]]
        }
    
    def visualize_learning_tree(self, root_word: str) -> str:
        """Visualisasi tree pembelajaran untuk debugging."""
        result = None
        for cascade_result in self.learning_history:
            if cascade_result.root_word == root_word:
                result = cascade_result
                break
        
        if not result:
            return f"No cascade found for '{root_word}'"
        
        tree_str = f"🌳 LEARNING TREE for '{root_word}':\n"
        tree_str += f"├── Total concepts: {result.total_concepts_learned}\n"
        tree_str += f"├── Relations found: {result.relations_discovered}\n"
        tree_str += f"└── Cascade depth: {result.cascade_depth}\n\n"
        
        def _build_tree_recursive(word: str, indent: str = ""):
            nonlocal tree_str
            if word in result.learning_tree:
                children = result.learning_tree[word]
                for i, child in enumerate(children):
                    is_last = i == len(children) - 1
                    connector = "└── " if is_last else "├── "
                    tree_str += f"{indent}{connector}{child}\n"
                    
                    next_indent = indent + ("    " if is_last else "│   ")
                    _build_tree_recursive(child, next_indent)
        
        _build_tree_recursive(root_word)
        return tree_str
    
    def save_semantic_graph(self, filepath: str):
        """Simpan semantic graph ke file."""
        graph_data = {}
        for word, node in self.semantic_graph.items():
            graph_data[word] = {
                'word_type': node.word_type,
                'definition': node.definition,
                'relations': node.relations,
                'depth': node.depth,
                'source': node.source
            }
        
        with open(filepath, 'w') as f:
            json.dump(graph_data, f, indent=2)
        
        print(f"📁 Semantic graph saved to {filepath}")


class ALLACascadeIntegration:
    """
    Integrasi SemanticCascadeEngine dengan ALLA.
    """
    
    def __init__(self, alla_engine):
        self.alla = alla_engine
        self.cascade_engine = SemanticCascadeEngine(alla_engine)
        self.cascade_enabled = False
    
    def enable_cascade_learning(self):
        """Aktifkan cascade learning."""
        self.cascade_enabled = True
        return "🌊 Cascade learning ENABLED - ALLA will now learn semantic networks, not just isolated words!"
    
    def disable_cascade_learning(self):
        """Nonaktifkan cascade learning."""
        self.cascade_enabled = False
        return "🌊 Cascade learning DISABLED - ALLA will learn words individually."
    
    def cascade_learn_word(self, word: str, definition: str, word_type: str, source: str = "user") -> CascadeResult:
        """Interface untuk cascade learning."""
        if not self.cascade_enabled:
            # Fallback to normal learning
            if not self.alla.lexicon.get_entry(word):
                self.cascade_engine._add_to_alla_lexicon(word, word_type, definition)
            return CascadeResult(
                root_word=word,
                total_concepts_learned=1,
                new_words=[word],
                relations_discovered=0,
                cascade_depth=0,
                learning_tree={word: []}
            )
        
        return self.cascade_engine.cascade_learn(word, definition, word_type, source)
    
    def get_cascade_stats(self):
        """Dapatkan statistik cascade learning."""
        return self.cascade_engine.get_cascade_statistics()
    
    def visualize_cascade(self, word: str):
        """Visualisasi cascade untuk kata tertentu."""
        return self.cascade_engine.visualize_learning_tree(word)
