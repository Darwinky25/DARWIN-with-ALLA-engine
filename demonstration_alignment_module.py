#!/usr/bin/env python3
"""
Multiple Demonstration Alignment Module
"Bandingkan semua contoh, cari perubahan yang konsisten dan anomali → indikasi multiple rules"
Aligns multiple examples to find consistent changes and detect rule anomalies
"""

import numpy as np
import json
import logging
from typing import Dict, List, Tuple, Any, Optional, Set
from dataclasses import dataclass, field
from collections import defaultdict, Counter
from datetime import datetime
import itertools

logger = logging.getLogger(__name__)

@dataclass
class DemonstrationAlignment:
    """Alignment analysis between demonstrations"""
    consistent_changes: List[Dict[str, Any]] = field(default_factory=list)
    anomalies: List[Dict[str, Any]] = field(default_factory=list)
    pattern_clusters: List[List[int]] = field(default_factory=list)  # Groups of examples with same pattern
    alignment_confidence: float = 0.0
    multi_rule_indicators: List[str] = field(default_factory=list)

@dataclass
class ConsistentChange:
    """A change that's consistent across multiple examples"""
    change_type: str  # "position", "color", "shape", "creation", "removal"
    pattern_description: str
    examples_supporting: List[int]
    consistency_score: float
    change_parameters: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RuleAnomaly:
    """An anomaly that suggests additional or different rules"""
    anomaly_type: str  # "outlier_example", "partial_consistency", "context_dependent"
    affected_examples: List[int]
    description: str
    potential_additional_rule: Optional[str] = None
    confidence: float = 0.0

class CrossExampleComparator:
    """Compares transformations across all example pairs"""
    
    def compare_all_examples(self, examples: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compare transformations across all example pairs"""
        
        logger.debug(f"Comparing {len(examples)} examples pairwise")
        
        comparison_matrix = {}
        transformation_features = []
        
        # Extract transformation features for each example
        for i, example in enumerate(examples):
            features = self._extract_transformation_features(example)
            transformation_features.append(features)
        
        # Compare each pair of examples
        for i in range(len(examples)):
            for j in range(i + 1, len(examples)):
                similarity = self._compare_transformation_features(
                    transformation_features[i], 
                    transformation_features[j]
                )
                comparison_matrix[(i, j)] = similarity
        
        return {
            "transformation_features": transformation_features,
            "pairwise_similarities": comparison_matrix,
            "average_similarity": sum(comparison_matrix.values()) / len(comparison_matrix) if comparison_matrix else 0.0
        }
    
    def _extract_transformation_features(self, example: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key transformation features from an example"""
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        
        features = {
            # Size changes
            "input_shape": input_grid.shape,
            "output_shape": output_grid.shape,
            "size_change": (output_grid.shape[0] - input_grid.shape[0], 
                           output_grid.shape[1] - input_grid.shape[1]),
            
            # Color changes
            "input_colors": set(np.unique(input_grid)),
            "output_colors": set(np.unique(output_grid)),
            "colors_added": set(np.unique(output_grid)) - set(np.unique(input_grid)),
            "colors_removed": set(np.unique(input_grid)) - set(np.unique(output_grid)),
            
            # Object count changes
            "input_object_count": len(np.unique(input_grid[input_grid != 0])),
            "output_object_count": len(np.unique(output_grid[output_grid != 0])),
            
            # Spatial properties
            "input_density": np.count_nonzero(input_grid) / input_grid.size,
            "output_density": np.count_nonzero(output_grid) / output_grid.size,
            
            # Pattern properties
            "input_symmetry": self._analyze_symmetry(input_grid),
            "output_symmetry": self._analyze_symmetry(output_grid),
            
            # Movement vectors (if applicable)
            "apparent_movement": self._detect_apparent_movement(input_grid, output_grid)
        }
        
        return features
    
    def _analyze_symmetry(self, grid: np.ndarray) -> Dict[str, bool]:
        """Analyze symmetry properties of a grid"""
        return {
            "horizontal": np.array_equal(grid, np.flipud(grid)),
            "vertical": np.array_equal(grid, np.fliplr(grid)),
            "rotational": np.array_equal(grid, np.rot90(grid, 2))
        }
    
    def _detect_apparent_movement(self, input_grid: np.ndarray, 
                                 output_grid: np.ndarray) -> Optional[Tuple[int, int]]:
        """Detect apparent movement vector between input and output"""
        if input_grid.shape != output_grid.shape:
            return None
        
        # Find center of mass for non-zero cells
        def center_of_mass(grid):
            nonzero_pos = np.where(grid != 0)
            if len(nonzero_pos[0]) == 0:
                return None
            return (np.mean(nonzero_pos[0]), np.mean(nonzero_pos[1]))
        
        input_com = center_of_mass(input_grid)
        output_com = center_of_mass(output_grid)
        
        if input_com is None or output_com is None:
            return None
        
        movement = (output_com[0] - input_com[0], output_com[1] - input_com[1])
        
        # Round to nearest integer for cleaner movement vectors
        return (round(movement[0]), round(movement[1]))
    
    def _compare_transformation_features(self, features1: Dict[str, Any], 
                                       features2: Dict[str, Any]) -> float:
        """Compare transformation features between two examples"""
        similarity_score = 0.0
        total_comparisons = 0
        
        # Size change similarity
        if features1["size_change"] == features2["size_change"]:
            similarity_score += 1.0
        total_comparisons += 1
        
        # Color change similarity
        colors_added_sim = len(features1["colors_added"] & features2["colors_added"]) / max(1, len(features1["colors_added"] | features2["colors_added"]))
        colors_removed_sim = len(features1["colors_removed"] & features2["colors_removed"]) / max(1, len(features1["colors_removed"] | features2["colors_removed"]))
        similarity_score += (colors_added_sim + colors_removed_sim) / 2
        total_comparisons += 1
        
        # Movement similarity
        if features1["apparent_movement"] == features2["apparent_movement"]:
            similarity_score += 1.0
        total_comparisons += 1
        
        # Symmetry similarity
        sym1 = features1["input_symmetry"]
        sym2 = features2["input_symmetry"]
        symmetry_matches = sum(1 for key in sym1 if sym1[key] == sym2[key])
        similarity_score += symmetry_matches / len(sym1)
        total_comparisons += 1
        
        return similarity_score / total_comparisons if total_comparisons > 0 else 0.0

class ConsistencyDetector:
    """Detects consistent patterns across demonstrations"""
    
    def detect_consistent_changes(self, comparison_data: Dict[str, Any]) -> List[ConsistentChange]:
        """Detect changes that are consistent across multiple examples"""
        
        features = comparison_data["transformation_features"]
        consistent_changes = []
        
        # Check size changes
        size_changes = [f["size_change"] for f in features]
        size_change_groups = self._group_by_value(size_changes)
        
        for size_change, examples in size_change_groups.items():
            if len(examples) >= 2:  # Consistent across at least 2 examples
                consistent_changes.append(ConsistentChange(
                    change_type="size",
                    pattern_description=f"Size change by {size_change}",
                    examples_supporting=examples,
                    consistency_score=len(examples) / len(features),
                    change_parameters={"size_delta": size_change}
                ))
        
        # Check movement patterns
        movements = [f["apparent_movement"] for f in features if f["apparent_movement"] is not None]
        if movements:
            movement_groups = self._group_by_value(movements)
            
            for movement, examples in movement_groups.items():
                if len(examples) >= 2:
                    consistent_changes.append(ConsistentChange(
                        change_type="movement",
                        pattern_description=f"Movement by vector {movement}",
                        examples_supporting=examples,
                        consistency_score=len(examples) / len(features),
                        change_parameters={"movement_vector": movement}
                    ))
        
        # Check color addition patterns
        color_additions = [tuple(sorted(f["colors_added"])) for f in features]
        color_add_groups = self._group_by_value(color_additions)
        
        for colors_added, examples in color_add_groups.items():
            if len(examples) >= 2 and colors_added:  # Non-empty color additions
                consistent_changes.append(ConsistentChange(
                    change_type="color_addition",
                    pattern_description=f"Colors {colors_added} added",
                    examples_supporting=examples,
                    consistency_score=len(examples) / len(features),
                    change_parameters={"colors_added": list(colors_added)}
                ))
        
        # Check color removal patterns
        color_removals = [tuple(sorted(f["colors_removed"])) for f in features]
        color_remove_groups = self._group_by_value(color_removals)
        
        for colors_removed, examples in color_remove_groups.items():
            if len(examples) >= 2 and colors_removed:  # Non-empty color removals
                consistent_changes.append(ConsistentChange(
                    change_type="color_removal",
                    pattern_description=f"Colors {colors_removed} removed",
                    examples_supporting=examples,
                    consistency_score=len(examples) / len(features),
                    change_parameters={"colors_removed": list(colors_removed)}
                ))
        
        return consistent_changes
    
    def _group_by_value(self, values: List[Any]) -> Dict[Any, List[int]]:
        """Group example indices by their values"""
        groups = defaultdict(list)
        for i, value in enumerate(values):
            groups[value].append(i)
        return dict(groups)

class AnomalyDetector:
    """Detects anomalies that suggest multiple rules or special cases"""
    
    def detect_anomalies(self, comparison_data: Dict[str, Any], 
                        consistent_changes: List[ConsistentChange]) -> List[RuleAnomaly]:
        """Detect anomalies in the demonstrations"""
        
        features = comparison_data["transformation_features"]
        similarities = comparison_data["pairwise_similarities"]
        anomalies = []
        
        # Detect outlier examples (low similarity to all others)
        outliers = self._detect_outlier_examples(similarities, len(features))
        for outlier_idx in outliers:
            anomalies.append(RuleAnomaly(
                anomaly_type="outlier_example",
                affected_examples=[outlier_idx],
                description=f"Example {outlier_idx} is significantly different from others",
                potential_additional_rule="Context-dependent transformation",
                confidence=0.8
            ))
        
        # Detect partial consistency (some examples follow a pattern, others don't)
        partial_anomalies = self._detect_partial_consistency_anomalies(consistent_changes, len(features))
        anomalies.extend(partial_anomalies)
        
        # Detect context-dependent changes
        context_anomalies = self._detect_context_dependent_anomalies(features)
        anomalies.extend(context_anomalies)
        
        return anomalies
    
    def _detect_outlier_examples(self, similarities: Dict[Tuple[int, int], float], 
                                num_examples: int) -> List[int]:
        """Detect examples that are outliers (low similarity to all others)"""
        # Calculate average similarity for each example
        example_avg_similarities = defaultdict(list)
        
        for (i, j), similarity in similarities.items():
            example_avg_similarities[i].append(similarity)
            example_avg_similarities[j].append(similarity)
        
        outliers = []
        overall_avg = sum(similarities.values()) / len(similarities) if similarities else 0.0
        
        for example_idx in range(num_examples):
            if example_idx in example_avg_similarities:
                avg_sim = sum(example_avg_similarities[example_idx]) / len(example_avg_similarities[example_idx])
                
                # If this example's average similarity is much lower than overall average
                if avg_sim < overall_avg * 0.6:  # 60% threshold
                    outliers.append(example_idx)
        
        return outliers
    
    def _detect_partial_consistency_anomalies(self, consistent_changes: List[ConsistentChange], 
                                            num_examples: int) -> List[RuleAnomaly]:
        """Detect cases where some examples follow a pattern, others don't"""
        anomalies = []
        
        for change in consistent_changes:
            # If a pattern applies to some but not all examples
            if 0.3 <= change.consistency_score <= 0.8:  # Partial consistency
                non_conforming = []
                for i in range(num_examples):
                    if i not in change.examples_supporting:
                        non_conforming.append(i)
                
                anomalies.append(RuleAnomaly(
                    anomaly_type="partial_consistency",
                    affected_examples=non_conforming,
                    description=f"Examples {non_conforming} don't follow pattern: {change.pattern_description}",
                    potential_additional_rule=f"Alternative rule for {change.change_type}",
                    confidence=1.0 - change.consistency_score
                ))
        
        return anomalies
    
    def _detect_context_dependent_anomalies(self, features: List[Dict[str, Any]]) -> List[RuleAnomaly]:
        """Detect changes that seem to depend on input context"""
        anomalies = []
        
        # Check if color changes depend on input colors
        color_change_patterns = defaultdict(list)
        
        for i, feature in enumerate(features):
            input_colors = feature["input_colors"]
            colors_added = feature["colors_added"]
            colors_removed = feature["colors_removed"]
            
            # Group by input color set
            color_change_patterns[tuple(sorted(input_colors))].append({
                "example_idx": i,
                "colors_added": colors_added,
                "colors_removed": colors_removed
            })
        
        # Check if different input color sets lead to different transformations
        for input_color_set, changes in color_change_patterns.items():
            if len(changes) >= 2:
                # Check if all changes are the same
                first_change = changes[0]
                all_same = all(
                    c["colors_added"] == first_change["colors_added"] and 
                    c["colors_removed"] == first_change["colors_removed"]
                    for c in changes
                )
                
                if not all_same:
                    affected_examples = [c["example_idx"] for c in changes]
                    anomalies.append(RuleAnomaly(
                        anomaly_type="context_dependent",
                        affected_examples=affected_examples,
                        description=f"Color transformations vary for input colors {input_color_set}",
                        potential_additional_rule="Context-sensitive color mapping",
                        confidence=0.7
                    ))
        
        return anomalies

class RuleClusterer:
    """Clusters examples by their transformation patterns to handle multi-rule tasks"""
    
    def cluster_by_rules(self, comparison_data: Dict[str, Any], 
                        consistent_changes: List[ConsistentChange]) -> List[List[int]]:
        """Cluster examples into groups that likely follow the same rule"""
        
        features = comparison_data["transformation_features"]
        similarities = comparison_data["pairwise_similarities"]
        
        # Start with high-similarity clusters
        clusters = []
        used_examples = set()
        
        # Create clusters based on similarity threshold
        similarity_threshold = 0.8
        
        for (i, j), similarity in similarities.items():
            if similarity >= similarity_threshold and i not in used_examples and j not in used_examples:
                # Start a new cluster
                cluster = [i, j]
                used_examples.add(i)
                used_examples.add(j)
                
                # Try to add more examples to this cluster
                for k in range(len(features)):
                    if k not in used_examples:
                        # Check similarity to all examples in cluster
                        cluster_similarities = []
                        for cluster_member in cluster:
                            if (k, cluster_member) in similarities:
                                cluster_similarities.append(similarities[(k, cluster_member)])
                            elif (cluster_member, k) in similarities:
                                cluster_similarities.append(similarities[(cluster_member, k)])
                        
                        if cluster_similarities and min(cluster_similarities) >= similarity_threshold:
                            cluster.append(k)
                            used_examples.add(k)
                
                clusters.append(cluster)
        
        # Add remaining examples as individual clusters
        for i in range(len(features)):
            if i not in used_examples:
                clusters.append([i])
        
        # Refine clusters based on consistent changes
        refined_clusters = self._refine_clusters_with_consistent_changes(clusters, consistent_changes)
        
        return refined_clusters
    
    def _refine_clusters_with_consistent_changes(self, initial_clusters: List[List[int]], 
                                               consistent_changes: List[ConsistentChange]) -> List[List[int]]:
        """Refine clusters using consistent change patterns"""
        
        # For each consistent change, check if it suggests merging or splitting clusters
        refined_clusters = initial_clusters.copy()
        
        for change in consistent_changes:
            if change.consistency_score >= 0.8:  # High consistency
                # Examples supporting this change should be in the same cluster
                supporting_examples = set(change.examples_supporting)
                
                # Find which clusters contain these examples
                affected_clusters = []
                for i, cluster in enumerate(refined_clusters):
                    if any(ex in supporting_examples for ex in cluster):
                        affected_clusters.append(i)
                
                # If examples are in different clusters but should be together, merge them
                if len(affected_clusters) > 1:
                    merged_cluster = []
                    for cluster_idx in sorted(affected_clusters, reverse=True):
                        merged_cluster.extend(refined_clusters.pop(cluster_idx))
                    
                    refined_clusters.append(merged_cluster)
        
        return refined_clusters

class MultipledemonstrationAlignmentModule:
    """Main module that coordinates all alignment and anomaly detection"""
    
    def __init__(self):
        self.comparator = CrossExampleComparator()
        self.consistency_detector = ConsistencyDetector()
        self.anomaly_detector = AnomalyDetector()
        self.rule_clusterer = RuleClusterer()
    
    def align_demonstrations(self, examples: List[Dict[str, Any]]) -> DemonstrationAlignment:
        """Main method: align multiple demonstrations and detect patterns/anomalies"""
        
        logger.info(f"Aligning {len(examples)} demonstrations")
        
        # Step 1: Compare all examples
        comparison_data = self.comparator.compare_all_examples(examples)
        
        # Step 2: Detect consistent changes
        consistent_changes = self.consistency_detector.detect_consistent_changes(comparison_data)
        
        # Step 3: Detect anomalies
        anomalies = self.anomaly_detector.detect_anomalies(comparison_data, consistent_changes)
        
        # Step 4: Cluster examples by rules
        pattern_clusters = self.rule_clusterer.cluster_by_rules(comparison_data, consistent_changes)
        
        # Step 5: Calculate alignment confidence
        alignment_confidence = self._calculate_alignment_confidence(
            comparison_data, consistent_changes, anomalies
        )
        
        # Step 6: Identify multi-rule indicators
        multi_rule_indicators = self._identify_multi_rule_indicators(
            consistent_changes, anomalies, pattern_clusters
        )
        
        alignment = DemonstrationAlignment(
            consistent_changes=[self._change_to_dict(c) for c in consistent_changes],
            anomalies=[self._anomaly_to_dict(a) for a in anomalies],
            pattern_clusters=pattern_clusters,
            alignment_confidence=alignment_confidence,
            multi_rule_indicators=multi_rule_indicators
        )
        
        logger.info(f"Alignment complete: {len(consistent_changes)} consistent patterns, "
                   f"{len(anomalies)} anomalies, {len(pattern_clusters)} rule clusters")
        
        return alignment
    
    def _calculate_alignment_confidence(self, comparison_data: Dict[str, Any], 
                                      consistent_changes: List[ConsistentChange], 
                                      anomalies: List[RuleAnomaly]) -> float:
        """Calculate confidence in the demonstration alignment"""
        
        # Base confidence from average similarity
        base_confidence = comparison_data["average_similarity"]
        
        # Boost confidence for high-consistency patterns
        consistency_boost = 0.0
        if consistent_changes:
            avg_consistency = sum(c.consistency_score for c in consistent_changes) / len(consistent_changes)
            consistency_boost = avg_consistency * 0.3
        
        # Reduce confidence for anomalies
        anomaly_penalty = len(anomalies) * 0.1
        
        final_confidence = min(1.0, base_confidence + consistency_boost - anomaly_penalty)
        return max(0.0, final_confidence)
    
    def _identify_multi_rule_indicators(self, consistent_changes: List[ConsistentChange], 
                                      anomalies: List[RuleAnomaly], 
                                      pattern_clusters: List[List[int]]) -> List[str]:
        """Identify indicators that suggest multiple rules are needed"""
        indicators = []
        
        # Multiple clusters suggest multiple rules
        if len(pattern_clusters) > 1:
            indicators.append(f"Multiple pattern clusters ({len(pattern_clusters)}) suggest different rules")
        
        # Partial consistency suggests additional rules
        partial_consistency_anomalies = [a for a in anomalies if a.anomaly_type == "partial_consistency"]
        if partial_consistency_anomalies:
            indicators.append(f"Partial consistency in {len(partial_consistency_anomalies)} patterns")
        
        # Context-dependent changes suggest conditional rules
        context_anomalies = [a for a in anomalies if a.anomaly_type == "context_dependent"]
        if context_anomalies:
            indicators.append(f"Context-dependent behavior in {len(context_anomalies)} cases")
        
        # Outliers suggest special case rules
        outlier_anomalies = [a for a in anomalies if a.anomaly_type == "outlier_example"]
        if outlier_anomalies:
            indicators.append(f"Outlier examples ({len(outlier_anomalies)}) may need special rules")
        
        # Low overall consistency suggests complex rule interactions
        if consistent_changes:
            avg_consistency = sum(c.consistency_score for c in consistent_changes) / len(consistent_changes)
            if avg_consistency < 0.6:
                indicators.append("Low average pattern consistency suggests complex rule interactions")
        
        return indicators
    
    def _change_to_dict(self, change: ConsistentChange) -> Dict[str, Any]:
        """Convert ConsistentChange to dictionary"""
        return {
            "change_type": change.change_type,
            "pattern_description": change.pattern_description,
            "examples_supporting": change.examples_supporting,
            "consistency_score": change.consistency_score,
            "change_parameters": change.change_parameters
        }
    
    def _anomaly_to_dict(self, anomaly: RuleAnomaly) -> Dict[str, Any]:
        """Convert RuleAnomaly to dictionary"""
        return {
            "anomaly_type": anomaly.anomaly_type,
            "affected_examples": anomaly.affected_examples,
            "description": anomaly.description,
            "potential_additional_rule": anomaly.potential_additional_rule,
            "confidence": anomaly.confidence
        }

def main():
    """Test the Multiple Demonstration Alignment Module"""
    module = MultipledemonstrationAlignmentModule()
    
    # Example with consistent pattern
    test_examples = [
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
        },
        # Anomaly: different pattern
        {
            'input': [[1, 1, 0], [0, 0, 0], [0, 0, 0]],
            'output': [[2, 2, 0], [0, 0, 0], [0, 0, 0]]  # Color change instead of movement
        }
    ]
    
    alignment = module.align_demonstrations(test_examples)
    
    print("Multiple Demonstration Alignment Module Test")
    print(f"Alignment confidence: {alignment.alignment_confidence:.2f}")
    print(f"Found {len(alignment.consistent_changes)} consistent patterns")
    print(f"Found {len(alignment.anomalies)} anomalies")
    print(f"Pattern clusters: {alignment.pattern_clusters}")
    
    if alignment.multi_rule_indicators:
        print("Multi-rule indicators:")
        for indicator in alignment.multi_rule_indicators:
            print(f"- {indicator}")

if __name__ == "__main__":
    main()
