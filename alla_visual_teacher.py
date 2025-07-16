"""
ALLA NATURAL LANGUAGE VISUAL REASONING MODULE
==============================================

This module embodies the ALLA Guiding Principles by creating a bridge between
human natural language instruction and ALLA's visual reasoning capabilities.

The human teacher speaks in natural language.
ALLA learns through grounded visual experience.
Technology facilitates, never replaces, this interaction.
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import json
from pathlib import Path

@dataclass
class VisualRule:
    """A rule that ALLA learns about visual patterns."""
    name: str
    description: str  # Human-readable description
    pattern_condition: str  # What to look for
    action: str  # What to do
    examples: List[Dict]  # Example grids where this rule applies
    confidence: float = 0.0
    
    def to_natural_language(self) -> str:
        """Convert rule back to natural language for transparency."""
        return f"When I see {self.pattern_condition}, I should {self.action}."

class VisualTeacher:
    """
    Embodies the principle: "The human teacher should not need to understand 
    Python, JSON, or complex syntax. They teach in natural language."
    """
    
    def __init__(self, alla_engine):
        self.alla = alla_engine
        self.visual_rules = []
        
    def teach_visual_rule(self, human_instruction: str, example_grid: List[List[int]]) -> str:
        """
        Core teaching interface - humans speak naturally, ALLA learns meaningfully.
        
        Example usage:
        teacher.teach_visual_rule(
            "When you see blue squares, move them down until they touch something",
            [[0,1,0], [0,0,0], [2,2,2]]
        )
        """
        
        # Parse natural language instruction into structured rule
        parsed_rule = self._parse_natural_instruction(human_instruction)
        
        if not parsed_rule:
            reflection = self.reflect_on_teaching_session(human_instruction, False)
            return f"I didn't understand that instruction. Could you rephrase it?\n\n{reflection}"
        
        # Create visual rule with example
        rule = VisualRule(
            name=f"rule_{len(self.visual_rules)+1}",
            description=human_instruction,
            pattern_condition=parsed_rule['pattern'],
            action=parsed_rule['action'],
            examples=[{'grid': example_grid, 'instruction': human_instruction}],
            confidence=0.8
        )
        
        self.visual_rules.append(rule)
        
        # Teach ALLA the underlying concepts through its existing learning system
        self._ground_rule_in_alla_knowledge(rule)
        
        # Reflect on successful learning
        reflection = self.reflect_on_teaching_session(human_instruction, True)
        return f"I learned: {rule.to_natural_language()}\n\n{reflection}"
        
    def explain_learning_progress(self) -> str:
        """
        ALLA explains what it has learned and how it thinks.
        Embodies: "Full transparency in reasoning and decision-making"
        """
        
        if not self.visual_rules:
            return "I haven't learned any visual rules yet. Teach me by showing me examples!"
        
        explanation = f"I have learned {len(self.visual_rules)} visual rules:\n\n"
        
        for i, rule in enumerate(self.visual_rules, 1):
            explanation += f"{i}. {rule.to_natural_language()}\n"
            explanation += f"   Confidence: {rule.confidence:.1f}\n"
            explanation += f"   Examples seen: {len(rule.examples)}\n\n"
        
        # Add semantic memory insights
        if hasattr(self.alla, 'semantic_memory'):
            visual_concepts = [node for node in self.alla.semantic_memory.nodes.values() 
                             if 'visual' in node.concept_type or 'rule' in node.concept_type]
            explanation += f"I have also built {len(visual_concepts)} semantic concepts "
            explanation += "that help me understand visual patterns.\n\n"
        
        explanation += "When you show me a new grid, I will:\n"
        explanation += "1. Analyze what I see (colors, patterns, shapes)\n"
        explanation += "2. Check which of my learned rules might apply\n"
        explanation += "3. Explain my reasoning transparently\n"
        explanation += "4. Apply the most suitable rule\n"
        explanation += "5. Learn from the outcome to improve\n"
        
        return explanation
    
    def reflect_on_teaching_session(self, human_instruction: str, success: bool) -> str:
        """
        ALLA reflects on a teaching session to improve future learning.
        Embodies: "Learning from every interaction"
        """
        
        reflection = f"Reflecting on instruction: '{human_instruction}'\n"
        
        if success:
            reflection += "✓ I successfully understood and learned from this instruction.\n"
            reflection += "This adds to my growing understanding of visual patterns.\n"
        else:
            reflection += "✗ I had difficulty understanding this instruction.\n"
            reflection += "I need to improve my natural language parsing or ask for clarification.\n"
        
        # Log reflection in ALLA's memory system
        self.alla._record_thought(f"Visual teaching reflection: {reflection}")
        
        return reflection
    
    def _parse_natural_instruction(self, instruction: str) -> Optional[Dict[str, str]]:
        """
        Parse natural language into structured components.
        This embodies the principle: Technology bridges human language to AI understanding.
        """
        instruction = instruction.lower()
        
        # Enhanced pattern recognition for common ARC instructions
        patterns = {
            'move_until_collision': {
                'triggers': [['move', 'down'], ['blue', 'move'], ['move', 'until'], ['down', 'touch']],
                'pattern': 'moving objects',
                'action': 'move until collision'
            },
            'copy_pattern': {
                'triggers': [['copy', 'repeat'], ['duplicate'], ['repeat', 'pattern']],
                'pattern': 'pattern to copy',
                'action': 'copy pattern'
            },
            'fill_enclosed': {
                'triggers': [['fill', 'enclosed'], ['fill', 'inside'], ['fill', 'area'], ['enclosed', 'area']],
                'pattern': 'enclosed area',
                'action': 'fill area'
            },
            'connect_objects': {
                'triggers': [['connect', 'objects'], ['connect', 'line'], ['line', 'between'], ['isolated', 'connect']],
                'pattern': 'objects to connect',
                'action': 'draw connection'
            }
        }
        
        # Check each pattern type
        for rule_type, config in patterns.items():
            for trigger_set in config['triggers']:
                if isinstance(trigger_set, list):
                    if all(trigger in instruction for trigger in trigger_set):
                        return {
                            'type': rule_type,
                            'pattern': config['pattern'],
                            'action': config['action']
                        }
                else:
                    if trigger_set in instruction:
                        return {
                            'type': rule_type,
                            'pattern': config['pattern'],
                            'action': config['action']
                        }
        
        # Fallback: try to extract basic action and object patterns
        if any(word in instruction for word in ['move', 'blue', 'red', 'down', 'up']):
            return {
                'type': 'basic_action',
                'pattern': 'visual objects',
                'action': 'perform action'
            }
        
        return None
    
    def _ground_rule_in_alla_knowledge(self, rule: VisualRule):
        """
        Connect visual rule to ALLA's semantic memory.
        This ensures transparency - humans can see how ALLA understands the rule.
        Embodies: "ALLA learns through grounded experience"
        """
        
        # Extract key concepts from the rule for semantic grounding
        rule_concepts = self._extract_rule_concepts(rule)
        
        # Teach ALLA the visual concepts through its existing teaching system
        for concept in rule_concepts:
            self.alla._teach_word(concept['word'], concept['type'], concept['expression'])
        
        # Add rule to semantic memory with rich connections
        from alla_engine import SemanticNode, SemanticEdge
        
        rule_node = SemanticNode(
            id=f"visual_rule:{rule.name}",
            concept_type="rule",
            name=rule.name,
            observations=1
        )
        self.alla.semantic_memory.add_node(rule_node)
        
        # Create semantic connections between rule and its components
        for concept in rule_concepts:
            concept_node = SemanticNode(
                id=f"concept:{concept['word']}",
                concept_type="visual_concept",
                name=concept['word'],
                observations=1
            )
            self.alla.semantic_memory.add_node(concept_node)
            
            # Link rule to concept
            edge = SemanticEdge(
                from_node=rule_node.id,
                to_node=concept_node.id,
                relationship="uses_concept",
                strength=0.8
            )
            self.alla.semantic_memory.add_edge(edge)
        
        # Store rule in ALLA's goal-oriented memory for future use
        self._store_rule_as_goal_pattern(rule)
        
        print(f"[VISUAL TEACHER] Grounded rule '{rule.name}' in ALLA's knowledge base")
        print(f"[VISUAL TEACHER] Created {len(rule_concepts)} semantic connections")
    
    def _extract_rule_concepts(self, rule: VisualRule) -> List[Dict[str, str]]:
        """Extract semantic concepts from a visual rule for grounding."""
        concepts = []
        
        # Pattern-based concept extraction
        if "move" in rule.action.lower():
            concepts.extend([
                {"word": "move_action", "type": "action", "expression": "obj.action_type == 'move'"},
                {"word": "spatial_movement", "type": "property", "expression": "obj.has_position_change == True"}
            ])
        
        if "down" in rule.description.lower():
            concepts.append({"word": "downward_direction", "type": "property", "expression": "obj.direction == 'down'"})
        
        if "blue" in rule.description.lower():
            concepts.append({"word": "blue_color", "type": "property", "expression": "obj.color == 'blue'"})
        
        if "touch" in rule.description.lower() or "until" in rule.description.lower():
            concepts.extend([
                {"word": "collision_detection", "type": "relation", "expression": "obj1.touches(obj2)"},
                {"word": "stopping_condition", "type": "condition", "expression": "obj.movement_blocked == True"}
            ])
        
        if "connect" in rule.description.lower():
            concepts.extend([
                {"word": "connection_action", "type": "action", "expression": "obj.action_type == 'connect'"},
                {"word": "line_drawing", "type": "property", "expression": "obj.creates_line == True"}
            ])
        
        return concepts
    
    def _store_rule_as_goal_pattern(self, rule: VisualRule):
        """Store visual rule as a goal pattern ALLA can pursue."""
        goal_description = f"Apply visual rule: {rule.description}"
        
        # Create goal using ALLA's existing goal system
        self.alla.current_goal = goal_description
        
        # Store rule metadata for future application
        if not hasattr(self.alla, 'visual_rule_patterns'):
            self.alla.visual_rule_patterns = {}
        
        self.alla.visual_rule_patterns[rule.name] = {
            'description': rule.description,
            'pattern_condition': rule.pattern_condition,
            'action': rule.action,
            'confidence': rule.confidence,
            'examples': rule.examples
        }

class VisualReasoner:
    """
    Embodies the principle: "ALLA learns through grounded experience."
    This class helps ALLA apply learned visual rules to new grids.
    """
    
    def __init__(self, alla_engine, visual_teacher):
        self.alla = alla_engine
        self.teacher = visual_teacher
        
    def analyze_grid(self, grid: List[List[int]]) -> Dict[str, Any]:
        """
        ALLA examines a grid and explains what it sees in human terms.
        This embodies transparency - humans can understand ALLA's perception.
        """
        
        analysis = {
            'grid_size': (len(grid), len(grid[0]) if grid else 0),
            'colors_present': self._find_colors(grid),
            'patterns_detected': self._detect_patterns(grid),
            'applicable_rules': [rule.name for rule in self.teacher.visual_rules if self._rule_matches_grid(rule, grid, {})],
            'alla_thoughts': self._get_alla_interpretation(grid)
        }
        
        return analysis
    
    def _find_colors(self, grid: List[List[int]]) -> List[int]:
        """Find all unique colors in the grid."""
        colors = set()
        for row in grid:
            colors.update(row)
        return sorted(list(colors))
    
    def _detect_patterns(self, grid: List[List[int]]) -> List[str]:
        """Detect basic visual patterns."""
        patterns = []
        
        # Simple pattern detection
        if self._has_horizontal_lines(grid):
            patterns.append("horizontal_lines")
        if self._has_vertical_lines(grid):
            patterns.append("vertical_lines")
        if self._has_isolated_objects(grid):
            patterns.append("isolated_objects")
            
        return patterns
    
    def _has_horizontal_lines(self, grid: List[List[int]]) -> bool:
        """Check for horizontal line patterns."""
        for row in grid:
            if len(set(row)) == 1 and row[0] != 0:  # All same non-background color
                return True
        return False
    
    def _has_vertical_lines(self, grid: List[List[int]]) -> bool:
        """Check for vertical line patterns."""
        if not grid:
            return False
        
        for col in range(len(grid[0])):
            column = [grid[row][col] for row in range(len(grid))]
            if len(set(column)) == 1 and column[0] != 0:
                return True
        return False
    
    def _has_isolated_objects(self, grid: List[List[int]]) -> bool:
        """Check for isolated colored objects."""
        # Simple check: look for non-background colors surrounded by background
        for i in range(1, len(grid)-1):
            for j in range(1, len(grid[0])-1):
                if grid[i][j] != 0:  # Non-background
                    # Check if surrounded by background
                    neighbors = [
                        grid[i-1][j], grid[i+1][j], 
                        grid[i][j-1], grid[i][j+1]
                    ]
                    if all(n == 0 for n in neighbors):
                        return True
        return False
    
    def apply_learned_rules(self, grid: List[List[int]]) -> Dict[str, Any]:
        """
        Apply ALLA's learned visual rules to solve a new grid.
        Embodies: "ALLA learns through grounded experience" and demonstrates transparency.
        """
        
        # First, analyze what we see
        analysis = self.analyze_grid(grid)
        
        # Find applicable rules
        applicable_rules = []
        for rule in self.teacher.visual_rules:
            if self._rule_matches_grid(rule, grid, analysis):
                applicable_rules.append(rule)
        
        # Apply the best matching rule
        if applicable_rules:
            best_rule = max(applicable_rules, key=lambda r: r.confidence)
            solution = self._apply_rule_to_grid(best_rule, grid)
            
            return {
                'analysis': analysis,
                'selected_rule': best_rule.name,
                'rule_description': best_rule.description,
                'reasoning': f"I chose '{best_rule.description}' because {self._explain_rule_selection(best_rule, analysis)}",
                'solution': solution,
                'confidence': best_rule.confidence
            }
        else:
            return {
                'analysis': analysis,
                'selected_rule': None,
                'reasoning': "No learned rules match this grid pattern",
                'solution': None,
                'confidence': 0.0
            }
    
    def _rule_matches_grid(self, rule: VisualRule, grid: List[List[int]], analysis: Dict) -> bool:
        """Check if a rule applies to the current grid."""
        
        # Simple pattern matching based on rule type
        rule_desc = rule.description.lower()
        
        if "move" in rule_desc and "blue" in rule_desc:
            return 1 in analysis['colors_present']  # Blue objects present
        
        if "connect" in rule_desc and "isolated" in rule_desc:
            return "isolated_objects" in analysis['patterns_detected']
        
        if "fill" in rule_desc:
            return self._has_enclosed_areas(grid)
        
        return False
    
    def _explain_rule_selection(self, rule: VisualRule, analysis: Dict) -> str:
        """Provide transparent reasoning for why a rule was selected."""
        explanations = []
        
        if 1 in analysis['colors_present'] and "blue" in rule.description.lower():
            explanations.append("I see blue objects")
        
        if "isolated_objects" in analysis['patterns_detected'] and "isolated" in rule.description.lower():
            explanations.append("I detected isolated objects")
        
        if len(analysis['colors_present']) > 1 and "connect" in rule.description.lower():
            explanations.append("multiple colors suggest connection might be needed")
        
        return " and ".join(explanations) if explanations else "it seemed most appropriate"
    
    def _apply_rule_to_grid(self, rule: VisualRule, grid: List[List[int]]) -> List[List[int]]:
        """
        Apply a visual rule to transform the grid.
        This is a simplified implementation - real version would be more sophisticated.
        """
        
        # Create a copy of the grid to modify
        result = [row[:] for row in grid]
        
        rule_desc = rule.description.lower()
        
        if "move" in rule_desc and "down" in rule_desc:
            result = self._apply_move_down_rule(result)
        elif "connect" in rule_desc:
            result = self._apply_connection_rule(result)
        elif "fill" in rule_desc:
            result = self._apply_fill_rule(result)
        
        return result
    
    def _apply_move_down_rule(self, grid: List[List[int]]) -> List[List[int]]:
        """Apply a 'move down' rule to the grid."""
        result = [row[:] for row in grid]
        
        # Find blue objects (color 1) and move them down
        for col in range(len(result[0])):
            # Find blue objects in this column
            blue_positions = []
            for row in range(len(result)):
                if result[row][col] == 1:
                    blue_positions.append(row)
            
            # Clear blue objects
            for row in blue_positions:
                result[row][col] = 0
            
            # Place them as far down as possible
            for blue_row in blue_positions:
                # Find the lowest available position
                target_row = len(result) - 1
                while target_row >= 0 and result[target_row][col] != 0:
                    target_row -= 1
                
                if target_row >= 0:
                    result[target_row][col] = 1
        
        return result
    
    def _apply_connection_rule(self, grid: List[List[int]]) -> List[List[int]]:
        """Apply a connection rule to connect isolated objects."""
        result = [row[:] for row in grid]
        
        # Find isolated objects
        objects = []
        for i in range(len(result)):
            for j in range(len(result[0])):
                if result[i][j] != 0:
                    objects.append((i, j, result[i][j]))
        
        # Connect first two different colored objects with a line
        if len(objects) >= 2:
            obj1, obj2 = objects[0], objects[1]
            # Simple horizontal line connection
            if obj1[0] == obj2[0]:  # Same row
                start_col, end_col = sorted([obj1[1], obj2[1]])
                for col in range(start_col + 1, end_col):
                    if result[obj1[0]][col] == 0:
                        result[obj1[0]][col] = obj1[2]  # Use first object's color
        
        return result
    
    def _apply_fill_rule(self, grid: List[List[int]]) -> List[List[int]]:
        """Apply a fill rule to enclosed areas."""
        # Simplified implementation
        return grid
    
    def _has_enclosed_areas(self, grid: List[List[int]]) -> bool:
        """Check for enclosed areas (simplified)."""
        # This is a placeholder - real implementation would use flood fill
        return False
    
    def _get_alla_interpretation(self, grid: List[List[int]]) -> str:
        """
        Get ALLA's semantic interpretation of the grid.
        This connects visual perception to ALLA's knowledge base.
        """
        
        # Convert grid to ALLA's world representation
        alla_objects = self._grid_to_alla_objects(grid)
        
        # Use ALLA's existing reasoning to interpret
        interpretations = []
        
        for obj in alla_objects:
            # Query ALLA's semantic memory about this object
            feedback, result = self.alla.process_command(f"what is {obj['color']}")
            if result:
                interpretations.append(f"I see {obj['color']} at position ({obj['x']}, {obj['y']})")
        
        return "; ".join(interpretations) if interpretations else "I see a grid with patterns"
    
    def _grid_to_alla_objects(self, grid: List[List[int]]) -> List[Dict]:
        """Convert grid to ALLA's object representation."""
        objects = []
        
        for i, row in enumerate(grid):
            for j, color_value in enumerate(row):
                if color_value != 0:  # Non-background
                    objects.append({
                        'x': j,
                        'y': i,
                        'color': self._color_value_to_name(color_value),
                        'shape': 'square'  # All grid cells are squares
                    })
        
        return objects
    
    def _color_value_to_name(self, value: int) -> str:
        """Convert color values to names ALLA can understand."""
        color_map = {
            0: 'black',
            1: 'blue', 
            2: 'red',
            3: 'green',
            4: 'yellow',
            5: 'gray',
            6: 'magenta',
            7: 'orange',
            8: 'cyan',
            9: 'brown'
        }
        return color_map.get(value, f'color_{value}')

def demonstrate_natural_teaching():
    """
    Demonstrate the ALLA Guiding Principles in action.
    Shows how a human can teach ALLA visual reasoning in natural language.
    Enhanced to show rule application and transparent reasoning.
    """
    
    print("=" * 60)
    print("ALLA NATURAL LANGUAGE VISUAL TEACHING DEMONSTRATION")
    print("=" * 60)
    print("Embodying the principle: Humans teach in their language,")
    print("ALLA learns through grounded experience.")
    print()
    
    # Load existing ALLA engine
    from alla_engine import AllaEngine
    alla = AllaEngine("visual_demo_memory.json")
    
    # Create teacher and reasoner
    teacher = VisualTeacher(alla)
    reasoner = VisualReasoner(alla, teacher)
    
    # Example 1: Human teaches a movement rule
    print("HUMAN TEACHER: 'When you see blue squares, move them down until they touch something'")
    example_grid = [
        [0, 1, 0],  # Blue square at top
        [0, 0, 0],  # Empty space
        [2, 2, 2]   # Red barrier at bottom
    ]
    
    response = teacher.teach_visual_rule(
        "When you see blue squares, move them down until they touch something",
        example_grid
    )
    print(f"ALLA: {response}")
    print("-" * 40)
    
    # Example 2: Human teaches another rule
    print("HUMAN TEACHER: 'When you see isolated objects, connect them with a line'")
    example_grid2 = [
        [1, 0, 0, 0, 2],  # Blue and red objects separated
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
    
    response2 = teacher.teach_visual_rule(
        "When you see isolated objects, connect them with a line",
        example_grid2
    )
    print(f"ALLA: {response2}")
    print("-" * 40)
    
    # Example 3: Show ALLA's learning progress (Transparency Principle)
    print("ALLA'S LEARNING PROGRESS:")
    progress = teacher.explain_learning_progress()
    print(progress)
    print("-" * 40)
    
    # Example 4: Test ALLA applying learned rules
    print("TESTING ALLA'S RULE APPLICATION:")
    test_grid = [
        [0, 1, 0, 0, 0],  # Blue square that can move down
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [2, 2, 2, 2, 2]   # Red barrier
    ]
    
    print("Test grid:")
    for row in test_grid:
        print(row)
    print()
    
    result = reasoner.apply_learned_rules(test_grid)
    
    print(f"ALLA's analysis: {result['analysis']['patterns_detected']}")
    print(f"Selected rule: {result['selected_rule']}")
    print(f"Reasoning: {result['reasoning']}")
    print(f"Confidence: {result['confidence']:.1f}")
    
    if result['solution']:
        print("Solution grid:")
        for row in result['solution']:
            print(row)
    else:
        print("No solution found")
    
    print()
    print("-" * 40)
    
    print("DEMONSTRATION COMPLETE")
    print("Key principles demonstrated:")
    print("✓ Human teaches in natural language")
    print("✓ ALLA learns through grounded visual experience")
    print("✓ Technology bridges understanding (parsing, grounding)")
    print("✓ Full transparency (ALLA explains its rules and reasoning)")
    print("✓ Integration with existing ALLA knowledge base")
    print("✓ Reflective learning and self-explanation")
    print("✓ Rule application with transparent decision-making")
    
    alla.shutdown()

if __name__ == "__main__":
    demonstrate_natural_teaching()
