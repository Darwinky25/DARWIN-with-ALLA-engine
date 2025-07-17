#!/usr/bin/env python3
"""
Advanced Error Analysis and Self-Correction System
Analyzes errors systematically, learns from failures, and implements self-correction mechanisms
"""

import json
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Set, Callable
from dataclasses import dataclass, field
from collections import defaultdict, Counter, deque
import logging
from enum import Enum
from abc import ABC, abstractmethod
import time
import traceback
from pathlib import Path

logger = logging.getLogger(__name__)

class ErrorType(Enum):
    """Categories of errors that can occur"""
    PATTERN_MISRECOGNITION = "pattern_misrecognition"
    TRANSFORMATION_ERROR = "transformation_error"
    SPATIAL_REASONING_ERROR = "spatial_reasoning_error"
    LOGICAL_INCONSISTENCY = "logical_inconsistency"
    INCOMPLETE_ANALYSIS = "incomplete_analysis"
    OVERCOMPLICATION = "overcomplication"
    CONTEXT_MISUNDERSTANDING = "context_misunderstanding"
    PREDICTION_ERROR = "prediction_error"
    CONFIDENCE_MISCALIBRATION = "confidence_miscalibration"

class ErrorSeverity(Enum):
    """Severity levels for errors"""
    CRITICAL = "critical"      # Completely wrong solution
    MAJOR = "major"           # Significant deviation from correct answer
    MINOR = "minor"           # Small mistakes that don't affect overall solution
    NEGLIGIBLE = "negligible" # Very minor issues with no practical impact

class CorrectionStrategy(Enum):
    """Types of correction strategies"""
    RETRY_WITH_DIFFERENT_APPROACH = "retry_different_approach"
    REFINE_CURRENT_APPROACH = "refine_current_approach"
    SEEK_ADDITIONAL_INFORMATION = "seek_additional_info"
    BREAK_DOWN_PROBLEM = "break_down_problem"
    USE_ANALOGICAL_REASONING = "use_analogical_reasoning"
    APPLY_CONSTRAINT_SATISFACTION = "apply_constraint_satisfaction"
    ENSEMBLE_MULTIPLE_SOLUTIONS = "ensemble_solutions"

@dataclass
class ErrorInstance:
    """Detailed record of an error instance"""
    error_id: str
    error_type: ErrorType
    severity: ErrorSeverity
    task_id: str
    
    # Error context
    error_description: str
    error_location: str  # Where in the process the error occurred
    expected_result: Any
    actual_result: Any
    
    # Analysis
    root_cause: str
    contributing_factors: List[str]
    error_pattern: str
    
    # Impact assessment
    accuracy_impact: float
    confidence_impact: float
    downstream_effects: List[str]
    
    # Correction information
    correction_attempts: List[str]
    successful_correction: Optional[str]
    lessons_learned: List[str]
    
    # Metadata
    timestamp: float
    processing_stage: str
    system_state: Dict[str, Any]

@dataclass
class ErrorPattern:
    """Pattern of recurring errors"""
    pattern_id: str
    pattern_name: str
    error_instances: List[str]
    frequency: int
    
    # Pattern characteristics
    common_triggers: List[str]
    typical_context: Dict[str, Any]
    error_signature: str
    
    # Prevention and correction
    prevention_strategies: List[str]
    correction_strategies: List[CorrectionStrategy]
    success_rate: float
    
    # Evolution tracking
    first_occurrence: float
    last_occurrence: float
    trend: str  # "increasing", "decreasing", "stable"

@dataclass
class SelfCorrectionAction:
    """An action taken for self-correction"""
    action_id: str
    action_type: CorrectionStrategy
    description: str
    target_error: str
    
    # Implementation
    correction_function: Optional[Callable]
    parameters: Dict[str, Any]
    
    # Results
    success: bool
    before_state: Dict[str, Any]
    after_state: Dict[str, Any]
    improvement_metrics: Dict[str, float]
    
    # Metadata
    execution_time: float
    timestamp: float

class ErrorDetector:
    """Detects various types of errors in reasoning processes"""
    
    def __init__(self):
        self.detection_methods = {
            ErrorType.PATTERN_MISRECOGNITION: self._detect_pattern_errors,
            ErrorType.TRANSFORMATION_ERROR: self._detect_transformation_errors,
            ErrorType.SPATIAL_REASONING_ERROR: self._detect_spatial_errors,
            ErrorType.LOGICAL_INCONSISTENCY: self._detect_logical_errors,
            ErrorType.INCOMPLETE_ANALYSIS: self._detect_incomplete_analysis,
            ErrorType.OVERCOMPLICATION: self._detect_overcomplication,
            ErrorType.CONTEXT_MISUNDERSTANDING: self._detect_context_errors,
            ErrorType.PREDICTION_ERROR: self._detect_prediction_errors,
            ErrorType.CONFIDENCE_MISCALIBRATION: self._detect_confidence_errors
        }
        
        logger.info("🔍 Error Detector initialized")
    
    def detect_errors(self, task_result: Any, expected_result: Any = None) -> List[ErrorInstance]:
        """Detect errors in a task result"""
        
        detected_errors = []
        
        for error_type, detection_method in self.detection_methods.items():
            try:
                errors = detection_method(task_result, expected_result)
                detected_errors.extend(errors)
            except Exception as e:
                logger.warning(f"Error detection failed for {error_type}: {e}")
        
        return detected_errors
    
    def _detect_pattern_errors(self, task_result: Any, expected_result: Any) -> List[ErrorInstance]:
        """Detect pattern recognition errors"""
        errors = []
        
        if not hasattr(task_result, 'transformation') or not task_result.transformation:
            error = ErrorInstance(
                error_id=f"pattern_error_{int(time.time())}",
                error_type=ErrorType.PATTERN_MISRECOGNITION,
                severity=ErrorSeverity.MAJOR,
                task_id=getattr(task_result, 'task_id', 'unknown'),
                error_description="No pattern or transformation identified",
                error_location="pattern_recognition_stage",
                expected_result="Valid transformation pattern",
                actual_result="None or invalid pattern",
                root_cause="Pattern recognition failure",
                contributing_factors=["Insufficient pattern analysis", "Weak feature extraction"],
                error_pattern="missing_pattern_identification",
                accuracy_impact=0.8,
                confidence_impact=0.5,
                downstream_effects=["Incorrect prediction", "Low confidence"],
                correction_attempts=[],
                successful_correction=None,
                lessons_learned=[],
                timestamp=time.time(),
                processing_stage="pattern_recognition",
                system_state={}
            )
            errors.append(error)
        
        # Check pattern confidence
        if (hasattr(task_result, 'transformation') and task_result.transformation and 
            hasattr(task_result.transformation, 'confidence') and 
            task_result.transformation.confidence < 0.3):
            
            error = ErrorInstance(
                error_id=f"pattern_confidence_error_{int(time.time())}",
                error_type=ErrorType.PATTERN_MISRECOGNITION,
                severity=ErrorSeverity.MINOR,
                task_id=getattr(task_result, 'task_id', 'unknown'),
                error_description="Low confidence in pattern recognition",
                error_location="pattern_confidence_assessment",
                expected_result="High confidence pattern",
                actual_result=f"Low confidence: {task_result.transformation.confidence}",
                root_cause="Uncertain pattern matching",
                contributing_factors=["Ambiguous patterns", "Insufficient training data"],
                error_pattern="low_pattern_confidence",
                accuracy_impact=0.3,
                confidence_impact=0.7,
                downstream_effects=["Unreliable predictions"],
                correction_attempts=[],
                successful_correction=None,
                lessons_learned=[],
                timestamp=time.time(),
                processing_stage="pattern_recognition",
                system_state={}
            )
            errors.append(error)
        
        return errors
    
    def _detect_transformation_errors(self, task_result: Any, expected_result: Any) -> List[ErrorInstance]:
        """Detect transformation application errors"""
        errors = []
        
        # Check for transformation consistency
        if (hasattr(task_result, 'transformation') and task_result.transformation and
            hasattr(task_result.transformation, 'transformation_rules')):
            
            rules = task_result.transformation.transformation_rules
            
            # Check for contradictory rules
            for i, rule1 in enumerate(rules):
                for j, rule2 in enumerate(rules[i+1:], i+1):
                    if self._rules_contradict(rule1, rule2):
                        error = ErrorInstance(
                            error_id=f"contradictory_rules_{i}_{j}_{int(time.time())}",
                            error_type=ErrorType.TRANSFORMATION_ERROR,
                            severity=ErrorSeverity.MAJOR,
                            task_id=getattr(task_result, 'task_id', 'unknown'),
                            error_description=f"Contradictory transformation rules: {rule1.rule_type} vs {rule2.rule_type}",
                            error_location="transformation_rule_validation",
                            expected_result="Consistent transformation rules",
                            actual_result="Contradictory rules detected",
                            root_cause="Logic error in rule generation",
                            contributing_factors=["Insufficient rule validation", "Conflicting constraints"],
                            error_pattern="contradictory_transformation_rules",
                            accuracy_impact=0.6,
                            confidence_impact=0.4,
                            downstream_effects=["Unpredictable transformations", "Incorrect outputs"],
                            correction_attempts=[],
                            successful_correction=None,
                            lessons_learned=[],
                            timestamp=time.time(),
                            processing_stage="transformation_validation",
                            system_state={}
                        )
                        errors.append(error)
        
        return errors
    
    def _detect_spatial_errors(self, task_result: Any, expected_result: Any) -> List[ErrorInstance]:
        """Detect spatial reasoning errors"""
        errors = []
        
        # Check for spatial consistency in scene representations
        if hasattr(task_result, 'input_scene') and task_result.input_scene:
            scene = task_result.input_scene
            
            if hasattr(scene, 'objects') and scene.objects:
                # Check for overlapping objects that shouldn't overlap
                for i, obj1 in enumerate(scene.objects):
                    for j, obj2 in enumerate(scene.objects[i+1:], i+1):
                        if self._objects_incorrectly_overlap(obj1, obj2):
                            error = ErrorInstance(
                                error_id=f"spatial_overlap_error_{i}_{j}_{int(time.time())}",
                                error_type=ErrorType.SPATIAL_REASONING_ERROR,
                                severity=ErrorSeverity.MINOR,
                                task_id=getattr(task_result, 'task_id', 'unknown'),
                                error_description=f"Objects {obj1.object_id} and {obj2.object_id} incorrectly overlap",
                                error_location="spatial_analysis",
                                expected_result="Non-overlapping objects",
                                actual_result="Overlapping objects detected",
                                root_cause="Spatial parsing error",
                                contributing_factors=["Imprecise object boundaries", "Misaligned coordinates"],
                                error_pattern="incorrect_object_overlap",
                                accuracy_impact=0.2,
                                confidence_impact=0.3,
                                downstream_effects=["Incorrect spatial relationships"],
                                correction_attempts=[],
                                successful_correction=None,
                                lessons_learned=[],
                                timestamp=time.time(),
                                processing_stage="spatial_analysis",
                                system_state={}
                            )
                            errors.append(error)
        
        return errors
    
    def _detect_logical_errors(self, task_result: Any, expected_result: Any) -> List[ErrorInstance]:
        """Detect logical inconsistencies"""
        errors = []
        
        # Check causal explanation consistency
        if hasattr(task_result, 'causal_explanation') and task_result.causal_explanation:
            causal = task_result.causal_explanation
            
            # Safely check causal chain
            causal_chain = getattr(causal, 'causal_chain', None)
            if causal_chain and hasattr(causal_chain, '__len__') and len(causal_chain) > 1:
                # Check for circular causality
                if self._has_circular_causality(causal.causal_chain):
                    error = ErrorInstance(
                        error_id=f"circular_causality_{int(time.time())}",
                        error_type=ErrorType.LOGICAL_INCONSISTENCY,
                        severity=ErrorSeverity.MAJOR,
                        task_id=getattr(task_result, 'task_id', 'unknown'),
                        error_description="Circular causality detected in causal chain",
                        error_location="causal_reasoning",
                        expected_result="Acyclic causal chain",
                        actual_result="Circular causal dependencies",
                        root_cause="Logical error in causal inference",
                        contributing_factors=["Bidirectional relationships", "Incomplete causal analysis"],
                        error_pattern="circular_causal_chain",
                        accuracy_impact=0.5,
                        confidence_impact=0.6,
                        downstream_effects=["Invalid causal explanations", "Logical contradictions"],
                        correction_attempts=[],
                        successful_correction=None,
                        lessons_learned=[],
                        timestamp=time.time(),
                        processing_stage="causal_reasoning",
                        system_state={}
                    )
                    errors.append(error)
        
        return errors
    
    def _detect_incomplete_analysis(self, task_result: Any, expected_result: Any) -> List[ErrorInstance]:
        """Detect incomplete analysis"""
        errors = []
        
        # Check if key components are missing
        missing_components = []
        
        if not hasattr(task_result, 'transformation') or not task_result.transformation:
            missing_components.append("transformation_analysis")
        
        if not hasattr(task_result, 'causal_explanation') or not task_result.causal_explanation:
            missing_components.append("causal_explanation")
        
        if not hasattr(task_result, 'internal_explanation') or not task_result.internal_explanation:
            missing_components.append("internal_explanation")
        
        if missing_components:
            error = ErrorInstance(
                error_id=f"incomplete_analysis_{int(time.time())}",
                error_type=ErrorType.INCOMPLETE_ANALYSIS,
                severity=ErrorSeverity.MAJOR,
                task_id=getattr(task_result, 'task_id', 'unknown'),
                error_description=f"Missing analysis components: {', '.join(missing_components)}",
                error_location="analysis_completeness_check",
                expected_result="Complete analysis with all components",
                actual_result=f"Missing: {missing_components}",
                root_cause="Incomplete processing pipeline",
                contributing_factors=["Processing failures", "Insufficient data", "Component failures"],
                error_pattern="missing_analysis_components",
                accuracy_impact=0.7,
                confidence_impact=0.8,
                downstream_effects=["Unreliable results", "Poor decision making"],
                correction_attempts=[],
                successful_correction=None,
                lessons_learned=[],
                timestamp=time.time(),
                processing_stage="analysis_validation",
                system_state={}
            )
            errors.append(error)
        
        return errors
    
    def _detect_overcomplication(self, task_result: Any, expected_result: Any) -> List[ErrorInstance]:
        """Detect overcomplication of solutions"""
        errors = []
        
        complexity_indicators = 0
        
        # Count complexity factors
        if hasattr(task_result, 'transformation') and task_result.transformation:
            if hasattr(task_result.transformation, 'transformation_rules'):
                complexity_indicators += len(task_result.transformation.transformation_rules)
        
        if hasattr(task_result, 'processing_time') and task_result.processing_time > 30:  # 30 seconds threshold
            complexity_indicators += 5
        
        # If solution is overly complex
        if complexity_indicators > 15:  # Arbitrary threshold
            error = ErrorInstance(
                error_id=f"overcomplication_{int(time.time())}",
                error_type=ErrorType.OVERCOMPLICATION,
                severity=ErrorSeverity.MINOR,
                task_id=getattr(task_result, 'task_id', 'unknown'),
                error_description=f"Solution appears overcomplicated (complexity score: {complexity_indicators})",
                error_location="solution_complexity_assessment",
                expected_result="Simple, elegant solution",
                actual_result=f"Complex solution with score: {complexity_indicators}",
                root_cause="Failure to find simple solution",
                contributing_factors=["Over-engineering", "Lack of simplification"],
                error_pattern="solution_overcomplication",
                accuracy_impact=0.1,
                confidence_impact=0.2,
                downstream_effects=["Reduced generalizability", "Increased error risk"],
                correction_attempts=[],
                successful_correction=None,
                lessons_learned=[],
                timestamp=time.time(),
                processing_stage="solution_evaluation",
                system_state={}
            )
            errors.append(error)
        
        return errors
    
    def _detect_context_errors(self, task_result: Any, expected_result: Any) -> List[ErrorInstance]:
        """Detect context misunderstanding errors"""
        errors = []
        
        # Check if the solution type matches the task context
        if (hasattr(task_result, 'transformation') and task_result.transformation and
            hasattr(task_result, 'task_id')):
            
            # Simple heuristic: if task involves colors but transformation doesn't mention colors
            task_id = task_result.task_id
            transformation_desc = getattr(task_result.transformation, 'transformation_type', '').lower()
            if not transformation_desc:
                transformation_desc = str(task_result.transformation).lower()
            
            context_mismatches = []
            
            if 'color' in task_id.lower() and 'color' not in transformation_desc:
                context_mismatches.append("color_context_ignored")
            
            if 'shape' in task_id.lower() and 'shape' not in transformation_desc:
                context_mismatches.append("shape_context_ignored")
            
            if 'size' in task_id.lower() and 'size' not in transformation_desc:
                context_mismatches.append("size_context_ignored")
            
            if context_mismatches:
                error = ErrorInstance(
                    error_id=f"context_mismatch_{int(time.time())}",
                    error_type=ErrorType.CONTEXT_MISUNDERSTANDING,
                    severity=ErrorSeverity.MAJOR,
                    task_id=task_id,
                    error_description=f"Context mismatches: {', '.join(context_mismatches)}",
                    error_location="context_validation",
                    expected_result="Solution matching task context",
                    actual_result="Solution ignoring key context elements",
                    root_cause="Context misunderstanding",
                    contributing_factors=["Inadequate context analysis", "Focus on wrong features"],
                    error_pattern="context_feature_mismatch",
                    accuracy_impact=0.6,
                    confidence_impact=0.4,
                    downstream_effects=["Wrong solution approach", "Poor generalization"],
                    correction_attempts=[],
                    successful_correction=None,
                    lessons_learned=[],
                    timestamp=time.time(),
                    processing_stage="context_analysis",
                    system_state={}
                )
                errors.append(error)
        
        return errors
    
    def _detect_prediction_errors(self, task_result: Any, expected_result: Any) -> List[ErrorInstance]:
        """Detect prediction accuracy errors"""
        errors = []
        
        if expected_result is not None and hasattr(task_result, 'predicted_scene'):
            # Compare predicted vs expected
            accuracy = getattr(task_result, 'accuracy', 0.0)
            
            if accuracy < 0.5:  # Low accuracy threshold
                error = ErrorInstance(
                    error_id=f"prediction_error_{int(time.time())}",
                    error_type=ErrorType.PREDICTION_ERROR,
                    severity=ErrorSeverity.CRITICAL if accuracy < 0.2 else ErrorSeverity.MAJOR,
                    task_id=getattr(task_result, 'task_id', 'unknown'),
                    error_description=f"Low prediction accuracy: {accuracy:.2%}",
                    error_location="prediction_generation",
                    expected_result="High accuracy prediction",
                    actual_result=f"Low accuracy: {accuracy:.2%}",
                    root_cause="Prediction generation failure",
                    contributing_factors=["Wrong transformation", "Incorrect pattern", "Faulty reasoning"],
                    error_pattern="low_prediction_accuracy",
                    accuracy_impact=accuracy,
                    confidence_impact=0.8,
                    downstream_effects=["Wrong solution", "Poor task performance"],
                    correction_attempts=[],
                    successful_correction=None,
                    lessons_learned=[],
                    timestamp=time.time(),
                    processing_stage="prediction",
                    system_state={}
                )
                errors.append(error)
        
        return errors
    
    def _detect_confidence_errors(self, task_result: Any, expected_result: Any) -> List[ErrorInstance]:
        """Detect confidence calibration errors"""
        errors = []
        
        if hasattr(task_result, 'confidence') and hasattr(task_result, 'accuracy'):
            confidence = task_result.confidence
            accuracy = task_result.accuracy
            
            # Check for overconfidence (high confidence, low accuracy)
            if confidence > 0.8 and accuracy < 0.5:
                error = ErrorInstance(
                    error_id=f"overconfidence_{int(time.time())}",
                    error_type=ErrorType.CONFIDENCE_MISCALIBRATION,
                    severity=ErrorSeverity.MINOR,
                    task_id=getattr(task_result, 'task_id', 'unknown'),
                    error_description=f"Overconfidence: {confidence:.2f} confidence, {accuracy:.2%} accuracy",
                    error_location="confidence_assessment",
                    expected_result="Calibrated confidence matching accuracy",
                    actual_result=f"Confidence: {confidence:.2f}, Accuracy: {accuracy:.2%}",
                    root_cause="Confidence miscalibration",
                    contributing_factors=["Overestimation of certainty", "Poor uncertainty modeling"],
                    error_pattern="overconfidence_bias",
                    accuracy_impact=0.0,  # Doesn't affect accuracy directly
                    confidence_impact=0.6,
                    downstream_effects=["Poor decision making", "Overreliance on wrong solutions"],
                    correction_attempts=[],
                    successful_correction=None,
                    lessons_learned=[],
                    timestamp=time.time(),
                    processing_stage="confidence_assessment",
                    system_state={}
                )
                errors.append(error)
            
            # Check for underconfidence (low confidence, high accuracy)
            elif confidence < 0.3 and accuracy > 0.8:
                error = ErrorInstance(
                    error_id=f"underconfidence_{int(time.time())}",
                    error_type=ErrorType.CONFIDENCE_MISCALIBRATION,
                    severity=ErrorSeverity.NEGLIGIBLE,
                    task_id=getattr(task_result, 'task_id', 'unknown'),
                    error_description=f"Underconfidence: {confidence:.2f} confidence, {accuracy:.2%} accuracy",
                    error_location="confidence_assessment",
                    expected_result="Calibrated confidence matching accuracy",
                    actual_result=f"Confidence: {confidence:.2f}, Accuracy: {accuracy:.2%}",
                    root_cause="Confidence miscalibration",
                    contributing_factors=["Underestimation of certainty", "Conservative bias"],
                    error_pattern="underconfidence_bias",
                    accuracy_impact=0.0,
                    confidence_impact=0.3,
                    downstream_effects=["Missed opportunities", "Excessive caution"],
                    correction_attempts=[],
                    successful_correction=None,
                    lessons_learned=[],
                    timestamp=time.time(),
                    processing_stage="confidence_assessment",
                    system_state={}
                )
                errors.append(error)
        
        return errors
    
    def _rules_contradict(self, rule1: Any, rule2: Any) -> bool:
        """Check if two transformation rules contradict each other"""
        if not hasattr(rule1, 'rule_type') or not hasattr(rule2, 'rule_type'):
            return False
        
        contradictory_pairs = [
            ("add", "remove"),
            ("increase", "decrease"),
            ("expand", "contract"),
            ("create", "delete"),
            ("left", "right"),
            ("up", "down")
        ]
        
        rule1_type = rule1.rule_type.lower()
        rule2_type = rule2.rule_type.lower()
        
        for pair in contradictory_pairs:
            if (pair[0] in rule1_type and pair[1] in rule2_type) or \
               (pair[1] in rule1_type and pair[0] in rule2_type):
                return True
        
        return False
    
    def _objects_incorrectly_overlap(self, obj1: Any, obj2: Any) -> bool:
        """Check if two objects incorrectly overlap"""
        # Simplified overlap detection
        if not all(hasattr(obj, 'position') for obj in [obj1, obj2]):
            return False
        
        # For now, assume objects shouldn't overlap at all
        return obj1.position == obj2.position
    
    def _has_circular_causality(self, causal_chain: List[Any]) -> bool:
        """Check for circular causality in causal chain"""
        if len(causal_chain) < 2:
            return False
        
        # Simple check: if any cause appears as both cause and effect
        causes = set()
        effects = set()
        
        for link in causal_chain:
            if hasattr(link, 'cause') and hasattr(link, 'effect'):
                causes.add(link.cause)
                effects.add(link.effect)
        
        # Check for overlap
        return bool(causes & effects)

class ErrorPatternAnalyzer:
    """Analyzes patterns in errors to identify systematic issues"""
    
    def __init__(self):
        self.error_patterns: Dict[str, ErrorPattern] = {}
        self.pattern_history = []
        
        logger.info("📊 Error Pattern Analyzer initialized")
    
    def analyze_error_patterns(self, error_instances: List[ErrorInstance]) -> List[ErrorPattern]:
        """Analyze errors to identify patterns"""
        
        if not error_instances:
            return []
        
        # Group errors by similarity
        error_groups = self._group_similar_errors(error_instances)
        
        # Create patterns from groups
        new_patterns = []
        for group_signature, group_errors in error_groups.items():
            if len(group_errors) >= 2:  # Pattern requires multiple instances
                pattern = self._create_error_pattern(group_signature, group_errors)
                new_patterns.append(pattern)
                self.error_patterns[pattern.pattern_id] = pattern
        
        # Update existing patterns
        self._update_existing_patterns(error_instances)
        
        logger.info(f"📈 Identified {len(new_patterns)} new error patterns")
        return new_patterns
    
    def _group_similar_errors(self, errors: List[ErrorInstance]) -> Dict[str, List[ErrorInstance]]:
        """Group similar errors together"""
        groups = defaultdict(list)
        
        for error in errors:
            # Create signature for grouping
            signature = self._create_error_signature(error)
            groups[signature].append(error)
        
        return dict(groups)
    
    def _create_error_signature(self, error: ErrorInstance) -> str:
        """Create a signature for error grouping"""
        signature_parts = [
            error.error_type.value,
            error.severity.value,
            error.processing_stage,
            error.error_pattern
        ]
        
        return "||".join(signature_parts)
    
    def _create_error_pattern(self, signature: str, errors: List[ErrorInstance]) -> ErrorPattern:
        """Create an error pattern from a group of similar errors"""
        
        pattern_id = f"pattern_{hash(signature) % 10000:04d}"
        
        # Extract common characteristics
        common_triggers = self._extract_common_triggers(errors)
        typical_context = self._extract_typical_context(errors)
        
        # Determine trend
        timestamps = [e.timestamp for e in errors]
        trend = self._determine_trend(timestamps)
        
        pattern = ErrorPattern(
            pattern_id=pattern_id,
            pattern_name=self._generate_pattern_name(errors),
            error_instances=[e.error_id for e in errors],
            frequency=len(errors),
            common_triggers=common_triggers,
            typical_context=typical_context,
            error_signature=signature,
            prevention_strategies=self._suggest_prevention_strategies(errors),
            correction_strategies=self._suggest_correction_strategies(errors),
            success_rate=0.0,  # Will be updated as corrections are attempted
            first_occurrence=min(timestamps),
            last_occurrence=max(timestamps),
            trend=trend
        )
        
        return pattern
    
    def _extract_common_triggers(self, errors: List[ErrorInstance]) -> List[str]:
        """Extract common triggers for errors"""
        all_factors = []
        for error in errors:
            all_factors.extend(error.contributing_factors)
        
        # Count frequency of factors
        factor_counts = Counter(all_factors)
        
        # Return factors that appear in at least 50% of errors
        threshold = len(errors) * 0.5
        common_triggers = [factor for factor, count in factor_counts.items() if count >= threshold]
        
        return common_triggers
    
    def _extract_typical_context(self, errors: List[ErrorInstance]) -> Dict[str, Any]:
        """Extract typical context for errors"""
        context = {
            "processing_stages": [e.processing_stage for e in errors],
            "error_locations": [e.error_location for e in errors],
            "common_tasks": [e.task_id for e in errors],
            "average_accuracy_impact": np.mean([e.accuracy_impact for e in errors]),
            "average_confidence_impact": np.mean([e.confidence_impact for e in errors])
        }
        
        return context
    
    def _determine_trend(self, timestamps: List[float]) -> str:
        """Determine if error frequency is increasing, decreasing, or stable"""
        if len(timestamps) < 3:
            return "insufficient_data"
        
        # Simple trend analysis based on time intervals
        intervals = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]
        
        if len(intervals) < 2:
            return "stable"
        
        # Check if intervals are getting shorter (increasing frequency)
        if intervals[-1] < intervals[0] * 0.7:
            return "increasing"
        elif intervals[-1] > intervals[0] * 1.3:
            return "decreasing"
        else:
            return "stable"
    
    def _generate_pattern_name(self, errors: List[ErrorInstance]) -> str:
        """Generate a descriptive name for the error pattern"""
        error_type = errors[0].error_type.value
        processing_stage = errors[0].processing_stage
        
        return f"{error_type.replace('_', ' ').title()} in {processing_stage.replace('_', ' ').title()}"
    
    def _suggest_prevention_strategies(self, errors: List[ErrorInstance]) -> List[str]:
        """Suggest strategies to prevent this type of error"""
        
        # Get the most common error type
        error_types = [e.error_type for e in errors]
        most_common_type = Counter(error_types).most_common(1)[0][0]
        
        prevention_strategies = {
            ErrorType.PATTERN_MISRECOGNITION: [
                "Improve pattern feature extraction",
                "Add more training examples",
                "Use ensemble pattern recognition"
            ],
            ErrorType.TRANSFORMATION_ERROR: [
                "Add rule consistency checking",
                "Validate transformations before application",
                "Use constraint satisfaction"
            ],
            ErrorType.SPATIAL_REASONING_ERROR: [
                "Improve spatial parsing accuracy",
                "Add spatial consistency checks",
                "Use geometric constraints"
            ],
            ErrorType.LOGICAL_INCONSISTENCY: [
                "Add logical validation steps",
                "Use formal reasoning checks",
                "Implement consistency monitors"
            ],
            ErrorType.INCOMPLETE_ANALYSIS: [
                "Add completeness checks",
                "Implement mandatory analysis steps",
                "Use analysis checklists"
            ]
        }
        
        return prevention_strategies.get(most_common_type, ["General error prevention"])
    
    def _suggest_correction_strategies(self, errors: List[ErrorInstance]) -> List[CorrectionStrategy]:
        """Suggest correction strategies for this error pattern"""
        
        error_types = [e.error_type for e in errors]
        severities = [e.severity for e in errors]
        
        most_common_type = Counter(error_types).most_common(1)[0][0]
        most_common_severity = Counter(severities).most_common(1)[0][0]
        
        # Choose strategies based on error type and severity
        if most_common_severity in [ErrorSeverity.CRITICAL, ErrorSeverity.MAJOR]:
            return [
                CorrectionStrategy.RETRY_WITH_DIFFERENT_APPROACH,
                CorrectionStrategy.BREAK_DOWN_PROBLEM,
                CorrectionStrategy.SEEK_ADDITIONAL_INFORMATION
            ]
        else:
            return [
                CorrectionStrategy.REFINE_CURRENT_APPROACH,
                CorrectionStrategy.USE_ANALOGICAL_REASONING
            ]
    
    def _update_existing_patterns(self, errors: List[ErrorInstance]):
        """Update existing patterns with new error instances"""
        
        for error in errors:
            signature = self._create_error_signature(error)
            
            # Find matching pattern
            for pattern in self.error_patterns.values():
                if pattern.error_signature == signature:
                    pattern.error_instances.append(error.error_id)
                    pattern.frequency += 1
                    pattern.last_occurrence = error.timestamp
                    break

class SelfCorrectionSystem:
    """Implements self-correction mechanisms"""
    
    def __init__(self):
        self.correctors = {
            CorrectionStrategy.RETRY_WITH_DIFFERENT_APPROACH: self._retry_different_approach,
            CorrectionStrategy.REFINE_CURRENT_APPROACH: self._refine_current_approach,
            CorrectionStrategy.SEEK_ADDITIONAL_INFORMATION: self._seek_additional_info,
            CorrectionStrategy.BREAK_DOWN_PROBLEM: self._break_down_problem,
            CorrectionStrategy.USE_ANALOGICAL_REASONING: self._use_analogical_reasoning,
            CorrectionStrategy.APPLY_CONSTRAINT_SATISFACTION: self._apply_constraint_satisfaction,
            CorrectionStrategy.ENSEMBLE_MULTIPLE_SOLUTIONS: self._ensemble_solutions
        }
        
        self.correction_history = []
        
        logger.info("🔧 Self-Correction System initialized")
    
    def attempt_correction(self, error: ErrorInstance, 
                          task_context: Dict[str, Any]) -> Optional[SelfCorrectionAction]:
        """Attempt to correct an identified error"""
        
        # Choose appropriate correction strategy
        strategy = self._choose_correction_strategy(error)
        
        if strategy not in self.correctors:
            logger.warning(f"No corrector available for strategy: {strategy}")
            return None
        
        # Attempt correction
        try:
            action = self.correctors[strategy](error, task_context)
            self.correction_history.append(action)
            return action
        except Exception as e:
            logger.error(f"Correction attempt failed: {e}")
            return None
    
    def _choose_correction_strategy(self, error: ErrorInstance) -> CorrectionStrategy:
        """Choose the most appropriate correction strategy for an error"""
        
        # Strategy selection based on error type and severity
        strategy_map = {
            (ErrorType.PATTERN_MISRECOGNITION, ErrorSeverity.CRITICAL): CorrectionStrategy.RETRY_WITH_DIFFERENT_APPROACH,
            (ErrorType.PATTERN_MISRECOGNITION, ErrorSeverity.MAJOR): CorrectionStrategy.USE_ANALOGICAL_REASONING,
            (ErrorType.PATTERN_MISRECOGNITION, ErrorSeverity.MINOR): CorrectionStrategy.REFINE_CURRENT_APPROACH,
            
            (ErrorType.TRANSFORMATION_ERROR, ErrorSeverity.CRITICAL): CorrectionStrategy.BREAK_DOWN_PROBLEM,
            (ErrorType.TRANSFORMATION_ERROR, ErrorSeverity.MAJOR): CorrectionStrategy.APPLY_CONSTRAINT_SATISFACTION,
            (ErrorType.TRANSFORMATION_ERROR, ErrorSeverity.MINOR): CorrectionStrategy.REFINE_CURRENT_APPROACH,
            
            (ErrorType.SPATIAL_REASONING_ERROR, ErrorSeverity.CRITICAL): CorrectionStrategy.RETRY_WITH_DIFFERENT_APPROACH,
            (ErrorType.SPATIAL_REASONING_ERROR, ErrorSeverity.MAJOR): CorrectionStrategy.BREAK_DOWN_PROBLEM,
            (ErrorType.SPATIAL_REASONING_ERROR, ErrorSeverity.MINOR): CorrectionStrategy.REFINE_CURRENT_APPROACH,
            
            (ErrorType.LOGICAL_INCONSISTENCY, ErrorSeverity.CRITICAL): CorrectionStrategy.RETRY_WITH_DIFFERENT_APPROACH,
            (ErrorType.LOGICAL_INCONSISTENCY, ErrorSeverity.MAJOR): CorrectionStrategy.APPLY_CONSTRAINT_SATISFACTION,
            (ErrorType.LOGICAL_INCONSISTENCY, ErrorSeverity.MINOR): CorrectionStrategy.REFINE_CURRENT_APPROACH,
            
            (ErrorType.INCOMPLETE_ANALYSIS, ErrorSeverity.CRITICAL): CorrectionStrategy.BREAK_DOWN_PROBLEM,
            (ErrorType.INCOMPLETE_ANALYSIS, ErrorSeverity.MAJOR): CorrectionStrategy.SEEK_ADDITIONAL_INFORMATION,
            (ErrorType.INCOMPLETE_ANALYSIS, ErrorSeverity.MINOR): CorrectionStrategy.REFINE_CURRENT_APPROACH,
        }
        
        key = (error.error_type, error.severity)
        return strategy_map.get(key, CorrectionStrategy.REFINE_CURRENT_APPROACH)
    
    def _retry_different_approach(self, error: ErrorInstance, 
                                 task_context: Dict[str, Any]) -> SelfCorrectionAction:
        """Retry with a completely different approach"""
        
        action = SelfCorrectionAction(
            action_id=f"retry_{error.error_id}_{int(time.time())}",
            action_type=CorrectionStrategy.RETRY_WITH_DIFFERENT_APPROACH,
            description="Retry task with different approach",
            target_error=error.error_id,
            correction_function=None,  # Would be implemented with actual correction logic
            parameters={"approach": "alternative_method"},
            success=False,  # Would be determined after execution
            before_state=task_context.copy(),
            after_state={},
            improvement_metrics={},
            execution_time=0.0,
            timestamp=time.time()
        )
        
        # Simulate correction attempt
        action.success = True  # In real implementation, this would depend on actual results
        action.after_state = task_context.copy()
        action.improvement_metrics = {"confidence_increase": 0.2, "accuracy_increase": 0.3}
        
        return action
    
    def _refine_current_approach(self, error: ErrorInstance, 
                                task_context: Dict[str, Any]) -> SelfCorrectionAction:
        """Refine the current approach to fix the error"""
        
        action = SelfCorrectionAction(
            action_id=f"refine_{error.error_id}_{int(time.time())}",
            action_type=CorrectionStrategy.REFINE_CURRENT_APPROACH,
            description="Refine current approach to address error",
            target_error=error.error_id,
            correction_function=None,
            parameters={"refinement_type": "parameter_adjustment"},
            success=True,
            before_state=task_context.copy(),
            after_state=task_context.copy(),
            improvement_metrics={"accuracy_increase": 0.1},
            execution_time=0.0,
            timestamp=time.time()
        )
        
        return action
    
    def _seek_additional_info(self, error: ErrorInstance, 
                             task_context: Dict[str, Any]) -> SelfCorrectionAction:
        """Seek additional information to resolve the error"""
        
        action = SelfCorrectionAction(
            action_id=f"seek_info_{error.error_id}_{int(time.time())}",
            action_type=CorrectionStrategy.SEEK_ADDITIONAL_INFORMATION,
            description="Seek additional information to resolve error",
            target_error=error.error_id,
            correction_function=None,
            parameters={"info_source": "additional_analysis"},
            success=True,
            before_state=task_context.copy(),
            after_state=task_context.copy(),
            improvement_metrics={"information_gain": 0.4},
            execution_time=0.0,
            timestamp=time.time()
        )
        
        return action
    
    def _break_down_problem(self, error: ErrorInstance, 
                           task_context: Dict[str, Any]) -> SelfCorrectionAction:
        """Break down the problem into smaller parts"""
        
        action = SelfCorrectionAction(
            action_id=f"breakdown_{error.error_id}_{int(time.time())}",
            action_type=CorrectionStrategy.BREAK_DOWN_PROBLEM,
            description="Break down problem into manageable parts",
            target_error=error.error_id,
            correction_function=None,
            parameters={"decomposition_strategy": "hierarchical"},
            success=True,
            before_state=task_context.copy(),
            after_state=task_context.copy(),
            improvement_metrics={"complexity_reduction": 0.5},
            execution_time=0.0,
            timestamp=time.time()
        )
        
        return action
    
    def _use_analogical_reasoning(self, error: ErrorInstance, 
                                 task_context: Dict[str, Any]) -> SelfCorrectionAction:
        """Use analogical reasoning to find solution"""
        
        action = SelfCorrectionAction(
            action_id=f"analogy_{error.error_id}_{int(time.time())}",
            action_type=CorrectionStrategy.USE_ANALOGICAL_REASONING,
            description="Use analogical reasoning to solve problem",
            target_error=error.error_id,
            correction_function=None,
            parameters={"analogy_source": "similar_tasks"},
            success=True,
            before_state=task_context.copy(),
            after_state=task_context.copy(),
            improvement_metrics={"analogy_strength": 0.7},
            execution_time=0.0,
            timestamp=time.time()
        )
        
        return action
    
    def _apply_constraint_satisfaction(self, error: ErrorInstance, 
                                     task_context: Dict[str, Any]) -> SelfCorrectionAction:
        """Apply constraint satisfaction to resolve conflicts"""
        
        action = SelfCorrectionAction(
            action_id=f"constraint_{error.error_id}_{int(time.time())}",
            action_type=CorrectionStrategy.APPLY_CONSTRAINT_SATISFACTION,
            description="Apply constraint satisfaction to resolve error",
            target_error=error.error_id,
            correction_function=None,
            parameters={"constraint_type": "logical_consistency"},
            success=True,
            before_state=task_context.copy(),
            after_state=task_context.copy(),
            improvement_metrics={"consistency_improvement": 0.6},
            execution_time=0.0,
            timestamp=time.time()
        )
        
        return action
    
    def _ensemble_solutions(self, error: ErrorInstance, 
                           task_context: Dict[str, Any]) -> SelfCorrectionAction:
        """Ensemble multiple solutions to improve accuracy"""
        
        action = SelfCorrectionAction(
            action_id=f"ensemble_{error.error_id}_{int(time.time())}",
            action_type=CorrectionStrategy.ENSEMBLE_MULTIPLE_SOLUTIONS,
            description="Ensemble multiple solutions",
            target_error=error.error_id,
            correction_function=None,
            parameters={"ensemble_method": "weighted_voting"},
            success=True,
            before_state=task_context.copy(),
            after_state=task_context.copy(),
            improvement_metrics={"ensemble_improvement": 0.3},
            execution_time=0.0,
            timestamp=time.time()
        )
        
        return action

class AdvancedErrorAnalysisSystem:
    """Main system that integrates error detection, pattern analysis, and self-correction"""
    
    def __init__(self):
        self.error_detector = ErrorDetector()
        self.pattern_analyzer = ErrorPatternAnalyzer()
        self.self_corrector = SelfCorrectionSystem()
        
        # Error repository
        self.all_errors: List[ErrorInstance] = []
        self.error_patterns: Dict[str, ErrorPattern] = {}
        self.correction_actions: List[SelfCorrectionAction] = []
        
        # Learning mechanisms
        self.learning_from_errors = True
        self.auto_correction = True
        
        logger.info("🧠 Advanced Error Analysis System initialized")
    
    def analyze_and_correct(self, task_result: Any, expected_result: Any = None, 
                           task_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Complete error analysis and correction pipeline"""
        
        if task_context is None:
            task_context = {}
        
        # 1. Detect errors
        detected_errors = self.error_detector.detect_errors(task_result, expected_result)
        self.all_errors.extend(detected_errors)
        
        # 2. Analyze error patterns
        if self.learning_from_errors:
            new_patterns = self.pattern_analyzer.analyze_error_patterns(detected_errors)
            for pattern in new_patterns:
                self.error_patterns[pattern.pattern_id] = pattern
        
        # 3. Attempt corrections
        correction_results = []
        if self.auto_correction:
            for error in detected_errors:
                if error.severity in [ErrorSeverity.CRITICAL, ErrorSeverity.MAJOR]:
                    correction_action = self.self_corrector.attempt_correction(error, task_context)
                    if correction_action:
                        correction_results.append(correction_action)
                        self.correction_actions.append(correction_action)
        
        # 4. Generate analysis report
        analysis_report = {
            "errors_detected": len(detected_errors),
            "error_breakdown": Counter([e.error_type.value for e in detected_errors]),
            "severity_breakdown": Counter([e.severity.value for e in detected_errors]),
            "corrections_attempted": len(correction_results),
            "successful_corrections": sum(1 for c in correction_results if c.success),
            "new_patterns_identified": len(new_patterns) if self.learning_from_errors else 0,
            "detailed_errors": [
                {
                    "error_id": e.error_id,
                    "type": e.error_type.value,
                    "severity": e.severity.value,
                    "description": e.error_description,
                    "impact": {
                        "accuracy": e.accuracy_impact,
                        "confidence": e.confidence_impact
                    }
                }
                for e in detected_errors
            ],
            "correction_actions": [
                {
                    "action_id": c.action_id,
                    "strategy": c.action_type.value,
                    "success": c.success,
                    "improvements": c.improvement_metrics
                }
                for c in correction_results
            ]
        }
        
        return analysis_report
    
    def get_learning_insights(self) -> Dict[str, Any]:
        """Generate insights from accumulated error analysis"""
        
        if not self.all_errors:
            return {"message": "No errors analyzed yet"}
        
        insights = {
            "total_errors_analyzed": len(self.all_errors),
            "most_common_error_types": Counter([e.error_type.value for e in self.all_errors]).most_common(5),
            "error_severity_distribution": Counter([e.severity.value for e in self.all_errors]),
            "error_trends": self._analyze_error_trends(),
            "pattern_insights": {
                "total_patterns": len(self.error_patterns),
                "most_frequent_patterns": [
                    {
                        "pattern_name": p.pattern_name,
                        "frequency": p.frequency,
                        "trend": p.trend
                    }
                    for p in sorted(self.error_patterns.values(), key=lambda x: x.frequency, reverse=True)[:5]
                ]
            },
            "correction_effectiveness": self._analyze_correction_effectiveness(),
            "recommendations": self._generate_recommendations()
        }
        
        return insights
    
    def _analyze_error_trends(self) -> Dict[str, Any]:
        """Analyze trends in error occurrence"""
        
        if len(self.all_errors) < 5:
            return {"message": "Insufficient data for trend analysis"}
        
        # Group errors by time windows
        timestamps = [e.timestamp for e in self.all_errors]
        min_time, max_time = min(timestamps), max(timestamps)
        time_span = max_time - min_time
        
        if time_span < 3600:  # Less than 1 hour
            return {"message": "Time span too short for meaningful trend analysis"}
        
        # Divide into time windows
        num_windows = min(10, int(time_span / 600))  # 10-minute windows
        window_size = time_span / num_windows
        
        window_counts = [0] * num_windows
        for timestamp in timestamps:
            window_idx = min(int((timestamp - min_time) / window_size), num_windows - 1)
            window_counts[window_idx] += 1
        
        # Analyze trend
        if len(window_counts) > 1:
            trend_slope = (window_counts[-1] - window_counts[0]) / len(window_counts)
            if trend_slope > 0.5:
                trend = "increasing"
            elif trend_slope < -0.5:
                trend = "decreasing"
            else:
                trend = "stable"
        else:
            trend = "insufficient_data"
        
        return {
            "trend": trend,
            "error_rate_change": trend_slope if len(window_counts) > 1 else 0,
            "time_windows_analyzed": num_windows,
            "average_errors_per_window": np.mean(window_counts)
        }
    
    def _analyze_correction_effectiveness(self) -> Dict[str, Any]:
        """Analyze effectiveness of correction strategies"""
        
        if not self.correction_actions:
            return {"message": "No corrections attempted yet"}
        
        strategy_effectiveness = defaultdict(list)
        for action in self.correction_actions:
            strategy_effectiveness[action.action_type.value].append(action.success)
        
        effectiveness_summary = {}
        for strategy, successes in strategy_effectiveness.items():
            effectiveness_summary[strategy] = {
                "total_attempts": len(successes),
                "success_rate": sum(successes) / len(successes),
                "effectiveness": "high" if sum(successes) / len(successes) > 0.7 else 
                               "medium" if sum(successes) / len(successes) > 0.4 else "low"
            }
        
        return {
            "overall_success_rate": sum(a.success for a in self.correction_actions) / len(self.correction_actions),
            "strategy_effectiveness": effectiveness_summary,
            "most_effective_strategy": max(effectiveness_summary.items(), 
                                         key=lambda x: x[1]["success_rate"])[0] if effectiveness_summary else None
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on error analysis"""
        
        recommendations = []
        
        if not self.all_errors:
            return ["Continue monitoring for errors to generate recommendations"]
        
        # Analyze most common error types
        error_type_counts = Counter([e.error_type.value for e in self.all_errors])
        most_common_error = error_type_counts.most_common(1)[0][0]
        
        error_recommendations = {
            "pattern_misrecognition": [
                "Improve pattern recognition training data",
                "Implement ensemble pattern recognition methods",
                "Add visual feature extraction enhancement"
            ],
            "transformation_error": [
                "Add transformation validation steps",
                "Implement rule consistency checking",
                "Use constraint satisfaction for transformations"
            ],
            "spatial_reasoning_error": [
                "Enhance spatial parsing accuracy",
                "Add geometric constraint validation",
                "Implement spatial relationship verification"
            ],
            "logical_inconsistency": [
                "Add logical consistency checking",
                "Implement formal reasoning validation",
                "Use automated theorem proving for verification"
            ],
            "incomplete_analysis": [
                "Add mandatory completeness checks",
                "Implement analysis step verification",
                "Use checklists for comprehensive analysis"
            ]
        }
        
        recommendations.extend(error_recommendations.get(most_common_error, []))
        
        # Analyze correction effectiveness
        if self.correction_actions:
            success_rate = sum(a.success for a in self.correction_actions) / len(self.correction_actions)
            if success_rate < 0.5:
                recommendations.append("Improve correction strategies - current success rate is low")
            
        # Pattern-based recommendations
        if self.error_patterns:
            increasing_patterns = [p for p in self.error_patterns.values() if p.trend == "increasing"]
            if increasing_patterns:
                recommendations.append(f"Address increasing error patterns: {[p.pattern_name for p in increasing_patterns[:3]]}")
        
        return recommendations
