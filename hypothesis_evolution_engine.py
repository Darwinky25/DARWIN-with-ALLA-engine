#!/usr/bin/env python3
"""
Hypothesis Evolution and Strategy Generation System
Generates, tests, and evolves hypotheses about ARC task solutions using genetic algorithms and reinforcement learning
"""

import json
import numpy as np
import random
from typing import Dict, List, Any, Optional, Tuple, Set, Callable
from dataclasses import dataclass, field
from collections import defaultdict, Counter, deque
import logging
from enum import Enum
from abc import ABC, abstractmethod
import copy
import time
from scipy.stats import entropy

logger = logging.getLogger(__name__)

class HypothesisType(Enum):
    """Types of hypotheses"""
    PATTERN_RECOGNITION = "pattern_recognition"
    TRANSFORMATION_RULE = "transformation_rule"
    CAUSAL_MECHANISM = "causal_mechanism"
    SPATIAL_RELATIONSHIP = "spatial_relationship"
    TEMPORAL_SEQUENCE = "temporal_sequence"
    COMPOSITIONAL_STRUCTURE = "compositional_structure"
    META_STRATEGY = "meta_strategy"

class FitnessMetric(Enum):
    """Metrics for evaluating hypothesis fitness"""
    ACCURACY = "accuracy"
    GENERALIZABILITY = "generalizability"  
    SIMPLICITY = "simplicity"
    CONSISTENCY = "consistency"
    NOVELTY = "novelty"
    EXPLANATORY_POWER = "explanatory_power"

@dataclass
class EvolvableHypothesis:
    """A hypothesis that can evolve through genetic operations"""
    hypothesis_id: str
    hypothesis_type: HypothesisType
    generation: int
    parent_ids: List[str]
    
    # Core hypothesis content
    description: str
    prediction_function: Optional[Callable]
    parameters: Dict[str, Any]
    rules: List[str]
    conditions: List[str]
    
    # Fitness metrics
    fitness_scores: Dict[FitnessMetric, float]
    overall_fitness: float
    
    # Evolution tracking
    mutations: List[str]
    crossover_history: List[str]
    test_results: List[Dict[str, Any]]
    
    # Validation
    validation_examples: List[str]
    success_rate: float
    confidence: float
    
    # Meta-information
    creation_time: float
    last_update_time: float
    usage_count: int

@dataclass
class EvolutionOperator:
    """Genetic operator for hypothesis evolution"""
    operator_name: str
    operator_type: str  # "mutation", "crossover", "selection"
    probability: float
    strength: float
    applicable_types: List[HypothesisType]
    description: str

@dataclass
class StrategyGenome:
    """Genetic representation of a problem-solving strategy"""
    genome_id: str
    strategy_components: List[str]
    component_weights: List[float]
    execution_order: List[int]
    adaptation_rules: List[str]
    fitness_history: List[float]
    generation: int

class HypothesisMutator:
    """Handles mutation operations on hypotheses"""
    
    def __init__(self):
        self.mutation_operators = {
            "parameter_tweak": self._mutate_parameters,
            "rule_modification": self._mutate_rules,
            "condition_change": self._mutate_conditions,
            "description_refinement": self._mutate_description,
            "complexity_adjustment": self._mutate_complexity
        }
    
    def mutate_hypothesis(self, hypothesis: EvolvableHypothesis, 
                         mutation_rate: float = 0.1) -> EvolvableHypothesis:
        """Apply mutations to a hypothesis"""
        
        mutated = copy.deepcopy(hypothesis)
        mutations_applied = []
        
        # Apply each mutation with given probability
        for op_name, op_func in self.mutation_operators.items():
            if random.random() < mutation_rate:
                try:
                    mutated = op_func(mutated)
                    mutations_applied.append(op_name)
                except Exception as e:
                    logger.warning(f"Mutation {op_name} failed: {e}")
        
        # Update metadata
        mutated.generation += 1
        mutated.mutations.extend(mutations_applied)
        mutated.last_update_time = time.time()
        mutated.hypothesis_id = f"{hypothesis.hypothesis_id}_mut_{mutated.generation}"
        
        return mutated
    
    def _mutate_parameters(self, hypothesis: EvolvableHypothesis) -> EvolvableHypothesis:
        """Mutate numerical parameters"""
        
        for param_name, param_value in hypothesis.parameters.items():
            if isinstance(param_value, (int, float)):
                # Add random noise
                noise = random.gauss(0, 0.1) * param_value
                hypothesis.parameters[param_name] = param_value + noise
                
                # Keep within reasonable bounds
                if isinstance(param_value, int):
                    hypothesis.parameters[param_name] = int(hypothesis.parameters[param_name])
                    hypothesis.parameters[param_name] = max(0, hypothesis.parameters[param_name])
        
        return hypothesis
    
    def _mutate_rules(self, hypothesis: EvolvableHypothesis) -> EvolvableHypothesis:
        """Mutate transformation rules"""
        
        if not hypothesis.rules:
            return hypothesis
        
        # Random rule modifications
        if random.random() < 0.3:  # Add new rule
            new_rule = self._generate_random_rule(hypothesis.hypothesis_type)
            hypothesis.rules.append(new_rule)
        
        if random.random() < 0.2 and len(hypothesis.rules) > 1:  # Remove rule
            hypothesis.rules.pop(random.randint(0, len(hypothesis.rules) - 1))
        
        if random.random() < 0.4:  # Modify existing rule
            rule_idx = random.randint(0, len(hypothesis.rules) - 1)
            hypothesis.rules[rule_idx] = self._modify_rule(hypothesis.rules[rule_idx])
        
        return hypothesis
    
    def _mutate_conditions(self, hypothesis: EvolvableHypothesis) -> EvolvableHypothesis:
        """Mutate application conditions"""
        
        if not hypothesis.conditions:
            return hypothesis
        
        # Modify condition thresholds
        for i, condition in enumerate(hypothesis.conditions):
            if any(op in condition for op in ['>', '<', '>=', '<=', '==']):
                # Extract and modify numerical thresholds
                modified_condition = self._modify_condition_threshold(condition)
                hypothesis.conditions[i] = modified_condition
        
        return hypothesis
    
    def _mutate_description(self, hypothesis: EvolvableHypothesis) -> EvolvableHypothesis:
        """Refine hypothesis description"""
        
        # Add refinement to description
        refinements = [
            "with enhanced precision",
            "considering edge cases", 
            "with improved generalization",
            "accounting for context",
            "with adaptive parameters"
        ]
        
        if random.random() < 0.3:
            refinement = random.choice(refinements)
            hypothesis.description += f" {refinement}"
        
        return hypothesis
    
    def _mutate_complexity(self, hypothesis: EvolvableHypothesis) -> EvolvableHypothesis:
        """Adjust hypothesis complexity"""
        
        current_complexity = len(hypothesis.rules) + len(hypothesis.conditions)
        
        if current_complexity < 3 and random.random() < 0.4:
            # Increase complexity
            hypothesis.rules.append(self._generate_random_rule(hypothesis.hypothesis_type))
        elif current_complexity > 8 and random.random() < 0.4:
            # Decrease complexity - simplify
            if hypothesis.rules:
                hypothesis.rules.pop()
            if hypothesis.conditions and random.random() < 0.5:
                hypothesis.conditions.pop()
        
        return hypothesis
    
    def _generate_random_rule(self, hypothesis_type: HypothesisType) -> str:
        """Generate a random rule based on hypothesis type"""
        
        rule_templates = {
            HypothesisType.PATTERN_RECOGNITION: [
                "detect_pattern_{pattern_type}",
                "match_template_{template_id}",
                "find_repetition_{axis}"
            ],
            HypothesisType.TRANSFORMATION_RULE: [
                "transform_{source}_to_{target}",
                "apply_operation_{op_name}",
                "conditional_transform_if_{condition}"
            ],
            HypothesisType.SPATIAL_RELATIONSHIP: [
                "maintain_relative_position_{relation}",
                "preserve_distance_{distance_type}",
                "align_objects_{alignment_type}"
            ]
        }
        
        templates = rule_templates.get(hypothesis_type, ["generic_rule_{param}"])
        template = random.choice(templates)
        
        # Fill in template parameters
        rule = template.format(
            pattern_type=random.choice(["symmetric", "repetitive", "gradient"]),
            template_id=random.randint(1, 10),
            axis=random.choice(["horizontal", "vertical", "diagonal"]),
            source=random.choice(["object", "color", "shape"]),
            target=random.choice(["new_object", "different_color", "modified_shape"]),
            op_name=random.choice(["rotate", "reflect", "scale", "translate"]),
            condition=random.choice(["size_threshold", "color_match", "position_check"]),
            relation=random.choice(["adjacent", "inside", "above"]),
            distance_type=random.choice(["manhattan", "euclidean", "chebyshev"]),
            alignment_type=random.choice(["vertical", "horizontal", "diagonal"]),
            param=random.randint(1, 100)
        )
        
        return rule
    
    def _modify_rule(self, rule: str) -> str:
        """Modify an existing rule"""
        
        modifications = [
            lambda r: r.replace("_", "_enhanced_"),
            lambda r: f"conditional_{r}",
            lambda r: f"{r}_with_validation",
            lambda r: r.replace("detect", "identify").replace("find", "locate"),
            lambda r: f"optimized_{r}"
        ]
        
        modifier = random.choice(modifications)
        return modifier(rule)
    
    def _modify_condition_threshold(self, condition: str) -> str:
        """Modify numerical thresholds in conditions"""
        
        import re
        
        # Find numbers in the condition
        numbers = re.findall(r'\d+\.?\d*', condition)
        
        if numbers:
            old_num = numbers[0]
            new_num = float(old_num) * random.uniform(0.8, 1.2)  # ±20% variation
            new_condition = condition.replace(old_num, f"{new_num:.2f}", 1)
            return new_condition
        
        return condition

class HypothesisCrossover:
    """Handles crossover operations between hypotheses"""
    
    def crossover_hypotheses(self, parent1: EvolvableHypothesis, 
                           parent2: EvolvableHypothesis) -> Tuple[EvolvableHypothesis, EvolvableHypothesis]:
        """Create offspring through crossover"""
        
        # Create children
        child1 = copy.deepcopy(parent1)
        child2 = copy.deepcopy(parent2)
        
        # Perform different types of crossover
        child1, child2 = self._rule_crossover(child1, child2, parent1, parent2)
        child1, child2 = self._parameter_crossover(child1, child2, parent1, parent2)
        child1, child2 = self._condition_crossover(child1, child2, parent1, parent2)
        
        # Update metadata
        generation = max(parent1.generation, parent2.generation) + 1
        
        child1.generation = generation
        child1.parent_ids = [parent1.hypothesis_id, parent2.hypothesis_id]
        child1.hypothesis_id = f"cross_{parent1.hypothesis_id}_{parent2.hypothesis_id}_{generation}_a"
        child1.crossover_history.append(f"{parent1.hypothesis_id} x {parent2.hypothesis_id}")
        child1.last_update_time = time.time()
        
        child2.generation = generation
        child2.parent_ids = [parent1.hypothesis_id, parent2.hypothesis_id]
        child2.hypothesis_id = f"cross_{parent1.hypothesis_id}_{parent2.hypothesis_id}_{generation}_b"
        child2.crossover_history.append(f"{parent1.hypothesis_id} x {parent2.hypothesis_id}")
        child2.last_update_time = time.time()
        
        return child1, child2
    
    def _rule_crossover(self, child1: EvolvableHypothesis, child2: EvolvableHypothesis,
                       parent1: EvolvableHypothesis, parent2: EvolvableHypothesis) -> Tuple[EvolvableHypothesis, EvolvableHypothesis]:
        """Exchange rules between parents"""
        
        if not parent1.rules or not parent2.rules:
            return child1, child2
        
        # Single-point crossover for rules
        if len(parent1.rules) > 1 and len(parent2.rules) > 1:
            crossover_point1 = random.randint(1, len(parent1.rules) - 1)
            crossover_point2 = random.randint(1, len(parent2.rules) - 1)
            
            child1.rules = parent1.rules[:crossover_point1] + parent2.rules[crossover_point2:]
            child2.rules = parent2.rules[:crossover_point2] + parent1.rules[crossover_point1:]
        
        return child1, child2
    
    def _parameter_crossover(self, child1: EvolvableHypothesis, child2: EvolvableHypothesis,
                           parent1: EvolvableHypothesis, parent2: EvolvableHypothesis) -> Tuple[EvolvableHypothesis, EvolvableHypothesis]:
        """Exchange parameters between parents"""
        
        # Uniform crossover for parameters
        all_params = set(parent1.parameters.keys()) | set(parent2.parameters.keys())
        
        for param in all_params:
            if random.random() < 0.5:
                # Swap parameter values
                if param in parent1.parameters and param in parent2.parameters:
                    child1.parameters[param] = parent2.parameters[param]
                    child2.parameters[param] = parent1.parameters[param]
                elif param in parent1.parameters:
                    child2.parameters[param] = parent1.parameters[param]
                elif param in parent2.parameters:
                    child1.parameters[param] = parent2.parameters[param]
        
        return child1, child2
    
    def _condition_crossover(self, child1: EvolvableHypothesis, child2: EvolvableHypothesis,
                           parent1: EvolvableHypothesis, parent2: EvolvableHypothesis) -> Tuple[EvolvableHypothesis, EvolvableHypothesis]:
        """Exchange conditions between parents"""
        
        # Mix conditions from both parents
        all_conditions = list(set(parent1.conditions + parent2.conditions))
        
        if len(all_conditions) > 1:
            random.shuffle(all_conditions)
            mid_point = len(all_conditions) // 2
            
            child1.conditions = all_conditions[:mid_point]
            child2.conditions = all_conditions[mid_point:]
        
        return child1, child2

class FitnessEvaluator:
    """Evaluates fitness of hypotheses across multiple metrics"""
    
    def __init__(self):
        self.fitness_weights = {
            FitnessMetric.ACCURACY: 0.3,
            FitnessMetric.GENERALIZABILITY: 0.25,
            FitnessMetric.SIMPLICITY: 0.15,
            FitnessMetric.CONSISTENCY: 0.15,
            FitnessMetric.NOVELTY: 0.1,
            FitnessMetric.EXPLANATORY_POWER: 0.05
        }
    
    def evaluate_fitness(self, hypothesis: EvolvableHypothesis, 
                        test_cases: List[Dict[str, Any]]) -> Dict[FitnessMetric, float]:
        """Evaluate hypothesis fitness across all metrics"""
        
        fitness_scores = {}
        
        # Evaluate each fitness metric
        fitness_scores[FitnessMetric.ACCURACY] = self._evaluate_accuracy(hypothesis, test_cases)
        fitness_scores[FitnessMetric.GENERALIZABILITY] = self._evaluate_generalizability(hypothesis, test_cases)
        fitness_scores[FitnessMetric.SIMPLICITY] = self._evaluate_simplicity(hypothesis)
        fitness_scores[FitnessMetric.CONSISTENCY] = self._evaluate_consistency(hypothesis)
        fitness_scores[FitnessMetric.NOVELTY] = self._evaluate_novelty(hypothesis)
        fitness_scores[FitnessMetric.EXPLANATORY_POWER] = self._evaluate_explanatory_power(hypothesis)
        
        # Calculate overall fitness
        overall_fitness = sum(score * self.fitness_weights[metric] 
                            for metric, score in fitness_scores.items())
        
        # Update hypothesis
        hypothesis.fitness_scores = fitness_scores
        hypothesis.overall_fitness = overall_fitness
        
        return fitness_scores
    
    def _evaluate_accuracy(self, hypothesis: EvolvableHypothesis, 
                          test_cases: List[Dict[str, Any]]) -> float:
        """Evaluate prediction accuracy"""
        
        if not test_cases:
            return 0.5  # Neutral score if no test cases
        
        correct_predictions = 0
        total_predictions = 0
        
        for test_case in test_cases:
            try:
                # Apply hypothesis to test case
                if hypothesis.prediction_function:
                    prediction = hypothesis.prediction_function(test_case.get('input'))
                    expected = test_case.get('output')
                    
                    if prediction is not None and expected is not None:
                        # Compare predictions (simplified)
                        if np.array_equal(prediction, expected):
                            correct_predictions += 1
                        total_predictions += 1
                
            except Exception as e:
                logger.warning(f"Error evaluating hypothesis {hypothesis.hypothesis_id}: {e}")
                total_predictions += 1  # Count as incorrect
        
        accuracy = correct_predictions / max(total_predictions, 1)
        return accuracy
    
    def _evaluate_generalizability(self, hypothesis: EvolvableHypothesis, 
                                 test_cases: List[Dict[str, Any]]) -> float:
        """Evaluate how well hypothesis generalizes across different test cases"""
        
        if len(test_cases) < 2:
            return 0.5
        
        # Measure consistency across different types of test cases
        case_types = {}
        for case in test_cases:
            case_type = case.get('type', 'unknown')
            if case_type not in case_types:
                case_types[case_type] = []
            case_types[case_type].append(case)
        
        # Calculate performance variance across case types
        type_performances = []
        for case_type, cases in case_types.items():
            type_accuracy = self._evaluate_accuracy(hypothesis, cases)
            type_performances.append(type_accuracy)
        
        if len(type_performances) > 1:
            # Lower variance indicates better generalization
            variance = np.var(type_performances)
            generalizability = max(0, 1 - variance)  # Convert variance to score
        else:
            generalizability = np.mean(type_performances) if type_performances else 0.5
        
        return generalizability
    
    def _evaluate_simplicity(self, hypothesis: EvolvableHypothesis) -> float:
        """Evaluate hypothesis simplicity (Occam's razor)"""
        
        # Count complexity factors
        rule_count = len(hypothesis.rules)
        condition_count = len(hypothesis.conditions)
        parameter_count = len(hypothesis.parameters)
        description_length = len(hypothesis.description.split())
        
        # Calculate complexity score
        total_complexity = rule_count + condition_count + parameter_count + description_length / 10
        
        # Convert to simplicity score (inverse of complexity)
        max_reasonable_complexity = 20  # Reasonable upper bound
        simplicity = max(0, 1 - total_complexity / max_reasonable_complexity)
        
        return simplicity
    
    def _evaluate_consistency(self, hypothesis: EvolvableHypothesis) -> float:
        """Evaluate internal consistency of hypothesis"""
        
        consistency_score = 1.0
        
        # Check for contradictory rules
        if len(hypothesis.rules) > 1:
            for i, rule1 in enumerate(hypothesis.rules):
                for j, rule2 in enumerate(hypothesis.rules[i+1:], i+1):
                    if self._rules_contradict(rule1, rule2):
                        consistency_score -= 0.1
        
        # Check if conditions are satisfiable
        if hypothesis.conditions:
            satisfiable_conditions = self._check_condition_satisfiability(hypothesis.conditions)
            if not satisfiable_conditions:
                consistency_score -= 0.2
        
        # Check parameter reasonableness
        for param_name, param_value in hypothesis.parameters.items():
            if not self._parameter_reasonable(param_name, param_value):
                consistency_score -= 0.05
        
        return max(0, consistency_score)
    
    def _evaluate_novelty(self, hypothesis: EvolvableHypothesis) -> float:
        """Evaluate how novel/creative the hypothesis is"""
        
        novelty_indicators = 0
        total_possible = 5
        
        # Check for novel rule combinations
        if len(set(hypothesis.rules)) == len(hypothesis.rules):  # All rules unique
            novelty_indicators += 1
        
        # Check for novel parameter combinations
        if hypothesis.parameters and len(hypothesis.parameters) > 3:
            novelty_indicators += 1
        
        # Check for creative descriptions
        creative_words = ["novel", "innovative", "creative", "unique", "adaptive"]
        if any(word in hypothesis.description.lower() for word in creative_words):
            novelty_indicators += 1
        
        # Check generation depth (later generations more novel)
        if hypothesis.generation > 5:
            novelty_indicators += 1
        
        # Check mutation count (more mutations = more novel)
        if len(hypothesis.mutations) > 3:
            novelty_indicators += 1
        
        novelty = novelty_indicators / total_possible
        return novelty
    
    def _evaluate_explanatory_power(self, hypothesis: EvolvableHypothesis) -> float:
        """Evaluate how well hypothesis explains phenomena"""
        
        explanatory_score = 0.5  # Base score
        
        # Rich description indicates better explanatory power
        description_words = len(hypothesis.description.split())
        if description_words > 10:
            explanatory_score += 0.2
        
        # Multiple rules suggest comprehensive explanation
        if len(hypothesis.rules) > 2:
            explanatory_score += 0.15
        
        # Conditions show nuanced understanding
        if len(hypothesis.conditions) > 1:
            explanatory_score += 0.15
        
        # Test results indicate empirical support
        if hypothesis.test_results and len(hypothesis.test_results) > 0:
            avg_test_performance = np.mean([r.get('score', 0) for r in hypothesis.test_results])
            explanatory_score += avg_test_performance * 0.2
        
        return min(1.0, explanatory_score)
    
    def _rules_contradict(self, rule1: str, rule2: str) -> bool:
        """Check if two rules contradict each other"""
        
        # Simple contradiction detection
        contradictory_pairs = [
            ("increase", "decrease"),
            ("add", "remove"),
            ("create", "delete"),
            ("expand", "contract"),
            ("left", "right"),
            ("up", "down")
        ]
        
        for pair in contradictory_pairs:
            if pair[0] in rule1.lower() and pair[1] in rule2.lower():
                return True
            if pair[1] in rule1.lower() and pair[0] in rule2.lower():
                return True
        
        return False
    
    def _check_condition_satisfiability(self, conditions: List[str]) -> bool:
        """Check if conditions can be simultaneously satisfied"""
        
        # Simplified satisfiability check
        # In a real implementation, this would be more sophisticated
        
        numeric_conditions = []
        for condition in conditions:
            if any(op in condition for op in ['>', '<', '>=', '<=', '==']):
                numeric_conditions.append(condition)
        
        # For now, assume satisfiable if not obviously contradictory
        return len(numeric_conditions) < 5  # Arbitrary threshold

    def _parameter_reasonable(self, param_name: str, param_value: Any) -> bool:
        """Check if parameter value is reasonable"""
        
        if isinstance(param_value, (int, float)):
            # Check for reasonable numeric ranges
            if param_value < -1000 or param_value > 1000:
                return False
            if param_name.lower().endswith('_probability') and not (0 <= param_value <= 1):
                return False
        
        return True

class HypothesisEvolutionEngine:
    """Main engine for hypothesis evolution using genetic algorithms"""
    
    def __init__(self, population_size: int = 50, mutation_rate: float = 0.1, 
                 crossover_rate: float = 0.7, elitism_rate: float = 0.1):
        
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism_rate = elitism_rate
        
        # Components
        self.mutator = HypothesisMutator()
        self.crossover = HypothesisCrossover()
        self.fitness_evaluator = FitnessEvaluator()
        
        # Population
        self.population: List[EvolvableHypothesis] = []
        self.generation_count = 0
        self.evolution_history = []
        
        # Statistics
        self.best_hypothesis_per_generation = []
        self.average_fitness_per_generation = []
        self.diversity_per_generation = []
        
        logger.info("🧬 Hypothesis Evolution Engine initialized")
    
    def initialize_population(self, initial_hypotheses: List[EvolvableHypothesis] = None) -> List[EvolvableHypothesis]:
        """Initialize the population with seed hypotheses"""
        
        if initial_hypotheses:
            self.population = initial_hypotheses[:self.population_size]
        else:
            self.population = []
        
        # Fill population with random hypotheses if needed
        while len(self.population) < self.population_size:
            random_hypothesis = self._generate_random_hypothesis()
            self.population.append(random_hypothesis)
        
        logger.info(f"🌱 Initialized population with {len(self.population)} hypotheses")
        return self.population
    
    def _generate_random_hypothesis(self) -> EvolvableHypothesis:
        """Generate a random hypothesis"""
        
        hypothesis_types = list(HypothesisType)
        h_type = random.choice(hypothesis_types)
        
        hypothesis = EvolvableHypothesis(
            hypothesis_id=f"random_{random.randint(1000, 9999)}",
            hypothesis_type=h_type,
            generation=0,
            parent_ids=[],
            description=f"Random {h_type.value} hypothesis",
            prediction_function=None,
            parameters={f"param_{i}": random.uniform(0, 1) for i in range(3)},
            rules=[self.mutator._generate_random_rule(h_type) for _ in range(random.randint(1, 4))],
            conditions=[f"condition_{i} > {random.uniform(0, 1):.2f}" for i in range(random.randint(1, 3))],
            fitness_scores={},
            overall_fitness=0.0,
            mutations=[],
            crossover_history=[],
            test_results=[],
            validation_examples=[],
            success_rate=0.0,
            confidence=0.5,
            creation_time=time.time(),
            last_update_time=time.time(),
            usage_count=0
        )
        
        return hypothesis
    
    def evolve_generation(self, test_cases: List[Dict[str, Any]]) -> List[EvolvableHypothesis]:
        """Evolve the population for one generation"""
        
        logger.info(f"🧬 Evolving generation {self.generation_count}")
        
        # 1. Evaluate fitness
        self._evaluate_population_fitness(test_cases)
        
        # 2. Record statistics
        self._record_generation_statistics()
        
        # 3. Selection
        selected_parents = self._selection()
        
        # 4. Create next generation
        next_generation = self._create_next_generation(selected_parents)
        
        # 5. Update population
        self.population = next_generation
        self.generation_count += 1
        
        logger.info(f"✅ Generation {self.generation_count} evolved. Best fitness: {max(h.overall_fitness for h in self.population):.3f}")
        
        return self.population
    
    def _evaluate_population_fitness(self, test_cases: List[Dict[str, Any]]):
        """Evaluate fitness for all hypotheses in population"""
        
        for hypothesis in self.population:
            self.fitness_evaluator.evaluate_fitness(hypothesis, test_cases)
    
    def _record_generation_statistics(self):
        """Record statistics for current generation"""
        
        fitnesses = [h.overall_fitness for h in self.population]
        
        # Best hypothesis
        best_hypothesis = max(self.population, key=lambda h: h.overall_fitness)
        self.best_hypothesis_per_generation.append({
            'generation': self.generation_count,
            'hypothesis_id': best_hypothesis.hypothesis_id,
            'fitness': best_hypothesis.overall_fitness,
            'description': best_hypothesis.description
        })
        
        # Average fitness
        avg_fitness = np.mean(fitnesses)
        self.average_fitness_per_generation.append(avg_fitness)
        
        # Population diversity (entropy of fitness distribution)
        fitness_bins = np.histogram(fitnesses, bins=10)[0]
        diversity = entropy(fitness_bins + 1e-10)  # Add small value to avoid log(0)
        self.diversity_per_generation.append(diversity)
    
    def _selection(self) -> List[EvolvableHypothesis]:
        """Select parents for next generation"""
        
        # Sort by fitness
        sorted_population = sorted(self.population, key=lambda h: h.overall_fitness, reverse=True)
        
        # Elitism: keep top performers
        elite_count = int(self.population_size * self.elitism_rate)
        elite = sorted_population[:elite_count]
        
        # Tournament selection for the rest
        selected = list(elite)
        tournament_size = 3
        
        while len(selected) < self.population_size:
            # Tournament selection
            tournament = random.sample(self.population, tournament_size)
            winner = max(tournament, key=lambda h: h.overall_fitness)
            selected.append(winner)
        
        return selected[:self.population_size]
    
    def _create_next_generation(self, parents: List[EvolvableHypothesis]) -> List[EvolvableHypothesis]:
        """Create next generation through crossover and mutation"""
        
        next_generation = []
        
        # Keep elite unchanged
        elite_count = int(self.population_size * self.elitism_rate)
        elite = sorted(parents, key=lambda h: h.overall_fitness, reverse=True)[:elite_count]
        next_generation.extend(copy.deepcopy(elite))
        
        # Create offspring through crossover and mutation
        while len(next_generation) < self.population_size:
            
            if random.random() < self.crossover_rate and len(parents) >= 2:
                # Crossover
                parent1, parent2 = random.sample(parents, 2)
                child1, child2 = self.crossover.crossover_hypotheses(parent1, parent2)
                
                # Mutate children
                if random.random() < self.mutation_rate:
                    child1 = self.mutator.mutate_hypothesis(child1, self.mutation_rate)
                if random.random() < self.mutation_rate:
                    child2 = self.mutator.mutate_hypothesis(child2, self.mutation_rate)
                
                next_generation.extend([child1, child2])
            
            else:
                # Mutation only
                parent = random.choice(parents)
                child = self.mutator.mutate_hypothesis(parent, self.mutation_rate)
                next_generation.append(child)
        
        return next_generation[:self.population_size]
    
    def get_best_hypotheses(self, top_k: int = 5) -> List[EvolvableHypothesis]:
        """Get the top-k best hypotheses from current population"""
        
        sorted_population = sorted(self.population, key=lambda h: h.overall_fitness, reverse=True)
        return sorted_population[:top_k]
    
    def evolve_until_convergence(self, test_cases: List[Dict[str, Any]], 
                               max_generations: int = 100, 
                               fitness_threshold: float = 0.95,
                               patience: int = 10) -> EvolvableHypothesis:
        """Evolve population until convergence or max generations"""
        
        logger.info(f"🚀 Starting evolution for up to {max_generations} generations")
        
        best_fitness_history = []
        generations_without_improvement = 0
        
        for generation in range(max_generations):
            # Evolve one generation
            self.evolve_generation(test_cases)
            
            # Check for convergence
            best_hypothesis = max(self.population, key=lambda h: h.overall_fitness)
            best_fitness = best_hypothesis.overall_fitness
            best_fitness_history.append(best_fitness)
            
            # Check if fitness threshold reached
            if best_fitness >= fitness_threshold:
                logger.info(f"🎯 Fitness threshold {fitness_threshold} reached at generation {generation}")
                break
            
            # Check for improvement
            if len(best_fitness_history) > 1:
                if best_fitness <= best_fitness_history[-2] + 1e-6:  # No significant improvement
                    generations_without_improvement += 1
                else:
                    generations_without_improvement = 0
            
            # Early stopping if no improvement
            if generations_without_improvement >= patience:
                logger.info(f"⏹️ Early stopping at generation {generation} due to lack of improvement")
                break
        
        final_best = max(self.population, key=lambda h: h.overall_fitness)
        logger.info(f"🏆 Evolution complete. Best fitness: {final_best.overall_fitness:.3f}")
        
        return final_best
    
    def generate_evolution_report(self) -> Dict[str, Any]:
        """Generate comprehensive report on evolution process"""
        
        report = {
            "evolution_summary": {
                "total_generations": self.generation_count,
                "population_size": self.population_size,
                "mutation_rate": self.mutation_rate,
                "crossover_rate": self.crossover_rate,
                "elitism_rate": self.elitism_rate
            },
            "performance_metrics": {
                "best_fitness_per_generation": [h['fitness'] for h in self.best_hypothesis_per_generation],
                "average_fitness_per_generation": self.average_fitness_per_generation,
                "diversity_per_generation": self.diversity_per_generation,
                "final_best_fitness": max(h.overall_fitness for h in self.population) if self.population else 0
            },
            "population_analysis": {
                "hypothesis_types": Counter([h.hypothesis_type.value for h in self.population]),
                "generation_distribution": Counter([h.generation for h in self.population]),
                "fitness_distribution": {
                    "mean": np.mean([h.overall_fitness for h in self.population]),
                    "std": np.std([h.overall_fitness for h in self.population]),
                    "min": min(h.overall_fitness for h in self.population),
                    "max": max(h.overall_fitness for h in self.population)
                }
            },
            "best_hypotheses": [
                {
                    "hypothesis_id": h.hypothesis_id,
                    "fitness": h.overall_fitness,
                    "description": h.description,
                    "generation": h.generation,
                    "rules": h.rules[:3],  # Top 3 rules
                    "fitness_breakdown": h.fitness_scores
                }
                for h in self.get_best_hypotheses(5)
            ]
        }
        
        return report
