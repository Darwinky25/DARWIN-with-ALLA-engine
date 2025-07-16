# ==============================================================================
# ARC_CORE.PY - ALLA Initiative Phase 1: Core Language & Scene Understanding
# ==============================================================================
# This module extends the existing ALLA engine with ARC-specific capabilities
# Built on top of ALLA v16.0's proven cognitive architecture

import json
import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass, field
from pathlib import Path

# Import existing ALLA components
from alla_engine import AllaEngine, SemanticNode, SemanticEdge
from world import WorldObject, Event

# ==============================================================================
# PHASE 1: ARC-SPECIFIC DATA STRUCTURES
# ==============================================================================

@dataclass
class ARCCell:
    """Represents a single cell in an ARC grid - extends WorldObject for ARC tasks."""
    x: int                    # Grid X coordinate (0-based)
    y: int                    # Grid Y coordinate (0-based) 
    color: int                # ARC color (0-9, where 0=black)
    grid_id: str              # Which grid this cell belongs to ("input_1", "output_1", etc.)
    
    # Extended properties for pattern recognition
    neighbors: List[Tuple[int, int]] = field(default_factory=list)
    is_edge: bool = False     # True if on grid boundary
    cluster_id: Optional[int] = None  # For grouping connected components
    
    def to_world_object(self) -> WorldObject:
        """Convert ARC cell to ALLA WorldObject for compatibility."""
        # Map ARC colors (0-9) to color names
        color_map = {
            0: 'black', 1: 'blue', 2: 'red', 3: 'green', 4: 'yellow',
            5: 'grey', 6: 'magenta', 7: 'orange', 8: 'cyan', 9: 'brown'
        }
        
        return WorldObject(
            id=hash(f"cell_{self.grid_id}_{self.x}_{self.y}"),  # Generate unique ID
            name=f"cell_at_{self.x}_{self.y}",
            shape='square',  # All ARC cells are squares
            color=color_map.get(self.color, 'unknown'),
            position=(self.x, self.y),  # 2D position as tuple
            size=1,
            material='grid_cell',
            weight=1,  # Required parameter
            hp=1,      # Required parameter
            owner='world'
        )

@dataclass 
class ARCGrid:
    """Represents a complete ARC grid (input or output)."""
    grid_id: str              # "input_1", "output_1", etc.
    width: int
    height: int
    cells: List[List[int]]    # 2D array of color values
    objects: List[ARCCell] = field(default_factory=list)
    
    def __post_init__(self):
        """Parse the grid into ARCCell objects."""
        self.objects = []
        for y in range(self.height):
            for x in range(self.width):
                if y < len(self.cells) and x < len(self.cells[y]):
                    color = self.cells[y][x]
                    cell = ARCCell(
                        x=x, y=y, color=color, grid_id=self.grid_id,
                        is_edge=(x == 0 or x == self.width-1 or y == 0 or y == self.height-1)
                    )
                    self.objects.append(cell)
    
    def get_cell(self, x: int, y: int) -> Optional[ARCCell]:
        """Get cell at specific coordinates."""
        for cell in self.objects:
            if cell.x == x and cell.y == y:
                return cell
        return None
    
    def get_non_black_cells(self) -> List[ARCCell]:
        """Get all cells that are not black (color != 0)."""
        return [cell for cell in self.objects if cell.color != 0]
    
    def find_connected_components(self) -> List[List[ARCCell]]:
        """Find groups of connected cells with the same color."""
        components = []
        visited = set()
        
        for cell in self.get_non_black_cells():
            if (cell.x, cell.y) not in visited:
                component = self._flood_fill(cell, visited)
                if component:
                    components.append(component)
        
        return components
    
    def _flood_fill(self, start_cell: ARCCell, visited: set) -> List[ARCCell]:
        """Flood fill algorithm to find connected component."""
        component = []
        stack = [start_cell]
        
        while stack:
            cell = stack.pop()
            if (cell.x, cell.y) in visited:
                continue
                
            visited.add((cell.x, cell.y))
            component.append(cell)
            
            # Check 4-connected neighbors
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = cell.x + dx, cell.y + dy
                neighbor = self.get_cell(nx, ny)
                if (neighbor and neighbor.color == cell.color and 
                    (nx, ny) not in visited):
                    stack.append(neighbor)
        
        return component

@dataclass
class ARCTask:
    """Represents a complete ARC task with training and test examples."""
    task_id: str
    train_inputs: List[ARCGrid] = field(default_factory=list)
    train_outputs: List[ARCGrid] = field(default_factory=list) 
    test_inputs: List[ARCGrid] = field(default_factory=list)
    test_outputs: List[ARCGrid] = field(default_factory=list)  # Usually empty
    
    @classmethod
    def from_json(cls, json_data: Dict[str, Any], task_id: str = "unknown") -> 'ARCTask':
        """Create ARCTask from standard ARC JSON format."""
        task = cls(task_id=task_id)
        
        # Parse training examples
        for i, example in enumerate(json_data.get('train', [])):
            input_grid = ARCGrid(
                grid_id=f"train_input_{i}",
                width=len(example['input'][0]) if example['input'] else 0,
                height=len(example['input']),
                cells=example['input']
            )
            output_grid = ARCGrid(
                grid_id=f"train_output_{i}",
                width=len(example['output'][0]) if example['output'] else 0,
                height=len(example['output']),
                cells=example['output']
            )
            task.train_inputs.append(input_grid)
            task.train_outputs.append(output_grid)
        
        # Parse test examples
        for i, example in enumerate(json_data.get('test', [])):
            input_grid = ARCGrid(
                grid_id=f"test_input_{i}",
                width=len(example['input'][0]) if example['input'] else 0,
                height=len(example['input']),
                cells=example['input']
            )
            task.test_inputs.append(input_grid)
            
            # Test outputs might not be provided
            if 'output' in example:
                output_grid = ARCGrid(
                    grid_id=f"test_output_{i}",
                    width=len(example['output'][0]) if example['output'] else 0,
                    height=len(example['output']),
                    cells=example['output']
                )
                task.test_outputs.append(output_grid)
        
        return task

# ==============================================================================
# PHASE 1: SCENE PARSER - THE AI'S "EYES"
# ==============================================================================

class ARCSceneParser:
    """Converts ARC grids into ALLA's internal WorldObject representation."""
    
    def __init__(self, alla_engine: AllaEngine):
        self.alla = alla_engine
        self.color_concepts = {
            0: 'black', 1: 'blue', 2: 'red', 3: 'green', 4: 'yellow',
            5: 'grey', 6: 'magenta', 7: 'orange', 8: 'cyan', 9: 'brown'
        }
    
    def parse_grid(self, grid: ARCGrid) -> List[WorldObject]:
        """Convert ARCGrid to list of WorldObjects that ALLA can understand."""
        world_objects = []
        
        for cell in grid.objects:
            # Skip black cells (background) unless specifically needed
            if cell.color == 0:
                continue
                
            world_obj = cell.to_world_object()
            world_objects.append(world_obj)
            
            # Ensure ALLA knows about this color
            self._ensure_color_concept(cell.color)
        
        return world_objects
    
    def parse_task(self, task: ARCTask) -> Dict[str, List[WorldObject]]:
        """Parse entire ARC task into ALLA-compatible format."""
        parsed = {}
        
        # Parse training examples
        for i, (input_grid, output_grid) in enumerate(zip(task.train_inputs, task.train_outputs)):
            parsed[f"train_input_{i}"] = self.parse_grid(input_grid)
            parsed[f"train_output_{i}"] = self.parse_grid(output_grid)
        
        # Parse test examples
        for i, input_grid in enumerate(task.test_inputs):
            parsed[f"test_input_{i}"] = self.parse_grid(input_grid)
            
        for i, output_grid in enumerate(task.test_outputs):
            parsed[f"test_output_{i}"] = self.parse_grid(output_grid)
            
        return parsed
    
    def _ensure_color_concept(self, arc_color: int):
        """Make sure ALLA understands this ARC color."""
        color_name = self.color_concepts.get(arc_color, 'unknown')
        
        # Check if ALLA already knows this color
        if not self.alla.lexicon.get_entry(color_name):
            # Teach ALLA about this color
            expression = f"obj.color == '{color_name}'"
            self.alla._teach_word(color_name, 'property', expression)
            print(f"[ARC Parser] Taught ALLA about color: {color_name}")

# ==============================================================================
# PHASE 1: KNOWLEDGE BOOTSTRAP
# ==============================================================================

class ARCKnowledgeBootstrap:
    """Creates the initial knowledge graph for ARC reasoning."""
    
    def __init__(self, alla_engine: AllaEngine):
        self.alla = alla_engine
    
    def bootstrap_arc_concepts(self):
        """Add core ARC concepts to ALLA's semantic memory."""
        print("[ARC Bootstrap] Adding core ARC concepts to ALLA's knowledge...")
        
        # Core spatial concepts
        spatial_concepts = [
            ("up", "property", "obj.position[1] < reference.position[1]"),
            ("down", "property", "obj.position[1] > reference.position[1]"),
            ("left", "property", "obj.position[0] < reference.position[0]"),
            ("right", "property", "obj.position[0] > reference.position[0]"),
            ("adjacent", "relation", "abs(obj1.position[0] - obj2.position[0]) + abs(obj1.position[1] - obj2.position[1]) == 1"),
            ("diagonal", "relation", "abs(obj1.position[0] - obj2.position[0]) == 1 and abs(obj1.position[1] - obj2.position[1]) == 1"),
        ]
        
        # ARC-specific concepts
        arc_concepts = [
            ("grid_cell", "noun", "obj.material == 'grid_cell'"),
            ("pattern", "noun", "obj.cluster_id is not None"),
            ("background", "property", "obj.color == 'black'"),
            ("foreground", "property", "obj.color != 'black'"),
        ]
        
        all_concepts = spatial_concepts + arc_concepts
        
        for word, word_type, expression in all_concepts:
            try:
                self.alla._teach_word(word, word_type, expression)
                print(f"  ✓ Added concept: {word}")
            except Exception as e:
                print(f"  ✗ Failed to add {word}: {e}")
        
        # Add semantic memory nodes for abstract concepts
        self._add_semantic_concepts()
        
        print("[ARC Bootstrap] Core ARC knowledge added successfully!")
    
    def _add_semantic_concepts(self):
        """Add abstract concepts to semantic memory."""
        concepts = [
            SemanticNode("concept:spatial_relation", "category", "spatial_relation", 1),
            SemanticNode("concept:color_property", "category", "color_property", 1),
            SemanticNode("concept:grid_structure", "category", "grid_structure", 1),
            SemanticNode("concept:transformation", "category", "transformation", 1),
        ]
        
        for concept in concepts:
            self.alla.semantic_memory.add_node(concept)
        
        # Add relationships
        edges = [
            SemanticEdge("concept:up", "concept:spatial_relation", "is_type_of"),
            SemanticEdge("concept:down", "concept:spatial_relation", "is_type_of"),
            SemanticEdge("concept:left", "concept:spatial_relation", "is_type_of"),
            SemanticEdge("concept:right", "concept:spatial_relation", "is_type_of"),
        ]
        
        for edge in edges:
            self.alla.semantic_memory.add_edge(edge)

# ==============================================================================
# PHASE 1: INTEGRATION - ARC-ENHANCED ALLA ENGINE
# ==============================================================================

class ARCAllaEngine(AllaEngine):
    """Enhanced ALLA engine with ARC capabilities."""
    
    def __init__(self, memory_path: str = "arc_alla_memory.json"):
        super().__init__(memory_path)
        
        # ARC-specific components
        self.scene_parser = ARCSceneParser(self)
        self.knowledge_bootstrap = ARCKnowledgeBootstrap(self)
        self.current_task: Optional[ARCTask] = None
        self.parsed_scenes: Dict[str, List[WorldObject]] = {}
        
        # Bootstrap ARC knowledge
        self.knowledge_bootstrap.bootstrap_arc_concepts()
        
        print("[ARCAllaEngine] ARC capabilities initialized!")
    
    def load_arc_task(self, task_path: Path) -> ARCTask:
        """Load an ARC task from JSON file."""
        print(f"[ARCAllaEngine] Loading ARC task from: {task_path}")
        
        with open(task_path, 'r') as f:
            task_data = json.load(f)
        
        task = ARCTask.from_json(task_data, str(task_path.stem))
        self.current_task = task
        
        # Parse all grids in the task
        self.parsed_scenes = self.scene_parser.parse_task(task)
        
        print(f"[ARCAllaEngine] Loaded task with {len(task.train_inputs)} training examples")
        return task
    
    def analyze_current_task(self) -> Dict[str, Any]:
        """Analyze the currently loaded ARC task."""
        if not self.current_task:
            return {"error": "No task loaded"}
        
        analysis = {
            "task_id": self.current_task.task_id,
            "training_examples": len(self.current_task.train_inputs),
            "test_examples": len(self.current_task.test_inputs),
            "grid_sizes": [],
            "colors_used": set(),
            "pattern_analysis": {}
        }
        
        # Analyze each training example
        for i, input_grid in enumerate(self.current_task.train_inputs):
            analysis["grid_sizes"].append({
                "input": (input_grid.width, input_grid.height),
                "output": (self.current_task.train_outputs[i].width, self.current_task.train_outputs[i].height)
            })
            
            # Collect colors used
            for cell in input_grid.objects:
                analysis["colors_used"].add(cell.color)
            for cell in self.current_task.train_outputs[i].objects:
                analysis["colors_used"].add(cell.color)
        
        analysis["colors_used"] = list(analysis["colors_used"])
        return analysis
    
    def visualize_grid(self, grid: ARCGrid) -> str:
        """Create a text visualization of an ARC grid."""
        if not grid.cells:
            return "Empty grid"
        
        viz = f"Grid: {grid.grid_id} ({grid.width}x{grid.height})\n"
        for row in grid.cells:
            viz += " ".join(str(cell) for cell in row) + "\n"
        return viz

def save_knowledge_bootstrap(file_path: Path):
    """Save the initial ARC knowledge graph to JSON."""
    bootstrap_knowledge = {
        "spatial_concepts": {
            "up": {"type": "property", "expression": "obj.position[1] < reference.position[1]"},
            "down": {"type": "property", "expression": "obj.position[1] > reference.position[1]"},
            "left": {"type": "property", "expression": "obj.position[0] < reference.position[0]"},
            "right": {"type": "property", "expression": "obj.position[0] > reference.position[0]"},
            "adjacent": {"type": "relation", "expression": "abs(obj1.position[0] - obj2.position[0]) + abs(obj1.position[1] - obj2.position[1]) == 1"},
        },
        "arc_concepts": {
            "grid_cell": {"type": "noun", "expression": "obj.material == 'grid_cell'"},
            "pattern": {"type": "noun", "expression": "obj.cluster_id is not None"},
            "background": {"type": "property", "expression": "obj.color == 'black'"},
            "foreground": {"type": "property", "expression": "obj.color != 'black'"},
        },
        "colors": {
            "black": {"type": "property", "expression": "obj.color == 'black'"},
            "blue": {"type": "property", "expression": "obj.color == 'blue'"},
            "red": {"type": "property", "expression": "obj.color == 'red'"},
            "green": {"type": "property", "expression": "obj.color == 'green'"},
            "yellow": {"type": "property", "expression": "obj.color == 'yellow'"},
            "grey": {"type": "property", "expression": "obj.color == 'grey'"},
            "magenta": {"type": "property", "expression": "obj.color == 'magenta'"},
            "orange": {"type": "property", "expression": "obj.color == 'orange'"},
            "cyan": {"type": "property", "expression": "obj.color == 'cyan'"},
            "brown": {"type": "property", "expression": "obj.color == 'brown'"},
        }
    }
    
    with open(file_path, 'w') as f:
        json.dump(bootstrap_knowledge, f, indent=2)
    
    print(f"[ARC Bootstrap] Knowledge saved to: {file_path}")

if __name__ == "__main__":
    # Create bootstrap knowledge file
    save_knowledge_bootstrap(Path("knowledge_graph.json"))
    print("Phase 1 implementation complete!")
