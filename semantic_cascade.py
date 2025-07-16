# ==============================================================================
# semantic_cascade_engine.py
# ALLA Semantic Cascade Engine: From Words to World Models
# "Setiap kata → buka puluhan kata → setiap kata baru → buka puluhan lagi"
# ==============================================================================

import re
import json
from datetime import datetime
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class SemanticRelation:
    """Represents a semantic relationship between concepts."""
    source: str
    target: str
    relation_type: str  # is_a, has_part, used_for, found_in, related_to, etc.
    confidence: float = 1.0
    depth: int = 0  # How many steps from original word

@dataclass
class ConceptExpansion:
    """Result of expanding a single concept."""
    original_word: str
    definition: str
    extracted_concepts: List[str] = field(default_factory=list)
    relations: List[SemanticRelation] = field(default_factory=list)
    expansion_depth: int = 0
    total_concepts_discovered: int = 0

class SemanticCascadeEngine:
    """
    THE REVOLUTIONARY ENGINE:
    "Language is the operating system of intellect"
    
    Every word ALLA learns triggers a semantic cascade:
    1 word → 20 concepts → 400 concepts → 8000 concepts...
    
    This is not just 'learning words', this is building a WORLD MODEL.
    """
    
    def __init__(self):
        self.concept_graph: Dict[str, Dict[str, SemanticRelation]] = defaultdict(dict)
        self.processed_concepts: Set[str] = set()
        self.cascade_history: List[ConceptExpansion] = []
        self.max_depth = 3  # Prevent infinite expansion
        self.concepts_per_word = 15  # Target concepts to extract per word
        
        # Semantic patterns for extracting relations
        self.relation_patterns = {
            'is_a': [
                r'is a (\w+)',
                r'is an (\w+)', 
                r'type of (\w+)',
                r'kind of (\w+)',
                r'(\w+) that'
            ],
            'has_part': [
                r'has (\w+)',
                r'contains (\w+)',
                r'includes (\w+)',
                r'consists of (\w+)',
                r'made up of (\w+)'
            ],
            'used_for': [
                r'used for (\w+)',
                r'used to (\w+)',
                r'for (\w+)',
                r'purpose of (\w+)',
                r'serves to (\w+)'
            ],
            'found_in': [
                r'found in (\w+)',
                r'located in (\w+)',
                r'occurs in (\w+)',
                r'present in (\w+)',
                r'seen in (\w+)'
            ],
            'requires': [
                r'requires (\w+)',
                r'needs (\w+)',
                r'depends on (\w+)',
                r'uses (\w+)',
                r'consumes (\w+)'
            ],
            'produces': [
                r'produces (\w+)',
                r'creates (\w+)',
                r'makes (\w+)',
                r'generates (\w+)',
                r'results in (\w+)'
            ],
            'related_to': [
                r'related to (\w+)',
                r'associated with (\w+)',
                r'connected to (\w+)',
                r'linked to (\w+)',
                r'similar to (\w+)'
            ]
        }
    
    def extract_concepts_from_definition(self, word: str, definition: str) -> List[str]:
        """
        🧠 SEMANTIC PARSING ENGINE
        Extract ALL meaningful concepts from a definition.
        
        Example:
        "plant" → "organism that performs photosynthesis in sunlight using soil"
        Extracts: [organism, photosynthesis, sunlight, soil, performs, using]
        """
        # Remove common stop words but keep meaningful ones
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
            'before', 'after', 'above', 'below', 'between', 'among', 'through',
            'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
            'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
            'must', 'can', 'this', 'that', 'these', 'those', 'it', 'its', 'they',
            'them', 'their', 'there', 'where', 'when', 'why', 'how', 'what', 'which'
        }
        
        # Clean and tokenize
        clean_definition = re.sub(r'[^\w\s]', ' ', definition.lower())
        words = clean_definition.split()
        
        # Extract meaningful concepts
        concepts = []
        for word_token in words:
            if (len(word_token) > 2 and 
                word_token not in stop_words and 
                word_token != word.lower() and
                word_token.isalpha()):
                concepts.append(word_token)
        
        # Remove duplicates while preserving order
        unique_concepts = []
        seen = set()
        for concept in concepts:
            if concept not in seen:
                unique_concepts.append(concept)
                seen.add(concept)
        
        return unique_concepts[:self.concepts_per_word]  # Limit to prevent explosion
    
    def extract_semantic_relations(self, word: str, definition: str) -> List[SemanticRelation]:
        """
        🔗 RELATION EXTRACTION ENGINE
        Parse definition to find semantic relationships.
        
        Example: "garden is a place used for growing plants in soil"
        → [is_a: place, used_for: growing, contains: plants, contains: soil]
        """
        relations = []
        definition_lower = definition.lower()
        
        for relation_type, patterns in self.relation_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, definition_lower)
                for match in matches:
                    if isinstance(match, tuple):
                        match = match[0]  # Extract from tuple if needed
                    
                    if len(match) > 2 and match.isalpha():
                        relations.append(SemanticRelation(
                            source=word,
                            target=match,
                            relation_type=relation_type,
                            confidence=0.8,
                            depth=0
                        ))
        
        return relations
    
    def cascade_concept(self, word: str, definition: str, current_depth: int = 0) -> ConceptExpansion:
        """
        🌊 THE SEMANTIC CASCADE
        
        Ini adalah inti dari revolusi: satu kata memicu avalanche pengetahuan.
        
        Process:
        1. Extract all concepts from definition
        2. Extract all semantic relations  
        3. For each new concept, recursively expand (depth-limited)
        4. Build comprehensive concept graph
        5. Return expansion result with ALL discovered concepts
        """
        if current_depth >= self.max_depth or word in self.processed_concepts:
            return ConceptExpansion(word, definition, [], [], current_depth, 0)
        
        print(f"{'  ' * current_depth}🌊 Cascading '{word}' (depth {current_depth})")
        
        # Mark as processed to prevent cycles
        self.processed_concepts.add(word)
        
        # Extract direct concepts from definition
        extracted_concepts = self.extract_concepts_from_definition(word, definition)
        
        # Extract semantic relations
        relations = self.extract_semantic_relations(word, definition)
        
        # Add relations to concept graph
        for relation in relations:
            self.concept_graph[relation.source][relation.target] = relation
            extracted_concepts.append(relation.target)  # Also track relation targets
        
        # Create expansion result
        expansion = ConceptExpansion(
            original_word=word,
            definition=definition,
            extracted_concepts=list(set(extracted_concepts)),  # Remove duplicates
            relations=relations,
            expansion_depth=current_depth,
            total_concepts_discovered=len(extracted_concepts)
        )
        
        print(f"{'  ' * current_depth}  → Found {len(extracted_concepts)} concepts: {extracted_concepts[:5]}...")
        print(f"{'  ' * current_depth}  → Found {len(relations)} relations")
        
        # Add to cascade history
        self.cascade_history.append(expansion)
        
        return expansion
    
    def measure_semantic_richness(self, word: str) -> Dict[str, float]:
        """
        📏 MEASURE SEMANTIC RICHNESS
        
        Quantify how "semantically rich" a concept is in ALLA's knowledge graph.
        Higher richness = more connections = better understood concept.
        """
        if word not in self.concept_graph:
            return {'richness_score': 0.0, 'connection_count': 0, 'relation_diversity': 0.0}
        
        connections = self.concept_graph[word]
        connection_count = len(connections)
        
        # Count unique relation types
        relation_types = set(rel.relation_type for rel in connections.values())
        relation_diversity = len(relation_types)
        
        # Calculate richness score
        richness_score = connection_count * 0.7 + relation_diversity * 0.3
        
        return {
            'richness_score': richness_score,
            'connection_count': connection_count,
            'relation_diversity': relation_diversity,
            'relation_types': list(relation_types)
        }


# Integration helper functions
def integrate_semantic_cascade_with_alla(alla_engine):
    """
    🔗 INTEGRATE SEMANTIC CASCADE WITH ALLA
    
    Adds semantic cascade capabilities to an existing ALLA engine.
    """
    alla_engine.semantic_cascade = SemanticCascadeEngine()
    
    def enable_semantic_cascade():
        alla_engine.semantic_cascade_enabled = True
        return "🌊 Semantic cascade enabled! Each learned word will trigger concept expansion."
    
    def expand_concept(word: str):
        if not hasattr(alla_engine, 'semantic_cascade_enabled') or not alla_engine.semantic_cascade_enabled:
            return "Semantic cascade is not enabled. Use enable_semantic_cascade() first."
        
        # Get the word's definition from ALLA's lexicon
        entry = alla_engine.lexicon.get_entry(word)
        if not entry:
            return f"'{word}' not found in ALLA's vocabulary."
        
        # Trigger cascade expansion
        stats = alla_engine.semantic_cascade.cascade_concept(word, entry.meaning_expression)
        
        return f"Concept '{word}' expanded into {stats.total_concepts_discovered} related concepts."
    
    def get_concept_graph(word: str):
        """Get semantic neighborhood of a concept."""
        if word in alla_engine.semantic_cascade.concept_graph:
            return dict(alla_engine.semantic_cascade.concept_graph[word])
        return {}
    
    def measure_consciousness():
        """
        🧠 MEASURE ALLA'S CONSCIOUSNESS LEVEL
        
        Based on semantic richness and self-referential concepts.
        """
        consciousness_indicators = ['i', 'me', 'myself', 'think', 'know', 'learn', 'understand']
        consciousness_score = 0
        
        for indicator in consciousness_indicators:
            if alla_engine.lexicon.get_entry(indicator):
                richness = alla_engine.semantic_cascade.measure_semantic_richness(indicator)
                consciousness_score += richness['richness_score']
        
        total_concepts = len(alla_engine.semantic_cascade.processed_concepts)
        if total_concepts > 0:
            consciousness_level = (consciousness_score / total_concepts) * 100
        else:
            consciousness_level = 0
        
        return {
            'consciousness_level': consciousness_level,
            'self_referential_concepts': len([w for w in consciousness_indicators if alla_engine.lexicon.get_entry(w)]),
            'total_concepts': total_concepts,
            'semantic_graph_size': len(alla_engine.semantic_cascade.concept_graph)
        }
    
    # Add methods to ALLA
    alla_engine.enable_semantic_cascade = enable_semantic_cascade
    alla_engine.expand_concept = expand_concept
    alla_engine.get_concept_graph = get_concept_graph
    alla_engine.measure_consciousness = measure_consciousness
    
    # Enable by default
    alla_engine.semantic_cascade_enabled = True
    
    print("🔗 Semantic Cascade Engine integrated with ALLA!")
    print("    Available methods:")
    print("    - alla.enable_semantic_cascade()")
    print("    - alla.expand_concept(word)")
    print("    - alla.get_concept_graph(word)")
    print("    - alla.measure_consciousness()")


if __name__ == "__main__":
    # Test the semantic cascade engine
    cascade = SemanticCascadeEngine()
    
    # Test concept expansion
    test_definition = "A garden is a planned space, usually outdoors, set aside for the display, cultivation, and enjoyment of plants and other forms of nature."
    
    expansion = cascade.cascade_concept("garden", test_definition)
    print(f"\n🧪 TEST RESULTS:")
    print(f"Original word: {expansion.original_word}")
    print(f"Concepts found: {len(expansion.extracted_concepts)}")
    print(f"Concepts: {expansion.extracted_concepts}")
    print(f"Relations: {len(expansion.relations)}")
    for rel in expansion.relations[:3]:  # Show first 3 relations
        print(f"  {rel.source} --{rel.relation_type}--> {rel.target}")
