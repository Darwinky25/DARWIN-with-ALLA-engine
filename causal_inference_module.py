#!/usr/bin/env python3
"""
ALLA Causal Inference Module - Understanding "Why" Things Change
Infers causal relationships between objects, actions, and transformations in ARC tasks
"""

import numpy as np
from typing import Dict, List, Tuple, Any, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import logging
from visual_scene_parser import VisualObject, SceneRepresentation, SpatialRelation
from visual_difference_analyzer import TransformationRule, SceneTransformation

logger = logging.getLogger(__name__)

class CausalRelationType(Enum):
    TRIGGER = "trigger"  # A causes B to happen
    ENABLE = "enable"    # A enables B to happen
    PREVENT = "prevent"  # A prevents B from happening
    CORRELATE = "correlate"  # A and B happen together
    SEQUENCE = "sequence"    # A happens before B

@dataclass
class CausalRelation:
    """Represents a causal relationship between events or objects"""
    cause: str  # What causes the effect
    effect: str  # What is the effect
    relation_type: CausalRelationType
    confidence: float
    evidence: List[str] = field(default_factory=list)
    context: str = ""

@dataclass
class CausalChain:
    """Represents a chain of causal relationships"""
    chain_id: str
    relations: List[CausalRelation]
    start_condition: str
    end_result: str
    confidence: float
    description: str = ""

@dataclass
class CausalExplanation:
    """Complete causal explanation for a transformation"""
    transformation_id: str
    primary_cause: str
    causal_chain: CausalChain
    alternative_explanations: List[CausalChain] = field(default_factory=list)
    confidence: float = 0.0

class CausalInferenceModule:
    """Infers causal relationships to understand why transformations occur"""
    
    def __init__(self):
        self.causal_knowledge_base = {}  # Store learned causal patterns
        self.causal_rules = {
            'spatial_proximity': self._infer_proximity_causation,
            'temporal_sequence': self._infer_temporal_causation,
            'property_change': self._infer_property_causation,
            'pattern_completion': self._infer_pattern_causation,
            'physics_based': self._infer_physics_causation
        }
        self.explanation_history = []
    
    def infer_causation(self, transformation: SceneTransformation, 
                       physics_events: Optional[List] = None) -> CausalExplanation:
        """Infer causal explanation for a transformation"""
        
        input_scene = transformation.input_scene
        output_scene = transformation.output_scene
        rules = transformation.transformation_rules
        
        # Generate candidate causal relations
        candidate_relations = []
        
        # Apply each causal inference rule
        for rule_name, rule_func in self.causal_rules.items():
            try:
                relations = rule_func(input_scene, output_scene, rules, physics_events or [])
                candidate_relations.extend(relations)
            except Exception as e:
                logger.warning(f"Causal rule {rule_name} failed: {e}")
        
        # Build causal chains from relations
        causal_chains = self._build_causal_chains(candidate_relations)
        
        # Select best explanation
        primary_chain = self._select_best_explanation(causal_chains)
        
        # Create explanation
        explanation = CausalExplanation(
            transformation_id=f"transform_{len(self.explanation_history)}",
            primary_cause=primary_chain.start_condition if primary_chain else "unknown",
            causal_chain=primary_chain if primary_chain else self._create_default_chain(),
            alternative_explanations=causal_chains[1:5] if len(causal_chains) > 1 else [],
            confidence=primary_chain.confidence if primary_chain else 0.0
        )
        
        self.explanation_history.append(explanation)
        
        logger.info(f"Causal inference: {explanation.primary_cause} -> {explanation.causal_chain.end_result}")
        
        return explanation
    
    def _infer_proximity_causation(self, input_scene: SceneRepresentation, 
                                  output_scene: SceneRepresentation,
                                  rules: List[TransformationRule],
                                  physics_events: List) -> List[CausalRelation]:
        """Infer causation based on spatial proximity"""
        relations = []
        
        # Find objects that changed and their neighbors
        input_objects = {obj.object_id: obj for obj in input_scene.objects}
        output_objects = {obj.object_id: obj for obj in output_scene.objects}
        
        # Identify changed objects
        changed_objects = []
        for rule in rules:
            if hasattr(rule, 'affected_objects'):
                changed_objects.extend(rule.affected_objects)
        
        # For each changed object, check proximity to other objects
        for obj_id in changed_objects:
            if obj_id in input_objects:
                input_obj = input_objects[obj_id]
                
                # Find nearby objects
                nearby_objects = self._find_nearby_objects(input_obj, input_scene.objects)
                
                for nearby_obj in nearby_objects:
                    # Infer that nearby object might have caused the change
                    relation = CausalRelation(
                        cause=f"proximity_to_{nearby_obj.object_id}",
                        effect=f"change_in_{obj_id}",
                        relation_type=CausalRelationType.TRIGGER,
                        confidence=0.6,
                        evidence=[f"Objects {obj_id} and {nearby_obj.object_id} are adjacent"],
                        context="spatial_proximity"
                    )
                    relations.append(relation)
        
        return relations
    
    def _find_nearby_objects(self, target_obj: VisualObject, 
                           all_objects: List[VisualObject]) -> List[VisualObject]:
        """Find objects near the target object"""
        nearby = []
        target_center = target_obj.center_of_mass
        
        for obj in all_objects:
            if obj.object_id != target_obj.object_id:
                distance = np.sqrt((obj.center_of_mass[0] - target_center[0])**2 + 
                                 (obj.center_of_mass[1] - target_center[1])**2)
                
                if distance <= 3.0:  # Nearby threshold
                    nearby.append(obj)
        
        return nearby
    
    def _infer_temporal_causation(self, input_scene: SceneRepresentation, 
                                 output_scene: SceneRepresentation,
                                 rules: List[TransformationRule],
                                 physics_events: List) -> List[CausalRelation]:
        """Infer causation based on temporal sequence"""
        relations = []
        
        if physics_events:
            # Create causal chain from physics events
            for i, event in enumerate(physics_events):
                if i > 0:
                    prev_event = physics_events[i-1]
                    
                    relation = CausalRelation(
                        cause=f"{prev_event.event_type}_{prev_event.frame}",
                        effect=f"{event.event_type}_{event.frame}",
                        relation_type=CausalRelationType.SEQUENCE,
                        confidence=0.8,
                        evidence=[f"Event {prev_event.event_type} preceded {event.event_type}"],
                        context="temporal_sequence"
                    )
                    relations.append(relation)
        
        return relations
    
    def _infer_property_causation(self, input_scene: SceneRepresentation, 
                                 output_scene: SceneRepresentation,
                                 rules: List[TransformationRule],
                                 physics_events: List) -> List[CausalRelation]:
        """Infer causation based on property changes"""
        relations = []
        
        for rule in rules:
            if rule.rule_type == "color_change":
                # Color change might be caused by specific patterns
                cause_description = self._identify_color_change_cause(rule, input_scene)
                
                relation = CausalRelation(
                    cause=cause_description,
                    effect=f"color_change_{rule.parameters.get('to_color', 'unknown')}",
                    relation_type=CausalRelationType.TRIGGER,
                    confidence=0.7,
                    evidence=[rule.description],
                    context="property_change"
                )
                relations.append(relation)
            
            elif rule.rule_type == "move_object":
                # Movement might be caused by physics or pattern rules
                cause = self._identify_movement_cause(rule, input_scene, physics_events)
                
                relation = CausalRelation(
                    cause=cause,
                    effect=f"movement_{rule.parameters.get('direction', 'unknown')}",
                    relation_type=CausalRelationType.TRIGGER,
                    confidence=0.8,
                    evidence=[rule.description],
                    context="movement_causation"
                )
                relations.append(relation)
        
        return relations
    
    def _identify_color_change_cause(self, rule: TransformationRule, 
                                   scene: SceneRepresentation) -> str:
        """Identify what might cause a color change"""
        # Check for patterns that might trigger color change
        
        if "symmetrical" in scene.dominant_patterns:
            return "symmetry_completion"
        elif "aligned" in scene.dominant_patterns:
            return "alignment_rule"
        elif len(scene.objects) > 3:
            return "object_interaction"
        else:
            return "intrinsic_property_change"
    
    def _identify_movement_cause(self, rule: TransformationRule, 
                               scene: SceneRepresentation,
                               physics_events: List) -> str:
        """Identify what might cause object movement"""
        direction = rule.parameters.get('direction', '')
        
        # Check if gravity is likely cause
        if direction in ['down', 'down_left', 'down_right']:
            return "gravity_force"
        
        # Check for physics events
        if physics_events and any(e.event_type == 'fall' for e in physics_events):
            return "physics_simulation"
        
        # Check for pattern-based movement
        if "aligned" in scene.dominant_patterns:
            return "pattern_alignment"
        elif "symmetrical" in scene.dominant_patterns:
            return "symmetry_requirement"
        else:
            return "rule_based_movement"
    
    def _infer_pattern_causation(self, input_scene: SceneRepresentation, 
                               output_scene: SceneRepresentation,
                               rules: List[TransformationRule],
                               physics_events: List) -> List[CausalRelation]:
        """Infer causation based on pattern completion"""
        relations = []
        
        input_patterns = set(input_scene.dominant_patterns)
        output_patterns = set(output_scene.dominant_patterns)
        
        new_patterns = output_patterns - input_patterns
        lost_patterns = input_patterns - output_patterns
        
        # Pattern emergence causation
        for pattern in new_patterns:
            if pattern == "symmetrical":
                relation = CausalRelation(
                    cause="symmetry_requirement",
                    effect="symmetrical_arrangement",
                    relation_type=CausalRelationType.TRIGGER,
                    confidence=0.8,
                    evidence=[f"Symmetry pattern emerged"],
                    context="pattern_completion"
                )
                relations.append(relation)
            
            elif pattern == "aligned":
                relation = CausalRelation(
                    cause="alignment_force",
                    effect="object_alignment",
                    relation_type=CausalRelationType.TRIGGER,
                    confidence=0.7,
                    evidence=[f"Alignment pattern emerged"],
                    context="pattern_completion"
                )
                relations.append(relation)
        
        return relations
    
    def _infer_physics_causation(self, input_scene: SceneRepresentation, 
                               output_scene: SceneRepresentation,
                               rules: List[TransformationRule],
                               physics_events: List) -> List[CausalRelation]:
        """Infer causation based on physics principles"""
        relations = []
        
        if not physics_events:
            return relations
        
        for event in physics_events:
            if event.event_type == "fall":
                relation = CausalRelation(
                    cause="gravitational_force",
                    effect="downward_movement",
                    relation_type=CausalRelationType.TRIGGER,
                    confidence=0.9,
                    evidence=[event.description],
                    context="physics_law"
                )
                relations.append(relation)
            
            elif event.event_type == "flow":
                relation = CausalRelation(
                    cause="fluid_dynamics",
                    effect="horizontal_spreading",
                    relation_type=CausalRelationType.TRIGGER,
                    confidence=0.8,
                    evidence=[event.description],
                    context="physics_law"
                )
                relations.append(relation)
        
        return relations
    
    def _build_causal_chains(self, relations: List[CausalRelation]) -> List[CausalChain]:
        """Build causal chains from individual relations"""
        if not relations:
            return []
        
        chains = []
        
        # Group relations by context
        context_groups = {}
        for relation in relations:
            context = relation.context
            if context not in context_groups:
                context_groups[context] = []
            context_groups[context].append(relation)
        
        # Create chains for each context
        for context, context_relations in context_groups.items():
            if len(context_relations) == 1:
                # Single relation chain
                rel = context_relations[0]
                chain = CausalChain(
                    chain_id=f"chain_{context}",
                    relations=[rel],
                    start_condition=rel.cause,
                    end_result=rel.effect,
                    confidence=rel.confidence,
                    description=f"{rel.cause} causes {rel.effect}"
                )
                chains.append(chain)
            
            else:
                # Multi-relation chain
                chain_confidence = sum(r.confidence for r in context_relations) / len(context_relations)
                
                chain = CausalChain(
                    chain_id=f"chain_{context}_multi",
                    relations=context_relations,
                    start_condition=context_relations[0].cause,
                    end_result=context_relations[-1].effect,
                    confidence=chain_confidence,
                    description=f"Multi-step causation in {context}"
                )
                chains.append(chain)
        
        return chains
    
    def _select_best_explanation(self, chains: List[CausalChain]) -> Optional[CausalChain]:
        """Select the best causal explanation from candidates"""
        if not chains:
            return None
        
        # Sort by confidence and complexity
        def chain_score(chain):
            confidence_score = chain.confidence
            complexity_penalty = len(chain.relations) * 0.05  # Prefer simpler explanations
            return confidence_score - complexity_penalty
        
        chains.sort(key=chain_score, reverse=True)
        return chains[0]
    
    def _create_default_chain(self) -> CausalChain:
        """Create default causal chain when no good explanation is found"""
        default_relation = CausalRelation(
            cause="unknown_rule",
            effect="observed_change",
            relation_type=CausalRelationType.CORRELATE,
            confidence=0.1,
            evidence=["No clear causal explanation found"],
            context="default"
        )
        
        return CausalChain(
            chain_id="default_chain",
            relations=[default_relation],
            start_condition="unknown_rule",
            end_result="observed_change",
            confidence=0.1,
            description="Unable to determine clear causation"
        )
    
    def explain_transformation(self, explanation: CausalExplanation) -> str:
        """Generate human-readable explanation of the transformation"""
        chain = explanation.causal_chain
        
        if not chain.relations:
            return "No clear causal explanation could be determined."
        
        explanation_parts = []
        
        # Start with primary cause
        explanation_parts.append(f"The transformation occurred because of {explanation.primary_cause}")
        
        # Describe the causal chain
        if len(chain.relations) == 1:
            rel = chain.relations[0]
            explanation_parts.append(f"which {rel.relation_type.value}s {rel.effect}")
        else:
            explanation_parts.append("which triggered a sequence of events:")
            for i, rel in enumerate(chain.relations):
                explanation_parts.append(f"  {i+1}. {rel.cause} {rel.relation_type.value}s {rel.effect}")
        
        # Add confidence
        confidence_text = "high" if explanation.confidence > 0.8 else "medium" if explanation.confidence > 0.5 else "low"
        explanation_parts.append(f"(Confidence: {confidence_text})")
        
        return " ".join(explanation_parts)
    
    def learn_causal_pattern(self, explanation: CausalExplanation, success: bool):
        """Learn from causal explanations to improve future inference"""
        pattern_key = f"{explanation.primary_cause}_{explanation.causal_chain.end_result}"
        
        if pattern_key not in self.causal_knowledge_base:
            self.causal_knowledge_base[pattern_key] = {
                'occurrences': 0,
                'successes': 0,
                'confidence': 0.0,
                'examples': []
            }
        
        pattern = self.causal_knowledge_base[pattern_key]
        pattern['occurrences'] += 1
        
        if success:
            pattern['successes'] += 1
        
        # Update confidence based on success rate
        pattern['confidence'] = pattern['successes'] / pattern['occurrences']
        
        # Store example
        pattern['examples'].append({
            'explanation_id': explanation.transformation_id,
            'success': success,
            'chain_description': explanation.causal_chain.description
        })
        
        # Keep only recent examples
        if len(pattern['examples']) > 10:
            pattern['examples'] = pattern['examples'][-10:]
    
    def get_causal_insights(self) -> Dict[str, Any]:
        """Get insights about learned causal patterns"""
        if not self.causal_knowledge_base:
            return {"message": "No causal patterns learned yet"}
        
        insights = {
            'total_patterns': len(self.causal_knowledge_base),
            'reliable_patterns': [],
            'unreliable_patterns': [],
            'most_common_causes': {},
            'most_common_effects': {}
        }
        
        # Analyze patterns
        for pattern_key, pattern_data in self.causal_knowledge_base.items():
            if pattern_data['confidence'] > 0.7 and pattern_data['occurrences'] >= 3:
                insights['reliable_patterns'].append({
                    'pattern': pattern_key,
                    'confidence': pattern_data['confidence'],
                    'occurrences': pattern_data['occurrences']
                })
            elif pattern_data['confidence'] < 0.3:
                insights['unreliable_patterns'].append({
                    'pattern': pattern_key,
                    'confidence': pattern_data['confidence'],
                    'occurrences': pattern_data['occurrences']
                })
        
        return insights

def main():
    """Test the causal inference module"""
    causal_module = CausalInferenceModule()
    
    print("🔗 Causal Inference Module Test")
    print("Module initialized and ready for causal reasoning")
    
    # This would be called by the main system with real transformation data
    print("✓ Causal inference patterns:")
    for rule_name in causal_module.causal_rules.keys():
        print(f"  - {rule_name}")

if __name__ == "__main__":
    main()
