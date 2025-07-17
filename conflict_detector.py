#!/usr/bin/env python3
"""
Conflict Detector Module
Detects conflicts between rule hypotheses and example validations, triggers revision loops
"""

import logging
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict, Counter

logger = logging.getLogger(__name__)

@dataclass
class ValidationConflict:
    """Represents a conflict between hypothesis and validation result"""
    hypothesis_id: str
    example_index: int
    expected_result: Any
    actual_result: Any
    conflict_type: str  # 'prediction_mismatch', 'rule_violation', 'logical_inconsistency'
    severity: float  # 0.0 to 1.0
    explanation: str
    suggested_revision: str = ""

@dataclass
class ConflictAnalysis:
    """Analysis of all conflicts for a set of hypotheses"""
    total_conflicts: int
    high_severity_conflicts: int
    conflict_patterns: Dict[str, int]
    revision_suggestions: List[str]
    overall_confidence_impact: float

class ConflictDetector:
    """Detects conflicts in hypothesis validation and suggests revisions"""
    
    def __init__(self):
        self.conflict_history = []
        self.revision_patterns = defaultdict(int)
        self.successful_revisions = defaultdict(list)
        
    def detect_conflicts(self, validation_results: List[Dict[str, Any]]) -> List[ValidationConflict]:
        """Detect conflicts in validation results"""
        conflicts = []
        
        logger.info(f"Detecting conflicts in {len(validation_results)} validation results")
        
        for result in validation_results:
            hypothesis_id = result.get('hypothesis_id', 'unknown')
            validations = result.get('validations', [])
            
            for i, validation in enumerate(validations):
                if validation.get('success', True):
                    continue
                    
                # Detected a validation failure - analyze the conflict
                conflict = self._analyze_validation_failure(hypothesis_id, i, validation)
                if conflict:
                    conflicts.append(conflict)
        
        logger.info(f"Detected {len(conflicts)} conflicts")
        return conflicts
    
    def _analyze_validation_failure(self, hypothesis_id: str, example_index: int, 
                                  validation: Dict[str, Any]) -> Optional[ValidationConflict]:
        """Analyze a specific validation failure to create a conflict"""
        
        expected = validation.get('expected')
        actual = validation.get('actual') 
        error_type = validation.get('error_type', 'unknown')
        
        # Determine conflict type and severity
        conflict_type = self._classify_conflict_type(error_type, expected, actual)
        severity = self._calculate_conflict_severity(conflict_type, expected, actual)
        explanation = self._generate_conflict_explanation(conflict_type, expected, actual)
        suggested_revision = self._suggest_revision(conflict_type, validation)
        
        return ValidationConflict(
            hypothesis_id=hypothesis_id,
            example_index=example_index,
            expected_result=expected,
            actual_result=actual,
            conflict_type=conflict_type,
            severity=severity,
            explanation=explanation,
            suggested_revision=suggested_revision
        )
    
    def _classify_conflict_type(self, error_type: str, expected: Any, actual: Any) -> str:
        """Classify the type of conflict"""
        
        if error_type == 'shape_mismatch':
            return 'prediction_mismatch'
        elif error_type == 'color_mismatch':
            return 'rule_violation'
        elif error_type == 'pattern_mismatch':
            return 'logical_inconsistency'
        elif error_type == 'transformation_error':
            return 'rule_violation'
        else:
            # Analyze based on expected vs actual
            if expected is None or actual is None:
                return 'prediction_mismatch'
            elif isinstance(expected, np.ndarray) and isinstance(actual, np.ndarray):
                if expected.shape != actual.shape:
                    return 'prediction_mismatch'
                else:
                    return 'rule_violation'
            else:
                return 'logical_inconsistency'
    
    def _calculate_conflict_severity(self, conflict_type: str, expected: Any, actual: Any) -> float:
        """Calculate the severity of a conflict (0.0 to 1.0)"""
        
        base_severity = {
            'prediction_mismatch': 0.8,
            'rule_violation': 0.6,
            'logical_inconsistency': 0.9
        }.get(conflict_type, 0.5)
        
        # Adjust based on how different expected vs actual are
        if isinstance(expected, np.ndarray) and isinstance(actual, np.ndarray):
            if expected.shape == actual.shape:
                # Calculate pixel-wise difference
                difference_ratio = np.mean(expected != actual)
                severity_adjustment = difference_ratio * 0.3
            else:
                # Shape mismatch is always high severity
                severity_adjustment = 0.2
        else:
            severity_adjustment = 0.1
        
        return min(1.0, base_severity + severity_adjustment)
    
    def _generate_conflict_explanation(self, conflict_type: str, expected: Any, actual: Any) -> str:
        """Generate human-readable explanation for the conflict"""
        
        if conflict_type == 'prediction_mismatch':
            if isinstance(expected, np.ndarray) and isinstance(actual, np.ndarray):
                if expected.shape != actual.shape:
                    return f"Output shape mismatch: expected {expected.shape}, got {actual.shape}"
                else:
                    diff_pixels = np.sum(expected != actual)
                    total_pixels = expected.size
                    return f"Pixel differences: {diff_pixels}/{total_pixels} pixels don't match"
            else:
                return f"Prediction mismatch: expected {expected}, got {actual}"
        
        elif conflict_type == 'rule_violation':
            return f"Hypothesis rule was violated - transformation produced unexpected result"
        
        elif conflict_type == 'logical_inconsistency':
            return f"Logical inconsistency detected between expected behavior and actual outcome"
        
        else:
            return f"Unknown conflict type: {conflict_type}"
    
    def _suggest_revision(self, conflict_type: str, validation: Dict[str, Any]) -> str:
        """Suggest how to revise the hypothesis to fix the conflict"""
        
        if conflict_type == 'prediction_mismatch':
            return "Revise output size prediction rules or spatial transformation logic"
        
        elif conflict_type == 'rule_violation':
            error_details = validation.get('error_details', '')
            if 'color' in error_details.lower():
                return "Revise color transformation rules"
            elif 'movement' in error_details.lower():
                return "Revise object movement/positioning rules"
            else:
                return "Revise core transformation logic"
        
        elif conflict_type == 'logical_inconsistency':
            return "Reconsider fundamental assumptions about task requirements"
        
        else:
            return "Perform general hypothesis refinement"
    
    def analyze_conflict_patterns(self, conflicts: List[ValidationConflict]) -> ConflictAnalysis:
        """Analyze patterns in conflicts to provide overall guidance"""
        
        if not conflicts:
            return ConflictAnalysis(
                total_conflicts=0,
                high_severity_conflicts=0,
                conflict_patterns={},
                revision_suggestions=[],
                overall_confidence_impact=0.0
            )
        
        # Count conflict types
        conflict_patterns = Counter(c.conflict_type for c in conflicts)
        
        # Count high severity conflicts
        high_severity_conflicts = sum(1 for c in conflicts if c.severity > 0.7)
        
        # Generate revision suggestions
        revision_suggestions = self._generate_revision_suggestions(conflicts)
        
        # Calculate confidence impact
        avg_severity = sum(c.severity for c in conflicts) / len(conflicts)
        confidence_impact = min(0.9, avg_severity * len(conflicts) / 10)
        
        return ConflictAnalysis(
            total_conflicts=len(conflicts),
            high_severity_conflicts=high_severity_conflicts,
            conflict_patterns=dict(conflict_patterns),
            revision_suggestions=revision_suggestions,
            overall_confidence_impact=confidence_impact
        )
    
    def _generate_revision_suggestions(self, conflicts: List[ValidationConflict]) -> List[str]:
        """Generate prioritized revision suggestions"""
        suggestions = []
        
        # Group conflicts by type
        conflict_groups = defaultdict(list)
        for conflict in conflicts:
            conflict_groups[conflict.conflict_type].append(conflict)
        
        # Priority order for addressing conflicts
        priority_order = ['logical_inconsistency', 'prediction_mismatch', 'rule_violation']
        
        for conflict_type in priority_order:
            if conflict_type in conflict_groups:
                conflicts_of_type = conflict_groups[conflict_type]
                suggestion = self._create_type_specific_suggestion(conflict_type, conflicts_of_type)
                suggestions.append(suggestion)
        
        return suggestions
    
    def _create_type_specific_suggestion(self, conflict_type: str, conflicts: List[ValidationConflict]) -> str:
        """Create specific suggestion for a type of conflict"""
        
        count = len(conflicts)
        avg_severity = sum(c.severity for c in conflicts) / count
        
        if conflict_type == 'logical_inconsistency':
            return f"HIGH PRIORITY: {count} logical inconsistencies detected (avg severity: {avg_severity:.2f}). Fundamental revision needed."
        
        elif conflict_type == 'prediction_mismatch':
            return f"MEDIUM PRIORITY: {count} prediction mismatches (avg severity: {avg_severity:.2f}). Revise output generation logic."
        
        elif conflict_type == 'rule_violation':
            return f"LOW PRIORITY: {count} rule violations (avg severity: {avg_severity:.2f}). Fine-tune transformation rules."
        
        else:
            return f"UNKNOWN: {count} conflicts of type {conflict_type} need investigation."
    
    def start_revision_loop(self, initial_hypotheses: List[Any], 
                           validation_function: Any,
                           examples: List[Dict[str, Any]],
                           max_iterations: int = 5) -> Tuple[List[Any], List[ValidationConflict]]:
        """Start an iterative revision loop to resolve conflicts"""
        
        logger.info(f"Starting revision loop with {len(initial_hypotheses)} initial hypotheses")
        
        current_hypotheses = initial_hypotheses.copy()
        all_conflicts = []
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            logger.info(f"Revision iteration {iteration}")
            
            # Validate current hypotheses
            validation_results = validation_function(current_hypotheses, examples)
            
            # Detect conflicts
            conflicts = self.detect_conflicts(validation_results)
            all_conflicts.extend(conflicts)
            
            if not conflicts:
                logger.info("No conflicts found - revision loop successful")
                break
            
            # Analyze conflicts
            conflict_analysis = self.analyze_conflict_patterns(conflicts)
            
            # Check if we should continue
            if conflict_analysis.high_severity_conflicts == 0:
                logger.info("No high-severity conflicts remaining")
                break
            
            # Generate revised hypotheses (simplified for now)
            current_hypotheses = self._generate_revised_hypotheses(
                current_hypotheses, conflicts, conflict_analysis
            )
            
            logger.info(f"Generated {len(current_hypotheses)} revised hypotheses")
        
        logger.info(f"Revision loop completed after {iteration-1} iterations")
        return current_hypotheses, all_conflicts
    
    def _generate_revised_hypotheses(self, current_hypotheses: List[Any], 
                                   conflicts: List[ValidationConflict],
                                   analysis: ConflictAnalysis) -> List[Any]:
        """Generate revised hypotheses based on conflicts (simplified implementation)"""
        
        # For now, just return current hypotheses
        # In a full implementation, this would:
        # 1. Identify which hypotheses caused which conflicts
        # 2. Apply specific revision strategies
        # 3. Generate new candidate hypotheses
        # 4. Rank them by likelihood of success
        
        return current_hypotheses

def main():
    """Test the conflict detector"""
    detector = ConflictDetector()
    
    # Simulate some validation results with conflicts
    validation_results = [
        {
            'hypothesis_id': 'hyp_1',
            'validations': [
                {'success': False, 'error_type': 'shape_mismatch', 'expected': (3, 3), 'actual': (2, 2)},
                {'success': True},
                {'success': False, 'error_type': 'color_mismatch', 'expected': 'blue', 'actual': 'red'}
            ]
        }
    ]
    
    conflicts = detector.detect_conflicts(validation_results)
    analysis = detector.analyze_conflict_patterns(conflicts)
    
    print(f"Detected {len(conflicts)} conflicts")
    print(f"Analysis: {analysis.revision_suggestions}")

if __name__ == "__main__":
    main()
