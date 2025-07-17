#!/usr/bin/env python3
"""
Integrated Demonstration-Driven ARC Solver
Combines all modules: Visual Rule Discovery, Hypothesis Generation, Validation, 
Demonstration Alignment, and Conflict Resolution for human-like ARC reasoning
"""

import numpy as np
import json
import logging
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import copy

# Import our custom modules
from visual_rule_discovery_engine import VisualRuleDiscoveryEngine
from rule_hypothesis_generator import RuleHypothesisGenerator, RuleHypothesis
from multi_example_rule_validator import MultiExampleRuleValidator
from demonstration_alignment_module import MultipledemonstrationAlignmentModule
from conflict_detector_revision_loop import ConflictDetector, RevisionLoop

logger = logging.getLogger(__name__)

@dataclass
class DemonstrationDrivenResult:
    """Result from demonstration-driven reasoning"""
    task_id: str
    success: bool
    predicted_output: Optional[np.ndarray]
    confidence: float
    
    # Discovery and analysis
    rule_discovery_report: Dict[str, Any]
    demonstration_alignment: Dict[str, Any]
    
    # Hypotheses and validation
    generated_hypotheses: List[Dict[str, Any]]
    validation_report: Dict[str, Any]
    
    # Conflict resolution
    conflicts_detected: List[Dict[str, Any]]
    revision_log: Dict[str, Any]
    
    # Final reasoning
    selected_hypothesis: Optional[Dict[str, Any]]
    reasoning_explanation: str
    processing_time: float

class DemonstrationDrivenARCSolver:
    """
    Main solver that uses demonstration comparison and iterative hypothesis revision
    to solve ARC tasks like humans do
    """
    
    def __init__(self):
        # Initialize all component modules
        self.rule_discovery_engine = VisualRuleDiscoveryEngine()
        self.hypothesis_generator = RuleHypothesisGenerator()
        self.rule_validator = MultiExampleRuleValidator()
        self.alignment_module = MultipledemonstrationAlignmentModule()
        self.revision_loop = RevisionLoop(max_iterations=3)
        
        # Statistics and learning
        self.solved_tasks = []
        self.learned_patterns = {}
        self.success_rate_history = []
    
    def solve_arc_task(self, task_data: Dict[str, Any]) -> DemonstrationDrivenResult:
        """
        Solve an ARC task using demonstration-driven reasoning
        """
        start_time = datetime.now()
        task_id = task_data.get('task_id', 'unknown')
        
        logger.info(f"Starting demonstration-driven solving for task {task_id}")
        
        try:
            # Extract training examples
            train_examples = task_data.get('train', [])
            test_input = task_data.get('test', [{}])[0].get('input', [])
            
            if len(train_examples) < 1:
                raise ValueError("Need at least 1 training example")
            
            # Step 1: Align demonstrations to find consistent patterns and anomalies
            logger.info("Step 1: Aligning demonstrations")
            alignment_result = self.alignment_module.align_demonstrations(train_examples)
            
            # Step 2: Discover visual transformation rules from examples
            logger.info("Step 2: Discovering transformation rules")
            discovery_report = self.rule_discovery_engine.discover_rules_from_examples(train_examples)
            
            # Step 3: Generate rule hypotheses based on discoveries
            logger.info("Step 3: Generating rule hypotheses")
            hypotheses = self.hypothesis_generator.generate_hypotheses(discovery_report)
            
            # Step 4: Validate hypotheses against all training examples
            logger.info("Step 4: Validating hypotheses")
            validation_report = self.rule_validator.validate_hypotheses(hypotheses, train_examples)
            
            # Step 5: Detect conflicts and run revision loop if needed
            logger.info("Step 5: Conflict detection and revision")
            revision_log = self.revision_loop.run_revision_loop(
                hypotheses, train_examples, self.rule_validator
            )
            
            # Step 6: Select best hypothesis and apply to test input
            logger.info("Step 6: Selecting hypothesis and generating prediction")
            selected_hypothesis, predicted_output, confidence = self._select_and_apply_hypothesis(
                revision_log["final_hypotheses"], 
                np.array(test_input),
                validation_report
            )
            
            # Step 7: Generate reasoning explanation
            reasoning_explanation = self._generate_reasoning_explanation(
                alignment_result, discovery_report, selected_hypothesis, 
                validation_report, revision_log
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            success = predicted_output is not None
            
            # Create comprehensive result
            result = DemonstrationDrivenResult(
                task_id=task_id,
                success=success,
                predicted_output=predicted_output,
                confidence=confidence,
                rule_discovery_report=discovery_report,
                demonstration_alignment=self._alignment_to_dict(alignment_result),
                generated_hypotheses=[self._hypothesis_to_dict(h) for h in hypotheses],
                validation_report=validation_report,
                conflicts_detected=revision_log.get("iterations", []),
                revision_log=revision_log,
                selected_hypothesis=selected_hypothesis,
                reasoning_explanation=reasoning_explanation,
                processing_time=processing_time
            )
            
            # Learn from this result
            self._learn_from_result(result)
            
            logger.info(f"Task {task_id} completed: success={success}, confidence={confidence:.2f}")
            return result
            
        except Exception as e:
            logger.error(f"Error solving task {task_id}: {e}")
            
            # Return error result
            processing_time = (datetime.now() - start_time).total_seconds()
            return DemonstrationDrivenResult(
                task_id=task_id,
                success=False,
                predicted_output=None,
                confidence=0.0,
                rule_discovery_report={},
                demonstration_alignment={},
                generated_hypotheses=[],
                validation_report={},
                conflicts_detected=[],
                revision_log={},
                selected_hypothesis=None,
                reasoning_explanation=f"Error: {str(e)}",
                processing_time=processing_time
            )
    
    def _select_and_apply_hypothesis(self, final_hypotheses: List[Dict[str, Any]], 
                                   test_input: np.ndarray,
                                   validation_report: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[np.ndarray], float]:
        """Select the best hypothesis and apply it to the test input"""
        
        if not final_hypotheses:
            return None, None, 0.0
        
        # Select hypothesis with highest confidence
        best_hypothesis_dict = max(final_hypotheses, key=lambda h: h.get("confidence", 0.0))
        
        # Find the corresponding RuleHypothesis object (simplified approach)
        # In a real implementation, we'd maintain references to the actual objects
        best_hypothesis = self._dict_to_hypothesis(best_hypothesis_dict)
        
        if not best_hypothesis:
            return best_hypothesis_dict, None, best_hypothesis_dict.get("confidence", 0.0)
        
        # Apply the hypothesis to the test input
        try:
            predicted_output = self.rule_validator.rule_simulator.simulate_rule(test_input, best_hypothesis)
            confidence = best_hypothesis_dict.get("confidence", 0.0)
            
            return best_hypothesis_dict, predicted_output, confidence
            
        except Exception as e:
            logger.error(f"Error applying hypothesis: {e}")
            return best_hypothesis_dict, None, 0.0
    
    def _dict_to_hypothesis(self, hypothesis_dict: Dict[str, Any]) -> Optional[RuleHypothesis]:
        """Convert hypothesis dictionary back to RuleHypothesis object (simplified)"""
        try:
            return RuleHypothesis(
                hypothesis_id=hypothesis_dict.get("hypothesis_id", "unknown"),
                rule_type=hypothesis_dict.get("rule_type", "unknown"),
                conditions=hypothesis_dict.get("conditions", {}),
                actions=hypothesis_dict.get("actions", {}),
                confidence=hypothesis_dict.get("confidence", 0.0)
            )
        except Exception:
            return None
    
    def _generate_reasoning_explanation(self, alignment_result, discovery_report: Dict[str, Any], 
                                      selected_hypothesis: Optional[Dict[str, Any]],
                                      validation_report: Dict[str, Any], 
                                      revision_log: Dict[str, Any]) -> str:
        """Generate human-readable explanation of the reasoning process"""
        
        explanation_parts = []
        
        # Demonstration analysis
        alignment_confidence = alignment_result.alignment_confidence
        explanation_parts.append(
            f"I analyzed {discovery_report.get('examples_analyzed', 0)} demonstration examples "
            f"and found patterns with {alignment_confidence:.1%} consistency."
        )
        
        # Pattern discovery
        num_patterns = len(discovery_report.get('discovered_patterns', []))
        if num_patterns > 0:
            explanation_parts.append(
                f"I discovered {num_patterns} transformation patterns by comparing "
                f"input-output changes across all examples."
            )
            
            # Describe key patterns
            for pattern in discovery_report.get('discovered_patterns', [])[:2]:  # Top 2
                pattern_desc = pattern.get('description', 'Unknown pattern')
                confidence = pattern.get('confidence', 0.0)
                explanation_parts.append(
                    f"- Pattern: {pattern_desc} (confidence: {confidence:.1%})"
                )
        
        # Multi-rule detection
        multi_rule_indicators = alignment_result.multi_rule_indicators
        if multi_rule_indicators:
            explanation_parts.append(
                f"I detected that this task might require multiple rules: {', '.join(multi_rule_indicators[:2])}"
            )
        
        # Hypothesis generation and validation
        num_hypotheses = len(validation_report.get('validation_results', []))
        explanation_parts.append(
            f"I generated {num_hypotheses} rule hypotheses and tested each against all examples."
        )
        
        # Best hypothesis
        if selected_hypothesis:
            rule_type = selected_hypothesis.get('rule_type', 'unknown')
            confidence = selected_hypothesis.get('confidence', 0.0)
            explanation_parts.append(
                f"My best hypothesis is a {rule_type} rule with {confidence:.1%} confidence."
            )
        
        # Conflict resolution
        total_conflicts = revision_log.get('total_conflicts_resolved', 0)
        if total_conflicts > 0:
            explanation_parts.append(
                f"I resolved {total_conflicts} conflicts by revising hypotheses that failed on some examples."
            )
        
        # Final reasoning
        if selected_hypothesis:
            explanation_parts.append(
                "I applied this rule to the test input to generate my prediction."
            )
        else:
            explanation_parts.append(
                "I could not find a sufficiently confident rule to apply to the test input."
            )
        
        return " ".join(explanation_parts)
    
    def _alignment_to_dict(self, alignment_result) -> Dict[str, Any]:
        """Convert alignment result to dictionary"""
        return {
            "consistent_changes": alignment_result.consistent_changes,
            "anomalies": alignment_result.anomalies,
            "pattern_clusters": alignment_result.pattern_clusters,
            "alignment_confidence": alignment_result.alignment_confidence,
            "multi_rule_indicators": alignment_result.multi_rule_indicators
        }
    
    def _hypothesis_to_dict(self, hypothesis: RuleHypothesis) -> Dict[str, Any]:
        """Convert RuleHypothesis to dictionary"""
        return {
            "hypothesis_id": hypothesis.hypothesis_id,
            "rule_type": hypothesis.rule_type,
            "conditions": hypothesis.conditions,
            "actions": hypothesis.actions,
            "confidence": hypothesis.confidence,
            "evidence": hypothesis.evidence
        }
    
    def _learn_from_result(self, result: DemonstrationDrivenResult):
        """Learn from the solving result to improve future performance"""
        
        self.solved_tasks.append({
            "task_id": result.task_id,
            "success": result.success,
            "confidence": result.confidence,
            "processing_time": result.processing_time,
            "patterns_discovered": len(result.rule_discovery_report.get('discovered_patterns', [])),
            "hypotheses_generated": len(result.generated_hypotheses),
            "conflicts_resolved": result.revision_log.get('total_conflicts_resolved', 0)
        })
        
        # Update success rate history
        recent_successes = sum(1 for task in self.solved_tasks[-10:] if task["success"])
        current_success_rate = recent_successes / min(10, len(self.solved_tasks))
        self.success_rate_history.append(current_success_rate)
        
        # Learn successful patterns
        if result.success and result.selected_hypothesis:
            pattern_key = result.selected_hypothesis.get("rule_type", "unknown")
            if pattern_key not in self.learned_patterns:
                self.learned_patterns[pattern_key] = []
            
            self.learned_patterns[pattern_key].append({
                "task_id": result.task_id,
                "hypothesis": result.selected_hypothesis,
                "confidence": result.confidence
            })
        
        logger.debug(f"Learning update: {len(self.solved_tasks)} tasks solved, "
                    f"current success rate: {current_success_rate:.1%}")
    
    def get_learning_summary(self) -> Dict[str, Any]:
        """Get summary of learning progress"""
        
        if not self.solved_tasks:
            return {"status": "No tasks solved yet"}
        
        total_tasks = len(self.solved_tasks)
        successful_tasks = sum(1 for task in self.solved_tasks if task["success"])
        avg_confidence = sum(task["confidence"] for task in self.solved_tasks) / total_tasks
        avg_processing_time = sum(task["processing_time"] for task in self.solved_tasks) / total_tasks
        
        return {
            "total_tasks_attempted": total_tasks,
            "successful_tasks": successful_tasks,
            "overall_success_rate": successful_tasks / total_tasks,
            "average_confidence": avg_confidence,
            "average_processing_time": avg_processing_time,
            "learned_pattern_types": list(self.learned_patterns.keys()),
            "success_rate_trend": self.success_rate_history[-5:] if len(self.success_rate_history) >= 5 else self.success_rate_history
        }

def main():
    """Test the integrated demonstration-driven solver"""
    solver = DemonstrationDrivenARCSolver()
    
    # Example task with multiple demonstrations
    test_task = {
        "task_id": "demo_task",
        "train": [
            {
                'input': [[1, 0, 0], [0, 0, 0], [0, 0, 0]],
                'output': [[0, 0, 0], [0, 0, 0], [1, 0, 0]]
            },
            {
                'input': [[0, 2, 0], [0, 0, 0], [0, 0, 0]],
                'output': [[0, 0, 0], [0, 0, 0], [0, 2, 0]]
            },
            {
                'input': [[0, 0, 3], [0, 0, 0], [0, 0, 0]],
                'output': [[0, 0, 0], [0, 0, 0], [0, 0, 3]]
            }
        ],
        "test": [
            {
                'input': [[4, 0, 0], [0, 0, 0], [0, 0, 0]]
            }
        ]
    }
    
    # Solve the task
    result = solver.solve_arc_task(test_task)
    
    print("Demonstration-Driven ARC Solver Test")
    print(f"Task: {result.task_id}")
    print(f"Success: {result.success}")
    print(f"Confidence: {result.confidence:.2f}")
    print(f"Processing time: {result.processing_time:.2f}s")
    print(f"\nReasoning: {result.reasoning_explanation}")
    
    if result.predicted_output is not None:
        print(f"\nPredicted output:")
        print(result.predicted_output)
    
    # Show learning summary
    learning_summary = solver.get_learning_summary()
    print(f"\nLearning Summary:")
    for key, value in learning_summary.items():
        print(f"- {key}: {value}")

if __name__ == "__main__":
    main()
