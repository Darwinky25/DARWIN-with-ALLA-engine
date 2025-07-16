# ==============================================================================
# semantic_bootstrapper.py
# ALLA Semantic Bootstrapping Engine (SBE)
# 
# "From one word, learn all words in its definition and build semantic networks"
# ==============================================================================

import re
import json
import requests
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field
from pathlib import Path
import time
from collections import deque, defaultdict

@dataclass
class ConceptNode:
    """Node in the concept graph."""
    word: str
    definition: str
    word_type: str
    bootstrap_depth: int = 0
    confidence: float = 1.0
    source: str = "user"
    related_concepts: Set[str] = field(default_factory=set)
    parent_concepts: Set[str] = field(default_factory=set)
    learned_timestamp: float = field(default_factory=time.time)

@dataclass
class BootstrapResult:
    """Result of the bootstrapping process."""
    root_word: str
    total_words_learned: int
    concept_graph_size: int
    max_depth_reached: int
    new_connections: int
    learning_tree: Dict[str, List[str]]
    bootstrap_time: float

class SemanticBootstrapper:
    """
    Engine that implements semantic bootstrapping.
    
    CORE PRINCIPLE: "Language is the operating system of intellect"
    
    Process:
    1. Input: 1 word
    2. Extract all words from its definition
    3. Recursive learning with depth limit
    4. Build concept graph
    5. Form semantic network
    6. Enable reasoning through connections
    """
    
    def __init__(self, alla_engine, max_depth: int = 3, confidence_threshold: float = 0.6):
        self.alla = alla_engine
        self.max_depth = max_depth
        self.confidence_threshold = confidence_threshold
        
        # Core data structures
        self.concept_graph: Dict[str, ConceptNode] = {}
        self.bootstrap_history: List[BootstrapResult] = []
        
        # Learning tracking
        self.current_session_words: Set[str] = set()
        self.graph_file = Path("concept_graph.json")
        self.bootstrap_log_file = Path("bootstrap_log.json")
        
        # Word extraction patterns
        self.important_word_patterns = [
            r'\b([a-z]{4,}(?:tion|sion|ment|ness|ity|ism|ogy|phy))\b',  # Abstract nouns
            r'\b([a-z]{3,}(?:ing|ed|er|est))\b',  # Verbs, comparatives
            r'\b([A-Z][a-z]{2,})\b',  # Proper nouns
            r'\b([a-z]{3,})\b'  # General words 3+ chars
        ]
        
        # Stopwords to filter out
        self.stopwords = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after',
            'above', 'below', 'between', 'among', 'under', 'over', 'within',
            'this', 'that', 'these', 'those', 'here', 'there', 'where', 'when',
            'how', 'why', 'what', 'which', 'who', 'whom', 'whose',
            'a', 'an', 'some', 'any', 'each', 'every', 'all', 'both', 'either',
            'neither', 'many', 'much', 'few', 'little', 'more', 'most', 'less',
            'least', 'several', 'enough', 'such', 'same', 'other', 'another',
            'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',
            'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'may', 'might', 'must', 'can', 'shall'
        }
        
        self.load_concept_graph()
    
    def bootstrap_word(self, word: str, source: str = "user") -> BootstrapResult:
        """
        MAIN SEMANTIC BOOTSTRAPPING FUNCTION
        
        Complete process:
        1. Get word definition
        2. Extract all important words
        3. Recursive learning up to max_depth
        4. Build concept graph
        5. Update connections
        """
        start_time = time.time()
        
        print(f"\nStarting semantic bootstrapping for '{word}'")
        print(f"   Max depth: {self.max_depth}")
        print(f"   Source: {source}")
        
        # Initialize result tracking
        result = BootstrapResult(
            root_word=word,
            total_words_learned=0,
            concept_graph_size=len(self.concept_graph),
            max_depth_reached=0,
            new_connections=0,
            learning_tree={},
            bootstrap_time=0.0
        )
        
        # Reset session tracking
        self.current_session_words.clear()
        
        # BFS queue: (word, definition, parent_word, depth)
        learning_queue = deque()
        processed_words = set()
        
        # Get initial definition
        initial_definition = self._get_word_definition(word)
        if not initial_definition:
            print(f"Could not get definition for '{word}'")
            return result
        
        # Start bootstrapping
        learning_queue.append((word, initial_definition, None, 0))
        
        while learning_queue and len(processed_words) < 100:  # Safety limit
            current_word, definition, parent_word, depth = learning_queue.popleft()
            
            if current_word in processed_words or depth > self.max_depth:
                continue
            
            processed_words.add(current_word)
            result.max_depth_reached = max(result.max_depth_reached, depth)
            
            print(f"\n  DEPTH {depth}: Bootstrap '{current_word}'")
            print(f"      Definition: {definition[:100]}...")
            
            # Create or update concept node
            concept_node = self._create_concept_node(current_word, definition, depth, source)
            self.concept_graph[current_word] = concept_node
            
            # Add to ALLA's lexicon if not exists
            if not self.alla.lexicon.get_entry(current_word):
                word_type = self._classify_word_type(current_word, definition)
                self._add_to_alla_lexicon(current_word, word_type, definition)
                self.current_session_words.add(current_word)
                result.total_words_learned += 1
                print(f"      ✅ Ditambahkan ke lexicon: {current_word} ({word_type})")
            
            # Extract important words from definition
            important_words = self._extract_important_words(definition)
            print(f"      🔗 Menemukan {len(important_words)} kata penting: {important_words[:5]}...")
            
            # Update learning tree
            if current_word not in result.learning_tree:
                result.learning_tree[current_word] = []
            
            # Add parent-child relationship
            if parent_word:
                if parent_word not in result.learning_tree:
                    result.learning_tree[parent_word] = []
                result.learning_tree[parent_word].append(current_word)
                
                # Update concept graph connections
                if parent_word in self.concept_graph:
                    self.concept_graph[parent_word].related_concepts.add(current_word)
                    self.concept_graph[current_word].parent_concepts.add(parent_word)
                    result.new_connections += 1
            
            # Queue important words for next depth level
            if depth < self.max_depth:
                for imp_word in important_words:
                    if imp_word not in processed_words and len(imp_word) > 2:
                        word_definition = self._get_word_definition(imp_word)
                        if word_definition:
                            learning_queue.append((imp_word, word_definition, current_word, depth + 1))
        
        # Finalize result
        result.concept_graph_size = len(self.concept_graph)
        result.bootstrap_time = time.time() - start_time
        
        # Save results
        self.bootstrap_history.append(result)
        self.save_concept_graph()
        self._log_bootstrap_session(result)
        
        print(f"\nSEMANTIC BOOTSTRAPPING COMPLETED!")
        print(f"   Root word: {result.root_word}")
        print(f"   Total kata dipelajari: {result.total_words_learned}")
        print(f"   Concept graph size: {result.concept_graph_size}")
        print(f"   Max depth: {result.max_depth_reached}")
        print(f"   New connections: {result.new_connections}")
        print(f"   Bootstrap time: {result.bootstrap_time:.2f}s")
        
        return result
    
    def _get_word_definition(self, word: str) -> Optional[str]:
        """Dapatkan definisi kata dari berbagai sumber."""
        # 1. Check ALLA's existing lexicon
        existing_entry = self.alla.lexicon.get_entry(word)
        if existing_entry and hasattr(existing_entry, 'definition'):
            return existing_entry.definition
        
        # 2. Try autonomous learning if available
        if hasattr(self.alla, 'autonomous_learning_enabled') and self.alla.autonomous_learning_enabled:
            if hasattr(self.alla, 'attempt_autonomous_learning'):
                success = self.alla.attempt_autonomous_learning(word, "semantic bootstrapping")
                if success:
                    new_entry = self.alla.lexicon.get_entry(word)
                    if new_entry and hasattr(new_entry, 'definition'):
                        return new_entry.definition
        
        # 3. Try direct API calls
        try:
            # Free Dictionary API
            response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}", timeout=3)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    entry = data[0]
                    if 'meanings' in entry and len(entry['meanings']) > 0:
                        meaning = entry['meanings'][0]
                        if 'definitions' in meaning and len(meaning['definitions']) > 0:
                            return meaning['definitions'][0].get('definition', '')
        except:
            pass
        
        # 4. Wikipedia summary
        try:
            response = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{word}", timeout=3)
            if response.status_code == 200:
                data = response.json()
                if 'extract' in data and data['extract']:
                    return data['extract']
        except:
            pass
        
        # 5. Simple fallback definitions
        simple_definitions = {
            'organism': 'a living being such as a plant or animal',
            'process': 'a series of actions or steps taken to achieve a result',
            'energy': 'the ability to do work or cause change',
            'system': 'a set of connected parts forming a complex whole',
            'structure': 'the arrangement of parts in something',
            'function': 'the purpose or role of something',
            'material': 'the substance from which something is made',
            'element': 'a basic component or part of something',
            'environment': 'the surrounding conditions in which something exists',
            'development': 'the process of growing or changing',
            'information': 'facts or knowledge about something',
            'relationship': 'the way things are connected or related',
            'activity': 'something that is done or happening',
            'behavior': 'the way something acts or responds',
            'characteristic': 'a typical feature or quality of something'
        }
        
        return simple_definitions.get(word.lower())
    
    def _extract_important_words(self, definition: str) -> List[str]:
        """Extract kata-kata penting dari definisi."""
        important_words = set()
        definition_lower = definition.lower()
        
        # Apply extraction patterns
        for pattern in self.important_word_patterns:
            matches = re.findall(pattern, definition_lower)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0] if match else ""
                
                cleaned_word = match.strip()
                if (len(cleaned_word) > 2 and 
                    cleaned_word not in self.stopwords and 
                    cleaned_word.isalpha()):
                    important_words.add(cleaned_word)
        
        # Sort by relevance (longer words first, then alphabetically)
        sorted_words = sorted(important_words, key=lambda x: (-len(x), x))
        
        # Limit to prevent explosion
        return sorted_words[:20]
    
    def _create_concept_node(self, word: str, definition: str, depth: int, source: str) -> ConceptNode:
        """Buat concept node baru."""
        return ConceptNode(
            word=word,
            definition=definition,
            word_type=self._classify_word_type(word, definition),
            bootstrap_depth=depth,
            confidence=max(0.5, 1.0 - (depth * 0.1)),  # Confidence decreases with depth
            source=source,
            related_concepts=set(),
            parent_concepts=set(),
            learned_timestamp=time.time()
        )
    
    def _classify_word_type(self, word: str, definition: str) -> str:
        """Klasifikasi tipe kata berdasarkan word dan definition."""
        definition_lower = definition.lower()
        word_lower = word.lower()
        
        # Social words
        if any(term in definition_lower for term in ['greeting', 'hello', 'goodbye', 'thank', 'please', 'polite']):
            return 'social'
        
        # Properties/adjectives
        if (word_lower.endswith(('ful', 'less', 'ous', 'ic', 'al', 'ive', 'able', 'ible')) or
            any(term in definition_lower for term in ['quality', 'characteristic', 'having', 'being'])):
            return 'property'
        
        # Actions/verbs
        if (word_lower.endswith(('ing', 'tion', 'sion', 'ment', 'ance', 'ence')) or
            any(term in definition_lower for term in ['action', 'process', 'activity', 'doing', 'performed'])):
            return 'action'
        
        # Relations
        if any(term in definition_lower for term in ['between', 'relationship', 'connection', 'link']):
            return 'relation'
        
        # Inquiry words
        if word_lower in ['what', 'where', 'when', 'why', 'how', 'who']:
            return 'inquiry'
        
        # Default to noun
        return 'noun'
    
    def _add_to_alla_lexicon(self, word: str, word_type: str, definition: str):
        """Tambahkan kata ke ALLA's lexicon dengan expression yang sesuai."""
        try:
            # Generate appropriate expression
            if word_type == 'social':
                expression = f"lambda: '{definition[:50]}...'"
            elif word_type == 'property':
                expression = f"lambda obj: hasattr(obj, '{word}') or '{word}' in str(obj).lower()"
            elif word_type == 'action':
                expression = f"lambda: 'action: {word}'"
            elif word_type == 'relation':
                expression = f"lambda obj1, obj2: '{word}' in str((obj1, obj2)).lower()"
            elif word_type == 'inquiry':
                expression = f"lambda: 'inquiry: {word}'"
            else:  # noun
                expression = f"lambda obj: '{word}' in str(obj).lower() or getattr(obj, 'type', '').lower() == '{word}'"
            
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
            print(f"      Warning: Error adding {word} to lexicon: {e}")
    
    def get_concept_connections(self, word: str) -> Dict[str, any]:
        """Dapatkan semua connections untuk konsep tertentu."""
        if word not in self.concept_graph:
            return {}
        
        node = self.concept_graph[word]
        return {
            'word': node.word,
            'definition': node.definition,
            'word_type': node.word_type,
            'depth': node.bootstrap_depth,
            'confidence': node.confidence,
            'related_concepts': list(node.related_concepts),
            'parent_concepts': list(node.parent_concepts),
            'source': node.source
        }
    
    def find_concept_path(self, word1: str, word2: str, max_hops: int = 3) -> Optional[List[str]]:
        """Cari jalur connections antara dua konsep."""
        if word1 not in self.concept_graph or word2 not in self.concept_graph:
            return None
        
        # BFS untuk menemukan shortest path
        queue = deque([(word1, [word1])])
        visited = {word1}
        
        while queue:
            current_word, path = queue.popleft()
            
            if len(path) > max_hops + 1:
                continue
            
            if current_word == word2:
                return path
            
            current_node = self.concept_graph[current_word]
            neighbors = current_node.related_concepts | current_node.parent_concepts
            
            for neighbor in neighbors:
                if neighbor not in visited and neighbor in self.concept_graph:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    def get_bootstrap_statistics(self) -> Dict:
        """Statistik bootstrap learning."""
        if not self.bootstrap_history:
            return {'total_sessions': 0}
        
        total_words = sum(result.total_words_learned for result in self.bootstrap_history)
        total_connections = sum(result.new_connections for result in self.bootstrap_history)
        avg_depth = sum(result.max_depth_reached for result in self.bootstrap_history) / len(self.bootstrap_history)
        avg_time = sum(result.bootstrap_time for result in self.bootstrap_history) / len(self.bootstrap_history)
        
        return {
            'total_sessions': len(self.bootstrap_history),
            'total_words_learned': total_words,
            'total_connections_made': total_connections,
            'concept_graph_size': len(self.concept_graph),
            'average_depth': avg_depth,
            'average_session_time': avg_time,
            'recent_sessions': [result.root_word for result in self.bootstrap_history[-5:]],
            'current_session_words': len(self.current_session_words)
        }
    
    def visualize_concept_map(self, root_word: str, max_depth: int = 2) -> str:
        """Visualisasi concept map untuk kata tertentu."""
        if root_word not in self.concept_graph:
            return f"❌ '{root_word}' not found in concept graph"
        
        map_str = f"CONCEPT MAP for '{root_word}':\n"
        map_str += "=" * 50 + "\n"
        
        visited = set()
        
        def _build_map_recursive(word: str, indent: str = "", depth: int = 0):
            nonlocal map_str, visited
            
            if word in visited or depth > max_depth or word not in self.concept_graph:
                return
            
            visited.add(word)
            node = self.concept_graph[word]
            
            # Node info
            map_str += f"{indent}📌 {word} ({node.word_type})\n"
            map_str += f"{indent}   └─ {node.definition[:60]}...\n"
            
            # Related concepts
            if node.related_concepts and depth < max_depth:
                sorted_related = sorted(node.related_concepts)[:5]  # Limit untuk readability
                for i, related in enumerate(sorted_related):
                    is_last = i == len(sorted_related) - 1
                    connector = "└── " if is_last else "├── "
                    next_indent = indent + ("    " if is_last else "│   ")
                    
                    map_str += f"{indent}🔗 {connector}{related}\n"
                    _build_map_recursive(related, next_indent, depth + 1)
        
        _build_map_recursive(root_word)
        return map_str
    
    def save_concept_graph(self):
        """Simpan concept graph ke file."""
        graph_data = {}
        for word, node in self.concept_graph.items():
            graph_data[word] = {
                'definition': node.definition,
                'word_type': node.word_type,
                'bootstrap_depth': node.bootstrap_depth,
                'confidence': node.confidence,
                'source': node.source,
                'related_concepts': list(node.related_concepts),
                'parent_concepts': list(node.parent_concepts),
                'learned_timestamp': node.learned_timestamp
            }
        
        with open(self.graph_file, 'w') as f:
            json.dump(graph_data, f, indent=2)
    
    def load_concept_graph(self):
        """Load concept graph dari file."""
        if not self.graph_file.exists():
            return
        
        try:
            with open(self.graph_file, 'r') as f:
                graph_data = json.load(f)
            
            for word, data in graph_data.items():
                node = ConceptNode(
                    word=word,
                    definition=data['definition'],
                    word_type=data['word_type'],
                    bootstrap_depth=data['bootstrap_depth'],
                    confidence=data['confidence'],
                    source=data['source'],
                    related_concepts=set(data['related_concepts']),
                    parent_concepts=set(data['parent_concepts']),
                    learned_timestamp=data['learned_timestamp']
                )
                self.concept_graph[word] = node
            
            print(f"📁 Loaded concept graph with {len(self.concept_graph)} concepts")
            
        except Exception as e:
            print(f"Warning: Error loading concept graph: {e}")
    
    def _log_bootstrap_session(self, result: BootstrapResult):
        """Log bootstrap session untuk analysis."""
        log_entry = {
            'timestamp': time.time(),
            'root_word': result.root_word,
            'total_words_learned': result.total_words_learned,
            'concept_graph_size': result.concept_graph_size,
            'max_depth_reached': result.max_depth_reached,
            'new_connections': result.new_connections,
            'bootstrap_time': result.bootstrap_time,
            'learning_tree': result.learning_tree
        }
        
        # Load existing log
        log_data = []
        if self.bootstrap_log_file.exists():
            try:
                with open(self.bootstrap_log_file, 'r') as f:
                    log_data = json.load(f)
            except:
                pass
        
        # Add new entry
        log_data.append(log_entry)
        
        # Keep only last 100 entries
        log_data = log_data[-100:]
        
        # Save
        with open(self.bootstrap_log_file, 'w') as f:
            json.dump(log_data, f, indent=2)


class ALLABootstrapIntegration:
    """
    🧠 INTEGRASI SEMANTIC BOOTSTRAPPING DENGAN ALLA
    
    Membuat ALLA bisa:
    - Bootstrap learn dari 1 kata → ekspansi ke puluhan konsep
    - Bangun concept graph otomatis
    - Reasoning melalui semantic connections
    - Visualisasi concept maps
    """
    
    def __init__(self, alla_engine):
        self.alla = alla_engine
        self.bootstrapper = SemanticBootstrapper(alla_engine)
        self.bootstrap_enabled = False
    
    def enable_semantic_bootstrapping(self):
        """Aktifkan semantic bootstrapping."""
        self.bootstrap_enabled = True
        return "🌱 Semantic Bootstrapping ENABLED - ALLA will now build concept networks, not just learn isolated words!"
    
    def disable_semantic_bootstrapping(self):
        """Nonaktifkan semantic bootstrapping."""
        self.bootstrap_enabled = False
        return "🌱 Semantic Bootstrapping DISABLED - ALLA will learn words individually."
    
    def bootstrap_learn_word(self, word: str, source: str = "user") -> BootstrapResult:
        """Interface untuk semantic bootstrapping."""
        if not self.bootstrap_enabled:
            # Fallback ke normal learning
            definition = self.bootstrapper._get_word_definition(word)
            if definition and not self.alla.lexicon.get_entry(word):
                word_type = self.bootstrapper._classify_word_type(word, definition)
                self.bootstrapper._add_to_alla_lexicon(word, word_type, definition)
            
            return BootstrapResult(
                root_word=word,
                total_words_learned=1,
                concept_graph_size=0,
                max_depth_reached=0,
                new_connections=0,
                learning_tree={word: []},
                bootstrap_time=0.0
            )
        
        return self.bootstrapper.bootstrap_word(word, source)
    
    def get_concept_connections(self, word: str):
        """Dapatkan connections untuk konsep."""
        return self.bootstrapper.get_concept_connections(word)
    
    def find_concept_path(self, word1: str, word2: str):
        """Cari jalur antara dua konsep."""
        return self.bootstrapper.find_concept_path(word1, word2)
    
    def get_bootstrap_stats(self):
        """Statistik bootstrapping."""
        return self.bootstrapper.get_bootstrap_statistics()
    
    def visualize_concept_map(self, word: str):
        """Visualisasi concept map."""
        return self.bootstrapper.visualize_concept_map(word)
    
    def explain_concept_relationship(self, word1: str, word2: str) -> str:
        """Jelaskan hubungan antara dua konsep."""
        path = self.find_concept_path(word1, word2)
        
        if not path:
            return f"❌ No semantic connection found between '{word1}' and '{word2}'"
        
        if len(path) == 2:
            return f"✅ '{word1}' and '{word2}' are directly connected in the concept graph"
        
        connection_str = f"🔗 Path from '{word1}' to '{word2}':\n"
        for i in range(len(path) - 1):
            connection_str += f"   {path[i]} → {path[i+1]}\n"
        
        return connection_str
    
    def query_concept_network(self, query: str) -> str:
        """Query terhadap concept network."""
        words = query.lower().split()
        
        # Find concepts mentioned in query
        mentioned_concepts = []
        for word in words:
            if word in self.bootstrapper.concept_graph:
                mentioned_concepts.append(word)
        
        if not mentioned_concepts:
            return "❌ No known concepts found in query"
        
        response = f"🧠 Concept Analysis for: '{query}'\n"
        response += "=" * 40 + "\n"
        
        for concept in mentioned_concepts:
            connections = self.get_concept_connections(concept)
            if connections:
                response += f"\n📌 {concept.upper()}:\n"
                response += f"   Type: {connections['word_type']}\n"
                response += f"   Definition: {connections['definition'][:100]}...\n"
                
                if connections['related_concepts']:
                    related = connections['related_concepts'][:3]
                    response += f"   Related: {', '.join(related)}\n"
        
        return response
