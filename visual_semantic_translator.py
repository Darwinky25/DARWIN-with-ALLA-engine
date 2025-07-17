#!/usr/bin/env python3
"""
ALLA Visual-Semantic Translator
Converts visual grid patterns into semantic language that ALLA can reason with.
"""

import json
import numpy as np
import os
import logging
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, field
from collections import defaultdict
import cv2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class VisualObject:
    """Represents a visual object with semantic properties"""
    id: str
    color: str
    shape: str
    size: Tuple[int, int]
    position: Tuple[int, int]
    bounding_box: Tuple[int, int, int, int]  # (min_row, min_col, max_row, max_col)
    properties: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SpatialRelation:
    """Represents spatial relationship between objects"""
    relation_type: str  # 'above', 'below', 'left_of', 'right_of', 'inside', 'outside', 'adjacent'
    object1_id: str
    object2_id: str
    distance: float = 0.0
    confidence: float = 1.0

@dataclass
class SemanticGrid:
    """Semantic representation of a visual grid"""
    grid_id: str
    dimensions: Tuple[int, int]
    objects: List[VisualObject] = field(default_factory=list)
    relations: List[SpatialRelation] = field(default_factory=list)
    global_properties: Dict[str, Any] = field(default_factory=dict)
    semantic_description: str = ""

class VisualSemanticTranslator:
    """Translates visual grids into semantic representations"""
    
    def __init__(self):
        self.color_names = {
            0: 'black', 1: 'blue', 2: 'red', 3: 'green', 4: 'yellow',
            5: 'grey', 6: 'pink', 7: 'orange', 8: 'cyan', 9: 'brown'
        }
        
        self.shape_classifiers = {
            'single_pixel': lambda positions: len(positions) == 1,
            'horizontal_line': lambda positions: self._is_horizontal_line(positions),
            'vertical_line': lambda positions: self._is_vertical_line(positions),
            'diagonal_line': lambda positions: self._is_diagonal_line(positions),
            'rectangle': lambda positions: self._is_rectangle(positions),
            'square': lambda positions: self._is_square(positions),
            'l_shape': lambda positions: self._is_l_shape(positions),
            'cross': lambda positions: self._is_cross(positions),
            'complex_shape': lambda positions: True  # fallback
        }
    
    def translate_grid_to_semantic(self, grid: np.ndarray, grid_id: str = "") -> SemanticGrid:
        """Translate visual grid to semantic representation"""
        semantic_grid = SemanticGrid(
            grid_id=grid_id,
            dimensions=grid.shape
        )
        
        # Extract objects
        semantic_grid.objects = self._extract_semantic_objects(grid)
        
        # Analyze spatial relations
        semantic_grid.relations = self._analyze_spatial_relations(semantic_grid.objects)
        
        # Extract global properties
        semantic_grid.global_properties = self._extract_global_properties(grid, semantic_grid.objects)
        
        # Generate semantic description
        semantic_grid.semantic_description = self._generate_semantic_description(semantic_grid)
        
        return semantic_grid
    
    def _extract_semantic_objects(self, grid: np.ndarray) -> List[VisualObject]:
        """Extract semantic objects from grid"""
        objects = []
        object_id = 0
        
        # Find connected components for each color
        for color_value in np.unique(grid):
            if color_value == 0:  # Skip background
                continue
            
            color_mask = (grid == color_value)
            connected_components = self._find_connected_components(color_mask)
            
            for component in connected_components:
                if len(component) == 0:
                    continue
                
                # Create visual object
                obj = VisualObject(
                    id=f"obj_{object_id}",
                    color=self.color_names.get(color_value, f"color_{color_value}"),
                    shape=self._classify_shape(component),
                    size=self._calculate_size(component),
                    position=self._calculate_center_position(component),
                    bounding_box=self._calculate_bounding_box(component),
                    properties=self._extract_object_properties(component, grid)
                )
                
                objects.append(obj)
                object_id += 1
        
        return objects
    
    def _find_connected_components(self, mask: np.ndarray) -> List[List[Tuple[int, int]]]:
        """Find connected components in binary mask"""
        visited = np.zeros_like(mask, dtype=bool)
        components = []
        
        for i in range(mask.shape[0]):
            for j in range(mask.shape[1]):
                if mask[i, j] and not visited[i, j]:
                    component = []
                    self._dfs_component(mask, i, j, visited, component)
                    if component:
                        components.append(component)
        
        return components
    
    def _dfs_component(self, mask: np.ndarray, row: int, col: int, 
                      visited: np.ndarray, component: List[Tuple[int, int]]):
        """DFS to find connected component"""
        if (row < 0 or row >= mask.shape[0] or col < 0 or col >= mask.shape[1] or
            visited[row, col] or not mask[row, col]):
            return
        
        visited[row, col] = True
        component.append((row, col))
        
        # Check 4-connected neighbors
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            self._dfs_component(mask, row + dr, col + dc, visited, component)
    
    def _classify_shape(self, positions: List[Tuple[int, int]]) -> str:
        """Classify shape based on positions"""
        for shape_name, classifier in self.shape_classifiers.items():
            if classifier(positions):
                return shape_name
        return 'complex_shape'
    
    def _is_horizontal_line(self, positions: List[Tuple[int, int]]) -> bool:
        """Check if positions form a horizontal line"""
        if len(positions) < 2:
            return False
        
        rows = [pos[0] for pos in positions]
        cols = [pos[1] for pos in positions]
        
        # All same row, consecutive columns
        if len(set(rows)) == 1:
            cols_sorted = sorted(cols)
            return all(cols_sorted[i+1] - cols_sorted[i] == 1 for i in range(len(cols_sorted)-1))
        
        return False
    
    def _is_vertical_line(self, positions: List[Tuple[int, int]]) -> bool:
        """Check if positions form a vertical line"""
        if len(positions) < 2:
            return False
        
        rows = [pos[0] for pos in positions]
        cols = [pos[1] for pos in positions]
        
        # All same column, consecutive rows
        if len(set(cols)) == 1:
            rows_sorted = sorted(rows)
            return all(rows_sorted[i+1] - rows_sorted[i] == 1 for i in range(len(rows_sorted)-1))
        
        return False
    
    def _is_diagonal_line(self, positions: List[Tuple[int, int]]) -> bool:
        """Check if positions form a diagonal line"""
        if len(positions) < 2:
            return False
        
        # Check if all positions lie on a diagonal
        positions_sorted = sorted(positions)
        first_pos = positions_sorted[0]
        
        # Check positive diagonal (top-left to bottom-right)
        positive_diag = all(
            pos[0] - first_pos[0] == pos[1] - first_pos[1] 
            for pos in positions_sorted
        )
        
        # Check negative diagonal (top-right to bottom-left)
        negative_diag = all(
            pos[0] - first_pos[0] == -(pos[1] - first_pos[1]) 
            for pos in positions_sorted
        )
        
        return positive_diag or negative_diag
    
    def _is_rectangle(self, positions: List[Tuple[int, int]]) -> bool:
        """Check if positions form a rectangle"""
        if len(positions) < 4:
            return False
        
        rows = [pos[0] for pos in positions]
        cols = [pos[1] for pos in positions]
        
        min_row, max_row = min(rows), max(rows)
        min_col, max_col = min(cols), max(cols)
        
        # Check if it's a filled rectangle
        expected_positions = set()
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                expected_positions.add((r, c))
        
        return set(positions) == expected_positions
    
    def _is_square(self, positions: List[Tuple[int, int]]) -> bool:
        """Check if positions form a square"""
        if not self._is_rectangle(positions):
            return False
        
        rows = [pos[0] for pos in positions]
        cols = [pos[1] for pos in positions]
        
        height = max(rows) - min(rows) + 1
        width = max(cols) - min(cols) + 1
        
        return height == width
    
    def _is_l_shape(self, positions: List[Tuple[int, int]]) -> bool:
        """Check if positions form an L shape"""
        if len(positions) < 3:
            return False
        
        # Simple L-shape detection - check for corner pattern
        rows = [pos[0] for pos in positions]
        cols = [pos[1] for pos in positions]
        
        # L-shape should have positions forming two perpendicular lines meeting at a corner
        # This is a simplified implementation
        return len(set(rows)) > 1 and len(set(cols)) > 1 and len(positions) < 10
    
    def _is_cross(self, positions: List[Tuple[int, int]]) -> bool:
        """Check if positions form a cross shape"""
        if len(positions) < 5:
            return False
        
        # Find center position(s)
        rows = [pos[0] for pos in positions]
        cols = [pos[1] for pos in positions]
        
        # Simple cross detection - check for intersection pattern
        center_candidates = []
        for pos in positions:
            # Count how many positions are in same row or column
            same_row = sum(1 for p in positions if p[0] == pos[0])
            same_col = sum(1 for p in positions if p[1] == pos[1])
            
            if same_row >= 2 and same_col >= 2:
                center_candidates.append(pos)
        
        return len(center_candidates) > 0
    
    def _calculate_size(self, positions: List[Tuple[int, int]]) -> Tuple[int, int]:
        """Calculate bounding box size"""
        if not positions:
            return (0, 0)
        
        rows = [pos[0] for pos in positions]
        cols = [pos[1] for pos in positions]
        
        height = max(rows) - min(rows) + 1
        width = max(cols) - min(cols) + 1
        
        return (height, width)
    
    def _calculate_center_position(self, positions: List[Tuple[int, int]]) -> Tuple[int, int]:
        """Calculate center position"""
        if not positions:
            return (0, 0)
        
        avg_row = sum(pos[0] for pos in positions) / len(positions)
        avg_col = sum(pos[1] for pos in positions) / len(positions)
        
        return (int(round(avg_row)), int(round(avg_col)))
    
    def _calculate_bounding_box(self, positions: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
        """Calculate bounding box (min_row, min_col, max_row, max_col)"""
        if not positions:
            return (0, 0, 0, 0)
        
        rows = [pos[0] for pos in positions]
        cols = [pos[1] for pos in positions]
        
        return (min(rows), min(cols), max(rows), max(cols))
    
    def _extract_object_properties(self, positions: List[Tuple[int, int]], 
                                 grid: np.ndarray) -> Dict[str, Any]:
        """Extract additional object properties"""
        properties = {}
        
        # Density (how filled the bounding box is)
        bbox = self._calculate_bounding_box(positions)
        bbox_area = (bbox[2] - bbox[0] + 1) * (bbox[3] - bbox[1] + 1)
        properties['density'] = len(positions) / bbox_area if bbox_area > 0 else 0
        
        # Compactness
        properties['compactness'] = self._calculate_compactness(positions)
        
        # Edge touching
        properties['touches_edge'] = self._touches_grid_edge(positions, grid.shape)
        
        # Corner position
        properties['in_corner'] = self._in_corner(positions, grid.shape)
        
        return properties
    
    def _calculate_compactness(self, positions: List[Tuple[int, int]]) -> float:
        """Calculate shape compactness (0-1, where 1 is most compact)"""
        if len(positions) <= 1:
            return 1.0
        
        # Simple compactness measure: ratio of area to perimeter squared
        area = len(positions)
        perimeter = self._calculate_perimeter(positions)
        
        if perimeter == 0:
            return 1.0
        
        # Normalize by circle compactness formula
        compactness = 4 * np.pi * area / (perimeter ** 2)
        return min(1.0, compactness)
    
    def _calculate_perimeter(self, positions: List[Tuple[int, int]]) -> int:
        """Calculate perimeter of shape"""
        position_set = set(positions)
        perimeter = 0
        
        for pos in positions:
            row, col = pos
            # Check 4-connected neighbors
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                neighbor = (row + dr, col + dc)
                if neighbor not in position_set:
                    perimeter += 1
        
        return perimeter
    
    def _touches_grid_edge(self, positions: List[Tuple[int, int]], 
                          grid_shape: Tuple[int, int]) -> bool:
        """Check if object touches grid edge"""
        max_row, max_col = grid_shape[0] - 1, grid_shape[1] - 1
        
        for row, col in positions:
            if row == 0 or row == max_row or col == 0 or col == max_col:
                return True
        
        return False
    
    def _in_corner(self, positions: List[Tuple[int, int]], 
                   grid_shape: Tuple[int, int]) -> bool:
        """Check if object is in a corner"""
        max_row, max_col = grid_shape[0] - 1, grid_shape[1] - 1
        corners = [(0, 0), (0, max_col), (max_row, 0), (max_row, max_col)]
        
        for corner in corners:
            if corner in positions:
                return True
        
        return False
    
    def _analyze_spatial_relations(self, objects: List[VisualObject]) -> List[SpatialRelation]:
        """Analyze spatial relations between objects"""
        relations = []
        
        for i, obj1 in enumerate(objects):
            for j, obj2 in enumerate(objects):
                if i >= j:
                    continue
                
                relation = self._determine_spatial_relation(obj1, obj2)
                if relation:
                    relations.append(relation)
        
        return relations
    
    def _determine_spatial_relation(self, obj1: VisualObject, obj2: VisualObject) -> Optional[SpatialRelation]:
        """Determine spatial relation between two objects"""
        bbox1 = obj1.bounding_box
        bbox2 = obj2.bounding_box
        
        # Calculate centers
        center1 = ((bbox1[0] + bbox1[2]) / 2, (bbox1[1] + bbox1[3]) / 2)
        center2 = ((bbox2[0] + bbox2[2]) / 2, (bbox2[1] + bbox2[3]) / 2)
        
        # Calculate distance
        distance = np.sqrt((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)
        
        # Determine relation type
        relation_type = None
        confidence = 1.0
        
        # Vertical relations
        if bbox1[2] < bbox2[0]:  # obj1 above obj2
            relation_type = "above"
        elif bbox2[2] < bbox1[0]:  # obj2 above obj1
            relation_type = "below"
        
        # Horizontal relations
        elif bbox1[3] < bbox2[1]:  # obj1 left of obj2
            relation_type = "left_of"
        elif bbox2[3] < bbox1[1]:  # obj2 left of obj1
            relation_type = "right_of"
        
        # Containment relations
        elif (bbox1[0] <= bbox2[0] and bbox1[1] <= bbox2[1] and 
              bbox1[2] >= bbox2[2] and bbox1[3] >= bbox2[3]):
            relation_type = "contains"
        elif (bbox2[0] <= bbox1[0] and bbox2[1] <= bbox1[1] and 
              bbox2[2] >= bbox1[2] and bbox2[3] >= bbox1[3]):
            relation_type = "contained_by"
        
        # Adjacent relation
        elif distance <= 2.0:
            relation_type = "adjacent"
            confidence = max(0.5, 1.0 - distance / 2.0)
        
        if relation_type:
            return SpatialRelation(
                relation_type=relation_type,
                object1_id=obj1.id,
                object2_id=obj2.id,
                distance=distance,
                confidence=confidence
            )
        
        return None
    
    def _extract_global_properties(self, grid: np.ndarray, objects: List[VisualObject]) -> Dict[str, Any]:
        """Extract global grid properties"""
        properties = {}
        
        # Basic properties
        properties['total_objects'] = len(objects)
        properties['grid_size'] = grid.shape
        properties['non_zero_cells'] = np.count_nonzero(grid)
        properties['density'] = properties['non_zero_cells'] / (grid.shape[0] * grid.shape[1])
        
        # Color analysis
        unique_colors = len(set(obj.color for obj in objects))
        properties['unique_colors'] = unique_colors
        properties['color_diversity'] = unique_colors / max(1, len(objects))
        
        # Shape analysis
        shape_counts = {}
        for obj in objects:
            shape_counts[obj.shape] = shape_counts.get(obj.shape, 0) + 1
        properties['shape_distribution'] = shape_counts
        properties['shape_diversity'] = len(shape_counts) / max(1, len(objects))
        
        # Symmetry analysis
        properties['horizontal_symmetry'] = self._check_horizontal_symmetry(grid)
        properties['vertical_symmetry'] = self._check_vertical_symmetry(grid)
        properties['rotational_symmetry'] = self._check_rotational_symmetry(grid)
        
        # Pattern analysis
        properties['has_repetition'] = self._detect_repetition_pattern(objects)
        properties['has_alignment'] = self._detect_alignment_pattern(objects)
        
        return properties
    
    def _check_horizontal_symmetry(self, grid: np.ndarray) -> bool:
        """Check for horizontal symmetry"""
        return np.array_equal(grid, np.flipud(grid))
    
    def _check_vertical_symmetry(self, grid: np.ndarray) -> bool:
        """Check for vertical symmetry"""
        return np.array_equal(grid, np.fliplr(grid))
    
    def _check_rotational_symmetry(self, grid: np.ndarray) -> bool:
        """Check for 180-degree rotational symmetry"""
        return np.array_equal(grid, np.rot90(grid, 2))
    
    def _detect_repetition_pattern(self, objects: List[VisualObject]) -> bool:
        """Detect if objects show repetition patterns"""
        if len(objects) < 2:
            return False
        
        # Check for repeated shapes or colors
        shapes = [obj.shape for obj in objects]
        colors = [obj.color for obj in objects]
        
        shape_counts = max(shapes.count(shape) for shape in set(shapes))
        color_counts = max(colors.count(color) for color in set(colors))
        
        return shape_counts >= 2 or color_counts >= 2
    
    def _detect_alignment_pattern(self, objects: List[VisualObject]) -> bool:
        """Detect if objects are aligned"""
        if len(objects) < 2:
            return False
        
        # Check for horizontal or vertical alignment
        rows = [obj.position[0] for obj in objects]
        cols = [obj.position[1] for obj in objects]
        
        # Horizontal alignment (same row)
        horizontal_aligned = len(set(rows)) < len(objects)
        
        # Vertical alignment (same column)
        vertical_aligned = len(set(cols)) < len(objects)
        
        return horizontal_aligned or vertical_aligned
    
    def _generate_semantic_description(self, semantic_grid: SemanticGrid) -> str:
        """Generate natural language description of the grid"""
        description_parts = []
        
        # Grid overview
        description_parts.append(f"Grid of size {semantic_grid.dimensions[0]}x{semantic_grid.dimensions[1]}")
        
        # Object summary
        if semantic_grid.objects:
            description_parts.append(f"contains {len(semantic_grid.objects)} objects")
            
            # Describe main objects
            object_descriptions = []
            for obj in semantic_grid.objects[:3]:  # Describe first 3 objects
                obj_desc = f"{obj.color} {obj.shape}"
                if obj.properties.get('touches_edge'):
                    obj_desc += " (at edge)"
                if obj.properties.get('in_corner'):
                    obj_desc += " (in corner)"
                object_descriptions.append(obj_desc)
            
            description_parts.append(f"including {', '.join(object_descriptions)}")
        
        # Global properties
        props = semantic_grid.global_properties
        if props.get('horizontal_symmetry'):
            description_parts.append("with horizontal symmetry")
        if props.get('vertical_symmetry'):
            description_parts.append("with vertical symmetry")
        if props.get('has_repetition'):
            description_parts.append("showing repetition patterns")
        if props.get('has_alignment'):
            description_parts.append("with aligned objects")
        
        # Spatial relations
        if semantic_grid.relations:
            relation_types = [r.relation_type for r in semantic_grid.relations]
            common_relations = [rel for rel, count in 
                              sorted([(rel, relation_types.count(rel)) for rel in set(relation_types)], 
                                   key=lambda x: x[1], reverse=True)[:2]]
            if common_relations:
                description_parts.append(f"spatial relations: {', '.join(common_relations)}")
        
        return "; ".join(description_parts)
    
    def create_transformation_rules(self, input_semantic: SemanticGrid, 
                                  output_semantic: SemanticGrid) -> List[str]:
        """Create transformation rules between input and output grids"""
        rules = []
        
        # Size transformation
        if input_semantic.dimensions != output_semantic.dimensions:
            if (output_semantic.dimensions[0] * output_semantic.dimensions[1] > 
                input_semantic.dimensions[0] * input_semantic.dimensions[1]):
                rules.append("expand_grid")
            else:
                rules.append("contract_grid")
        
        # Object count changes
        input_count = len(input_semantic.objects)
        output_count = len(output_semantic.objects)
        
        if output_count > input_count:
            rules.append("add_objects")
        elif output_count < input_count:
            rules.append("remove_objects")
        
        # Color changes
        input_colors = set(obj.color for obj in input_semantic.objects)
        output_colors = set(obj.color for obj in output_semantic.objects)
        
        if output_colors - input_colors:
            rules.append("introduce_new_colors")
        if input_colors - output_colors:
            rules.append("remove_colors")
        
        # Shape transformations
        input_shapes = set(obj.shape for obj in input_semantic.objects)
        output_shapes = set(obj.shape for obj in output_semantic.objects)
        
        if output_shapes != input_shapes:
            rules.append("transform_shapes")
        
        # Symmetry changes
        input_props = input_semantic.global_properties
        output_props = output_semantic.global_properties
        
        if (not input_props.get('horizontal_symmetry') and 
            output_props.get('horizontal_symmetry')):
            rules.append("create_horizontal_symmetry")
        
        if (not input_props.get('vertical_symmetry') and 
            output_props.get('vertical_symmetry')):
            rules.append("create_vertical_symmetry")
        
        # Pattern changes
        if (not input_props.get('has_repetition') and 
            output_props.get('has_repetition')):
            rules.append("create_repetition_pattern")
        
        return rules

def main():
    """Demonstrate visual-semantic translation"""
    translator = VisualSemanticTranslator()
    
    # Example grid
    example_grid = np.array([
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ])
    
    semantic = translator.translate_grid_to_semantic(example_grid, "example")
    
    print("🔍 Visual-Semantic Translation Demo")
    print(f"📝 Semantic Description: {semantic.semantic_description}")
    print(f"🎯 Objects found: {len(semantic.objects)}")
    for obj in semantic.objects:
        print(f"  - {obj.color} {obj.shape} at {obj.position}")
    print(f"🔗 Relations: {len(semantic.relations)}")
    for rel in semantic.relations:
        print(f"  - {rel.object1_id} {rel.relation_type} {rel.object2_id}")

if __name__ == "__main__":
    main()
