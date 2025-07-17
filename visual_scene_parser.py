#!/usr/bin/env python3
"""
ALLA Visual Scene Parser - Scene Understanding for ARC Tasks
Converts grids into meaningful object representations with attributes and relationships.
"""

import numpy as np
import json
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, field
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

@dataclass
class VisualObject:
    """Represents a visual object with semantic attributes"""
    object_id: str
    color: int
    shape_type: str  # "line", "rectangle", "L_shape", "complex", "dot"
    positions: List[Tuple[int, int]]
    bounding_box: Dict[str, int]
    size: int
    center_of_mass: Tuple[float, float]
    orientation: str = "unknown"  # "horizontal", "vertical", "diagonal"
    compactness: float = 0.0  # how dense the object is
    
    def __post_init__(self):
        if self.positions:
            self.size = len(self.positions)
            self.center_of_mass = self._calculate_center_of_mass()
            self.compactness = self._calculate_compactness()
    
    def _calculate_center_of_mass(self) -> Tuple[float, float]:
        if not self.positions:
            return (0.0, 0.0)
        
        total_x = sum(pos[1] for pos in self.positions)  # col
        total_y = sum(pos[0] for pos in self.positions)  # row
        
        return (total_y / len(self.positions), total_x / len(self.positions))
    
    def _calculate_compactness(self) -> float:
        """Calculate how compact/dense the object is"""
        if not self.positions or len(self.positions) == 1:
            return 1.0
        
        bbox_area = ((self.bounding_box['max_row'] - self.bounding_box['min_row'] + 1) * 
                    (self.bounding_box['max_col'] - self.bounding_box['min_col'] + 1))
        
        return len(self.positions) / bbox_area if bbox_area > 0 else 0.0

@dataclass
class SpatialRelation:
    """Represents spatial relationship between objects"""
    object1_id: str
    object2_id: str
    relation_type: str  # "above", "below", "left_of", "right_of", "touching", "inside", "surrounding"
    distance: float
    confidence: float = 1.0

@dataclass
class SceneRepresentation:
    """Complete scene understanding"""
    objects: List[VisualObject]
    relations: List[SpatialRelation]
    grid_size: Tuple[int, int]
    background_color: int = 0
    scene_complexity: float = 0.0
    dominant_patterns: List[str] = field(default_factory=list)

class VisualSceneParser:
    """Converts ARC grids into semantic scene representations"""
    
    def __init__(self):
        self.shape_classifiers = {
            'line': self._is_line,
            'rectangle': self._is_rectangle,
            'L_shape': self._is_L_shape,
            'T_shape': self._is_T_shape,
            'cross': self._is_cross,
            'complex': self._is_complex_shape
        }
    
    def parse_grid_to_scene(self, grid: np.ndarray, scene_id: str = "") -> SceneRepresentation:
        """Parse grid into complete scene representation"""
        
        # 1. Extract objects
        objects = self._extract_objects(grid)
        
        # 2. Analyze spatial relations
        relations = self._analyze_spatial_relations(objects)
        
        # 3. Detect scene patterns
        patterns = self._detect_scene_patterns(objects, relations, grid)
        
        # 4. Calculate scene complexity
        complexity = self._calculate_scene_complexity(objects, relations)
        
        scene = SceneRepresentation(
            objects=objects,
            relations=relations,
            grid_size=grid.shape,
            background_color=0,
            scene_complexity=complexity,
            dominant_patterns=patterns
        )
        
        logger.info(f"Parsed scene: {len(objects)} objects, {len(relations)} relations, complexity: {complexity:.2f}")
        return scene
    
    def _extract_objects(self, grid: np.ndarray) -> List[VisualObject]:
        """Extract meaningful objects from grid"""
        objects = []
        visited = np.zeros_like(grid, dtype=bool)
        object_id_counter = 0
        
        # Find connected components for each color
        unique_colors = np.unique(grid[grid != 0])
        
        for color in unique_colors:
            color_positions = np.where(grid == color)
            
            for row, col in zip(color_positions[0], color_positions[1]):
                if not visited[row, col]:
                    # Extract connected component
                    component_positions = []
                    self._dfs_extract(grid, row, col, color, visited, component_positions)
                    
                    if component_positions:
                        # Create object
                        obj = self._create_object_from_positions(
                            component_positions, color, f"obj_{object_id_counter}"
                        )
                        objects.append(obj)
                        object_id_counter += 1
        
        return objects
    
    def _dfs_extract(self, grid: np.ndarray, row: int, col: int, target_color: int,
                    visited: np.ndarray, positions: List[Tuple[int, int]]):
        """DFS to extract connected component"""
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
            visited[row, col] or grid[row, col] != target_color):
            return
        
        visited[row, col] = True
        positions.append((row, col))
        
        # Check 4-connected neighbors
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            self._dfs_extract(grid, row + dr, col + dc, target_color, visited, positions)
    
    def _create_object_from_positions(self, positions: List[Tuple[int, int]], 
                                    color: int, object_id: str) -> VisualObject:
        """Create VisualObject from positions"""
        if not positions:
            return None
        
        # Calculate bounding box
        rows = [p[0] for p in positions]
        cols = [p[1] for p in positions]
        
        bounding_box = {
            'min_row': min(rows),
            'max_row': max(rows),
            'min_col': min(cols),
            'max_col': max(cols)
        }
        
        # Classify shape
        shape_type = self._classify_shape(positions, bounding_box)
        
        # Determine orientation
        orientation = self._determine_orientation(positions, bounding_box)
        
        return VisualObject(
            object_id=object_id,
            color=color,
            shape_type=shape_type,
            positions=positions,
            bounding_box=bounding_box,
            size=len(positions),
            center_of_mass=(0, 0),  # Will be calculated in __post_init__
            orientation=orientation
        )
    
    def _classify_shape(self, positions: List[Tuple[int, int]], bbox: Dict[str, int]) -> str:
        """Classify shape based on positions"""
        if len(positions) == 1:
            return "dot"
        
        # Test each shape classifier
        for shape_name, classifier in self.shape_classifiers.items():
            if classifier(positions, bbox):
                return shape_name
        
        return "complex"
    
    def _is_line(self, positions: List[Tuple[int, int]], bbox: Dict[str, int]) -> bool:
        """Check if positions form a line"""
        if len(positions) < 2:
            return False
        
        rows = [p[0] for p in positions]
        cols = [p[1] for p in positions]
        
        # Horizontal line
        if len(set(rows)) == 1 and len(set(cols)) >= 2:
            # Check if positions are contiguous
            sorted_cols = sorted(set(cols))
            return sorted_cols == list(range(min(sorted_cols), max(sorted_cols) + 1))
        
        # Vertical line
        if len(set(cols)) == 1 and len(set(rows)) >= 2:
            sorted_rows = sorted(set(rows))
            return sorted_rows == list(range(min(sorted_rows), max(sorted_rows) + 1))
        
        # Diagonal line (simple check)
        if len(positions) >= 3:
            # Check if all points lie on same diagonal
            first_pos = positions[0]
            for pos in positions[1:]:
                if abs(pos[0] - first_pos[0]) != abs(pos[1] - first_pos[1]):
                    return False
            return True
        
        return False
    
    def _is_rectangle(self, positions: List[Tuple[int, int]], bbox: Dict[str, int]) -> bool:
        """Check if positions form a rectangle"""
        if len(positions) < 4:
            return False
        
        expected_area = ((bbox['max_row'] - bbox['min_row'] + 1) * 
                        (bbox['max_col'] - bbox['min_col'] + 1))
        
        # Filled rectangle
        if len(positions) == expected_area:
            return True
        
        # Rectangle border (hollow)
        if len(positions) >= 8:  # Minimum for a hollow rectangle
            # Check if positions form the perimeter
            perimeter_positions = set()
            
            # Add top and bottom edges
            for col in range(bbox['min_col'], bbox['max_col'] + 1):
                perimeter_positions.add((bbox['min_row'], col))
                perimeter_positions.add((bbox['max_row'], col))
            
            # Add left and right edges
            for row in range(bbox['min_row'], bbox['max_row'] + 1):
                perimeter_positions.add((row, bbox['min_col']))
                perimeter_positions.add((row, bbox['max_col']))
            
            return set(positions) == perimeter_positions
        
        return False
    
    def _is_L_shape(self, positions: List[Tuple[int, int]], bbox: Dict[str, int]) -> bool:
        """Check if positions form an L shape"""
        if len(positions) < 3:
            return False
        
        rows = [p[0] for p in positions]
        cols = [p[1] for p in positions]
        
        # L-shape typically has positions along two perpendicular lines
        # Find corner point (appears in both horizontal and vertical segments)
        
        row_counts = defaultdict(int)
        col_counts = defaultdict(int)
        
        for pos in positions:
            row_counts[pos[0]] += 1
            col_counts[pos[1]] += 1
        
        # Find potential corner (row and col that appear frequently)
        corner_candidates = []
        for pos in positions:
            if row_counts[pos[0]] > 1 and col_counts[pos[1]] > 1:
                corner_candidates.append(pos)
        
        if corner_candidates:
            # Simple L-shape detection
            return True
        
        return False
    
    def _is_T_shape(self, positions: List[Tuple[int, int]], bbox: Dict[str, int]) -> bool:
        """Check if positions form a T shape"""
        if len(positions) < 5:
            return False
        
        # T-shape has one horizontal line and one vertical line intersecting
        rows = [p[0] for p in positions]
        cols = [p[1] for p in positions]
        
        row_counts = defaultdict(int)
        col_counts = defaultdict(int)
        
        for pos in positions:
            row_counts[pos[0]] += 1
            col_counts[pos[1]] += 1
        
        # Look for intersection pattern
        max_row_count = max(row_counts.values()) if row_counts else 0
        max_col_count = max(col_counts.values()) if col_counts else 0
        
        # T-shape typically has one dominant row and one dominant column
        return max_row_count >= 3 and max_col_count >= 3
    
    def _is_cross(self, positions: List[Tuple[int, int]], bbox: Dict[str, int]) -> bool:
        """Check if positions form a cross/plus shape"""
        if len(positions) < 5:
            return False
        
        # Cross has intersection at center
        center_row = (bbox['min_row'] + bbox['max_row']) // 2
        center_col = (bbox['min_col'] + bbox['max_col']) // 2
        
        # Check if center position exists
        if (center_row, center_col) not in positions:
            return False
        
        # Check for arms extending in 4 directions
        has_up = any(p[0] < center_row and p[1] == center_col for p in positions)
        has_down = any(p[0] > center_row and p[1] == center_col for p in positions)
        has_left = any(p[0] == center_row and p[1] < center_col for p in positions)
        has_right = any(p[0] == center_row and p[1] > center_col for p in positions)
        
        return has_up and has_down and has_left and has_right
    
    def _is_complex_shape(self, positions: List[Tuple[int, int]], bbox: Dict[str, int]) -> bool:
        """Default classifier for complex shapes"""
        return len(positions) > 10  # Large/complex shapes
    
    def _determine_orientation(self, positions: List[Tuple[int, int]], bbox: Dict[str, int]) -> str:
        """Determine orientation of the object"""
        height = bbox['max_row'] - bbox['min_row'] + 1
        width = bbox['max_col'] - bbox['min_col'] + 1
        
        if height > width * 1.5:
            return "vertical"
        elif width > height * 1.5:
            return "horizontal"
        elif len(positions) >= 3:
            # Check for diagonal alignment
            first_pos = positions[0]
            diagonal_count = 0
            for pos in positions[1:]:
                if abs(pos[0] - first_pos[0]) == abs(pos[1] - first_pos[1]):
                    diagonal_count += 1
            
            if diagonal_count >= len(positions) * 0.7:
                return "diagonal"
        
        return "square"
    
    def _analyze_spatial_relations(self, objects: List[VisualObject]) -> List[SpatialRelation]:
        """Analyze spatial relations between objects"""
        relations = []
        
        for i, obj1 in enumerate(objects):
            for j, obj2 in enumerate(objects):
                if i >= j:
                    continue
                
                relation = self._determine_relation(obj1, obj2)
                if relation:
                    relations.append(relation)
        
        return relations
    
    def _determine_relation(self, obj1: VisualObject, obj2: VisualObject) -> Optional[SpatialRelation]:
        """Determine spatial relation between two objects"""
        bbox1 = obj1.bounding_box
        bbox2 = obj2.bounding_box
        
        # Calculate distance between centers
        center1 = obj1.center_of_mass
        center2 = obj2.center_of_mass
        distance = np.sqrt((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)
        
        # Determine primary relation
        relation_type = "near"
        confidence = 0.5
        
        # Vertical relations
        if bbox1['max_row'] < bbox2['min_row']:
            relation_type = "above"
            confidence = 0.9
        elif bbox2['max_row'] < bbox1['min_row']:
            relation_type = "below"
            confidence = 0.9
        
        # Horizontal relations
        elif bbox1['max_col'] < bbox2['min_col']:
            relation_type = "left_of"
            confidence = 0.9
        elif bbox2['max_col'] < bbox1['min_col']:
            relation_type = "right_of"
            confidence = 0.9
        
        # Containment
        elif (bbox1['min_row'] <= bbox2['min_row'] and bbox1['max_row'] >= bbox2['max_row'] and
              bbox1['min_col'] <= bbox2['min_col'] and bbox1['max_col'] >= bbox2['max_col']):
            relation_type = "surrounding"
            confidence = 0.8
        elif (bbox2['min_row'] <= bbox1['min_row'] and bbox2['max_row'] >= bbox1['max_row'] and
              bbox2['min_col'] <= bbox1['min_col'] and bbox2['max_col'] >= bbox1['max_col']):
            relation_type = "inside"
            confidence = 0.8
        
        # Touching (adjacent)
        elif distance <= 2.0:  # Close proximity
            relation_type = "touching"
            confidence = 0.7
        
        return SpatialRelation(
            object1_id=obj1.object_id,
            object2_id=obj2.object_id,
            relation_type=relation_type,
            distance=distance,
            confidence=confidence
        )
    
    def _detect_scene_patterns(self, objects: List[VisualObject], 
                             relations: List[SpatialRelation], grid: np.ndarray) -> List[str]:
        """Detect high-level scene patterns"""
        patterns = []
        
        # Symmetry detection
        if self._has_symmetry(objects, grid):
            patterns.append("symmetrical")
        
        # Alignment patterns
        if self._has_alignment(objects):
            patterns.append("aligned")
        
        # Size patterns
        size_pattern = self._detect_size_pattern(objects)
        if size_pattern:
            patterns.append(size_pattern)
        
        # Color patterns
        color_pattern = self._detect_color_pattern(objects)
        if color_pattern:
            patterns.append(color_pattern)
        
        # Density patterns
        if len(objects) > grid.size * 0.3:
            patterns.append("dense")
        elif len(objects) <= 3:
            patterns.append("sparse")
        
        return patterns
    
    def _has_symmetry(self, objects: List[VisualObject], grid: np.ndarray) -> bool:
        """Check if scene has symmetry"""
        # Simple symmetry check
        return (np.array_equal(grid, np.flipud(grid)) or 
                np.array_equal(grid, np.fliplr(grid)) or
                np.array_equal(grid, np.rot90(grid, 2)))
    
    def _has_alignment(self, objects: List[VisualObject]) -> bool:
        """Check if objects are aligned"""
        if len(objects) < 3:
            return False
        
        # Check horizontal alignment
        centers_y = [obj.center_of_mass[0] for obj in objects]
        if len(set(round(y, 1) for y in centers_y)) <= 2:
            return True
        
        # Check vertical alignment
        centers_x = [obj.center_of_mass[1] for obj in objects]
        if len(set(round(x, 1) for x in centers_x)) <= 2:
            return True
        
        return False
    
    def _detect_size_pattern(self, objects: List[VisualObject]) -> Optional[str]:
        """Detect size patterns in objects"""
        if len(objects) < 2:
            return None
        
        sizes = [obj.size for obj in objects]
        unique_sizes = set(sizes)
        
        if len(unique_sizes) == 1:
            return "uniform_size"
        elif len(unique_sizes) == len(sizes):
            return "varied_size"
        elif max(sizes) > min(sizes) * 3:
            return "size_contrast"
        
        return None
    
    def _detect_color_pattern(self, objects: List[VisualObject]) -> Optional[str]:
        """Detect color patterns in objects"""
        if len(objects) < 2:
            return None
        
        colors = [obj.color for obj in objects]
        unique_colors = set(colors)
        
        if len(unique_colors) == 1:
            return "monochrome"
        elif len(unique_colors) == len(colors):
            return "varied_colors"
        else:
            return "mixed_colors"
    
    def _calculate_scene_complexity(self, objects: List[VisualObject], 
                                   relations: List[SpatialRelation]) -> float:
        """Calculate scene complexity score"""
        complexity = 0.0
        
        # Object complexity
        complexity += len(objects) * 0.2
        
        # Shape complexity
        complex_shapes = sum(1 for obj in objects if obj.shape_type == "complex")
        complexity += complex_shapes * 0.3
        
        # Relation complexity
        complexity += len(relations) * 0.1
        
        # Size variation
        if objects:
            sizes = [obj.size for obj in objects]
            size_std = np.std(sizes) if len(sizes) > 1 else 0
            complexity += size_std * 0.05
        
        return float(complexity)
    
    def compare_scenes(self, scene1: SceneRepresentation, 
                      scene2: SceneRepresentation) -> Dict[str, Any]:
        """Compare two scenes to detect transformations"""
        comparison = {
            'object_count_change': len(scene2.objects) - len(scene1.objects),
            'size_change': scene2.grid_size != scene1.grid_size,
            'complexity_change': scene2.scene_complexity - scene1.scene_complexity,
            'pattern_changes': [],
            'object_transformations': [],
            'new_relations': [],
            'lost_relations': []
        }
        
        # Pattern changes
        set1 = set(scene1.dominant_patterns)
        set2 = set(scene2.dominant_patterns)
        comparison['pattern_changes'] = {
            'added': list(set2 - set1),
            'removed': list(set1 - set2),
            'preserved': list(set1 & set2)
        }
        
        # Object transformations (simplified)
        if len(scene1.objects) == len(scene2.objects):
            for i, (obj1, obj2) in enumerate(zip(scene1.objects, scene2.objects)):
                if obj1.color != obj2.color:
                    comparison['object_transformations'].append(f"color_change_{i}")
                if obj1.shape_type != obj2.shape_type:
                    comparison['object_transformations'].append(f"shape_change_{i}")
                if abs(obj1.center_of_mass[0] - obj2.center_of_mass[0]) > 0.5:
                    comparison['object_transformations'].append(f"position_change_{i}")
        
        return comparison

def main():
    """Test the visual scene parser"""
    parser = VisualSceneParser()
    
    # Test with a simple grid
    test_grid = np.array([
        [0, 1, 0, 0],
        [0, 1, 0, 2],
        [0, 1, 0, 2],
        [0, 0, 0, 0]
    ])
    
    scene = parser.parse_grid_to_scene(test_grid, "test_scene")
    
    print("🔍 Visual Scene Parser Test")
    print(f"Objects found: {len(scene.objects)}")
    for obj in scene.objects:
        print(f"  {obj.object_id}: {obj.shape_type} (color {obj.color}, size {obj.size})")
    
    print(f"Relations found: {len(scene.relations)}")
    for rel in scene.relations:
        print(f"  {rel.object1_id} {rel.relation_type} {rel.object2_id}")
    
    print(f"Scene patterns: {scene.dominant_patterns}")
    print(f"Complexity: {scene.scene_complexity:.2f}")

if __name__ == "__main__":
    main()
