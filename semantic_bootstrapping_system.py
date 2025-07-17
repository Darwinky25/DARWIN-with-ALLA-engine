#!/usr/bin/env python3
"""
Advanced Semantic Bootstrapping System - Builds conceptual understanding from visual patterns
Bridges visual patterns to semantic concepts through progressive abstraction
"""

import json
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from collections import defaultdict, Counter
import logging
from enum import Enum
import networkx as nx
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class ConceptualLevel(Enum):
    """Levels of conceptual understanding"""
    PERCEPTUAL = "perceptual"        # Basic visual features
    OBJECT = "object"                # Object-level concepts
    RELATIONAL = "relational"        # Relationships between objects
    SPATIAL = "spatial"              # Spatial arrangements and patterns
    TEMPORAL = "temporal"            # Temporal sequences and changes
    FUNCTIONAL = "functional"        # Purpose and function
    ABSTRACT = "abstract"            # High-level abstract concepts

@dataclass
class SemanticConcept:
    """A semantic concept learned from visual patterns"""
    concept_id: str
    name: str
    level: ConceptualLevel
    description: str
    visual_signatures: List[str]     # Visual patterns that instantiate this concept
    semantic_properties: Dict[str, Any]
    relationships: Dict[str, List[str]]  # Relations to other concepts
    instantiation_count: int
    confidence: float
    abstraction_path: List[str]      # How this concept was derived
    linguistic_grounding: List[str]  # Natural language descriptions

@dataclass
class ConceptualMapping:
    """Mapping between visual patterns and semantic concepts"""
    pattern_id: str
    concept_id: str
    mapping_strength: float
    evidence: List[str]
    context: str
    validation_examples: List[str]

@dataclass
class AbstractionLevel:
    """A level in the abstraction hierarchy"""
    level_id: str
    level_name: str
    concepts: List[str]
    abstraction_rules: List[str]
    emergence_patterns: List[str]

class ConceptualAbstractor(ABC):
    """Abstract base class for concept abstraction"""
    
    @abstractmethod
    def abstract_concepts(self, lower_concepts: List[SemanticConcept]) -> List[SemanticConcept]:
        """Abstract higher-level concepts from lower-level ones"""
        pass

class SpatialAbstractor(ConceptualAbstractor):
    """Abstracts spatial concepts from visual patterns"""
    
    def abstract_concepts(self, lower_concepts: List[SemanticConcept]) -> List[SemanticConcept]:
        """Abstract spatial concepts like 'inside', 'above', 'connected'"""
        spatial_concepts = []
        
        # Look for spatial relationship patterns
        spatial_patterns = {
            "containment": ["inside", "contains", "enclosed"],
            "adjacency": ["next_to", "adjacent", "touching"],
            "orientation": ["above", "below", "left", "right"],
            "alignment": ["aligned", "parallel", "perpendicular"],
            "symmetry": ["symmetric", "mirrored", "reflected"]
        }
        
        for pattern_type, keywords in spatial_patterns.items():
            related_concepts = [c for c in lower_concepts 
                              if any(keyword in c.description.lower() for keyword in keywords)]
            
            if len(related_concepts) >= 2:  # Need multiple examples
                spatial_concept = self._create_spatial_concept(pattern_type, related_concepts)
                spatial_concepts.append(spatial_concept)
        
        return spatial_concepts
    
    def _create_spatial_concept(self, pattern_type: str, 
                               related_concepts: List[SemanticConcept]) -> SemanticConcept:
        """Create a spatial concept from related lower-level concepts"""
        
        concept_id = f"spatial_{pattern_type}_{len(related_concepts)}"
        
        # Aggregate visual signatures
        visual_signatures = []
        for concept in related_concepts:
            visual_signatures.extend(concept.visual_signatures)
        
        # Determine semantic properties
        semantic_properties = {
            "spatial_type": pattern_type,
            "dimensionality": self._infer_dimensionality(related_concepts),
            "symmetry_type": self._infer_symmetry(related_concepts),
            "invariance_properties": self._infer_invariances(related_concepts)
        }
        
        return SemanticConcept(
            concept_id=concept_id,
            name=f"Spatial {pattern_type.title()}",
            level=ConceptualLevel.SPATIAL,
            description=f"Abstract spatial concept representing {pattern_type} relationships",
            visual_signatures=visual_signatures,
            semantic_properties=semantic_properties,
            relationships={"composed_of": [c.concept_id for c in related_concepts]},
            instantiation_count=sum(c.instantiation_count for c in related_concepts),
            confidence=np.mean([c.confidence for c in related_concepts]),
            abstraction_path=[c.concept_id for c in related_concepts],
            linguistic_grounding=[pattern_type, f"{pattern_type}_relationship"]
        )
    
    def _infer_dimensionality(self, concepts: List[SemanticConcept]) -> str:
        """Infer the dimensionality of spatial concepts"""
        # Simple heuristic based on concept descriptions
        if any("3d" in c.description.lower() or "depth" in c.description.lower() for c in concepts):
            return "3D"
        elif any("2d" in c.description.lower() or "plane" in c.description.lower() for c in concepts):
            return "2D"
        else:
            return "1D"
    
    def _infer_symmetry(self, concepts: List[SemanticConcept]) -> str:
        """Infer symmetry properties"""
        symmetry_indicators = ["symmetric", "mirror", "reflect", "rotation"]
        if any(any(indicator in c.description.lower() for indicator in symmetry_indicators) 
               for c in concepts):
            return "symmetric"
        else:
            return "asymmetric"
    
    def _infer_invariances(self, concepts: List[SemanticConcept]) -> List[str]:
        """Infer what properties remain invariant"""
        invariances = []
        
        # Check for common invariance patterns
        if any("rotation" in c.description.lower() for c in concepts):
            invariances.append("rotation_invariant")
        if any("scale" in c.description.lower() for c in concepts):
            invariances.append("scale_invariant")
        if any("translation" in c.description.lower() for c in concepts):
            invariances.append("translation_invariant")
        
        return invariances

class FunctionalAbstractor(ConceptualAbstractor):
    """Abstracts functional concepts from patterns"""
    
    def abstract_concepts(self, lower_concepts: List[SemanticConcept]) -> List[SemanticConcept]:
        """Abstract functional concepts like 'selection', 'transformation', 'generation'"""
        functional_concepts = []
        
        functional_patterns = {
            "selection": ["select", "choose", "pick", "filter"],
            "transformation": ["transform", "change", "modify", "convert"],
            "generation": ["create", "generate", "produce", "spawn"],
            "elimination": ["remove", "delete", "eliminate", "erase"],
            "duplication": ["copy", "duplicate", "replicate", "clone"]
        }
        
        for function_type, keywords in functional_patterns.items():
            related_concepts = [c for c in lower_concepts 
                              if any(keyword in c.description.lower() for keyword in keywords)]
            
            if len(related_concepts) >= 2:
                functional_concept = self._create_functional_concept(function_type, related_concepts)
                functional_concepts.append(functional_concept)
        
        return functional_concepts
    
    def _create_functional_concept(self, function_type: str, 
                                  related_concepts: List[SemanticConcept]) -> SemanticConcept:
        """Create a functional concept"""
        
        concept_id = f"functional_{function_type}_{len(related_concepts)}"
        
        semantic_properties = {
            "function_type": function_type,
            "input_requirements": self._infer_input_requirements(related_concepts),
            "output_characteristics": self._infer_output_characteristics(related_concepts),
            "operation_complexity": self._infer_complexity(related_concepts)
        }
        
        return SemanticConcept(
            concept_id=concept_id,
            name=f"Functional {function_type.title()}",
            level=ConceptualLevel.FUNCTIONAL,
            description=f"Abstract functional concept representing {function_type} operations",
            visual_signatures=[sig for c in related_concepts for sig in c.visual_signatures],
            semantic_properties=semantic_properties,
            relationships={"implements": [c.concept_id for c in related_concepts]},
            instantiation_count=sum(c.instantiation_count for c in related_concepts),
            confidence=np.mean([c.confidence for c in related_concepts]),
            abstraction_path=[c.concept_id for c in related_concepts],
            linguistic_grounding=[function_type, f"{function_type}_operation"]
        )
    
    def _infer_input_requirements(self, concepts: List[SemanticConcept]) -> List[str]:
        """Infer what inputs are required for this function"""
        requirements = []
        for concept in concepts:
            if "object" in concept.description.lower():
                requirements.append("object_input")
            if "pattern" in concept.description.lower():
                requirements.append("pattern_input")
            if "grid" in concept.description.lower():
                requirements.append("grid_input")
        return list(set(requirements))
    
    def _infer_output_characteristics(self, concepts: List[SemanticConcept]) -> List[str]:
        """Infer characteristics of the output"""
        characteristics = []
        for concept in concepts:
            if "new" in concept.description.lower():
                characteristics.append("creates_new")
            if "modified" in concept.description.lower():
                characteristics.append("modifies_existing")
            if "multiple" in concept.description.lower():
                characteristics.append("multiple_outputs")
        return list(set(characteristics))
    
    def _infer_complexity(self, concepts: List[SemanticConcept]) -> str:
        """Infer the complexity level of the operation"""
        total_signatures = sum(len(c.visual_signatures) for c in concepts)
        if total_signatures > 10:
            return "high"
        elif total_signatures > 5:
            return "medium"
        else:
            return "low"

class SemanticBootstrappingSystem:
    """Advanced semantic bootstrapping system for ARC tasks"""
    
    def __init__(self):
        self.semantic_concepts: Dict[str, SemanticConcept] = {}
        self.conceptual_mappings: List[ConceptualMapping] = []
        self.abstraction_hierarchy = nx.DiGraph()
        self.concept_graph = nx.Graph()
        
        # Abstraction engines
        self.abstractors = {
            ConceptualLevel.SPATIAL: SpatialAbstractor(),
            ConceptualLevel.FUNCTIONAL: FunctionalAbstractor()
        }
        
        # Initialize base concepts
        self._initialize_base_concepts()
        
        logger.info("🌱 Semantic Bootstrapping System initialized")
    
    def _initialize_base_concepts(self):
        """Initialize fundamental base concepts"""
        
        base_concepts = [
            # Perceptual concepts
            SemanticConcept(
                concept_id="color_change",
                name="Color Change",
                level=ConceptualLevel.PERCEPTUAL,
                description="Change in color of visual elements",
                visual_signatures=["color_0_to_1", "color_1_to_2", "color_any"],
                semantic_properties={"property_type": "color", "change_type": "discrete"},
                relationships={},
                instantiation_count=0,
                confidence=0.9,
                abstraction_path=[],
                linguistic_grounding=["color", "change", "transformation"]
            ),
            
            # Object concepts  
            SemanticConcept(
                concept_id="single_object",
                name="Single Object",
                level=ConceptualLevel.OBJECT,
                description="A single coherent visual object",
                visual_signatures=["connected_region", "isolated_shape"],
                semantic_properties={"object_count": 1, "coherence": "high"},
                relationships={},
                instantiation_count=0,
                confidence=0.8,
                abstraction_path=[],
                linguistic_grounding=["object", "thing", "entity"]
            ),
            
            # Relational concepts
            SemanticConcept(
                concept_id="spatial_adjacency",
                name="Spatial Adjacency", 
                level=ConceptualLevel.RELATIONAL,
                description="Objects that are next to each other",
                visual_signatures=["adjacent_cells", "touching_objects"],
                semantic_properties={"relation_type": "spatial", "distance": "zero"},
                relationships={},
                instantiation_count=0,
                confidence=0.7,
                abstraction_path=[],
                linguistic_grounding=["adjacent", "next_to", "touching"]
            )
        ]
        
        for concept in base_concepts:
            self.semantic_concepts[concept.concept_id] = concept
            self.abstraction_hierarchy.add_node(concept.concept_id, level=concept.level.value)
    
    def bootstrap_from_visual_patterns(self, visual_patterns: List[Dict[str, Any]]) -> List[SemanticConcept]:
        """Bootstrap semantic concepts from visual patterns"""
        logger.info(f"Bootstrapping concepts from {len(visual_patterns)} visual patterns")
        
        new_concepts = []
        
        # Group patterns by similarity
        pattern_groups = self._group_similar_patterns(visual_patterns)
        
        # Extract concepts from each group
        for group_id, group_patterns in pattern_groups.items():
            if len(group_patterns) >= 2:  # Need multiple examples
                concept = self._extract_concept_from_patterns(group_id, group_patterns)
                if concept:
                    new_concepts.append(concept)
        
        # Add new concepts to repository
        for concept in new_concepts:
            self.semantic_concepts[concept.concept_id] = concept
            self.abstraction_hierarchy.add_node(concept.concept_id, level=concept.level.value)
        
        # Create mappings between patterns and concepts
        self._create_pattern_concept_mappings(visual_patterns, new_concepts)
        
        logger.info(f"✅ Bootstrapped {len(new_concepts)} new semantic concepts")
        return new_concepts
    
    def _group_similar_patterns(self, patterns: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group similar visual patterns together"""
        groups = defaultdict(list)
        
        for pattern in patterns:
            # Create a signature for grouping
            signature = self._create_pattern_signature(pattern)
            groups[signature].append(pattern)
        
        return dict(groups)
    
    def _create_pattern_signature(self, pattern: Dict[str, Any]) -> str:
        """Create a signature for pattern grouping"""
        signature_parts = []
        
        # Include pattern type
        if 'type' in pattern:
            signature_parts.append(f"type:{pattern['type']}")
        
        # Include transformation aspects
        if 'transformation' in pattern:
            signature_parts.append(f"transform:{pattern['transformation']}")
        
        # Include object characteristics
        if 'objects' in pattern:
            objects = pattern['objects']
            if hasattr(objects, '__len__') and not isinstance(objects, str):
                signature_parts.append(f"objects:{len(objects)}")
            else:
                signature_parts.append(f"objects:{objects}")
        
        # Include spatial characteristics
        if 'spatial_pattern' in pattern:
            signature_parts.append(f"spatial:{pattern['spatial_pattern']}")
        
        return "||".join(signature_parts)
    
    def _extract_concept_from_patterns(self, group_id: str, 
                                     patterns: List[Dict[str, Any]]) -> Optional[SemanticConcept]:
        """Extract a semantic concept from a group of similar patterns"""
        
        # Determine concept level based on pattern characteristics
        concept_level = self._determine_concept_level(patterns)
        
        # Extract common features
        common_features = self._extract_common_features(patterns)
        
        if not common_features:
            return None
        
        # Generate concept properties
        concept_id = f"learned_{group_id}_{len(patterns)}"
        concept_name = self._generate_concept_name(common_features)
        description = self._generate_concept_description(common_features, patterns)
        
        visual_signatures = []
        for pattern in patterns:
            if 'signature' in pattern:
                visual_signatures.append(pattern['signature'])
        
        semantic_properties = {
            "pattern_frequency": len(patterns),
            "common_features": common_features,
            "complexity_level": self._assess_complexity(patterns)
        }
        
        concept = SemanticConcept(
            concept_id=concept_id,
            name=concept_name,
            level=concept_level,
            description=description,
            visual_signatures=visual_signatures,
            semantic_properties=semantic_properties,
            relationships={},
            instantiation_count=len(patterns),
            confidence=min(0.9, len(patterns) / 5.0),  # Higher confidence with more examples
            abstraction_path=[],
            linguistic_grounding=self._generate_linguistic_grounding(common_features)
        )
        
        return concept
    
    def _determine_concept_level(self, patterns: List[Dict[str, Any]]) -> ConceptualLevel:
        """Determine the appropriate conceptual level for patterns"""
        
        # Analyze pattern characteristics to determine level
        has_objects = any('objects' in p for p in patterns)
        has_relations = any('relations' in p for p in patterns)
        has_spatial = any('spatial' in str(p) for p in patterns)
        has_temporal = any('temporal' in str(p) or 'sequence' in str(p) for p in patterns)
        has_functional = any('function' in str(p) or 'purpose' in str(p) for p in patterns)
        
        if has_functional:
            return ConceptualLevel.FUNCTIONAL
        elif has_temporal:
            return ConceptualLevel.TEMPORAL
        elif has_spatial:
            return ConceptualLevel.SPATIAL
        elif has_relations:
            return ConceptualLevel.RELATIONAL
        elif has_objects:
            return ConceptualLevel.OBJECT
        else:
            return ConceptualLevel.PERCEPTUAL
    
    def _extract_common_features(self, patterns: List[Dict[str, Any]]) -> List[str]:
        """Extract features common across patterns"""
        if not patterns:
            return []
        
        # Get all possible features
        all_features = set()
        pattern_features = []
        
        for pattern in patterns:
            features = set()
            
            # Extract features from pattern structure
            for key, value in pattern.items():
                if isinstance(value, (str, int, float)):
                    features.add(f"{key}:{value}")
                elif isinstance(value, list):
                    features.add(f"{key}:list_{len(value)}")
                elif isinstance(value, dict):
                    features.add(f"{key}:dict")
            
            pattern_features.append(features)
            all_features.update(features)
        
        # Find features present in at least 70% of patterns
        threshold = len(patterns) * 0.7
        common_features = []
        
        for feature in all_features:
            count = sum(1 for p_features in pattern_features if feature in p_features)
            if count >= threshold:
                common_features.append(feature)
        
        return common_features
    
    def _generate_concept_name(self, common_features: List[str]) -> str:
        """Generate a human-readable name for the concept"""
        if not common_features:
            return "Unknown Concept"
        
        # Extract key terms from features
        key_terms = []
        for feature in common_features[:3]:  # Use top 3 features
            if ':' in feature:
                term = feature.split(':')[0]
                key_terms.append(term.replace('_', ' ').title())
        
        return ' '.join(key_terms) if key_terms else "Learned Concept"
    
    def _generate_concept_description(self, common_features: List[str], 
                                    patterns: List[Dict[str, Any]]) -> str:
        """Generate a description for the concept"""
        if not common_features:
            return "A concept learned from visual patterns"
        
        feature_desc = ', '.join(common_features[:5])  # Top 5 features
        return f"A concept characterized by {feature_desc}, learned from {len(patterns)} similar patterns"
    
    def _assess_complexity(self, patterns: List[Dict[str, Any]]) -> str:
        """Assess the complexity level of patterns"""
        avg_size = np.mean([len(str(p)) for p in patterns])
        
        if avg_size > 500:
            return "high"
        elif avg_size > 200:
            return "medium"
        else:
            return "low"
    
    def _generate_linguistic_grounding(self, common_features: List[str]) -> List[str]:
        """Generate linguistic grounding for the concept"""
        grounding = []
        
        for feature in common_features:
            if ':' in feature:
                term = feature.split(':')[0]
                grounding.append(term.replace('_', ' '))
        
        return grounding
    
    def _create_pattern_concept_mappings(self, patterns: List[Dict[str, Any]], 
                                       concepts: List[SemanticConcept]):
        """Create mappings between patterns and concepts"""
        
        for pattern in patterns:
            pattern_signature = self._create_pattern_signature(pattern)
            
            # Find best matching concept
            best_concept = None
            best_score = 0.0
            
            for concept in concepts:
                score = self._calculate_mapping_strength(pattern, concept)
                if score > best_score:
                    best_score = score
                    best_concept = concept
            
            # Create mapping if strong enough
            if best_concept and best_score > 0.5:
                mapping = ConceptualMapping(
                    pattern_id=pattern.get('id', pattern_signature),
                    concept_id=best_concept.concept_id,
                    mapping_strength=best_score,
                    evidence=[f"Pattern signature match: {best_score:.2f}"],
                    context="bootstrapping",
                    validation_examples=[]
                )
                self.conceptual_mappings.append(mapping)
    
    def _calculate_mapping_strength(self, pattern: Dict[str, Any], 
                                  concept: SemanticConcept) -> float:
        """Calculate the strength of mapping between pattern and concept"""
        
        pattern_signature = self._create_pattern_signature(pattern)
        
        # Check if pattern signature matches any visual signature
        signature_match = 0.0
        for visual_sig in concept.visual_signatures:
            if visual_sig in pattern_signature:
                signature_match = 1.0
                break
        
        # Check feature overlap
        pattern_features = set()
        for key, value in pattern.items():
            pattern_features.add(f"{key}:{value}")
        
        concept_features = set(concept.semantic_properties.get('common_features', []))
        feature_overlap = len(pattern_features & concept_features) / max(len(pattern_features), 1)
        
        # Combine scores
        mapping_strength = (signature_match * 0.6 + feature_overlap * 0.4)
        
        return mapping_strength
    
    def perform_conceptual_abstraction(self) -> List[SemanticConcept]:
        """Perform multi-level conceptual abstraction"""
        logger.info("🚀 Performing conceptual abstraction")
        
        new_abstract_concepts = []
        
        # Get concepts at each level
        level_concepts = defaultdict(list)
        for concept in self.semantic_concepts.values():
            level_concepts[concept.level].append(concept)
        
        # Perform abstraction for each level
        for level, abstractor in self.abstractors.items():
            if level in level_concepts and len(level_concepts[level]) >= 2:
                abstract_concepts = abstractor.abstract_concepts(level_concepts[level])
                new_abstract_concepts.extend(abstract_concepts)
        
        # Add new abstract concepts
        for concept in new_abstract_concepts:
            self.semantic_concepts[concept.concept_id] = concept
            self.abstraction_hierarchy.add_node(concept.concept_id, level=concept.level.value)
            
            # Add edges in abstraction hierarchy
            for source_concept_id in concept.abstraction_path:
                self.abstraction_hierarchy.add_edge(source_concept_id, concept.concept_id)
        
        logger.info(f"✅ Created {len(new_abstract_concepts)} abstract concepts")
        return new_abstract_concepts
    
    def bridge_to_language(self, concepts: List[SemanticConcept]) -> Dict[str, List[str]]:
        """Bridge semantic concepts to natural language descriptions"""
        logger.info("🌉 Bridging concepts to language")
        
        language_bridges = {}
        
        for concept in concepts:
            descriptions = []
            
            # Generate basic description
            descriptions.append(concept.description)
            
            # Add property-based descriptions
            for prop_name, prop_value in concept.semantic_properties.items():
                descriptions.append(f"Has {prop_name.replace('_', ' ')}: {prop_value}")
            
            # Add relational descriptions
            for rel_type, related_concepts in concept.relationships.items():
                if related_concepts:
                    descriptions.append(f"{rel_type.replace('_', ' ').title()} {len(related_concepts)} other concepts")
            
            # Add linguistic grounding
            if concept.linguistic_grounding:
                descriptions.append(f"Related to: {', '.join(concept.linguistic_grounding)}")
            
            language_bridges[concept.concept_id] = descriptions
        
        return language_bridges
    
    def find_concept_analogies(self, source_concept_id: str, 
                             candidates: Optional[List[str]] = None) -> List[Tuple[str, float]]:
        """Find analogous concepts based on structural similarity"""
        
        if source_concept_id not in self.semantic_concepts:
            return []
        
        source_concept = self.semantic_concepts[source_concept_id]
        candidates = candidates or list(self.semantic_concepts.keys())
        
        analogies = []
        
        for candidate_id in candidates:
            if candidate_id == source_concept_id:
                continue
                
            candidate_concept = self.semantic_concepts[candidate_id]
            similarity = self._calculate_concept_similarity(source_concept, candidate_concept)
            
            if similarity > 0.3:  # Threshold for considering as analogy
                analogies.append((candidate_id, similarity))
        
        # Sort by similarity
        analogies.sort(key=lambda x: x[1], reverse=True)
        
        return analogies[:5]  # Top 5 analogies
    
    def _calculate_concept_similarity(self, concept1: SemanticConcept, 
                                   concept2: SemanticConcept) -> float:
        """Calculate similarity between two concepts"""
        
        similarity_scores = []
        
        # Level similarity
        level_similarity = 1.0 if concept1.level == concept2.level else 0.5
        similarity_scores.append(level_similarity)
        
        # Property similarity
        props1 = set(concept1.semantic_properties.keys())
        props2 = set(concept2.semantic_properties.keys())
        prop_similarity = len(props1 & props2) / max(len(props1 | props2), 1)
        similarity_scores.append(prop_similarity)
        
        # Linguistic grounding similarity
        ling1 = set(concept1.linguistic_grounding)
        ling2 = set(concept2.linguistic_grounding)
        ling_similarity = len(ling1 & ling2) / max(len(ling1 | ling2), 1)
        similarity_scores.append(ling_similarity)
        
        # Relationship similarity
        rel1 = set(concept1.relationships.keys())
        rel2 = set(concept2.relationships.keys())
        rel_similarity = len(rel1 & rel2) / max(len(rel1 | rel2), 1)
        similarity_scores.append(rel_similarity)
        
        # Average similarity
        return float(np.mean(similarity_scores))
    
    def generate_concept_explanations(self, concept_id: str) -> List[str]:
        """Generate natural language explanations for a concept"""
        
        if concept_id not in self.semantic_concepts:
            return ["Concept not found"]
        
        concept = self.semantic_concepts[concept_id]
        explanations = []
        
        # Basic explanation
        explanations.append(f"{concept.name} is {concept.description}")
        
        # Level-based explanation
        explanations.append(f"This is a {concept.level.value}-level concept")
        
        # Property explanations
        for prop_name, prop_value in concept.semantic_properties.items():
            explanations.append(f"It has the property {prop_name.replace('_', ' ')}: {prop_value}")
        
        # Confidence explanation
        explanations.append(f"Confidence in this concept: {concept.confidence:.0%}")
        
        # Instantiation explanation
        explanations.append(f"This concept has been observed {concept.instantiation_count} times")
        
        # Abstraction explanation
        if concept.abstraction_path:
            explanations.append(f"This concept was derived from: {', '.join(concept.abstraction_path)}")
        
        return explanations
    
    def get_semantic_summary(self) -> Dict[str, Any]:
        """Generate a comprehensive summary of the semantic system"""
        
        summary = {
            "total_concepts": len(self.semantic_concepts),
            "concepts_by_level": Counter([c.level.value for c in self.semantic_concepts.values()]),
            "total_mappings": len(self.conceptual_mappings),
            "abstraction_depth": len(self.abstraction_hierarchy) if self.abstraction_hierarchy else 0,
            "average_confidence": np.mean([c.confidence for c in self.semantic_concepts.values()]) if self.semantic_concepts else 0.0,
            "total_instantiations": sum([c.instantiation_count for c in self.semantic_concepts.values()]),
            "concepts_with_language": sum(1 for c in self.semantic_concepts.values() if c.linguistic_grounding)
        }
        
        return summary
