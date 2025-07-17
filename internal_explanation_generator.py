#!/usr/bin/env python3
"""
ALLA Internal Explanation Generator - Natural Language Self-Explanation
Generates human-like explanations for ALLA's reasoning process
"""

import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, field
import logging
from visual_scene_parser import SceneRepresentation, VisualObject
from visual_difference_analyzer import SceneTransformation, TransformationRule
from causal_inference_module import CausalExplanation, CausalChain
from micro_physics_engine import PhysicsEvent

logger = logging.getLogger(__name__)

@dataclass
class ExplanationComponent:
    """A component of an explanation"""
    component_type: str  # "observation", "inference", "conclusion", "reasoning_step"
    content: str
    confidence: float
    supporting_evidence: List[str] = field(default_factory=list)

@dataclass
class InternalExplanation:
    """Complete internal explanation of ALLA's reasoning"""
    explanation_id: str
    task_description: str
    reasoning_components: List[ExplanationComponent]
    confidence: float
    explanation_text: str
    meta_reasoning: str = ""  # Explanation of the explanation process

class InternalExplanationGenerator:
    """Generates natural language explanations of ALLA's reasoning process"""
    
    def __init__(self):
        self.explanation_templates = {
            'observation': [
                "I observe that {observation}",
                "Looking at the input, I can see {observation}",
                "The scene contains {observation}",
                "I notice {observation}"
            ],
            'inference': [
                "This suggests that {inference}",
                "From this, I can infer that {inference}",
                "This leads me to believe that {inference}",
                "I conclude that {inference}"
            ],
            'causal': [
                "This happens because {cause}",
                "The reason for this is {cause}",
                "{cause} causes this transformation",
                "I think {cause} is responsible for this change"
            ],
            'physics': [
                "Following the rules of physics, {physics_rule}",
                "Due to {physics_rule}, objects will {physics_effect}",
                "Physics tells us that {physics_rule}",
                "The physical law of {physics_rule} applies here"
            ],
            'pattern': [
                "I recognize the pattern: {pattern}",
                "This follows a {pattern} pattern",
                "The transformation shows {pattern}",
                "I see a {pattern} structure"
            ],
            'prediction': [
                "Therefore, I predict that {prediction}",
                "Based on this reasoning, {prediction} should happen",
                "My conclusion is that {prediction}",
                "I expect {prediction} to occur"
            ]
        }
        
        self.common_sense_knowledge = {
            'gravity': "objects fall downward unless supported",
            'collision': "objects stop when they hit something solid",
            'symmetry': "patterns tend to be balanced and symmetrical",
            'containment': "objects stay within their containers",
            'alignment': "similar objects often align with each other",
            'color_consistency': "color changes usually follow systematic rules",
            'size_preservation': "objects typically maintain their size unless explicitly transformed"
        }
    
    def generate_explanation(self, 
                           scene_transformation: SceneTransformation,
                           causal_explanation: CausalExplanation,
                           physics_events: List[PhysicsEvent] = None,
                           reasoning_trace: List[str] = None) -> InternalExplanation:
        """Generate complete internal explanation"""
        
        explanation_components = []
        
        # 1. Initial observations
        observation_components = self._generate_observation_explanations(scene_transformation)
        explanation_components.extend(observation_components)
        
        # 2. Difference analysis
        difference_components = self._generate_difference_explanations(scene_transformation)
        explanation_components.extend(difference_components)
        
        # 3. Causal reasoning
        causal_components = self._generate_causal_explanations(causal_explanation)
        explanation_components.extend(causal_components)
        
        # 4. Physics reasoning
        if physics_events:
            physics_components = self._generate_physics_explanations(physics_events)
            explanation_components.extend(physics_components)
        
        # 5. Pattern recognition
        pattern_components = self._generate_pattern_explanations(scene_transformation)
        explanation_components.extend(pattern_components)
        
        # 6. Final prediction/conclusion
        conclusion_components = self._generate_conclusion_explanations(scene_transformation)
        explanation_components.extend(conclusion_components)
        
        # Compile into coherent explanation
        explanation_text = self._compile_explanation_text(explanation_components)
        
        # Calculate overall confidence
        overall_confidence = self._calculate_explanation_confidence(explanation_components)
        
        # Generate meta-reasoning
        meta_reasoning = self._generate_meta_reasoning(explanation_components)
        
        explanation = InternalExplanation(
            explanation_id=f"explanation_{len(explanation_components)}",
            task_description=self._generate_task_description(scene_transformation),
            reasoning_components=explanation_components,
            confidence=overall_confidence,
            explanation_text=explanation_text,
            meta_reasoning=meta_reasoning
        )
        
        logger.info(f"Generated explanation with {len(explanation_components)} components")
        return explanation
    
    def _generate_observation_explanations(self, transformation: SceneTransformation) -> List[ExplanationComponent]:
        """Generate explanations for initial observations"""
        components = []
        
        input_scene = transformation.input_scene
        output_scene = transformation.output_scene
        
        # Describe input scene
        input_description = self._describe_scene(input_scene, "input")
        components.append(ExplanationComponent(
            component_type="observation",
            content=f"I observe that the input scene has {input_description}",
            confidence=0.9,
            supporting_evidence=[f"Input analysis: {len(input_scene.objects)} objects"]
        ))
        
        # Describe output scene
        output_description = self._describe_scene(output_scene, "output")
        components.append(ExplanationComponent(
            component_type="observation",
            content=f"The output scene shows {output_description}",
            confidence=0.9,
            supporting_evidence=[f"Output analysis: {len(output_scene.objects)} objects"]
        ))
        
        return components
    
    def _describe_scene(self, scene: SceneRepresentation, scene_type: str) -> str:
        """Generate natural description of a scene"""
        parts = []
        
        # Object count and types
        if len(scene.objects) == 0:
            parts.append("no objects")
        elif len(scene.objects) == 1:
            obj = scene.objects[0]
            parts.append(f"one {self._describe_object(obj)}")
        else:
            parts.append(f"{len(scene.objects)} objects")
            
            # Describe object types
            shape_counts = {}
            for obj in scene.objects:
                shape = obj.shape_type
                shape_counts[shape] = shape_counts.get(shape, 0) + 1
            
            shape_descriptions = []
            for shape, count in shape_counts.items():
                if count == 1:
                    shape_descriptions.append(f"a {shape}")
                else:
                    shape_descriptions.append(f"{count} {shape}s")
            
            if shape_descriptions:
                parts.append(f"including {', '.join(shape_descriptions)}")
        
        # Grid size
        parts.append(f"in a {scene.grid_size[0]}x{scene.grid_size[1]} grid")
        
        # Patterns
        if scene.dominant_patterns:
            pattern_text = ", ".join(scene.dominant_patterns)
            parts.append(f"with {pattern_text} characteristics")
        
        return " ".join(parts)
    
    def _describe_object(self, obj: VisualObject) -> str:
        """Generate natural description of an object"""
        color_names = {
            0: "black", 1: "blue", 2: "red", 3: "green", 4: "yellow",
            5: "grey", 6: "pink", 7: "orange", 8: "cyan", 9: "brown"
        }
        
        color_name = color_names.get(obj.color, f"color-{obj.color}")
        
        if obj.size == 1:
            return f"{color_name} dot"
        else:
            return f"{color_name} {obj.shape_type} of size {obj.size}"
    
    def _generate_difference_explanations(self, transformation: SceneTransformation) -> List[ExplanationComponent]:
        """Generate explanations for observed differences"""
        components = []
        
        for rule in transformation.transformation_rules:
            explanation = self._explain_transformation_rule(rule)
            
            components.append(ExplanationComponent(
                component_type="inference",
                content=explanation,
                confidence=rule.confidence,
                supporting_evidence=rule.evidence
            ))
        
        return components
    
    def _explain_transformation_rule(self, rule: TransformationRule) -> str:
        """Generate natural explanation for a transformation rule"""
        rule_explanations = {
            'color_change': "I notice that {affected_objects} changed color from {from_color} to {to_color}",
            'move_object': "I see that objects moved {direction}",
            'size_increase': "Objects became larger",
            'size_decrease': "Objects became smaller",
            'add_objects': "New objects appeared in the scene",
            'remove_objects': "Some objects disappeared from the scene",
            'grid_tiling': "The entire pattern was repeated in a tiling arrangement",
            'scale_up': "The whole scene was scaled up by a factor",
            'pattern_emergence': "A new pattern ({pattern}) emerged",
            'spatial_change': "The spatial relationships between objects changed"
        }
        
        template = rule_explanations.get(rule.rule_type, f"A {rule.rule_type} transformation occurred")
        
        # Fill in parameters
        try:
            return template.format(**rule.parameters)
        except (KeyError, AttributeError):
            return f"I observe a {rule.rule_type}: {rule.description}"
    
    def _generate_causal_explanations(self, causal_explanation: CausalExplanation) -> List[ExplanationComponent]:
        """Generate explanations for causal reasoning"""
        components = []
        
        if causal_explanation.primary_cause != "unknown":
            # Explain the primary cause
            components.append(ExplanationComponent(
                component_type="reasoning_step",
                content=f"I believe this transformation occurs because of {causal_explanation.primary_cause}",
                confidence=causal_explanation.confidence,
                supporting_evidence=[causal_explanation.causal_chain.description]
            ))
            
            # Explain the causal chain
            chain = causal_explanation.causal_chain
            if len(chain.relations) > 1:
                chain_explanation = self._explain_causal_chain(chain)
                components.append(ExplanationComponent(
                    component_type="reasoning_step",
                    content=chain_explanation,
                    confidence=chain.confidence,
                    supporting_evidence=[rel.cause for rel in chain.relations]
                ))
        
        return components
    
    def _explain_causal_chain(self, chain: CausalChain) -> str:
        """Explain a causal chain in natural language"""
        if len(chain.relations) == 1:
            rel = chain.relations[0]
            return f"Specifically, {rel.cause} {rel.relation_type.value}s {rel.effect}"
        
        parts = ["This happens through a series of steps:"]
        for i, rel in enumerate(chain.relations):
            parts.append(f"({i+1}) {rel.cause} {rel.relation_type.value}s {rel.effect}")
        
        return " ".join(parts)
    
    def _generate_physics_explanations(self, physics_events: List[PhysicsEvent]) -> List[ExplanationComponent]:
        """Generate explanations for physics reasoning"""
        components = []
        
        if not physics_events:
            return components
        
        # Group events by type
        event_groups = {}
        for event in physics_events:
            event_type = event.event_type
            if event_type not in event_groups:
                event_groups[event_type] = []
            event_groups[event_type].append(event)
        
        # Explain each type of physics event
        for event_type, events in event_groups.items():
            physics_explanation = self._explain_physics_events(event_type, events)
            
            components.append(ExplanationComponent(
                component_type="reasoning_step",
                content=physics_explanation,
                confidence=sum(e.confidence for e in events) / len(events),
                supporting_evidence=[e.description for e in events[:3]]  # Top 3 events
            ))
        
        return components
    
    def _explain_physics_events(self, event_type: str, events: List[PhysicsEvent]) -> str:
        """Explain physics events in natural language"""
        physics_explanations = {
            'fall': "Following the law of gravity, objects naturally fall downward until they encounter a solid surface",
            'flow': "Like a fluid, the material spreads horizontally to fill available space",
            'collision': "Objects stop moving when they collide with solid barriers",
            'bounce': "When objects hit surfaces, they bounce back according to physics principles"
        }
        
        base_explanation = physics_explanations.get(event_type, f"Physics event of type {event_type} occurred")
        
        if len(events) > 1:
            return f"{base_explanation} This happened {len(events)} times in the simulation"
        else:
            return base_explanation
    
    def _generate_pattern_explanations(self, transformation: SceneTransformation) -> List[ExplanationComponent]:
        """Generate explanations for pattern recognition"""
        components = []
        
        input_patterns = set(transformation.input_scene.dominant_patterns)
        output_patterns = set(transformation.output_scene.dominant_patterns)
        
        # Patterns that emerged
        new_patterns = output_patterns - input_patterns
        for pattern in new_patterns:
            components.append(ExplanationComponent(
                component_type="inference",
                content=f"I recognize that a {pattern} pattern has emerged in the output",
                confidence=0.7,
                supporting_evidence=[f"Pattern analysis shows {pattern}"]
            ))
        
        # Patterns that were preserved
        preserved_patterns = input_patterns & output_patterns
        if preserved_patterns:
            components.append(ExplanationComponent(
                component_type="observation",
                content=f"The {', '.join(preserved_patterns)} characteristics are maintained",
                confidence=0.8,
                supporting_evidence=[f"Pattern consistency across transformation"]
            ))
        
        return components
    
    def _generate_conclusion_explanations(self, transformation: SceneTransformation) -> List[ExplanationComponent]:
        """Generate conclusion explanations"""
        components = []
        
        # Overall transformation summary
        transformation_summary = self._summarize_transformation(transformation)
        
        components.append(ExplanationComponent(
            component_type="conclusion",
            content=f"In summary, {transformation_summary}",
            confidence=transformation.confidence,
            supporting_evidence=[f"Transformation type: {transformation.transformation_type}"]
        ))
        
        # Confidence in reasoning
        if transformation.confidence > 0.8:
            confidence_text = "I am quite confident in this analysis"
        elif transformation.confidence > 0.5:
            confidence_text = "I am moderately confident in this reasoning"
        else:
            confidence_text = "I am somewhat uncertain about this interpretation"
        
        components.append(ExplanationComponent(
            component_type="conclusion",
            content=confidence_text,
            confidence=transformation.confidence,
            supporting_evidence=[f"Overall confidence: {transformation.confidence:.2f}"]
        ))
        
        return components
    
    def _summarize_transformation(self, transformation: SceneTransformation) -> str:
        """Summarize the overall transformation"""
        rule_types = [rule.rule_type for rule in transformation.transformation_rules]
        
        if 'grid_tiling' in rule_types:
            return "this transformation repeats the input pattern in a tiled arrangement"
        elif 'color_change' in rule_types:
            return "this transformation involves systematic color changes"
        elif 'move_object' in rule_types:
            return "this transformation moves objects according to specific rules"
        elif 'scale_up' in rule_types:
            return "this transformation scales up the input pattern"
        else:
            return f"this is a {transformation.transformation_type} transformation with {len(rule_types)} distinct changes"
    
    def _compile_explanation_text(self, components: List[ExplanationComponent]) -> str:
        """Compile explanation components into coherent text"""
        text_parts = []
        
        # Group components by type for better flow
        observations = [c for c in components if c.component_type == "observation"]
        inferences = [c for c in components if c.component_type == "inference"]
        reasoning_steps = [c for c in components if c.component_type == "reasoning_step"]
        conclusions = [c for c in components if c.component_type == "conclusion"]
        
        # Add observations
        if observations:
            text_parts.append("OBSERVATIONS:")
            for obs in observations:
                text_parts.append(f"- {obs.content}")
        
        # Add inferences
        if inferences:
            text_parts.append("\nANALYSIS:")
            for inf in inferences:
                text_parts.append(f"- {inf.content}")
        
        # Add reasoning steps
        if reasoning_steps:
            text_parts.append("\nREASONING:")
            for step in reasoning_steps:
                text_parts.append(f"- {step.content}")
        
        # Add conclusions
        if conclusions:
            text_parts.append("\nCONCLUSION:")
            for conc in conclusions:
                text_parts.append(f"- {conc.content}")
        
        return "\n".join(text_parts)
    
    def _calculate_explanation_confidence(self, components: List[ExplanationComponent]) -> float:
        """Calculate overall confidence in the explanation"""
        if not components:
            return 0.0
        
        total_confidence = sum(comp.confidence for comp in components)
        return total_confidence / len(components)
    
    def _generate_meta_reasoning(self, components: List[ExplanationComponent]) -> str:
        """Generate explanation of the explanation process"""
        meta_parts = []
        
        component_counts = {}
        for comp in components:
            comp_type = comp.component_type
            component_counts[comp_type] = component_counts.get(comp_type, 0) + 1
        
        meta_parts.append("MY REASONING PROCESS:")
        meta_parts.append(f"I generated this explanation using {len(components)} reasoning components:")
        
        for comp_type, count in component_counts.items():
            meta_parts.append(f"- {count} {comp_type} step(s)")
        
        avg_confidence = self._calculate_explanation_confidence(components)
        meta_parts.append(f"Overall confidence in my reasoning: {avg_confidence:.2f}")
        
        return "\n".join(meta_parts)
    
    def _generate_task_description(self, transformation: SceneTransformation) -> str:
        """Generate a description of the task being explained"""
        input_size = transformation.input_scene.grid_size
        output_size = transformation.output_scene.grid_size
        
        return (f"Transform a {input_size[0]}x{input_size[1]} grid to a {output_size[0]}x{output_size[1]} grid "
                f"using {len(transformation.transformation_rules)} transformation rules")

def main():
    """Test the internal explanation generator"""
    generator = InternalExplanationGenerator()
    
    print("💭 Internal Explanation Generator Test")
    print("Generator initialized with explanation templates:")
    
    for template_type, templates in generator.explanation_templates.items():
        print(f"  - {template_type}: {len(templates)} templates")
    
    print(f"\nCommon sense knowledge: {len(generator.common_sense_knowledge)} concepts")

if __name__ == "__main__":
    main()
