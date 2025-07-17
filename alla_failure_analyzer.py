#!/usr/bin/env python3
"""
ALLA Failure Analyzer - Error-Based Learning Loop
Analyzes failures to evolve concepts, hypotheses, and reasoning patterns.
"""

import json
import numpy as np
import os
import logging
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, field
from collections import defaultdict, Counter
from datetime import datetime
import networkx as nx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class FailureAnalysis:
    """Analysis of why a task failed"""
    task_id: str
    failure_type: str  # perception, rule_conflict, incomplete_hypothesis, transformation_error
    root_cause: str
    visual_confusion: List[str] = field(default_factory=list)
    semantic_gaps: List[str] = field(default_factory=list)
    hypothesis_conflicts: List[str] = field(default_factory=list)
    proposed_fix: str = ""
    confidence: float = 0.0

@dataclass
class HypothesisEvolution:
    """Tracks how hypotheses evolve"""
    original_name: str
    evolved_name: str
    reason: str
    confidence_change: float
    evidence: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

class ARCFailureAnalyzer:
    """Analyzes ARC task failures to drive autonomous learning"""
    
    def __init__(self):
        self.failure_patterns = defaultdict(list)
        self.semantic_gaps = defaultdict(int)
        self.visual_confusions = defaultdict(int)
        self.hypothesis_evolution_log = []
        self.compound_patterns = {}
        
    def analyze_failed_task(self, task_data: Dict, predicted_output: np.ndarray, 
                           expected_output: np.ndarray, trace: Any) -> FailureAnalysis:
        """Deep analysis of why a task failed"""
        
        failure_analysis = FailureAnalysis(
            task_id=trace.task_id,
            failure_type="unknown",
            root_cause="",
            confidence=0.0
        )
        
        # 1. Visual Perception Analysis
        visual_issues = self._analyze_visual_perception(task_data, predicted_output, expected_output)
        failure_analysis.visual_confusion.extend(visual_issues)
        
        # 2. Semantic Gap Analysis
        semantic_issues = self._analyze_semantic_gaps(trace)
        failure_analysis.semantic_gaps.extend(semantic_issues)
        
        # 3. Hypothesis Conflict Analysis
        hypothesis_issues = self._analyze_hypothesis_conflicts(trace)
        failure_analysis.hypothesis_conflicts.extend(hypothesis_issues)
        
        # 4. Determine Primary Failure Type
        failure_analysis.failure_type = self._classify_failure_type(
            visual_issues, semantic_issues, hypothesis_issues
        )
        
        # 5. Generate Root Cause
        failure_analysis.root_cause = self._identify_root_cause(failure_analysis)
        
        # 6. Propose Fix
        failure_analysis.proposed_fix = self._propose_fix(failure_analysis)
        failure_analysis.confidence = self._calculate_analysis_confidence(failure_analysis)
        
        logger.info(f"Failure Analysis for {trace.task_id}: {failure_analysis.failure_type} - {failure_analysis.root_cause}")
        
        return failure_analysis
    
    def _analyze_visual_perception(self, task_data: Dict, predicted: np.ndarray, 
                                 expected: np.ndarray) -> List[str]:
        """Analyze visual perception issues"""
        issues = []
        
        # Shape mismatch
        if predicted.shape != expected.shape:
            issues.append(f"shape_mismatch: predicted {predicted.shape} vs expected {expected.shape}")
            
        # Color distribution analysis
        pred_colors = set(np.unique(predicted))
        exp_colors = set(np.unique(expected))
        
        if pred_colors != exp_colors:
            issues.append(f"color_mismatch: predicted {pred_colors} vs expected {exp_colors}")
        
        # Pattern structure analysis
        if predicted.shape == expected.shape:
            # Check structural differences
            structure_diff = self._analyze_structure_difference(predicted, expected)
            if structure_diff:
                issues.extend(structure_diff)
        
        # Analyze training examples for clues
        train_examples = task_data.get('train', [])
        for i, example in enumerate(train_examples):
            input_grid = np.array(example['input'])
            output_grid = np.array(example['output'])
            
            # Check if we're missing transformation patterns
            transformation_hints = self._detect_transformation_hints(input_grid, output_grid)
            issues.extend([f"missed_transformation_{i}: {hint}" for hint in transformation_hints])
        
        return issues
    
    def _analyze_structure_difference(self, predicted: np.ndarray, expected: np.ndarray) -> List[str]:
        """Analyze structural differences between predicted and expected"""
        issues = []
        
        # Connected components analysis
        pred_components = self._count_connected_components(predicted)
        exp_components = self._count_connected_components(expected)
        
        if pred_components != exp_components:
            issues.append(f"component_count_mismatch: {pred_components} vs {exp_components}")
        
        # Symmetry analysis
        pred_symmetry = self._analyze_symmetry(predicted)
        exp_symmetry = self._analyze_symmetry(expected)
        
        if pred_symmetry != exp_symmetry:
            issues.append(f"symmetry_mismatch: {pred_symmetry} vs {exp_symmetry}")
        
        # Pattern density
        pred_density = np.count_nonzero(predicted) / predicted.size
        exp_density = np.count_nonzero(expected) / expected.size
        
        if abs(pred_density - exp_density) > 0.2:
            issues.append(f"density_mismatch: {pred_density:.2f} vs {exp_density:.2f}")
        
        return issues
    
    def _count_connected_components(self, grid: np.ndarray) -> int:
        """Count connected components in grid"""
        visited = np.zeros_like(grid, dtype=bool)
        components = 0
        
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                if grid[i, j] != 0 and not visited[i, j]:
                    self._dfs_component_count(grid, i, j, visited)
                    components += 1
        
        return components
    
    def _dfs_component_count(self, grid: np.ndarray, row: int, col: int, visited: np.ndarray):
        """DFS for component counting"""
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
            visited[row, col] or grid[row, col] == 0):
            return
        
        visited[row, col] = True
        
        # Check 4-connected neighbors
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            self._dfs_component_count(grid, row + dr, col + dc, visited)
    
    def _analyze_symmetry(self, grid: np.ndarray) -> str:
        """Analyze symmetry properties"""
        if np.array_equal(grid, np.flipud(grid)):
            return "horizontal_symmetry"
        elif np.array_equal(grid, np.fliplr(grid)):
            return "vertical_symmetry"
        elif np.array_equal(grid, np.rot90(grid, 2)):
            return "rotational_symmetry"
        else:
            return "no_symmetry"
    
    def _detect_transformation_hints(self, input_grid: np.ndarray, output_grid: np.ndarray) -> List[str]:
        """Detect transformation hints from training examples"""
        hints = []
        
        # Size relationship
        if output_grid.size > input_grid.size:
            hints.append("expansion_needed")
        elif output_grid.size < input_grid.size:
            hints.append("contraction_needed")
        
        # Object count analysis
        input_objects = len(np.unique(input_grid[input_grid != 0]))
        output_objects = len(np.unique(output_grid[output_grid != 0]))
        
        if output_objects > input_objects:
            hints.append("new_objects_created")
        elif output_objects < input_objects:
            hints.append("objects_removed")
        
        # Pattern replication
        if self._is_pattern_replicated(input_grid, output_grid):
            hints.append("pattern_replication")
        
        return hints
    
    def _is_pattern_replicated(self, input_grid: np.ndarray, output_grid: np.ndarray) -> bool:
        """Check if input pattern is replicated in output"""
        input_h, input_w = input_grid.shape
        output_h, output_w = output_grid.shape
        
        if output_h % input_h == 0 and output_w % input_w == 0:
            tiles_h = output_h // input_h
            tiles_w = output_w // input_w
            
            if tiles_h > 1 or tiles_w > 1:
                # Check if it's a clean replication
                for th in range(tiles_h):
                    for tw in range(tiles_w):
                        start_h = th * input_h
                        start_w = tw * input_w
                        tile = output_grid[start_h:start_h + input_h, start_w:start_w + input_w]
                        
                        similarity = np.sum(tile == input_grid) / input_grid.size
                        if similarity > 0.8:
                            return True
        
        return False
    
    def _analyze_semantic_gaps(self, trace: Any) -> List[str]:
        """Analyze semantic understanding gaps"""
        gaps = []
        
        # Check if concepts were created but not used effectively
        if trace.new_concepts_created and not trace.success:
            gaps.append("new_concepts_not_integrated")
        
        # Check for missing fundamental concepts
        if "gravity" not in trace.concepts_used and any("fall" in step for step in trace.reasoning_steps):
            gaps.append("missing_gravity_concept")
        
        if "symmetry" not in trace.concepts_used and any("mirror" in step or "reflect" in step for step in trace.reasoning_steps):
            gaps.append("missing_symmetry_concept")
        
        # Check for logical reasoning gaps
        if len(trace.reasoning_steps) < 3:
            gaps.append("insufficient_reasoning_depth")
        
        if trace.failure_points and any("unknown" in fp for fp in trace.failure_points):
            gaps.append("pattern_recognition_failure")
        
        return gaps
    
    def _analyze_hypothesis_conflicts(self, trace: Any) -> List[str]:
        """Analyze hypothesis conflicts"""
        conflicts = []
        
        # Multiple competing hypotheses
        if len(trace.hypotheses_tested) > 3:
            conflicts.append("hypothesis_confusion")
        
        # Low confidence hypotheses used
        # Note: This would need access to hypothesis confidence values
        
        # Contradictory reasoning steps
        reasoning_text = " ".join(trace.reasoning_steps).lower()
        if "expand" in reasoning_text and "shrink" in reasoning_text:
            conflicts.append("contradictory_size_reasoning")
        
        if "add" in reasoning_text and "remove" in reasoning_text:
            conflicts.append("contradictory_object_reasoning")
        
        return conflicts
    
    def _classify_failure_type(self, visual_issues: List[str], semantic_issues: List[str], 
                              hypothesis_issues: List[str]) -> str:
        """Classify the primary failure type"""
        if len(visual_issues) > len(semantic_issues) + len(hypothesis_issues):
            return "perception"
        elif len(semantic_issues) > len(visual_issues) + len(hypothesis_issues):
            return "semantic_gap"
        elif len(hypothesis_issues) > 0:
            return "hypothesis_conflict"
        elif any("transformation" in issue for issue in visual_issues):
            return "transformation_error"
        else:
            return "incomplete_reasoning"
    
    def _identify_root_cause(self, analysis: FailureAnalysis) -> str:
        """Identify the root cause of failure"""
        if analysis.failure_type == "perception":
            if any("shape_mismatch" in vc for vc in analysis.visual_confusion):
                return "Failed to predict correct output dimensions"
            elif any("color_mismatch" in vc for vc in analysis.visual_confusion):
                return "Color transformation rules not understood"
            else:
                return "Visual pattern structure not recognized"
        
        elif analysis.failure_type == "semantic_gap":
            if "missing_gravity_concept" in analysis.semantic_gaps:
                return "Lacks understanding of gravity/falling behavior"
            elif "missing_symmetry_concept" in analysis.semantic_gaps:
                return "Lacks understanding of symmetry operations"
            elif "insufficient_reasoning_depth" in analysis.semantic_gaps:
                return "Multi-step reasoning capability insufficient"
            else:
                return "Missing key conceptual understanding"
        
        elif analysis.failure_type == "hypothesis_conflict":
            return "Multiple competing hypotheses caused confusion"
        
        elif analysis.failure_type == "transformation_error":
            return "Transformation algorithm implementation incorrect"
        
        else:
            return "Incomplete reasoning chain"
    
    def _propose_fix(self, analysis: FailureAnalysis) -> str:
        """Propose a fix for the identified failure"""
        if analysis.failure_type == "perception":
            if "shape_mismatch" in analysis.root_cause:
                return "Create dimension prediction rules based on input analysis"
            elif "color" in analysis.root_cause:
                return "Develop color transformation mapping rules"
            else:
                return "Enhance visual pattern recognition with more structural features"
        
        elif analysis.failure_type == "semantic_gap":
            if "gravity" in analysis.root_cause:
                return "Bootstrap gravity concept with downward movement rules"
            elif "symmetry" in analysis.root_cause:
                return "Bootstrap symmetry concepts with reflection/rotation rules"
            elif "reasoning_depth" in analysis.root_cause:
                return "Implement multi-step reasoning chains with intermediate validation"
            else:
                return "Research and bootstrap missing conceptual knowledge"
        
        elif analysis.failure_type == "hypothesis_conflict":
            return "Implement hypothesis ranking and conflict resolution"
        
        elif analysis.failure_type == "transformation_error":
            return "Debug and refine transformation implementation algorithms"
        
        else:
            return "Extend reasoning capability with more systematic analysis"
    
    def _calculate_analysis_confidence(self, analysis: FailureAnalysis) -> float:
        """Calculate confidence in the failure analysis"""
        confidence = 0.5  # Base confidence
        
        # More issues identified = higher confidence in analysis
        total_issues = (len(analysis.visual_confusion) + 
                       len(analysis.semantic_gaps) + 
                       len(analysis.hypothesis_conflicts))
        
        confidence += min(0.4, total_issues * 0.1)
        
        # Specific failure types we understand well
        if analysis.failure_type in ["perception", "semantic_gap"]:
            confidence += 0.2
        
        return min(1.0, confidence)
    
    def evolve_hypotheses_from_failures(self, failures: List[FailureAnalysis]) -> List[HypothesisEvolution]:
        """Evolve hypotheses based on failure patterns"""
        evolutions = []
        
        # Group failures by type
        failure_groups = defaultdict(list)
        for failure in failures:
            failure_groups[failure.failure_type].append(failure)
        
        # Analyze perception failures
        if "perception" in failure_groups:
            perception_failures = failure_groups["perception"]
            
            # If many shape mismatches, create dimension prediction hypothesis
            shape_mismatches = sum(1 for f in perception_failures 
                                 if any("shape_mismatch" in vc for vc in f.visual_confusion))
            
            if shape_mismatches >= 3:
                evolution = HypothesisEvolution(
                    original_name="basic_transformation",
                    evolved_name="dimension_aware_transformation",
                    reason=f"Evolved due to {shape_mismatches} shape mismatch failures",
                    confidence_change=0.3,
                    evidence=[f.task_id for f in perception_failures[:3]]
                )
                evolutions.append(evolution)
        
        # Analyze semantic gaps
        if "semantic_gap" in failure_groups:
            semantic_failures = failure_groups["semantic_gap"]
            
            # Gravity concept needed
            gravity_needed = sum(1 for f in semantic_failures
                               if "missing_gravity_concept" in f.semantic_gaps)
            
            if gravity_needed >= 2:
                evolution = HypothesisEvolution(
                    original_name="spatial_transformation",
                    evolved_name="gravity_aware_transformation",
                    reason=f"Added gravity concept due to {gravity_needed} failures",
                    confidence_change=0.4,
                    evidence=[f.task_id for f in semantic_failures if "missing_gravity_concept" in f.semantic_gaps]
                )
                evolutions.append(evolution)
        
        # Create compound patterns from multiple failure types
        if len(failure_groups) >= 2:
            compound_evolution = HypothesisEvolution(
                original_name="single_step_reasoning",
                evolved_name="multi_modal_reasoning",
                reason="Combined multiple failure types into compound reasoning",
                confidence_change=0.2,
                evidence=[f.task_id for f in failures[:5]]
            )
            evolutions.append(compound_evolution)
        
        self.hypothesis_evolution_log.extend(evolutions)
        return evolutions
    
    def create_semantic_concepts_from_failures(self, failures: List[FailureAnalysis]) -> List[Dict[str, Any]]:
        """Create new semantic concepts based on failure analysis"""
        new_concepts = []
        
        # Analyze common failure patterns
        all_visual_confusions = []
        all_semantic_gaps = []
        
        for failure in failures:
            all_visual_confusions.extend(failure.visual_confusion)
            all_semantic_gaps.extend(failure.semantic_gaps)
        
        confusion_counts = Counter(all_visual_confusions)
        gap_counts = Counter(all_semantic_gaps)
        
        # Create concepts for common visual confusions
        for confusion, count in confusion_counts.most_common(5):
            if count >= 3:  # Threshold for concept creation
                concept = {
                    'name': f"visual_{confusion.replace('_', '_').lower()}",
                    'type': 'visual_recognition',
                    'definition': f"Visual recognition pattern for {confusion}",
                    'creation_reason': f"Created due to {count} similar visual failures",
                    'examples': [f.task_id for f in failures if confusion in f.visual_confusion][:3]
                }
                new_concepts.append(concept)
        
        # Create concepts for semantic gaps
        for gap, count in gap_counts.most_common(5):
            if count >= 2:
                concept = {
                    'name': gap.replace('missing_', '').replace('_concept', ''),
                    'type': 'semantic_rule',
                    'definition': f"Semantic rule addressing {gap}",
                    'creation_reason': f"Created due to {count} semantic gap failures",
                    'examples': [f.task_id for f in failures if gap in f.semantic_gaps][:3]
                }
                new_concepts.append(concept)
        
        logger.info(f"Created {len(new_concepts)} new concepts from failure analysis")
        return new_concepts
    
    def generate_failure_insights(self, failures: List[FailureAnalysis]) -> Dict[str, Any]:
        """Generate insights from failure analysis"""
        insights = {
            'total_failures_analyzed': len(failures),
            'failure_type_distribution': Counter(f.failure_type for f in failures),
            'root_cause_patterns': Counter(f.root_cause for f in failures),
            'proposed_fixes': Counter(f.proposed_fix for f in failures),
            'average_analysis_confidence': sum(f.confidence for f in failures) / len(failures) if failures else 0,
            'top_visual_confusions': Counter([vc for f in failures for vc in f.visual_confusion]).most_common(10),
            'top_semantic_gaps': Counter([sg for f in failures for sg in f.semantic_gaps]).most_common(10),
            'recommendations': self._generate_failure_recommendations(failures)
        }
        
        return insights
    
    def _generate_failure_recommendations(self, failures: List[FailureAnalysis]) -> List[str]:
        """Generate specific recommendations based on failure patterns"""
        recommendations = []
        
        failure_types = Counter(f.failure_type for f in failures)
        
        if failure_types['perception'] > len(failures) * 0.4:
            recommendations.append("Focus on visual perception improvements - implement better shape and color analysis")
        
        if failure_types['semantic_gap'] > len(failures) * 0.3:
            recommendations.append("Expand semantic knowledge base - research and bootstrap missing concepts")
        
        if failure_types['hypothesis_conflict'] > len(failures) * 0.2:
            recommendations.append("Implement hypothesis ranking and conflict resolution mechanisms")
        
        # Check for specific patterns
        all_fixes = [f.proposed_fix for f in failures]
        if sum(1 for fix in all_fixes if 'gravity' in fix) >= 3:
            recommendations.append("Priority: Implement gravity and physics-based reasoning concepts")
        
        if sum(1 for fix in all_fixes if 'symmetry' in fix) >= 3:
            recommendations.append("Priority: Develop comprehensive symmetry operation capabilities")
        
        return recommendations

def main():
    """Demonstrate failure analysis capabilities"""
    analyzer = ARCFailureAnalyzer()
    
    # This would be called by the main learning system
    print("ALLA Failure Analyzer initialized")
    print("Ready to analyze failures and drive autonomous learning")

if __name__ == "__main__":
    main()
