#!/usr/bin/env python3
"""
ALLA Micro-Physics Engine - Common Sense Physical Reasoning
Simulates basic physics like gravity, collision, flow for ARC task understanding
"""

import numpy as np
from typing import Dict, List, Tuple, Any, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import logging
from visual_scene_parser import VisualObject, SceneRepresentation

logger = logging.getLogger(__name__)

class PhysicsRule(Enum):
    GRAVITY = "gravity"
    COLLISION = "collision"
    FLOW = "flow"
    MAGNETISM = "magnetism"
    BOUNCE = "bounce"
    FRICTION = "friction"
    CONTAINMENT = "containment"

@dataclass
class PhysicsState:
    """Represents the physics state of an object"""
    object_id: str
    position: Tuple[int, int]
    velocity: Tuple[float, float] = (0.0, 0.0)
    is_solid: bool = True
    is_movable: bool = True
    mass: float = 1.0
    is_container: bool = False
    is_fluid: bool = False

@dataclass
class PhysicsEvent:
    """Represents a physics event that occurred"""
    event_type: str  # "fall", "collision", "flow", "stick"
    affected_objects: List[str]
    description: str
    confidence: float
    frame: int = 0

class MicroPhysicsEngine:
    """Simulates basic physics for ARC task understanding"""
    
    def __init__(self):
        self.physics_rules = {
            PhysicsRule.GRAVITY: self._apply_gravity,
            PhysicsRule.COLLISION: self._apply_collision,
            PhysicsRule.FLOW: self._apply_flow,
            PhysicsRule.CONTAINMENT: self._apply_containment,
            PhysicsRule.BOUNCE: self._apply_bounce
        }
        
        self.simulation_history = []
        self.learned_physics_patterns = {}
    
    def simulate_physics(self, scene: SceneRepresentation, 
                        active_rules: List[PhysicsRule] = None,
                        max_steps: int = 10) -> Dict[str, Any]:
        """Simulate physics on a scene and return the result"""
        
        if active_rules is None:
            active_rules = [PhysicsRule.GRAVITY, PhysicsRule.COLLISION, PhysicsRule.CONTAINMENT]
        
        # Initialize physics states for objects
        physics_states = self._initialize_physics_states(scene)
        
        # Create working grid
        grid = self._scene_to_grid(scene)
        
        events = []
        simulation_frames = [grid.copy()]
        
        # Run simulation steps
        for step in range(max_steps):
            step_events = []
            grid_changed = False
            
            # Apply each active rule
            for rule in active_rules:
                if rule in self.physics_rules:
                    rule_events, grid, states_updated = self.physics_rules[rule](
                        grid, physics_states, step
                    )
                    step_events.extend(rule_events)
                    if states_updated:
                        grid_changed = True
            
            events.extend(step_events)
            
            if grid_changed:
                simulation_frames.append(grid.copy())
            else:
                # Simulation has stabilized
                break
        
        result = {
            'final_grid': grid,
            'simulation_frames': simulation_frames,
            'physics_events': events,
            'steps_taken': step + 1,
            'stabilized': not grid_changed,
            'physics_summary': self._summarize_physics_events(events)
        }
        
        return result
    
    def _initialize_physics_states(self, scene: SceneRepresentation) -> Dict[str, PhysicsState]:
        """Initialize physics states for all objects in scene"""
        states = {}
        
        for obj in scene.objects:
            # Determine object properties based on shape and context
            is_solid = True
            is_movable = True
            mass = float(obj.size)  # Larger objects are heavier
            is_container = self._is_container_shape(obj)
            is_fluid = False  # Could be enhanced to detect fluid-like objects
            
            states[obj.object_id] = PhysicsState(
                object_id=obj.object_id,
                position=(int(obj.center_of_mass[0]), int(obj.center_of_mass[1])),
                is_solid=is_solid,
                is_movable=is_movable,
                mass=mass,
                is_container=is_container,
                is_fluid=is_fluid
            )
        
        return states
    
    def _is_container_shape(self, obj: VisualObject) -> bool:
        """Determine if an object can act as a container"""
        # Simple heuristic: rectangles and large objects can be containers
        return (obj.shape_type in ["rectangle", "complex"] and 
                obj.compactness < 0.8 and  # Not completely filled
                obj.size > 4)  # Reasonably large
    
    def _scene_to_grid(self, scene: SceneRepresentation) -> np.ndarray:
        """Convert scene representation back to grid"""
        grid = np.zeros(scene.grid_size, dtype=int)
        
        for obj in scene.objects:
            for pos in obj.positions:
                if 0 <= pos[0] < grid.shape[0] and 0 <= pos[1] < grid.shape[1]:
                    grid[pos[0], pos[1]] = obj.color
        
        return grid
    
    def _apply_gravity(self, grid: np.ndarray, states: Dict[str, PhysicsState], 
                      step: int) -> Tuple[List[PhysicsEvent], np.ndarray, bool]:
        """Apply gravity - objects fall down until they hit something"""
        events = []
        grid_changed = False
        new_grid = grid.copy()
        
        # Process objects from bottom to top to avoid conflicts
        movable_objects = []
        
        # Find all movable colored pixels
        for row in range(grid.shape[0] - 1, -1, -1):
            for col in range(grid.shape[1]):
                if grid[row, col] != 0:
                    # Check if this pixel can fall
                    if self._can_fall(grid, row, col):
                        movable_objects.append((row, col, grid[row, col]))
        
        # Apply gravity to movable objects
        for row, col, color in movable_objects:
            # Find how far this pixel can fall
            fall_distance = self._calculate_fall_distance(grid, row, col)
            
            if fall_distance > 0:
                new_row = row + fall_distance
                
                # Clear original position
                new_grid[row, col] = 0
                
                # Set new position
                new_grid[new_row, col] = color
                
                grid_changed = True
                
                events.append(PhysicsEvent(
                    event_type="fall",
                    affected_objects=[f"pixel_{row}_{col}"],
                    description=f"Object fell {fall_distance} units",
                    confidence=0.9,
                    frame=step
                ))
        
        return events, new_grid, grid_changed
    
    def _can_fall(self, grid: np.ndarray, row: int, col: int) -> bool:
        """Check if a pixel can fall down"""
        # Can't fall if at bottom
        if row >= grid.shape[0] - 1:
            return False
        
        # Can fall if space below is empty
        return grid[row + 1, col] == 0
    
    def _calculate_fall_distance(self, grid: np.ndarray, row: int, col: int) -> int:
        """Calculate how far an object can fall"""
        distance = 0
        current_row = row
        
        while (current_row + 1 < grid.shape[0] and 
               grid[current_row + 1, col] == 0):
            distance += 1
            current_row += 1
        
        return distance
    
    def _apply_collision(self, grid: np.ndarray, states: Dict[str, PhysicsState], 
                        step: int) -> Tuple[List[PhysicsEvent], np.ndarray, bool]:
        """Apply collision detection and response"""
        events = []
        
        # For now, collision is mostly handled by gravity stopping
        # Could be enhanced for lateral collisions
        
        return events, grid, False
    
    def _apply_flow(self, grid: np.ndarray, states: Dict[str, PhysicsState], 
                   step: int) -> Tuple[List[PhysicsEvent], np.ndarray, bool]:
        """Apply fluid flow dynamics"""
        events = []
        grid_changed = False
        new_grid = grid.copy()
        
        # Simple water-like flow: pixels try to spread horizontally at the bottom
        for row in range(grid.shape[0] - 1, -1, -1):
            for col in range(grid.shape[1]):
                if grid[row, col] != 0:
                    # Check if this pixel is "fluid-like" (isolated or bottom of column)
                    if self._is_fluid_pixel(grid, row, col):
                        # Try to flow left or right
                        flow_applied = self._apply_horizontal_flow(new_grid, row, col)
                        if flow_applied:
                            grid_changed = True
                            events.append(PhysicsEvent(
                                event_type="flow",
                                affected_objects=[f"pixel_{row}_{col}"],
                                description="Fluid flow occurred",
                                confidence=0.7,
                                frame=step
                            ))
        
        return events, new_grid, grid_changed
    
    def _is_fluid_pixel(self, grid: np.ndarray, row: int, col: int) -> bool:
        """Check if a pixel behaves like fluid"""
        # Simple heuristic: if it's at the bottom of its column or isolated
        if row == grid.shape[0] - 1:
            return True  # Bottom row
        
        if grid[row + 1, col] == 0:
            return True  # Floating pixel
        
        return False
    
    def _apply_horizontal_flow(self, grid: np.ndarray, row: int, col: int) -> bool:
        """Apply horizontal flow for a pixel"""
        color = grid[row, col]
        
        # Check left and right neighbors
        can_flow_left = col > 0 and grid[row, col - 1] == 0
        can_flow_right = col < grid.shape[1] - 1 and grid[row, col + 1] == 0
        
        if can_flow_left and can_flow_right:
            # Choose randomly or based on some logic
            direction = -1 if np.random.random() < 0.5 else 1
        elif can_flow_left:
            direction = -1
        elif can_flow_right:
            direction = 1
        else:
            return False
        
        # Apply flow
        new_col = col + direction
        grid[row, col] = 0
        grid[row, new_col] = color
        
        return True
    
    def _apply_containment(self, grid: np.ndarray, states: Dict[str, PhysicsState], 
                          step: int) -> Tuple[List[PhysicsEvent], np.ndarray, bool]:
        """Apply containment physics - objects stay within containers"""
        events = []
        
        # This would involve more complex logic to detect containers
        # and ensure objects don't escape them
        
        return events, grid, False
    
    def _apply_bounce(self, grid: np.ndarray, states: Dict[str, PhysicsState], 
                     step: int) -> Tuple[List[PhysicsEvent], np.ndarray, bool]:
        """Apply bounce physics"""
        events = []
        
        # Simple bounce could reverse direction when hitting walls
        # This is a placeholder for more sophisticated bounce physics
        
        return events, grid, False
    
    def _summarize_physics_events(self, events: List[PhysicsEvent]) -> Dict[str, Any]:
        """Summarize physics events for analysis"""
        if not events:
            return {"total_events": 0, "event_types": {}, "dominant_physics": "static"}
        
        event_counts = {}
        for event in events:
            event_type = event.event_type
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        dominant_physics = max(event_counts.keys(), key=lambda x: event_counts[x])
        
        return {
            "total_events": len(events),
            "event_types": event_counts,
            "dominant_physics": dominant_physics,
            "average_confidence": sum(e.confidence for e in events) / len(events),
            "physics_active": len(events) > 0
        }
    
    def predict_physics_outcome(self, initial_grid: np.ndarray, 
                               transformation_rules: List[str]) -> np.ndarray:
        """Predict the outcome of applying physics to a grid"""
        
        # Determine which physics rules to apply based on transformation context
        active_rules = []
        
        if any("fall" in rule or "gravity" in rule for rule in transformation_rules):
            active_rules.append(PhysicsRule.GRAVITY)
        
        if any("flow" in rule or "spread" in rule for rule in transformation_rules):
            active_rules.append(PhysicsRule.FLOW)
        
        if any("bounce" in rule or "collision" in rule for rule in transformation_rules):
            active_rules.append(PhysicsRule.BOUNCE)
        
        # If no specific rules, apply gravity as default
        if not active_rules:
            active_rules = [PhysicsRule.GRAVITY]
        
        # Create a temporary scene for simulation
        temp_scene = self._grid_to_temp_scene(initial_grid)
        
        # Run simulation
        result = self.simulate_physics(temp_scene, active_rules)
        
        return result['final_grid']
    
    def _grid_to_temp_scene(self, grid: np.ndarray) -> SceneRepresentation:
        """Convert grid to temporary scene for physics simulation"""
        # This is a simplified conversion - in practice, you'd use the visual parser
        from visual_scene_parser import VisualSceneParser
        
        parser = VisualSceneParser()
        return parser.parse_grid_to_scene(grid, "temp_physics_scene")
    
    def analyze_physics_requirements(self, input_grid: np.ndarray, 
                                   output_grid: np.ndarray) -> List[PhysicsRule]:
        """Analyze what physics rules might be needed to get from input to output"""
        required_rules = []
        
        # Check for gravity patterns
        if self._requires_gravity(input_grid, output_grid):
            required_rules.append(PhysicsRule.GRAVITY)
        
        # Check for flow patterns
        if self._requires_flow(input_grid, output_grid):
            required_rules.append(PhysicsRule.FLOW)
        
        # Check for collision patterns
        if self._requires_collision(input_grid, output_grid):
            required_rules.append(PhysicsRule.COLLISION)
        
        return required_rules
    
    def _requires_gravity(self, input_grid: np.ndarray, output_grid: np.ndarray) -> bool:
        """Check if gravity is needed to explain the transformation"""
        # Simple heuristic: objects moved downward
        input_objects = np.where(input_grid != 0)
        output_objects = np.where(output_grid != 0)
        
        if len(input_objects[0]) == 0 or len(output_objects[0]) == 0:
            return False
        
        input_center_y = np.mean(input_objects[0])
        output_center_y = np.mean(output_objects[0])
        
        # If overall center of mass moved down significantly
        return output_center_y > input_center_y + 0.5
    
    def _requires_flow(self, input_grid: np.ndarray, output_grid: np.ndarray) -> bool:
        """Check if flow is needed to explain the transformation"""
        # Simple heuristic: objects spread horizontally while moving down
        input_width = self._calculate_horizontal_spread(input_grid)
        output_width = self._calculate_horizontal_spread(output_grid)
        
        return output_width > input_width * 1.2
    
    def _requires_collision(self, input_grid: np.ndarray, output_grid: np.ndarray) -> bool:
        """Check if collision is needed to explain the transformation"""
        # Simple heuristic: objects stopped moving (stabilized at bottom)
        if output_grid.shape[0] == 0:
            return False
        
        # Check if objects are at bottom row
        bottom_row_input = np.sum(input_grid[-1, :] != 0)
        bottom_row_output = np.sum(output_grid[-1, :] != 0)
        
        return bottom_row_output > bottom_row_input
    
    def _calculate_horizontal_spread(self, grid: np.ndarray) -> float:
        """Calculate horizontal spread of objects in grid"""
        objects = np.where(grid != 0)
        if len(objects[1]) == 0:
            return 0.0
        
        return float(np.max(objects[1]) - np.min(objects[1]) + 1)
    
    def create_physics_explanation(self, events: List[PhysicsEvent]) -> str:
        """Create human-readable explanation of physics events"""
        if not events:
            return "No physics interactions detected - static scene"
        
        explanations = []
        event_counts = {}
        
        for event in events:
            event_type = event.event_type
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        for event_type, count in event_counts.items():
            if event_type == "fall":
                explanations.append(f"Objects fell due to gravity ({count} instances)")
            elif event_type == "flow":
                explanations.append(f"Fluid-like spreading occurred ({count} instances)")
            elif event_type == "collision":
                explanations.append(f"Collision interactions happened ({count} instances)")
        
        return "; ".join(explanations)

def main():
    """Test the micro-physics engine"""
    engine = MicroPhysicsEngine()
    
    # Test with falling objects
    test_grid = np.array([
        [0, 1, 0, 2],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ])
    
    # Create temporary scene
    temp_scene = engine._grid_to_temp_scene(test_grid)
    
    # Simulate physics
    result = engine.simulate_physics(temp_scene, [PhysicsRule.GRAVITY])
    
    print("🌍 Micro-Physics Engine Test")
    print(f"Initial grid:")
    print(test_grid)
    print(f"\nFinal grid after physics:")
    print(result['final_grid'])
    print(f"\nPhysics events: {len(result['physics_events'])}")
    
    for event in result['physics_events']:
        print(f"  - {event.event_type}: {event.description}")
    
    print(f"\nPhysics summary: {result['physics_summary']}")

if __name__ == "__main__":
    main()
