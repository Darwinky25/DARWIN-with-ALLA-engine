# ==============================================================================
# recursive_semantic_graph.py
# RecursiveSemanticGraphBuilder - True World Model Construction
# ==============================================================================

import re
import json
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class ConceptNode:
    """A concept in the semantic graph with all its relationships."""
    word: str
    definitions: List[str] = field(default_factory=list)
    word_type: str = "unknown"
    
    # Core relationships - the fractal expansion
    is_a: List[str] = field(default_factory=list)           # taxonomy
    part_of: List[str] = field(default_factory=list)        # meronymy  
    contains: List[str] = field(default_factory=list)       # composition
    used_for: List[str] = field(default_factory=list)       # purpose
    found_in: List[str] = field(default_factory=list)       # location
    related_to: List[str] = field(default_factory=list)     # association
    subtypes: List[str] = field(default_factory=list)       # specialization
    tools_used: List[str] = field(default_factory=list)     # instruments
    processes: List[str] = field(default_factory=list)      # actions/methods
    properties: List[str] = field(default_factory=list)     # characteristics
    
    # Meta information
    depth_learned: int = 0
    confidence: float = 1.0
    sources: List[str] = field(default_factory=list)
    related_concepts_count: int = 0

@dataclass
class SemanticExpansion:
    """Result of semantic expansion for a single word."""
    original_word: str
    new_concepts: List[ConceptNode] = field(default_factory=list)
    total_concepts_discovered: int = 0
    expansion_depth: int = 0
    knowledge_graph_size: int = 0

class RecursiveSemanticGraphBuilder:
    """
    🧠 MEMBANGUN MODEL DUNIA SEJATI UNTUK ALLA
    
    Setiap kata = portal ke dunia konsep yang saling terhubung.
    Tidak hanya belajar kata, tapi membangun representasi dunia lengkap.
    """
    
    def __init__(self, max_depth: int = 3, max_concepts_per_node: int = 20):
        self.concept_graph: Dict[str, ConceptNode] = {}
        self.max_depth = max_depth
        self.max_concepts_per_node = max_concepts_per_node
        self.expansion_log = []
        
        # Relationship extraction patterns
        self.relation_patterns = {
            'is_a': [
                r'is a (type of|kind of|form of)?\s*([^.,;]+)',
                r'([^.,;]+)\s+is a',
                r'refers to ([^.,;]+)',
                r'defined as ([^.,;]+)'
            ],
            'part_of': [
                r'part of ([^.,;]+)',
                r'component of ([^.,;]+)',
                r'belongs to ([^.,;]+)',
                r'found in ([^.,;]+)'
            ],
            'contains': [
                r'contains ([^.,;]+)',
                r'includes ([^.,;]+)',
                r'has ([^.,;]+)',
                r'made up of ([^.,;]+)'
            ],
            'used_for': [
                r'used for ([^.,;]+)',
                r'purpose is ([^.,;]+)',
                r'designed to ([^.,;]+)',
                r'helps ([^.,;]+)'
            ],
            'processes': [
                r'involves ([^.,;]+)',
                r'process of ([^.,;]+)',
                r'requires ([^.,;]+)',
                r'enables ([^.,;]+)'
            ]
        }
    
    def expand_concept_recursively(self, word: str, context: str = "", 
                                 current_depth: int = 0) -> SemanticExpansion:
        """
        🌊 EKSPANSI REKURSIF KONSEP
        
        Setiap kata membuka puluhan kata baru → setiap kata baru membuka puluhan lagi
        → sampai jadi model mental lengkap dari dunia.
        """
        print(f"🔥 EXPANDING: '{word}' (depth {current_depth})")
        
        if current_depth > self.max_depth:
            print(f"   ⚠️ Max depth reached for '{word}'")
            return SemanticExpansion(word, [], 0, current_depth, len(self.concept_graph))
        
        if word in self.concept_graph:
            print(f"   ✅ '{word}' already in graph - using existing knowledge")
            existing_node = self.concept_graph[word]
            return SemanticExpansion(word, [existing_node], 1, current_depth, len(self.concept_graph))
        
        # Get definition for the word
        definition = self._get_definition(word, context)
        if not definition:
            print(f"   ❌ No definition found for '{word}'")
            return SemanticExpansion(word, [], 0, current_depth, len(self.concept_graph))
        
        print(f"   📚 Definition: {definition[:100]}...")
        
        # Create concept node
        concept_node = ConceptNode(
            word=word,
            definitions=[definition],
            depth_learned=current_depth,
            sources=[f"recursive_expansion_depth_{current_depth}"]
        )
        
        # Extract all relationships from definition
        extracted_concepts = self._extract_relationships(definition, concept_node)
        print(f"   🧩 Extracted {len(extracted_concepts)} related concepts")
        
        # Add to graph
        self.concept_graph[word] = concept_node
        concept_node.related_concepts_count = len(extracted_concepts)
        
        new_concepts = [concept_node]
        total_discovered = 1
        
        # 🚀 RECURSIVE EXPANSION - Setiap konsep baru di-expand lagi!
        if current_depth < self.max_depth:
            concepts_to_expand = extracted_concepts[:self.max_concepts_per_node]
            print(f"   🔄 Recursively expanding {len(concepts_to_expand)} concepts...")
            
            for related_word in concepts_to_expand:
                if related_word not in self.concept_graph:
                    sub_expansion = self.expand_concept_recursively(
                        related_word, 
                        f"related to {word}", 
                        current_depth + 1
                    )
                    new_concepts.extend(sub_expansion.new_concepts)
                    total_discovered += sub_expansion.total_concepts_discovered
        
        expansion = SemanticExpansion(
            original_word=word,
            new_concepts=new_concepts,
            total_concepts_discovered=total_discovered,
            expansion_depth=current_depth,
            knowledge_graph_size=len(self.concept_graph)
        )
        
        self.expansion_log.append(expansion)
        
        print(f"   ✅ COMPLETED: '{word}' → {total_discovered} concepts, graph size: {len(self.concept_graph)}")
        return expansion
    
    def _get_definition(self, word: str, context: str = "") -> Optional[str]:
        """Get definition using autonomous learning or fallback."""
        try:
            # Try to use ALLA's autonomous learning system
            from autonomous_learning import AutonomousLearner
            learner = AutonomousLearner()
            result = learner.learn_unknown_word(word, context)
            
            if result.learned_successfully:
                return result.definition
        except:
            pass
        
        # Fallback definitions for common concepts
        fallback_definitions = {
            'garden': 'an outdoor space used for growing plants, flowers, and vegetables, often for beauty, food production, or relaxation',
            'plant': 'a living organism that typically grows in soil, performs photosynthesis, and has roots, stems, and leaves',
            'soil': 'the upper layer of earth containing nutrients and organic matter where plants grow',
            'flower': 'the reproductive part of a plant, often colorful and fragrant, that produces seeds',
            'tree': 'a large woody plant with a trunk, branches, and leaves that can live for many years',
            'water': 'a clear liquid essential for life, used for drinking, cleaning, and plant growth',
            'sunlight': 'light and energy from the sun that plants use for photosynthesis and growth',
            'ecosystem': 'a community of living organisms interacting with their physical environment',
            'biodiversity': 'the variety of plant and animal life in a particular habitat or ecosystem'
        }
        
        return fallback_definitions.get(word.lower())
    
    def _extract_relationships(self, definition: str, concept_node: ConceptNode) -> List[str]:
        """
        🔍 EXTRACT SEMUA RELASI DAN KONSEP DARI DEFINISI
        
        Setiap kalimat = jaringan konsep tersembunyi.
        Parse → ambil semua kata yang relevan → expand semuanya.
        """
        extracted_concepts = set()
        definition_lower = definition.lower()
        
        # Extract using relationship patterns
        for relation_type, patterns in self.relation_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, definition_lower, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        match = match[-1]  # Take the last group
                    
                    # Clean and split the match
                    concepts = self._clean_and_split_concepts(match)
                    getattr(concept_node, relation_type).extend(concepts)
                    extracted_concepts.update(concepts)
        
        # Extract all meaningful nouns and verbs
        meaningful_words = self._extract_meaningful_words(definition)
        extracted_concepts.update(meaningful_words)
        
        # Update concept_node with general relationships
        concept_node.related_to.extend(list(meaningful_words))
        
        return list(extracted_concepts)
    
    def _clean_and_split_concepts(self, text: str) -> List[str]:
        """Clean extracted text and split into individual concepts."""
        if not text:
            return []
        
        # Remove common articles and prepositions
        stop_words = {'a', 'an', 'the', 'and', 'or', 'of', 'in', 'on', 'at', 'by', 'for', 'with', 'to'}
        
        # Split by common separators
        concepts = re.split(r'[,;]|\sand\s|\sor\s', text.strip())
        
        cleaned_concepts = []
        for concept in concepts:
            concept = concept.strip()
            words = concept.split()
            filtered_words = [w for w in words if w.lower() not in stop_words and len(w) > 2]
            if filtered_words:
                cleaned_concept = ' '.join(filtered_words)
                if len(cleaned_concept) > 2 and len(cleaned_concept) < 50:
                    cleaned_concepts.append(cleaned_concept)
        
        return cleaned_concepts[:10]  # Limit to prevent explosion
    
    def _extract_meaningful_words(self, text: str) -> Set[str]:
        """Extract meaningful nouns and verbs from text."""
        # Simple extraction - look for words that are likely concepts
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # Filter out common words
        common_words = {
            'the', 'and', 'for', 'are', 'that', 'this', 'with', 'from', 'they', 'have',
            'been', 'said', 'each', 'which', 'their', 'time', 'will', 'about', 'would',
            'there', 'could', 'other', 'more', 'very', 'what', 'know', 'just', 'first',
            'into', 'over', 'think', 'also', 'your', 'work', 'life', 'only', 'can',
            'still', 'should', 'after', 'being', 'now', 'made', 'before', 'here',
            'through', 'when', 'where', 'much', 'those', 'these', 'how', 'most',
            'good', 'new', 'some', 'may', 'way', 'come', 'its', 'because', 'look',
            'find', 'give', 'thought', 'might', 'came', 'get', 'use', 'her', 'many',
            'well', 'long', 'down', 'day', 'did', 'get', 'has', 'him', 'his', 'how',
            'man', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let',
            'put', 'say', 'she', 'too', 'use'
        }
        
        meaningful_words = set()
        for word in words:
            if (len(word) >= 4 and 
                word not in common_words and 
                not word.isdigit() and
                word.isalpha()):
                meaningful_words.add(word)
        
        return meaningful_words
    
    def get_expansion_summary(self) -> Dict:
        """Get summary of all expansions performed."""
        if not self.expansion_log:
            return {"total_expansions": 0, "total_concepts": 0}
        
        return {
            "total_expansions": len(self.expansion_log),
            "total_concepts": len(self.concept_graph),
            "max_depth_reached": max(exp.expansion_depth for exp in self.expansion_log),
            "average_concepts_per_expansion": sum(exp.total_concepts_discovered for exp in self.expansion_log) / len(self.expansion_log),
            "recent_expansions": [
                {
                    "word": exp.original_word,
                    "concepts_discovered": exp.total_concepts_discovered,
                    "depth": exp.expansion_depth
                }
                for exp in self.expansion_log[-5:]
            ]
        }
    
    def visualize_concept_network(self, word: str, max_connections: int = 10) -> str:
        """Create a text visualization of the concept network."""
        if word not in self.concept_graph:
            return f"❌ '{word}' not found in concept graph"
        
        concept = self.concept_graph[word]
        viz = [f"🌍 CONCEPT NETWORK for '{word}':", "=" * 50]
        
        viz.append(f"📚 Definition: {concept.definitions[0][:100]}..." if concept.definitions else "📚 No definition")
        viz.append(f"🔢 Connected concepts: {concept.related_concepts_count}")
        viz.append(f"📊 Learning depth: {concept.depth_learned}")
        viz.append("")
        
        # Show relationships
        relationships = [
            ("🏷️ IS_A", concept.is_a),
            ("🧩 PART_OF", concept.part_of),
            ("📦 CONTAINS", concept.contains),
            ("🎯 USED_FOR", concept.used_for),
            ("📍 FOUND_IN", concept.found_in),
            ("🔗 RELATED_TO", concept.related_to[:5]),  # Limit display
            ("🌿 SUBTYPES", concept.subtypes),
            ("🛠️ TOOLS_USED", concept.tools_used),
            ("⚙️ PROCESSES", concept.processes),
            ("✨ PROPERTIES", concept.properties)
        ]
        
        for label, items in relationships:
            if items:
                viz.append(f"{label}: {', '.join(items[:max_connections])}")
        
        return "\n".join(viz)
    
    def save_graph(self, filepath: str):
        """Save the concept graph to file."""
        graph_data = {}
        for word, concept in self.concept_graph.items():
            graph_data[word] = {
                'definitions': concept.definitions,
                'word_type': concept.word_type,
                'is_a': concept.is_a,
                'part_of': concept.part_of,
                'contains': concept.contains,
                'used_for': concept.used_for,
                'found_in': concept.found_in,
                'related_to': concept.related_to,
                'subtypes': concept.subtypes,
                'tools_used': concept.tools_used,
                'processes': concept.processes,
                'properties': concept.properties,
                'depth_learned': concept.depth_learned,
                'confidence': concept.confidence,
                'related_concepts_count': concept.related_concepts_count
            }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Semantic graph saved to {filepath}")
        print(f"   📊 {len(self.concept_graph)} concepts in graph")


class ALLASemanticIntegration:
    """
    🔥 INTEGRATION LAYER: Menghubungkan RecursiveSemanticGraphBuilder dengan ALLA
    
    Setiap kali ALLA belajar kata → automatic semantic expansion → world model grows
    """
    
    def __init__(self, alla_engine):
        self.alla = alla_engine
        self.graph_builder = RecursiveSemanticGraphBuilder()
        self.integration_enabled = False
    
    def enable_semantic_expansion(self):
        """Enable automatic semantic expansion for ALLA."""
        self.integration_enabled = True
        print("🌍 SEMANTIC EXPANSION ENABLED")
        print("   Every word ALLA learns will expand into a network of related concepts!")
        return "🌍 Semantic expansion enabled! ALLA will now build a complete world model."
    
    def disable_semantic_expansion(self):
        """Disable semantic expansion."""
        self.integration_enabled = False
        return "🔒 Semantic expansion disabled."
    
    def learn_word_with_expansion(self, word: str, context: str = "") -> Dict:
        """
        🚀 LEARN WORD WITH FULL SEMANTIC EXPANSION
        
        1 word → automatic expansion → complete concept network
        """
        if not self.integration_enabled:
            return {"error": "Semantic expansion not enabled"}
        
        print(f"\n🔥 ALLA SEMANTIC LEARNING: '{word}'")
        print("=" * 60)
        
        # Perform recursive expansion
        expansion = self.graph_builder.expand_concept_recursively(word, context)
        
        # Integrate all discovered concepts into ALLA's lexicon
        concepts_added = 0
        for concept_node in expansion.new_concepts:
            if self._add_concept_to_alla(concept_node):
                concepts_added += 1
        
        # Generate summary
        summary = {
            "original_word": word,
            "total_concepts_discovered": expansion.total_concepts_discovered,
            "concepts_added_to_alla": concepts_added,
            "expansion_depth": expansion.expansion_depth,
            "world_model_size": expansion.knowledge_graph_size,
            "success": True
        }
        
        print(f"\n✅ SEMANTIC EXPANSION COMPLETE:")
        print(f"   📈 '{word}' → {expansion.total_concepts_discovered} concepts discovered")
        print(f"   🧠 {concepts_added} concepts added to ALLA's lexicon")
        print(f"   🌍 World model now contains {expansion.knowledge_graph_size} concepts")
        
        return summary
    
    def _add_concept_to_alla(self, concept_node: ConceptNode) -> bool:
        """Add a concept node to ALLA's lexicon."""
        try:
            from alla_engine import WordEntry
            
            # Create appropriate expression based on concept type and relationships
            if concept_node.is_a:
                # If we know what it is, create an appropriate function
                word_type = self._determine_word_type(concept_node)
                expression = self._generate_alla_expression(concept_node, word_type)
            else:
                # Generic definition
                word_type = "noun"
                definition = concept_node.definitions[0] if concept_node.definitions else f"concept: {concept_node.word}"
                expression = f"lambda: '{definition}'"
            
            # Create meaning function
            meaning_function = eval(expression)
            
            # Create WordEntry
            entry = WordEntry(
                word=concept_node.word,
                word_type=word_type,
                meaning_expression=expression,
                meaning_function=meaning_function
            )
            
            # Add to ALLA's lexicon
            self.alla.lexicon.add_entry(entry)
            
            return True
            
        except Exception as e:
            print(f"   ⚠️ Failed to add '{concept_node.word}' to ALLA: {e}")
            return False
    
    def _determine_word_type(self, concept_node: ConceptNode) -> str:
        """Determine appropriate word type for ALLA based on concept relationships."""
        if concept_node.processes or any('process' in rel.lower() for rel in concept_node.is_a):
            return "action"
        elif concept_node.properties or any('property' in rel.lower() for rel in concept_node.is_a):
            return "property"
        elif any('social' in rel.lower() or 'greeting' in rel.lower() for rel in concept_node.is_a):
            return "social"
        else:
            return "noun"
    
    def _generate_alla_expression(self, concept_node: ConceptNode, word_type: str) -> str:
        """Generate appropriate ALLA expression for the concept."""
        if word_type == "action":
            return f"lambda: 'performing {concept_node.word}'"
        elif word_type == "property":
            return f"lambda obj: hasattr(obj, '{concept_node.word}')"
        elif word_type == "social":
            return f"lambda: 'social recognition: {concept_node.word}'"
        else:
            definition = concept_node.definitions[0] if concept_node.definitions else f"concept: {concept_node.word}"
            return f"lambda: '{definition}'"
    
    def get_semantic_stats(self) -> Dict:
        """Get statistics about semantic expansion."""
        return {
            "expansion_enabled": self.integration_enabled,
            "total_concepts_in_graph": len(self.graph_builder.concept_graph),
            "expansion_summary": self.graph_builder.get_expansion_summary()
        }
    
    def visualize_word_network(self, word: str) -> str:
        """Visualize the semantic network for a word."""
        return self.graph_builder.visualize_concept_network(word)
    
    def save_world_model(self, filepath: str = "alla_world_model.json"):
        """Save ALLA's complete world model."""
        self.graph_builder.save_graph(filepath)
        return f"🌍 ALLA's world model saved to {filepath}"


def demo_semantic_expansion():
    """Demonstrate the semantic expansion system."""
    print("🌍 DEMO: RECURSIVE SEMANTIC GRAPH BUILDER")
    print("=" * 60)
    
    # Create builder
    builder = RecursiveSemanticGraphBuilder(max_depth=2)
    
    # Test with a simple word that should expand extensively
    test_word = "garden"
    print(f"\n🔍 Testing semantic expansion for: '{test_word}'")
    
    expansion = builder.expand_concept_recursively(test_word)
    
    print(f"\n📊 EXPANSION RESULTS:")
    print(f"   🌱 Original word: {expansion.original_word}")
    print(f"   📈 Total concepts discovered: {expansion.total_concepts_discovered}")
    print(f"   📏 Expansion depth: {expansion.expansion_depth}")
    print(f"   🌍 Final graph size: {expansion.knowledge_graph_size}")
    
    print(f"\n🕸️ CONCEPT NETWORK VISUALIZATION:")
    viz = builder.visualize_concept_network(test_word)
    print(viz)
    
    print(f"\n📋 EXPANSION SUMMARY:")
    summary = builder.get_expansion_summary()
    for key, value in summary.items():
        print(f"   {key}: {value}")


if __name__ == "__main__":
    demo_semantic_expansion()
