# ==============================================================================
# ARC_PHASE2_PREVIEW.PY - ALLA Initiative Phase 2 Symbolic Reasoning Foundation
# ==============================================================================
# This module provides a preview of Phase 2 capabilities and the framework
# for the symbolic reasoning engine that will build on Phase 1.

from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
from arc_core import ARCGrid, ARCCell, ARCTask

class ARCActionType(Enum):
    """Enumeration of fundamental ARC transformation actions."""
    MOVE = "move"
    COPY = "copy"
    DELETE = "delete"
    CHANGE_COLOR = "change_color"
    ROTATE = "rotate"
    FLIP = "flip"
    SCALE = "scale"
    FILL = "fill"
    EXTRACT_PATTERN = "extract_pattern"
    APPLY_PATTERN = "apply_pattern"

@dataclass
class ARCAction:
    """Represents a single atomic action in ARC space."""
    action_type: ARCActionType
    target_filter: Callable[[ARCCell], bool]  # Which cells to act on
    parameters: Dict[str, Any]  # Action-specific parameters
    description: str  # Human-readable description
    
    def __repr__(self):
        return f"ARCAction({self.action_type.value}: {self.description})"

@dataclass 
class ARCRule:
    """Represents a complete transformation rule."""
    rule_id: str
    name: str
    description: str
    actions: List[ARCAction]
    preconditions: List[Callable[[ARCGrid], bool]]  # Conditions that must be met
    confidence: float = 0.0  # How confident we are this rule works
    
    def applies_to(self, grid: ARCGrid) -> bool:
        """Check if this rule can be applied to the given grid."""
        return all(condition(grid) for condition in self.preconditions)
    
    def __repr__(self):
        return f"ARCRule({self.rule_id}: {self.name})"

class ARCRuleBase:
    """Phase 2 Foundation: Library of fundamental ARC transformation rules."""
    
    def __init__(self):
        self.rules: Dict[str, ARCRule] = {}
        self._initialize_core_rules()
    
    def _initialize_core_rules(self):
        """Initialize the basic set of ARC transformation rules."""
        
        # Rule 1: Move objects down
        move_down_rule = ARCRule(
            rule_id="move_down",
            name="Move Objects Down",
            description="Move all non-black objects down until they hit bottom or another object",
            actions=[
                ARCAction(
                    action_type=ARCActionType.MOVE,
                    target_filter=lambda cell: cell.color != 0,  # Non-black cells
                    parameters={"direction": "down", "until": "collision"},
                    description="Move non-black cells down until collision"
                )
            ],
            preconditions=[
                lambda grid: any(cell.color != 0 for cell in grid.objects),  # Has non-black cells
                lambda grid: grid.height > 1  # Grid is tall enough to move
            ]
        )
        self.rules["move_down"] = move_down_rule
        
        # Rule 2: Change color
        change_color_rule = ARCRule(
            rule_id="change_color",
            name="Change Color",
            description="Change all objects of one color to another color",
            actions=[
                ARCAction(
                    action_type=ARCActionType.CHANGE_COLOR,
                    target_filter=lambda cell: True,  # Will be customized
                    parameters={"from_color": None, "to_color": None},  # Will be filled
                    description="Change object colors"
                )
            ],
            preconditions=[
                lambda grid: len(set(cell.color for cell in grid.objects)) > 1  # Multiple colors
            ]
        )
        self.rules["change_color"] = change_color_rule
        
        # Rule 3: Copy pattern
        copy_pattern_rule = ARCRule(
            rule_id="copy_pattern", 
            name="Copy Pattern",
            description="Copy a pattern to another location",
            actions=[
                ARCAction(
                    action_type=ARCActionType.EXTRACT_PATTERN,
                    target_filter=lambda cell: cell.color != 0,
                    parameters={"region": None},  # Will be specified
                    description="Extract pattern from source region"
                ),
                ARCAction(
                    action_type=ARCActionType.APPLY_PATTERN,
                    target_filter=lambda cell: True,
                    parameters={"target_location": None},  # Will be specified
                    description="Apply pattern to target location"
                )
            ],
            preconditions=[
                lambda grid: any(cell.color != 0 for cell in grid.objects)  # Has content
            ]
        )
        self.rules["copy_pattern"] = copy_pattern_rule
        
        print(f"[ARCRuleBase] Initialized {len(self.rules)} core transformation rules")
    
    def get_rule(self, rule_id: str) -> Optional[ARCRule]:
        """Get a specific rule by ID."""
        return self.rules.get(rule_id)
    
    def find_applicable_rules(self, grid: ARCGrid) -> List[ARCRule]:
        """Find all rules that could apply to the given grid."""
        applicable = []
        for rule in self.rules.values():
            if rule.applies_to(grid):
                applicable.append(rule)
        return applicable
    
    def add_rule(self, rule: ARCRule):
        """Add a new rule to the rule base."""
        self.rules[rule.rule_id] = rule
        print(f"[ARCRuleBase] Added new rule: {rule.rule_id}")

class ARCRuleParser:
    """Phase 2 Foundation: Parser for structured ARC commands."""
    
    def __init__(self, rule_base: ARCRuleBase):
        self.rule_base = rule_base
    
    def parse_command(self, command: Dict[str, Any]) -> Optional[ARCRule]:
        """Parse a structured command into an executable rule.
        
        Example command:
        {
            'action': 'move',
            'target': 'all_blue_objects', 
            'param': 'down',
            'condition': 'until_collision'
        }
        """
        action_name = command.get('action')
        target = command.get('target')
        param = command.get('param')
        
        if action_name == 'move':
            # Create a movement rule
            target_filter = self._parse_target_filter(target)
            direction = param
            
            move_action = ARCAction(
                action_type=ARCActionType.MOVE,
                target_filter=target_filter,
                parameters={"direction": direction, "until": "collision"},
                description=f"Move {target} {direction}"
            )
            
            return ARCRule(
                rule_id=f"custom_move_{target}_{direction}",
                name=f"Move {target} {direction}",
                description=f"Move {target} in direction {direction}",
                actions=[move_action],
                preconditions=[]  # Will be inferred
            )
        
        return None
    
    def _parse_target_filter(self, target_spec: str) -> Callable[[ARCCell], bool]:
        """Convert target specification to filter function."""
        if target_spec == "all_blue_objects":
            return lambda cell: cell.color == 1  # Blue
        elif target_spec == "all_red_objects":
            return lambda cell: cell.color == 2  # Red
        elif target_spec == "all_non_black_objects":
            return lambda cell: cell.color != 0
        else:
            # Default: all objects
            return lambda cell: True

class ARCExecutionEngine:
    """Phase 2 Foundation: Engine to execute ARC transformation rules."""
    
    def __init__(self):
        self.execution_log: List[str] = []
    
    def execute_rule(self, rule: ARCRule, input_grid: ARCGrid) -> ARCGrid:
        """Execute a rule on an input grid to produce output grid."""
        self.execution_log.append(f"Executing rule: {rule.rule_id}")
        
        # Start with a copy of the input grid
        output_grid = self._copy_grid(input_grid, f"{input_grid.grid_id}_output")
        
        # Execute each action in sequence
        for action in rule.actions:
            output_grid = self._execute_action(action, output_grid)
        
        self.execution_log.append(f"Rule execution complete: {rule.rule_id}")
        return output_grid
    
    def _execute_action(self, action: ARCAction, grid: ARCGrid) -> ARCGrid:
        """Execute a single action on a grid."""
        self.execution_log.append(f"  Executing action: {action.action_type.value}")
        
        if action.action_type == ARCActionType.MOVE:
            return self._execute_move(action, grid)
        elif action.action_type == ARCActionType.CHANGE_COLOR:
            return self._execute_color_change(action, grid)
        # Add other action types as needed
        
        return grid  # No change if action not implemented
    
    def _execute_move(self, action: ARCAction, grid: ARCGrid) -> ARCGrid:
        """Execute a MOVE action."""
        direction = action.parameters.get("direction", "down")
        
        # Find cells that match the target filter
        target_cells = [cell for cell in grid.objects if action.target_filter(cell)]
        
        if direction == "down":
            # Move cells down
            for cell in target_cells:
                new_y = min(grid.height - 1, cell.y + 1)
                # Check for collisions with other objects
                while new_y < grid.height - 1:
                    collision = any(
                        other.x == cell.x and other.y == new_y + 1 and other.color != 0
                        for other in grid.objects if other != cell
                    )
                    if collision:
                        break
                    new_y += 1
                
                # Update the grid
                if new_y != cell.y:
                    # Clear old position
                    if cell.y < len(grid.cells) and cell.x < len(grid.cells[cell.y]):
                        grid.cells[cell.y][cell.x] = 0
                    # Set new position
                    if new_y < len(grid.cells) and cell.x < len(grid.cells[new_y]):
                        grid.cells[new_y][cell.x] = cell.color
                    cell.y = new_y
        
        return grid
    
    def _execute_color_change(self, action: ARCAction, grid: ARCGrid) -> ARCGrid:
        """Execute a CHANGE_COLOR action."""
        from_color = action.parameters.get("from_color", 1)
        to_color = action.parameters.get("to_color", 2)
        
        for cell in grid.objects:
            if cell.color == from_color:
                cell.color = to_color
                # Update grid cells array
                if cell.y < len(grid.cells) and cell.x < len(grid.cells[cell.y]):
                    grid.cells[cell.y][cell.x] = to_color
        
        return grid
    
    def _copy_grid(self, source: ARCGrid, new_id: str) -> ARCGrid:
        """Create a deep copy of a grid."""
        # Deep copy the cells array
        new_cells = [row[:] for row in source.cells]
        
        # Create new grid
        new_grid = ARCGrid(
            grid_id=new_id,
            width=source.width,
            height=source.height,
            cells=new_cells
        )
        
        return new_grid

# ==============================================================================
# PHASE 2 PREVIEW DEMO
# ==============================================================================

def demo_phase2_preview():
    """Demonstrate Phase 2 symbolic reasoning capabilities."""
    print("=" * 60)
    print("ALLA INITIATIVE - PHASE 2 PREVIEW")
    print("Symbolic Reasoning Engine Foundation")
    print("=" * 60)
    
    # Create rule base
    rule_base = ARCRuleBase()
    parser = ARCRuleParser(rule_base)
    executor = ARCExecutionEngine()
    
    print(f"\n[Phase 2 Preview] Rule Base initialized with {len(rule_base.rules)} rules")
    
    # Create a simple test grid
    test_grid = ARCGrid(
        grid_id="test_input",
        width=3,
        height=3,
        cells=[
            [0, 1, 0],  # Blue cell at top
            [0, 0, 0],
            [0, 0, 0]
        ]
    )
    
    print(f"\nInput Grid:")
    for row in test_grid.cells:
        print("  " + " ".join(str(cell) for cell in row))
    
    # Find applicable rules
    applicable_rules = rule_base.find_applicable_rules(test_grid)
    print(f"\nApplicable rules: {[rule.rule_id for rule in applicable_rules]}")
    
    # Execute the move_down rule
    if "move_down" in rule_base.rules:
        move_rule = rule_base.rules["move_down"]
        print(f"\nExecuting rule: {move_rule.name}")
        
        output_grid = executor.execute_rule(move_rule, test_grid)
        
        print(f"\nOutput Grid:")
        for row in output_grid.cells:
            print("  " + " ".join(str(cell) for cell in row))
        
        print(f"\nExecution Log:")
        for log_entry in executor.execution_log:
            print(f"  {log_entry}")
    
    # Test command parsing
    print(f"\n[Phase 2 Preview] Testing command parsing...")
    
    command = {
        'action': 'move',
        'target': 'all_blue_objects',
        'param': 'down'
    }
    
    parsed_rule = parser.parse_command(command)
    if parsed_rule:
        print(f"Parsed command into rule: {parsed_rule.rule_id}")
        print(f"  Description: {parsed_rule.description}")
        print(f"  Actions: {len(parsed_rule.actions)}")
    
    print(f"\n✓ Phase 2 Foundation Ready!")
    print(f"  ✓ Rule base with fundamental transformation actions")
    print(f"  ✓ Command parser for structured rule creation")
    print(f"  ✓ Execution engine for applying rules to grids")
    print(f"  ✓ Framework ready for natural language integration")

if __name__ == "__main__":
    demo_phase2_preview()
