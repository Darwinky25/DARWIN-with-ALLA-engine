#!/usr/bin/env python3
"""
Enhanced ALLA ARC Learning System - Human-Level Reasoning for ARC Tasks
Integrates all cognitive components: visual parsing, physics simulation, causal reasoning, and self-explanation
"""

import json
import numpy as np
import os
import glob
import time
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict, Counter

# Import all cognitive components
from visual_scene_parser import VisualSceneParser, SceneRepresentation
from visual_difference_analyzer import VisualDifferenceAnalyzer, SceneTransformation
from micro_physics_engine import MicroPhysicsEngine, PhysicsRule
from causal_inference_module import CausalInferenceModule, CausalExplanation
from internal_explanation_generator import InternalExplanationGenerator, InternalExplanation
from alla_failure_analyzer import ARCFailureAnalyzer, FailureAnalysis

# Import new advanced cognitive components
from meta_learning_engine import MetaLearningEngine, MetaPattern, RecursiveHypothesis
from semantic_bootstrapping_system import SemanticBootstrappingSystem, SemanticConcept
from hypothesis_evolution_engine import HypothesisEvolutionEngine, EvolvableHypothesis
from advanced_error_analysis_system import AdvancedErrorAnalysisSystem, ErrorInstance

# Import new demonstration-driven components
try:
    from demonstration_alignment_module import MultipledemonstrationAlignmentModule
    from conflict_detector import ConflictDetector  
    from demonstration_driven_arc_solver import DemonstrationDrivenARCSolver
    DEMONSTRATION_MODULES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Demonstration modules not available: {e}")
    DEMONSTRATION_MODULES_AVAILABLE = False

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('enhanced_alla.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class EnhancedTaskResult:
    """Enhanced task result with full cognitive trace"""
    task_id: str
    success: bool
    accuracy: float
    input_scene: Optional[SceneRepresentation]
    output_scene: Optional[SceneRepresentation]
    predicted_scene: Optional[SceneRepresentation]
    transformation: Optional[SceneTransformation]
    causal_explanation: Optional[CausalExplanation]
    internal_explanation: Optional[InternalExplanation]
    physics_simulation: Dict[str, Any]
    failure_analysis: Optional[FailureAnalysis]
    processing_time: float
    confidence: float

@dataclass
class CognitiveLearningStats:
    """Statistics about cognitive learning progress"""
    total_tasks: int = 0
    successful_tasks: int = 0
    failed_tasks: int = 0
    average_accuracy: float = 0.0
    cognitive_components_used: Dict[str, int] = field(default_factory=dict)
    explanation_quality: float = 0.0
    causal_understanding: float = 0.0
    physics_accuracy: float = 0.0
    pattern_recognition_rate: float = 0.0

class EnhancedALLASystem:
    """Enhanced ALLA with human-level cognitive reasoning for ARC tasks"""
    
    def __init__(self, data_path: str = "d:/DARWIN/ARC-AGI-2/data/training"):
        self.data_path = data_path
        
        # Initialize cognitive components
        self.visual_parser = VisualSceneParser()
        self.difference_analyzer = VisualDifferenceAnalyzer()
        self.physics_engine = MicroPhysicsEngine()
        self.causal_module = CausalInferenceModule()
        self.explanation_generator = InternalExplanationGenerator()
        self.failure_analyzer = ARCFailureAnalyzer()
        
        # Initialize advanced cognitive components
        self.meta_learning_engine = MetaLearningEngine()
        self.semantic_bootstrapper = SemanticBootstrappingSystem()
        self.hypothesis_evolver = HypothesisEvolutionEngine()
        self.error_analyzer = AdvancedErrorAnalysisSystem()
        
        # Initialize demonstration-driven components (optional)
        if DEMONSTRATION_MODULES_AVAILABLE:
            self.alignment_module = MultipledemonstrationAlignmentModule()
            self.conflict_detector = ConflictDetector()
            self.demonstration_solver = DemonstrationDrivenARCSolver()
        else:
            self.alignment_module = None
            self.conflict_detector = None
            self.demonstration_solver = None
        
        # Learning state
        self.task_results = []
        self.learning_stats = CognitiveLearningStats()
        self.learned_patterns = {}
        self.cognitive_insights = {}
        
        # Meta-cognitive state
        self.meta_patterns = {}
        self.semantic_concepts = {}
        self.evolved_hypotheses = []
        self.error_patterns = {}
        
        logger.info("Enhanced ALLA System initialized with full cognitive architecture")
    
    def process_arc_task(self, task_file: str) -> EnhancedTaskResult:
        """Process a single ARC task with full cognitive reasoning"""
        start_time = time.time()
        task_id = Path(task_file).stem
        
        logger.info(f"Processing task {task_id} with cognitive reasoning")
        
        try:
            # Load task data
            with open(task_file, 'r') as f:
                task_data = json.load(f)
            
            # Extract training examples and test case
            train_examples = task_data['train']
            test_case = task_data['test'][0]
            
            # Process training examples to learn transformation pattern
            transformations = []
            for i, example in enumerate(train_examples):
                input_grid = np.array(example['input'])
                output_grid = np.array(example['output'])
                
                # Analyze transformation
                transformation = self.difference_analyzer.analyze_transformation(
                    input_grid, output_grid, f"{task_id}_example_{i}"
                )
                transformations.append(transformation)
            
            # Find consistent transformation patterns
            consistent_patterns = self.difference_analyzer.find_consistent_transformations(transformations)
            
            # Parse test input
            test_input = np.array(test_case['input'])
            test_expected = np.array(test_case['output']) if 'output' in test_case else None
            
            # Apply cognitive reasoning to predict output
            predicted_output, cognitive_trace = self._apply_cognitive_reasoning(
                test_input, transformations, consistent_patterns, task_id
            )
            
            # Evaluate result
            success, accuracy = self._evaluate_prediction(predicted_output, test_expected)
            
            # Create result with full cognitive trace
            result = EnhancedTaskResult(
                task_id=task_id,
                success=success,
                accuracy=accuracy,
                input_scene=cognitive_trace['input_scene'],
                output_scene=cognitive_trace.get('expected_scene'),
                predicted_scene=cognitive_trace.get('predicted_scene'),
                transformation=cognitive_trace['transformation'],
                causal_explanation=cognitive_trace['causal_explanation'],
                internal_explanation=cognitive_trace['internal_explanation'],
                physics_simulation=cognitive_trace['physics_simulation'],
                failure_analysis=cognitive_trace.get('failure_analysis'),
                processing_time=time.time() - start_time,
                confidence=cognitive_trace['overall_confidence']
            )
            
            # Apply advanced cognitive processing
            test_cases = [{'input': test_input, 'output': test_expected}] if test_expected is not None else []
            advanced_results = self._apply_advanced_cognitive_processing(result, test_cases)
            
            # Apply meta-learning strategies
            task_context = {
                'transformation_type': result.transformation.transformation_type if result.transformation else 'unknown',
                'task_id': task_id,
                'accuracy': accuracy,
                'confidence': result.confidence
            }
            meta_strategy_results = self._apply_meta_learning_strategies(task_context)
            
            # Update result with advanced cognitive insights
            result.physics_simulation.update({
                'advanced_processing': advanced_results,
                'meta_strategies': meta_strategy_results
            })
            
            # Learn from result
            self._learn_from_result(result)
            
            logger.info(f"Task {task_id}: {accuracy:.2%} accuracy, {result.confidence:.2f} confidence")
            return result
            
        except Exception as e:
            logger.error(f"Failed to process task {task_id}: {e}")
            
            # Create error result
            return EnhancedTaskResult(
                task_id=task_id,
                success=False,
                accuracy=0.0,
                input_scene=None,
                output_scene=None,
                predicted_scene=None,
                transformation=None,
                causal_explanation=None,
                internal_explanation=None,
                physics_simulation={},
                failure_analysis=None,
                processing_time=time.time() - start_time,
                confidence=0.0
            )
    
    def _apply_cognitive_reasoning(self, test_input: np.ndarray, 
                                 transformations: List[SceneTransformation],
                                 consistent_patterns: Dict[str, Any],
                                 task_id: str) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Apply full cognitive reasoning to predict output"""
        
        cognitive_trace = {}
        
        # 1. Visual Scene Understanding
        logger.debug("Step 1: Visual scene parsing")
        input_scene = self.visual_parser.parse_grid_to_scene(test_input, f"{task_id}_test_input")
        cognitive_trace['input_scene'] = input_scene
        
        # 2. Pattern Analysis from Training Examples
        logger.debug("Step 2: Pattern analysis")
        if transformations:
            # Use the most confident transformation as reference
            reference_transformation = max(transformations, key=lambda t: t.confidence)
            cognitive_trace['transformation'] = reference_transformation
        else:
            # Create default transformation
            reference_transformation = self._create_default_transformation(input_scene)
            cognitive_trace['transformation'] = reference_transformation
        
        # 3. Physics Simulation
        logger.debug("Step 3: Physics simulation")
        physics_rules = self._determine_physics_rules(reference_transformation)
        physics_result = self.physics_engine.simulate_physics(
            input_scene, physics_rules, max_steps=15
        )
        cognitive_trace['physics_simulation'] = physics_result
        
        # 4. Causal Inference
        logger.debug("Step 4: Causal reasoning")
        causal_explanation = self.causal_module.infer_causation(
            reference_transformation, physics_result.get('physics_events', [])
        )
        cognitive_trace['causal_explanation'] = causal_explanation
        
        # 5. Prediction Generation
        logger.debug("Step 5: Prediction generation")
        predicted_output = self._generate_prediction(
            test_input, consistent_patterns, physics_result, reference_transformation
        )
        
        if predicted_output is not None:
            predicted_scene = self.visual_parser.parse_grid_to_scene(
                predicted_output, f"{task_id}_prediction"
            )
            cognitive_trace['predicted_scene'] = predicted_scene
        
        # 6. Internal Explanation Generation
        logger.debug("Step 6: Self-explanation")
        internal_explanation = self.explanation_generator.generate_explanation(
            reference_transformation,
            causal_explanation,
            physics_result.get('physics_events', [])
        )
        cognitive_trace['internal_explanation'] = internal_explanation
        
        # 7. Overall Confidence Assessment
        cognitive_trace['overall_confidence'] = self._calculate_overall_confidence(
            reference_transformation, causal_explanation, physics_result, internal_explanation
        )
        
        logger.debug(f"Cognitive reasoning complete: {cognitive_trace['overall_confidence']:.2f} confidence")
        
        return predicted_output, cognitive_trace
    
    def _determine_physics_rules(self, transformation: SceneTransformation) -> List[PhysicsRule]:
        """Determine which physics rules to apply based on transformation analysis"""
        rules = []
        
        for t_rule in (transformation.transformation_rules if hasattr(transformation.transformation_rules, '__iter__') and not isinstance(transformation.transformation_rules, str) else []):
            if t_rule.rule_type == "move_object":
                direction = t_rule.parameters.get('direction', '')
                if 'down' in direction:
                    rules.append(PhysicsRule.GRAVITY)
                rules.append(PhysicsRule.COLLISION)
            
            elif 'flow' in t_rule.rule_type or 'spread' in t_rule.description:
                rules.append(PhysicsRule.FLOW)
            
            elif 'bounce' in t_rule.description:
                rules.append(PhysicsRule.BOUNCE)
        
        # Default physics rules if none detected
        if not rules:
            rules = [PhysicsRule.GRAVITY, PhysicsRule.COLLISION]
        
        return rules
    
    def _generate_prediction(self, test_input: np.ndarray,
                           consistent_patterns: Dict[str, Any],
                           physics_result: Dict[str, Any],
                           transformation: SceneTransformation) -> np.ndarray:
        """Generate prediction using all available information"""
        
        # Try multiple prediction methods and combine
        predictions = []
        
        # Method 1: Pattern-based prediction
        if consistent_patterns.get('consistent_rules'):
            pattern_prediction = self.difference_analyzer.predict_transformation(
                test_input, consistent_patterns
            )
            if pattern_prediction is not None:
                predictions.append(('pattern', pattern_prediction, 0.8))
        
        # Method 2: Physics-based prediction
        physics_prediction = physics_result.get('final_grid')
        if physics_prediction is not None and not np.array_equal(physics_prediction, test_input):
            predictions.append(('physics', physics_prediction, 0.7))
        
        # Method 3: Direct transformation application
        if transformation and transformation.transformation_rules:
            try:
                direct_prediction = self._apply_direct_transformation(test_input, transformation)
                if direct_prediction is not None:
                    predictions.append(('direct', direct_prediction, 0.6))
            except Exception as e:
                logger.debug(f"Direct transformation failed: {e}")
        
        # Select best prediction
        if predictions:
            # Sort by confidence and select best
            predictions.sort(key=lambda x: x[2], reverse=True)
            best_method, best_prediction, confidence = predictions[0]
            logger.debug(f"Selected {best_method} prediction with confidence {confidence}")
            return best_prediction
        else:
            logger.warning("No valid predictions generated, returning input")
            return test_input
    
    def _apply_direct_transformation(self, input_grid: np.ndarray, 
                                   transformation: SceneTransformation) -> np.ndarray:
        """Apply transformation rules directly to input"""
        output = input_grid.copy()
        
        for rule in (transformation.transformation_rules if hasattr(transformation.transformation_rules, '__iter__') and not isinstance(transformation.transformation_rules, str) else []):
            if rule.rule_type == "grid_tiling":
                tiles_h = rule.parameters.get("tiles_h", 2)
                tiles_w = rule.parameters.get("tiles_w", 2)
                output = self._tile_grid(output, tiles_h, tiles_w)
            
            elif rule.rule_type == "color_mapping":
                mappings = rule.parameters.get("mappings", {})
                output = self._apply_color_mapping(output, mappings)
            
            elif rule.rule_type == "scale_up":
                scale_factor = rule.parameters.get("scale_factor", 2)
                output = self._scale_grid(output, scale_factor)
        
        return output
    
    def _tile_grid(self, grid: np.ndarray, tiles_h: int, tiles_w: int) -> np.ndarray:
        """Tile grid in specified pattern"""
        h, w = grid.shape
        output = np.zeros((h * tiles_h, w * tiles_w), dtype=grid.dtype)
        
        for th in range(tiles_h):
            for tw in range(tiles_w):
                start_h = th * h
                start_w = tw * w
                output[start_h:start_h + h, start_w:start_w + w] = grid
        
        return output
    
    def _apply_color_mapping(self, grid: np.ndarray, mappings: Dict[int, int]) -> np.ndarray:
        """Apply color mapping to grid"""
        output = grid.copy()
        for from_color, to_color in mappings.items():
            output[grid == from_color] = to_color
        return output
    
    def _scale_grid(self, grid: np.ndarray, scale_factor: int) -> np.ndarray:
        """Scale grid by factor"""
        h, w = grid.shape
        output = np.zeros((h * scale_factor, w * scale_factor), dtype=grid.dtype)
        
        for i in range(h):
            for j in range(w):
                value = grid[i, j]
                start_i = i * scale_factor
                start_j = j * scale_factor
                output[start_i:start_i + scale_factor, start_j:start_j + scale_factor] = value
        
        return output
    
    def _create_default_transformation(self, input_scene: SceneRepresentation) -> SceneTransformation:
        """Create a default transformation when none can be determined"""
        from visual_difference_analyzer import TransformationRule
        
        default_rule = TransformationRule(
            rule_type="identity",
            description="No transformation detected",
            confidence=0.1,
            parameters={}
        )
        
        return SceneTransformation(
            input_scene=input_scene,
            output_scene=input_scene,  # Same as input
            transformation_rules=[default_rule],
            transformation_type="simple",
            confidence=0.1
        )
    
    def _calculate_overall_confidence(self, transformation: SceneTransformation,
                                    causal_explanation: CausalExplanation,
                                    physics_result: Dict[str, Any],
                                    internal_explanation: InternalExplanation) -> float:
        """Calculate overall confidence in the reasoning"""
        confidences = []
        
        if transformation:
            confidences.append(transformation.confidence)
        
        if causal_explanation:
            confidences.append(causal_explanation.confidence)
        
        if physics_result.get('physics_summary', {}).get('physics_active', False):
            confidences.append(0.8)  # Physics adds confidence
        else:
            confidences.append(0.5)  # Neutral when no physics
        
        if internal_explanation:
            confidences.append(internal_explanation.confidence)
        
        return sum(confidences) / len(confidences) if confidences else 0.0
    
    def _evaluate_prediction(self, predicted: np.ndarray, 
                           expected: Optional[np.ndarray]) -> Tuple[bool, float]:
        """Evaluate prediction accuracy"""
        if expected is None:
            return False, 0.0
        
        if predicted is None:
            return False, 0.0
        
        if predicted.shape != expected.shape:
            return False, 0.0
        
        # Calculate pixel-wise accuracy
        correct_pixels = np.sum(predicted == expected)
        total_pixels = np.prod(expected.shape)
        accuracy = correct_pixels / total_pixels
        
        success = accuracy > 0.95  # 95% threshold for success
        
        return success, accuracy
    
    def _learn_from_result(self, result: EnhancedTaskResult):
        """Enhanced learning from task result with meta-cognitive insights"""
        
        # Store result
        self.task_results.append(result)
        
        # Update learning statistics
        self.learning_stats.total_tasks += 1
        if result.success:
            self.learning_stats.successful_tasks += 1
        else:
            self.learning_stats.failed_tasks += 1
        
        # Update average accuracy
        total_accuracy = sum(r.accuracy for r in self.task_results)
        self.learning_stats.average_accuracy = total_accuracy / len(self.task_results)
        
        # Update component usage statistics
        components_used = {
            'visual_parser': 1,
            'difference_analyzer': 1,
            'physics_engine': 1 if result.physics_simulation else 0,
            'causal_module': 1 if result.causal_explanation else 0,
            'explanation_generator': 1 if result.internal_explanation else 0,
            'meta_learning': 1 if 'meta_strategies' in result.physics_simulation else 0,
            'semantic_bootstrapper': 1 if 'semantic_concepts' in result.physics_simulation.get('advanced_processing', {}) else 0,
            'hypothesis_evolver': 1 if 'evolved_hypotheses' in result.physics_simulation.get('advanced_processing', {}) else 0,
            'error_analyzer': 1 if 'error_analysis' in result.physics_simulation.get('advanced_processing', {}) else 0
        }
        
        for component, used in components_used.items():
            if component not in self.learning_stats.cognitive_components_used:
                self.learning_stats.cognitive_components_used[component] = 0
            self.learning_stats.cognitive_components_used[component] += used
        
        # Update explanation quality
        if result.internal_explanation:
            # Use available attributes instead of reasoning_steps
            explanation_quality = min(1.0, result.confidence)  # Simplified metric
            self.learning_stats.explanation_quality = (
                (self.learning_stats.explanation_quality * (self.learning_stats.total_tasks - 1) + explanation_quality) /
                self.learning_stats.total_tasks
            )
        
        # Update causal understanding
        if result.causal_explanation:
            # Use confidence as a simplified metric since causal_chain might not have __len__
            causal_quality = min(1.0, result.causal_explanation.confidence if hasattr(result.causal_explanation, 'confidence') else 0.5)
            self.learning_stats.causal_understanding = (
                (self.learning_stats.causal_understanding * (self.learning_stats.total_tasks - 1) + causal_quality) /
                self.learning_stats.total_tasks
            )
        
        # Update physics accuracy
        if result.physics_simulation:
            physics_quality = 0.8 if result.success else 0.3  # Simplified metric
            self.learning_stats.physics_accuracy = (
                (self.learning_stats.physics_accuracy * (self.learning_stats.total_tasks - 1) + physics_quality) /
                self.learning_stats.total_tasks
            )
        
        # Update pattern recognition rate
        if result.transformation:
            pattern_quality = result.confidence
            self.learning_stats.pattern_recognition_rate = (
                (self.learning_stats.pattern_recognition_rate * (self.learning_stats.total_tasks - 1) + pattern_quality) /
                self.learning_stats.total_tasks
            )
        
        # Store learned patterns
        if result.transformation and result.success:
            pattern_key = result.transformation.transformation_type
            if pattern_key not in self.learned_patterns:
                self.learned_patterns[pattern_key] = {
                    'count': 0,
                    'success_rate': 0.0,
                    'examples': []
                }
            
            pattern_data = self.learned_patterns[pattern_key]
            pattern_data['count'] += 1
            pattern_data['success_rate'] = (
                (pattern_data['success_rate'] * (pattern_data['count'] - 1) + result.accuracy) /
                pattern_data['count']
            )
            pattern_data['examples'].append(result.task_id)
            
            # Keep only recent examples
            if len(pattern_data['examples']) > 10:
                pattern_data['examples'] = pattern_data['examples'][-10:]
        
        # Extract cognitive insights
        if 'advanced_processing' in result.physics_simulation:
            advanced = result.physics_simulation['advanced_processing']
            
            # Store meta-patterns
            if 'meta_patterns' in advanced:
                for pattern in advanced['meta_patterns']:
                    self.cognitive_insights[f"meta_pattern_{pattern.pattern_id}"] = {
                        'type': 'meta_pattern',
                        'confidence': pattern.confidence,
                        'usage_count': pattern.usage_count,
                        'learned_from': pattern.learned_from_tasks
                    }
            
            # Store semantic concepts
            if 'semantic_concepts' in advanced:
                for concept in advanced['semantic_concepts']:
                    self.cognitive_insights[f"concept_{concept.concept_id}"] = {
                        'type': 'semantic_concept',
                        'level': concept.level.value,
                        'confidence': concept.confidence,
                        'instantiation_count': concept.instantiation_count
                    }
        
        logger.debug(f"Learned from task {result.task_id}: accuracy={result.accuracy:.2%}, confidence={result.confidence:.2f}")
    
    def evolve_learning_strategies(self) -> Dict[str, Any]:
        """Evolve learning strategies based on accumulated experience"""
        
        logger.info("Evolving learning strategies based on experience")
        
        evolution_results = {}
        
        # 1. Evolve meta-learning strategies
        if len(self.task_results) >= 10:
            strategy_performance = self.meta_learning_engine.evolve_learning_strategies(self.task_results)
            evolution_results['meta_strategy_performance'] = strategy_performance
        
        # 2. Evolve hypothesis population
        if self.evolved_hypotheses and len(self.task_results) >= 5:
            test_cases = []
            for result in self.task_results[-10:]:
                if hasattr(result, 'input_scene') and hasattr(result, 'predicted_scene'):
                    test_case = {
                        'input': result.input_scene,
                        'output': result.predicted_scene,
                        'accuracy': result.accuracy
                    }
                    test_cases.append(test_case)
            
            if test_cases:
                best_hypothesis = self.hypothesis_evolver.evolve_until_convergence(
                    test_cases, max_generations=20, fitness_threshold=0.9, patience=5
                )
                evolution_results['best_evolved_hypothesis'] = {
                    'hypothesis_id': best_hypothesis.hypothesis_id,
                    'fitness': best_hypothesis.overall_fitness,
                    'generation': best_hypothesis.generation
                }
        
        # 3. Consolidate error patterns
        if hasattr(self.error_analyzer, 'error_patterns') and self.error_analyzer.error_patterns:
            pattern_consolidation = {}
            for pattern_id, pattern in self.error_analyzer.error_patterns.items():
                pattern_consolidation[pattern_id] = {
                    'frequency': pattern.frequency,
                    'trend': pattern.trend,
                    'prevention_strategies': pattern.prevention_strategies
                }
            evolution_results['error_pattern_consolidation'] = pattern_consolidation
        
        # 4. Update semantic concept hierarchy
        if self.semantic_concepts:
            concept_evolution = self.semantic_bootstrapper.perform_conceptual_abstraction()
            evolution_results['concept_evolution'] = len(concept_evolution)
        
        return evolution_results

    def _apply_advanced_cognitive_processing(self, task_result: EnhancedTaskResult, 
                                           test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Apply advanced cognitive processing including meta-learning and hypothesis evolution"""
        
        advanced_results = {}
        
        try:
            # 1. Error Analysis and Self-Correction
            logger.debug("Step 1: Advanced error analysis")
            error_analysis = self.error_analyzer.analyze_and_correct(
                task_result, 
                expected_result=None,  # Would be provided if available
                task_context={"task_id": task_result.task_id}
            )
            advanced_results['error_analysis'] = error_analysis
            
            # 2. Meta-Learning Pattern Extraction
            logger.debug("Step 2: Meta-learning pattern extraction")
            if hasattr(self, 'task_results') and len(self.task_results) > 1:
                meta_patterns = self.meta_learning_engine.extract_meta_patterns(self.task_results[-10:])
                self.meta_patterns.update({p.pattern_id: p for p in meta_patterns})
                advanced_results['meta_patterns'] = len(meta_patterns)
            
            # 3. Semantic Concept Bootstrapping
            logger.debug("Step 3: Semantic concept bootstrapping")
            if task_result.transformation:
                visual_patterns = self._extract_visual_patterns_from_result(task_result)
                new_concepts = self.semantic_bootstrapper.bootstrap_from_visual_patterns(visual_patterns)
                self.semantic_concepts.update({c.concept_id: c for c in new_concepts})
                advanced_results['semantic_concepts'] = len(new_concepts)
            
            # 4. Hypothesis Evolution (simplified for stability)
            logger.debug("Step 4: Hypothesis evolution")
            if test_cases and len(test_cases) > 0:
                # Create and evaluate a simple hypothesis
                hypothesis = self._create_hypothesis_from_result(task_result)
                if hypothesis:
                    advanced_results['hypothesis_created'] = True
                    self.evolved_hypotheses.append(hypothesis)
            
            # 5. Meta-Strategy Application
            logger.debug("Step 5: Meta-strategy application")
            task_context = {
                'transformation_type': task_result.transformation.transformation_type if task_result.transformation else 'unknown',
                'task_id': task_result.task_id,
                'accuracy': task_result.accuracy,
                'confidence': task_result.confidence
            }
            meta_strategy_results = self._apply_meta_learning_strategies(task_context)
            advanced_results['meta_strategies'] = meta_strategy_results
            
        except Exception as e:
            logger.warning(f"Advanced cognitive processing failed: {e}")
            advanced_results['error'] = str(e)
        
        return advanced_results
    
    def _extract_visual_patterns_from_result(self, task_result: EnhancedTaskResult) -> List[Dict[str, Any]]:
        """Extract visual patterns from task result for semantic bootstrapping"""
        
        patterns = []
        
        try:
            # Pattern from transformation
            if task_result.transformation:
                pattern = {
                    'id': f"{task_result.task_id}_transformation",
                    'type': 'transformation',
                    'transformation': task_result.transformation.transformation_type,
                    'signature': getattr(task_result.transformation, 'transformation_type', 'unknown'),
                    'objects': len(task_result.transformation.transformation_rules) if (task_result.transformation.transformation_rules and hasattr(task_result.transformation.transformation_rules, '__len__')) else 0
                }
                patterns.append(pattern)
            
            # Pattern from input scene
            if task_result.input_scene and hasattr(task_result.input_scene, 'objects'):
                pattern = {
                    'id': f"{task_result.task_id}_input_scene",
                    'type': 'scene',
                    'objects': len(task_result.input_scene.objects) if (task_result.input_scene.objects and hasattr(task_result.input_scene.objects, '__len__')) else 0,
                    'signature': f"scene_with_{len(task_result.input_scene.objects) if (task_result.input_scene.objects and hasattr(task_result.input_scene.objects, '__len__')) else 0}_objects"
                }
                patterns.append(pattern)
            
            # Pattern from physics simulation
            if task_result.physics_simulation:
                pattern = {
                    'id': f"{task_result.task_id}_physics",
                    'type': 'physics',
                    'signature': 'physics_simulation',
                    'complexity': len(str(task_result.physics_simulation))
                }
                patterns.append(pattern)
                
        except Exception as e:
            logger.warning(f"Pattern extraction failed: {e}")
        
        return patterns
    
    def _create_hypothesis_from_result(self, task_result: EnhancedTaskResult):
        """Create a simple hypothesis from task result"""
        
        try:
            from hypothesis_evolution_engine import HypothesisType, EvolvableHypothesis
            
            if not task_result.transformation:
                return None
            
            # Determine hypothesis type
            transformation_desc = getattr(task_result.transformation, 'transformation_type', '').lower()
            
            if 'pattern' in transformation_desc:
                h_type = HypothesisType.PATTERN_RECOGNITION
            elif 'spatial' in transformation_desc:
                h_type = HypothesisType.SPATIAL_RELATIONSHIP
            elif 'cause' in transformation_desc:
                h_type = HypothesisType.CAUSAL_MECHANISM
            else:
                h_type = HypothesisType.TRANSFORMATION_RULE
            
            # Extract rules
            rules = []
            if task_result.transformation.transformation_rules and hasattr(task_result.transformation.transformation_rules, '__iter__') and not isinstance(task_result.transformation.transformation_rules, str):
                rules = [getattr(rule, 'description', str(rule)) for rule in task_result.transformation.transformation_rules]
            
            # Create hypothesis
            hypothesis = EvolvableHypothesis(
                hypothesis_id=f"hyp_{task_result.task_id}_{int(time.time())}",
                hypothesis_type=h_type,
                generation=0,
                parent_ids=[],
                description=getattr(task_result.transformation, 'transformation_type', 'Unknown transformation'),
                prediction_function=None,
                parameters={
                    'confidence': task_result.confidence,
                    'accuracy': task_result.accuracy
                },
                rules=rules,
                conditions=[f"confidence > {max(0.1, task_result.confidence - 0.1)}"],
                fitness_scores={},
                overall_fitness=task_result.accuracy,
                mutations=[],
                crossover_history=[],
                test_results=[],
                validation_examples=[task_result.task_id],
                success_rate=task_result.accuracy,
                confidence=task_result.confidence,
                creation_time=time.time(),
                last_update_time=time.time(),
                usage_count=1
            )
            
            return hypothesis
            
        except Exception as e:
            logger.warning(f"Hypothesis creation failed: {e}")
            return None
    
    def _apply_meta_learning_strategies(self, task_context: Dict[str, Any]) -> Dict[str, Any]:
        """Apply meta-learning strategies to improve task solving"""
        
        strategy_results = {}
        
        try:
            # Get best strategy for current task
            best_strategy = self.meta_learning_engine.get_best_strategy_for_task(task_context)
            strategy_results['selected_strategy'] = best_strategy
            
            # Apply strategy-specific optimizations
            if best_strategy == "analogy_mapping":
                # Look for similar tasks and apply analogical reasoning
                analogies = self._find_task_analogies(task_context)
                strategy_results['analogies'] = analogies
            
            elif best_strategy == "compositional_generalization":
                # Break down complex patterns into simpler components
                components = self._decompose_task_components(task_context)
                strategy_results['components'] = components
            
            elif best_strategy == "causal_abstraction":
                # Focus on causal mechanisms
                causal_focus = self._identify_causal_elements(task_context)
                strategy_results['causal_elements'] = causal_focus
            
            elif best_strategy == "recursive_decomposition":
                # Apply recursive problem solving
                recursive_structure = self._identify_recursive_structure(task_context)
                strategy_results['recursive_structure'] = recursive_structure
                
        except Exception as e:
            logger.warning(f"Meta-learning strategy application failed: {e}")
            strategy_results['error'] = str(e)
        
        return strategy_results
    
    def _find_task_analogies(self, task_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find analogous tasks for analogical reasoning"""
        
        analogies = []
        current_type = task_context.get('transformation_type', 'unknown')
        
        # Look through previous results for similar transformation types
        for result in self.task_results[-20:]:  # Last 20 tasks
            if (result.transformation and 
                result.transformation.transformation_type == current_type and
                result.success):
                
                analogy = {
                    'task_id': result.task_id,
                    'similarity_score': 0.8,  # Would calculate actual similarity
                    'successful_approach': result.transformation.transformation_type,
                    'key_insights': [getattr(rule, 'description', str(rule)) for rule in (result.transformation.transformation_rules or [])[:3]]
                }
                analogies.append(analogy)
        
        return analogies[:3]  # Top 3 analogies
    
    def _decompose_task_components(self, task_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Decompose task into simpler components"""
        
        components = [
            {
                'component_type': 'visual_analysis',
                'description': 'Analyze visual elements and patterns',
                'complexity': 'low'
            },
            {
                'component_type': 'transformation_identification',
                'description': 'Identify transformation rules',
                'complexity': 'medium'
            },
            {
                'component_type': 'pattern_application',
                'description': 'Apply identified patterns to prediction',
                'complexity': 'medium'
            }
        ]
        
        return components
    
    def _identify_causal_elements(self, task_context: Dict[str, Any]) -> Dict[str, Any]:
        """Identify key causal elements in the task"""
        
        causal_elements = {
            'potential_causes': ['object_properties', 'spatial_relationships', 'transformation_rules'],
            'potential_effects': ['object_changes', 'position_changes', 'pattern_emergence'],
            'causal_chains': ['cause -> transformation -> effect'],
            'focus_areas': ['object_interactions', 'rule_applications']
        }
        
        return causal_elements
    
    def _identify_recursive_structure(self, task_context: Dict[str, Any]) -> Dict[str, Any]:
        """Identify recursive structure in the task"""
        
        recursive_structure = {
            'base_case': 'Simple single-step transformation',
            'recursive_case': 'Apply transformation repeatedly',
            'termination_condition': 'No more objects to transform',
            'recursion_depth': 'unknown'
        }
        
        return recursive_structure
    
    def process_arc_task_with_demonstrations(self, task_file: str) -> EnhancedTaskResult:
        """Process ARC task using demonstration-driven approach when available"""
        
        if not DEMONSTRATION_MODULES_AVAILABLE or self.demonstration_solver is None:
            logger.info("Demonstration modules not available, falling back to standard processing")
            return self.process_arc_task(task_file)
        
        try:
            # Load task data
            with open(task_file, 'r') as f:
                task_data = json.load(f)
            
            task_id = os.path.basename(task_file).replace('.json', '')
            
            # Use demonstration-driven solver
            result = self.demonstration_solver.solve_task(task_id, task_data)
            
            # Convert to EnhancedTaskResult format
            enhanced_result = EnhancedTaskResult(
                task_id=task_id,
                success=result['success'],
                accuracy=1.0 if result['success'] else 0.0,
                input_scene=None,  # Would be filled in full implementation
                output_scene=None,
                predicted_scene=None,
                transformation=None,
                causal_explanation=None,
                internal_explanation=result.get('reasoning', ''),
                physics_simulation={'demonstration_driven': True},
                failure_analysis=None,
                processing_time=result.get('processing_time', 0.0),
                confidence=result.get('confidence', 0.0)
            )
            
            # Learn from the result
            self._learn_from_result(enhanced_result)
            
            logger.info(f"Demonstration-driven processing complete for {task_id}")
            return enhanced_result
            
        except Exception as e:
            logger.error(f"Demonstration-driven processing failed: {e}")
            return self.process_arc_task(task_file)
    
    def generate_comprehensive_learning_report(self) -> Dict[str, Any]:
        """Generate comprehensive learning report with all cognitive insights"""
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'execution_summary': {
                'total_tasks_processed': self.learning_stats.total_tasks,
                'successful_tasks': self.learning_stats.successful_tasks,
                'failed_tasks': self.learning_stats.failed_tasks,
                'overall_success_rate': (self.learning_stats.successful_tasks / 
                                       max(1, self.learning_stats.total_tasks)),
                'average_accuracy': self.learning_stats.average_accuracy,
                'average_confidence': sum(r.confidence for r in self.task_results) / 
                                   max(1, len(self.task_results))
            },
            'cognitive_component_usage': self.learning_stats.cognitive_components_used,
            'cognitive_quality_metrics': {
                'explanation_quality': self.learning_stats.explanation_quality,
                'causal_understanding': self.learning_stats.causal_understanding,
                'physics_accuracy': self.learning_stats.physics_accuracy,
                'pattern_recognition_rate': self.learning_stats.pattern_recognition_rate
            },
            'learned_patterns': self.learned_patterns,
            'cognitive_insights': self.cognitive_insights,
            'meta_patterns_discovered': len(self.meta_patterns),
            'semantic_concepts_created': len(self.semantic_concepts),
            'evolved_hypotheses': len(self.evolved_hypotheses),
            'demonstration_driven_capabilities': DEMONSTRATION_MODULES_AVAILABLE
        }
        
        # Add task-specific insights
        if self.task_results:
            recent_results = self.task_results[-10:]
            report['recent_performance'] = {
                'recent_success_rate': sum(1 for r in recent_results if r.success) / len(recent_results),
                'recent_avg_accuracy': sum(r.accuracy for r in recent_results) / len(recent_results),
                'recent_avg_confidence': sum(r.confidence for r in recent_results) / len(recent_results),
                'improvement_trend': 'stable'  # Could calculate actual trend
            }
        
        # Add learning trajectory
        if len(self.task_results) >= 5:
            early_accuracy = sum(r.accuracy for r in self.task_results[:5]) / 5
            late_accuracy = sum(r.accuracy for r in self.task_results[-5:]) / 5
            report['learning_trajectory'] = {
                'early_performance': early_accuracy,
                'late_performance': late_accuracy,
                'improvement': late_accuracy - early_accuracy,
                'learning_detected': late_accuracy > early_accuracy + 0.05
            }
        
        logger.info("Generated comprehensive learning report")
        return report
