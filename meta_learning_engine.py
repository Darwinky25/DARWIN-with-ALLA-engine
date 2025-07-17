#!/usr/bin/env python3
"""
Meta-Learning Engine - Learns how to learn ARC patterns
Implements recursive reasoning, cross-task abstraction, and meta-cognitive strategies
"""

import json
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from collections import defaultdict, Counter
import logging
from enum import Enum
import networkx as nx

logger = logging.getLogger(__name__)

class MetaCognitionLevel(Enum):
    """Levels of meta-cognitive processing"""
    SURFACE = "surface"          # Pattern matching
    STRUCTURAL = "structural"     # Relational understanding
    FUNCTIONAL = "functional"     # Purpose/goal understanding
    STRATEGIC = "strategic"       # Method selection
    REFLECTIVE = "reflective"     # Self-monitoring

@dataclass
class MetaPattern:
    """Abstract pattern that generalizes across tasks"""
    pattern_id: str
    abstraction_level: MetaCognitionLevel
    pattern_signature: str
    applicable_contexts: List[str]
    success_rate: float
    usage_count: int
    learned_from_tasks: List[str]
    transformation_type: str
    meta_rules: List[str]
    confidence: float

@dataclass
class RecursiveHypothesis:
    """Hypothesis that can be recursively refined"""
    hypothesis_id: str
    level: int  # Recursion depth
    parent_hypothesis: Optional[str]
    child_hypotheses: List[str]
    description: str
    evidence: List[str]
    confidence: float
    validation_status: str  # "pending", "confirmed", "refuted"
    refinement_history: List[str]

@dataclass
class MetaLearningInsight:
    """High-level insights about learning process"""
    insight_type: str
    description: str
    applicable_domains: List[str]
    discovery_method: str
    confidence: float
    validation_examples: List[str]
    meta_knowledge: Dict[str, Any]

class MetaLearningEngine:
    """Advanced meta-learning engine for ARC pattern discovery"""
    
    def __init__(self):
        self.meta_patterns: Dict[str, MetaPattern] = {}
        self.recursive_hypotheses: Dict[str, RecursiveHypothesis] = {}
        self.meta_insights: List[MetaLearningInsight] = []
        self.concept_hierarchy = nx.DiGraph()
        self.learning_strategies: Dict[str, Any] = {}
        self.meta_memory: Dict[str, Any] = {}
        
        # Initialize base meta-cognitive strategies
        self._initialize_meta_strategies()
        
        logger.info("🧠 Meta-Learning Engine initialized")
    
    def _initialize_meta_strategies(self):
        """Initialize fundamental meta-learning strategies"""
        self.learning_strategies = {
            "analogy_mapping": {
                "description": "Map structural similarities between tasks",
                "strength": 0.8,
                "applicable_contexts": ["spatial_reasoning", "object_transformation"]
            },
            "compositional_generalization": {
                "description": "Combine simple patterns into complex ones",
                "strength": 0.7,
                "applicable_contexts": ["multi_step_transforms", "sequential_operations"]
            },
            "causal_abstraction": {
                "description": "Abstract causal mechanisms from specific instances",
                "strength": 0.9,
                "applicable_contexts": ["cause_effect", "conditional_rules"]
            },
            "recursive_decomposition": {
                "description": "Break complex problems into recursive subproblems",
                "strength": 0.6,
                "applicable_contexts": ["nested_patterns", "fractal_structures"]
            }
        }
    
    def extract_meta_patterns(self, task_results: List[Any]) -> List[MetaPattern]:
        """Extract abstract patterns that generalize across multiple tasks"""
        logger.info("🔍 Extracting meta-patterns from task results")
        
        extracted_patterns = []
        
        # Group tasks by transformation types
        transformation_groups = defaultdict(list)
        for result in task_results:
            if result.transformation:
                t_type = result.transformation.transformation_type
                transformation_groups[t_type].append(result)
        
        # Extract patterns from each group
        for t_type, group_results in transformation_groups.items():
            if len(group_results) >= 2:  # Need multiple examples
                pattern = self._extract_pattern_from_group(t_type, group_results)
                if pattern:
                    extracted_patterns.append(pattern)
        
        # Update meta-pattern repository
        for pattern in extracted_patterns:
            self.meta_patterns[pattern.pattern_id] = pattern
        
        logger.info(f"✅ Extracted {len(extracted_patterns)} meta-patterns")
        return extracted_patterns
    
    def _extract_pattern_from_group(self, t_type: str, results: List[Any]) -> Optional[MetaPattern]:
        """Extract a meta-pattern from a group of similar transformations"""
        
        # Analyze common elements across transformations
        common_rules = []
        common_contexts = []
        success_rates = []
        
        for result in results:
            if result.transformation and result.transformation.transformation_rules:
                # Ensure transformation_rules is iterable and not just an int
                if hasattr(result.transformation.transformation_rules, '__iter__') and not isinstance(result.transformation.transformation_rules, str):
                    common_rules.extend([rule.rule_type for rule in result.transformation.transformation_rules])
                    success_rates.append(result.accuracy)
        
        if not common_rules:
            return None
        
        # Find most frequent rules
        rule_counts = Counter(common_rules)
        dominant_rules = [rule for rule, count in rule_counts.most_common(3)]
        
        # Create pattern signature
        pattern_signature = f"{t_type}::{'-'.join(sorted(dominant_rules))}"
        
        # Generate pattern ID
        pattern_id = f"meta_{hash(pattern_signature) % 10000:04d}"
        
        # Determine abstraction level
        abstraction_level = self._determine_abstraction_level(dominant_rules, results)
        
        pattern = MetaPattern(
            pattern_id=pattern_id,
            abstraction_level=abstraction_level,
            pattern_signature=pattern_signature,
            applicable_contexts=[t_type],
            success_rate=float(np.mean(success_rates)) if success_rates else 0.0,
            usage_count=len(results),
            learned_from_tasks=[r.task_id for r in results],
            transformation_type=t_type,
            meta_rules=dominant_rules,
            confidence=min(0.9, len(results) / 5.0)  # More examples = higher confidence
        )
        
        return pattern
    
    def _determine_abstraction_level(self, rules: List[str], results: List[Any]) -> MetaCognitionLevel:
        """Determine the appropriate abstraction level for a pattern"""
        
        # Simple heuristics for abstraction level
        if any("recursive" in rule or "nested" in rule for rule in rules):
            return MetaCognitionLevel.REFLECTIVE
        elif any("goal" in rule or "purpose" in rule for rule in rules):
            return MetaCognitionLevel.STRATEGIC
        elif any("function" in rule or "role" in rule for rule in rules):
            return MetaCognitionLevel.FUNCTIONAL
        elif any("relation" in rule or "connect" in rule for rule in rules):
            return MetaCognitionLevel.STRUCTURAL
        else:
            return MetaCognitionLevel.SURFACE
    
    def generate_recursive_hypotheses(self, task_result: Any, max_depth: int = 3) -> List[RecursiveHypothesis]:
        """Generate recursive hypotheses about task solution"""
        logger.debug(f"🔄 Generating recursive hypotheses for {task_result.task_id}")
        
        hypotheses = []
        
        # Start with base hypothesis
        base_hypothesis = self._create_base_hypothesis(task_result)
        hypotheses.append(base_hypothesis)
        
        # Generate recursive refinements
        current_hypotheses = [base_hypothesis]
        
        for depth in range(1, max_depth + 1):
            next_hypotheses = []
            
            for parent_hyp in current_hypotheses:
                child_hyps = self._refine_hypothesis(parent_hyp, task_result, depth)
                next_hypotheses.extend(child_hyps)
                hypotheses.extend(child_hyps)
            
            current_hypotheses = next_hypotheses
            
            # Stop if no new hypotheses generated
            if not current_hypotheses:
                break
        
        # Store hypotheses
        for hyp in hypotheses:
            self.recursive_hypotheses[hyp.hypothesis_id] = hyp
        
        return hypotheses
    
    def _create_base_hypothesis(self, task_result: Any) -> RecursiveHypothesis:
        """Create the base hypothesis for a task"""
        
        if task_result.transformation:
            description = f"Task follows {task_result.transformation.transformation_type} pattern"
            evidence = [rule.description for rule in task_result.transformation.transformation_rules]
        else:
            description = "Task requires pattern identification"
            evidence = ["No clear transformation identified"]
        
        hypothesis_id = f"{task_result.task_id}_base_hyp"
        
        return RecursiveHypothesis(
            hypothesis_id=hypothesis_id,
            level=0,
            parent_hypothesis=None,
            child_hypotheses=[],
            description=description,
            evidence=evidence,
            confidence=task_result.confidence if hasattr(task_result, 'confidence') else 0.5,
            validation_status="pending",
            refinement_history=[]
        )
    
    def _refine_hypothesis(self, parent_hyp: RecursiveHypothesis, 
                          task_result: Any, depth: int) -> List[RecursiveHypothesis]:
        """Refine a hypothesis into more specific child hypotheses"""
        
        child_hypotheses = []
        
        # Generate refinements based on different aspects
        refinement_aspects = [
            "spatial_reasoning",
            "temporal_sequence", 
            "causal_mechanism",
            "compositional_structure"
        ]
        
        for aspect in refinement_aspects:
            child_hyp = self._create_aspect_hypothesis(parent_hyp, aspect, task_result, depth)
            if child_hyp:
                child_hypotheses.append(child_hyp)
                parent_hyp.child_hypotheses.append(child_hyp.hypothesis_id)
        
        return child_hypotheses
    
    def _create_aspect_hypothesis(self, parent_hyp: RecursiveHypothesis, 
                                 aspect: str, task_result: Any, depth: int) -> Optional[RecursiveHypothesis]:
        """Create a hypothesis focused on a specific aspect"""
        
        aspect_descriptions = {
            "spatial_reasoning": f"Spatial transformation involving {aspect}",
            "temporal_sequence": f"Sequential operation with {aspect} dependencies",
            "causal_mechanism": f"Causal chain driven by {aspect}",
            "compositional_structure": f"Compositional pattern with {aspect} elements"
        }
        
        if aspect not in aspect_descriptions:
            return None
        
        hypothesis_id = f"{parent_hyp.hypothesis_id}_{aspect}_{depth}"
        
        return RecursiveHypothesis(
            hypothesis_id=hypothesis_id,
            level=depth,
            parent_hypothesis=parent_hyp.hypothesis_id,
            child_hypotheses=[],
            description=aspect_descriptions[aspect],
            evidence=[f"Derived from {parent_hyp.description}"],
            confidence=parent_hyp.confidence * 0.8,  # Reduced confidence for deeper hypotheses
            validation_status="pending",
            refinement_history=[]
        )
    
    def cross_task_abstraction(self, task_results: List[Any]) -> List[MetaLearningInsight]:
        """Perform cross-task abstraction to discover meta-insights"""
        logger.info("🌐 Performing cross-task abstraction")
        
        insights = []
        
        # Group tasks by various criteria
        groupings = {
            "by_success": self._group_by_success(task_results),
            "by_transformation": self._group_by_transformation(task_results),
            "by_complexity": self._group_by_complexity(task_results)
        }
        
        # Extract insights from each grouping
        for grouping_type, groups in groupings.items():
            group_insights = self._extract_insights_from_grouping(grouping_type, groups)
            insights.extend(group_insights)
        
        # Find universal patterns
        universal_insights = self._find_universal_patterns(task_results)
        insights.extend(universal_insights)
        
        # Store insights
        self.meta_insights.extend(insights)
        
        logger.info(f"✅ Discovered {len(insights)} meta-learning insights")
        return insights
    
    def _group_by_success(self, task_results: List[Any]) -> Dict[str, List[Any]]:
        """Group tasks by success rate"""
        groups = {"high_success": [], "medium_success": [], "low_success": []}
        
        for result in task_results:
            accuracy = getattr(result, 'accuracy', 0.0)
            if accuracy >= 0.8:
                groups["high_success"].append(result)
            elif accuracy >= 0.5:
                groups["medium_success"].append(result)
            else:
                groups["low_success"].append(result)
        
        return groups
    
    def _group_by_transformation(self, task_results: List[Any]) -> Dict[str, List[Any]]:
        """Group tasks by transformation type"""
        groups = defaultdict(list)
        
        for result in task_results:
            if result.transformation:
                t_type = result.transformation.transformation_type
                groups[t_type].append(result)
            else:
                groups["unknown"].append(result)
        
        return dict(groups)
    
    def _group_by_complexity(self, task_results: List[Any]) -> Dict[str, List[Any]]:
        """Group tasks by complexity level"""
        groups = {"simple": [], "moderate": [], "complex": []}
        
        for result in task_results:
            # Estimate complexity based on processing time and transformation rules
            complexity_score = 0
            
            if hasattr(result, 'processing_time'):
                complexity_score += min(result.processing_time / 10.0, 1.0)
            
            if result.transformation and result.transformation.transformation_rules and hasattr(result.transformation.transformation_rules, '__len__'):
                complexity_score += len(result.transformation.transformation_rules) / 10.0
            
            if complexity_score < 0.3:
                groups["simple"].append(result)
            elif complexity_score < 0.7:
                groups["moderate"].append(result)
            else:
                groups["complex"].append(result)
        
        return groups
    
    def _extract_insights_from_grouping(self, grouping_type: str, 
                                       groups: Dict[str, List[Any]]) -> List[MetaLearningInsight]:
        """Extract insights from a specific grouping"""
        insights = []
        
        for group_name, group_results in groups.items():
            if len(group_results) < 2:
                continue
            
            # Analyze common characteristics
            common_features = self._find_common_features(group_results)
            
            if common_features:
                insight = MetaLearningInsight(
                    insight_type=f"{grouping_type}_{group_name}",
                    description=f"Tasks in {group_name} group share: {', '.join(common_features)}",
                    applicable_domains=[grouping_type],
                    discovery_method="cross_task_analysis",
                    confidence=min(0.9, len(group_results) / 10.0),
                    validation_examples=[r.task_id for r in group_results[:3]],
                    meta_knowledge={"features": common_features, "group_size": len(group_results)}
                )
                insights.append(insight)
        
        return insights
    
    def _find_common_features(self, results: List[Any]) -> List[str]:
        """Find common features across a group of results"""
        features = []
        
        # Check for common transformation types
        transformation_types = [r.transformation.transformation_type 
                               for r in results if r.transformation]
        if transformation_types:
            most_common_type = Counter(transformation_types).most_common(1)[0]
            if most_common_type[1] >= len(results) * 0.7:  # 70% prevalence
                features.append(f"transformation_type:{most_common_type[0]}")
        
        # Check for common accuracy ranges
        accuracies = [getattr(r, 'accuracy', 0.0) for r in results]
        if accuracies:
            avg_accuracy = np.mean(accuracies)
            features.append(f"avg_accuracy:{avg_accuracy:.2f}")
        
        # Check for common confidence levels
        confidences = [getattr(r, 'confidence', 0.0) for r in results]
        if confidences:
            avg_confidence = np.mean(confidences)
            features.append(f"avg_confidence:{avg_confidence:.2f}")
        
        return features
    
    def _find_universal_patterns(self, task_results: List[Any]) -> List[MetaLearningInsight]:
        """Find patterns that apply across all or most tasks"""
        insights = []
        
        if not task_results:
            return insights
        
        # Universal insight: relationship between confidence and accuracy
        confidences = [getattr(r, 'confidence', 0.0) for r in task_results]
        accuracies = [getattr(r, 'accuracy', 0.0) for r in task_results]
        
        if confidences and accuracies:
            correlation = np.corrcoef(confidences, accuracies)[0, 1]
            if not np.isnan(correlation) and abs(correlation) > 0.5:
                insight = MetaLearningInsight(
                    insight_type="universal_confidence_accuracy",
                    description=f"Confidence and accuracy show {correlation:.2f} correlation",
                    applicable_domains=["all_tasks"],
                    discovery_method="statistical_analysis",
                    confidence=min(0.8, abs(correlation)),
                    validation_examples=[r.task_id for r in task_results[:5]],
                    meta_knowledge={"correlation": correlation, "sample_size": len(task_results)}
                )
                insights.append(insight)
        
        return insights
    
    def evolve_learning_strategies(self, task_results: List[Any]) -> Dict[str, Any]:
        """Evolve and improve learning strategies based on results"""
        logger.info("Evolving learning strategies")
        
        strategy_performance = {}
        
        # Evaluate current strategies
        for strategy_name, strategy in self.learning_strategies.items():
            performance = self._evaluate_strategy_performance(strategy_name, task_results)
            strategy_performance[strategy_name] = performance
            
            # Update strategy strength based on performance
            strategy["strength"] = min(1.0, strategy["strength"] * (1 + performance / 10))
        
        # Generate new strategies if needed
        if max(strategy_performance.values()) < 0.6:  # If all strategies performing poorly
            new_strategies = self._generate_new_strategies(task_results)
            self.learning_strategies.update(new_strategies)
        
        logger.info(f"Strategy evolution complete. Best performance: {max(strategy_performance.values()):.2f}")
        return strategy_performance
    
    def _evaluate_strategy_performance(self, strategy_name: str, task_results: List[Any]) -> float:
        """Evaluate how well a strategy performs"""
        
        relevant_results = []
        strategy = self.learning_strategies[strategy_name]
        
        for result in task_results:
            if result.transformation:
                t_type = result.transformation.transformation_type
                if t_type in strategy.get("applicable_contexts", []):
                    relevant_results.append(result)
        
        if not relevant_results:
            return 0.5  # Neutral performance if no relevant tasks
        
        # Calculate average accuracy for relevant tasks
        accuracies = [getattr(r, 'accuracy', 0.0) for r in relevant_results]
        return float(np.mean(accuracies)) if accuracies else 0.5
    
    def _generate_new_strategies(self, task_results: List[Any]) -> Dict[str, Any]:
        """Generate new learning strategies based on task analysis"""
        new_strategies = {}
        
        # Analyze failure patterns to create new strategies
        failed_results = [r for r in task_results if getattr(r, 'success', False) == False]
        
        if failed_results:
            # Strategy for handling failed pattern types
            failed_types = [r.transformation.transformation_type 
                           for r in failed_results if r.transformation]
            
            if failed_types:
                most_failed_type = Counter(failed_types).most_common(1)[0][0]
                
                new_strategies[f"adaptive_{most_failed_type}"] = {
                    "description": f"Adaptive strategy for {most_failed_type} patterns",
                    "strength": 0.5,
                    "applicable_contexts": [most_failed_type],
                    "generated": True
                }
        
        return new_strategies
    
    def get_best_strategy_for_task(self, task_context: Dict[str, Any]) -> str:
        """Select the best learning strategy for a given task context"""
        
        task_type = task_context.get("transformation_type", "unknown")
        
        # Find strategies applicable to this task type
        applicable_strategies = {}
        for name, strategy in self.learning_strategies.items():
            if task_type in strategy.get("applicable_contexts", []):
                applicable_strategies[name] = strategy["strength"]
        
        if applicable_strategies:
            # Return strategy with highest strength
            return max(applicable_strategies.items(), key=lambda x: x[1])[0] if applicable_strategies else "pattern_recognition"
        else:
            # Return most generally effective strategy
            return max(self.learning_strategies, 
                      key=lambda x: self.learning_strategies[x]["strength"])
    
    def generate_meta_knowledge_summary(self) -> Dict[str, Any]:
        """Generate a comprehensive summary of meta-knowledge"""
        
        summary = {
            "meta_patterns": {
                "total_patterns": len(self.meta_patterns),
                "abstraction_levels": Counter([p.abstraction_level.value for p in self.meta_patterns.values()]),
                "pattern_types": Counter([p.transformation_type for p in self.meta_patterns.values()]),
                "average_confidence": np.mean([p.confidence for p in self.meta_patterns.values()]) if self.meta_patterns else 0.0
            },
            "recursive_hypotheses": {
                "total_hypotheses": len(self.recursive_hypotheses),
                "max_depth": max([h.level for h in self.recursive_hypotheses.values()]) if self.recursive_hypotheses else 0,
                "validation_status": Counter([h.validation_status for h in self.recursive_hypotheses.values()]),
                "average_confidence": np.mean([h.confidence for h in self.recursive_hypotheses.values()]) if self.recursive_hypotheses else 0.0
            },
            "meta_insights": {
                "total_insights": len(self.meta_insights),
                "insight_types": Counter([i.insight_type for i in self.meta_insights]),
                "discovery_methods": Counter([i.discovery_method for i in self.meta_insights]),
                "average_confidence": np.mean([i.confidence for i in self.meta_insights]) if self.meta_insights else 0.0
            },
            "learning_strategies": {
                "total_strategies": len(self.learning_strategies),
                "strategy_strengths": {name: s["strength"] for name, s in self.learning_strategies.items()},
                "generated_strategies": sum(1 for s in self.learning_strategies.values() if s.get("generated", False))
            }
        }
        
        return summary
