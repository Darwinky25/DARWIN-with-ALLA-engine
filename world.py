# ==============================================================================
# world.py
# Version 1.0 - The "Genesis" Living World Engine
#
# MISSION: To create a standalone, dynamic, and persistent world simulation
#          with its own rules, objects, and history. The ALLA agent will
#          interact with this world as a separate entity.
# ==============================================================================

import json
import random
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional
from dataclasses import dataclass, field, asdict

# ==============================================================================
# PART 1: CORE WORLD DATA MODELS
# These define the "matter" and "history" of our universe.
# ==============================================================================

@dataclass
class WorldObject:
    """Represents a single, physical object in the world."""
    # Core Attributes
    id: int
    name: str
    shape: str
    color: str
    position: Optional[Tuple[int, int]]  # (x, y) or None if held/inside another object

    # Physical Attributes
    material: str
    size: int
    weight: int
    hp: int
    
    # State Attributes
    owner: str = 'world'  # 'world', 'alla', 'user'
    is_breakable: bool = False
    is_burning: bool = False
    
    # Container Attributes
    is_container: bool = False
    is_open: bool = True
    contains: List[int] = field(default_factory=list)  # List of object IDs
    capacity: int = 0

    def __repr__(self) -> str:
        """A clear representation for logging and debugging."""
        loc = f"pos={self.position}" if self.owner == 'world' else f"loc='{self.owner}'"
        return f"Object(id={self.id}, name='{self.name}', shape='{self.shape}', color='{self.color}', {loc})"

    def get_properties(self) -> Dict[str, Any]:
        """Returns a dictionary of all object properties for comparison."""
        return {
            'shape': self.shape,
            'color': self.color,
            'material': self.material,
            'size': self.size,
            'weight': self.weight,
            'owner': self.owner
        }

@dataclass
class Event:
    """Records a single, significant event that occurred in the world."""
    id: int
    time: int
    type: str  # e.g., 'CREATE', 'DESTROY', 'TRANSFER', 'PUT_IN'
    details: Dict[str, Any]

# ==============================================================================
# PART 2: THE WORLD ENGINE
# This class manages the state, physics, and evolution of the simulation.
# ==============================================================================

class LivingWorld:
    """The main engine that simulates the dynamic world."""

    def __init__(self, size: Tuple[int, int] = (20, 15)):
        self.size_x, self.size_y = size
        self.time = 0
        self._objects: Dict[int, WorldObject] = {}
        self._event_log: List[Event] = []
        self._next_obj_id = 1
        self._next_event_id = 1
        print(f"Living World initiated with size {size}.")

    def _record_event(self, event_type: str, details: Dict):
        """Internal method to log every significant event."""
        event = Event(id=self._next_event_id, time=self.time, type=event_type, details=details)
        self._event_log.append(event)
        self._next_event_id += 1
        print(f"  EVENT LOG (t={self.time}): {event_type} - {details}")

    def _get_empty_position(self) -> Optional[Tuple[int, int]]:
        """Finds a random empty spot in the world."""
        occupied_pos = {obj.position for obj in self._objects.values() if obj.position and obj.owner == 'world'}
        for _ in range(self.size_x * self.size_y):
            pos = (random.randint(0, self.size_x - 1), random.randint(0, self.size_y - 1))
            if pos not in occupied_pos:
                return pos
        return None

    # --- PUBLIC API for creating and modifying the world ---

    def create_object(self, name: str, shape: str = 'lump', color: str = 'grey', size: int = 5, material: str = 'unknown', owner: str = 'world', **kwargs) -> Optional[WorldObject]:
        """Creates a new object and adds it to the world. The main creation method."""
        if any(obj.name.lower() == name.lower() for obj in self._objects.values()):
            print(f"WORLD ERROR: Object with name '{name}' already exists.")
            return None
        
        # Determine position based on owner
        if owner == 'world':
            pos = self._get_empty_position()
            if pos is None:
                print("WORLD ERROR: No empty space to create new object.")
                return None
        else:
            pos = None  # Objects owned by agents don't have world positions

        obj_id = self._next_obj_id
        self._next_obj_id += 1

        new_obj = WorldObject(
            id=obj_id,
            name=name,
            position=pos,
            shape=shape,
            color=color,
            size=size,
            weight=kwargs.get('weight', size),
            hp=kwargs.get('hp', 100),
            material=material,
            owner=owner,
            is_container=kwargs.get('is_container', False),
            capacity=size if kwargs.get('is_container', False) else 0
        )
        self._objects[obj_id] = new_obj
        self._record_event('CREATE', {'object_id': obj_id, 'name': name, 'owner': owner})
        return new_obj

    def destroy_object(self, name: str) -> Optional[WorldObject]:
        """Destroys an object by name and removes it from the world."""
        obj = self.get_object(name=name)
        if not obj:
            return None
        
        del self._objects[obj.id]
        self._record_event('DESTROY', {'object_id': obj.id, 'name': obj.name})
        return obj

    def transfer_ownership(self, obj: WorldObject, new_owner: str) -> bool:
        """Changes the owner of an object and records the transfer."""
        if new_owner.lower() in ['user', 'alla', 'world']:
            old_owner = obj.owner
            obj.owner = new_owner.lower()
            
            # Update position based on new owner
            if new_owner.lower() == 'world':
                obj.position = self._get_empty_position()
            else:
                obj.position = None
            
            self._record_event('TRANSFER', {
                'object_id': obj.id, 
                'name': obj.name, 
                'from_owner': old_owner, 
                'to_owner': new_owner.lower()
            })
            return True
        return False

    def get_object(self, obj_id: int = -1, name: str = "") -> Optional[WorldObject]:
        """Finds an object by its ID or name."""
        if obj_id != -1:
            return self._objects.get(obj_id)
        if name:
            return next((obj for obj in self._objects.values() if obj.name.lower() == name.lower()), None)
        return None
        
    def get_all_objects(self, in_world_only: bool = False) -> List[WorldObject]:
        """Returns all objects in the simulation."""
        if in_world_only:
            return [obj for obj in self._objects.values() if obj.owner == 'world']
        return list(self._objects.values())

    def get_objects_by_owner(self, owner: str) -> List[WorldObject]:
        """Returns all objects owned by a specific agent."""
        return [obj for obj in self._objects.values() if obj.owner == owner.lower()]

    def get_events(self) -> List[Event]:
        """Returns all recorded events."""
        return self._event_log.copy()

    def get_current_time(self) -> int:
        """Returns the current world time."""
        return self.time

    def tick(self):
        """Advances world time by one step and applies dynamic rules."""
        self.time += 1
        print(f"\n--- TICK {self.time} ---")
        # In the future, this is where dynamic rules like fire spreading would go.
        # For now, it just advances time.

    def save_state(self, file_path: str = "genesis_world.json"):
        """Saves the entire world state (objects and events) to a file."""
        print(f"Saving world state to '{file_path}'...")
        state = {
            "time": self.time,
            "size_x": self.size_x,
            "size_y": self.size_y,
            "next_obj_id": self._next_obj_id,
            "next_event_id": self._next_event_id,
            "objects": [asdict(obj) for obj in self._objects.values()],
            "events": [asdict(event) for event in self._event_log]
        }
        try:
            with Path(file_path).open('w') as f:
                json.dump(state, f, indent=4)
            print("World state saved successfully.")
        except Exception as e:
            print(f"ERROR saving world state: {e}")
            
    def load_state(self, file_path: str = "genesis_world.json"):
        """Loads a world state from a file, overwriting the current state."""
        print(f"Loading world state from '{file_path}'...")
        try:
            with Path(file_path).open('r') as f:
                state = json.load(f)
            self.time = state.get('time', 0)
            self.size_x = state.get('size_x', 20)
            self.size_y = state.get('size_y', 15)
            self._next_obj_id = state.get('next_obj_id', 1)
            self._next_event_id = state.get('next_event_id', 1)
            
            # Reconstruct objects with proper list handling
            self._objects = {}
            for obj_data in state.get('objects', []):
                if 'contains' not in obj_data:
                    obj_data['contains'] = []
                # Fix position: convert list back to tuple if needed
                if obj_data.get('position') and isinstance(obj_data['position'], list):
                    obj_data['position'] = tuple(obj_data['position'])
                obj = WorldObject(**obj_data)
                self._objects[obj.id] = obj
            
            # Reconstruct events
            self._event_log = [Event(**event_data) for event_data in state.get('events', [])]
            print(f"World state loaded successfully. Time: {self.time}, Objects: {len(self._objects)}")
        except FileNotFoundError:
            print(f"INFO: No world state file found at '{file_path}'. Starting a new world.")
        except Exception as e:
            print(f"ERROR loading world state: {e}")

# ==============================================================================
# MAIN EXECUTION (DEMONSTRATION & WORLD CREATION)
# ==============================================================================

if __name__ == "__main__":
    print("===================================================")
    print("=      LIVING WORLD (GENESIS) - SIMULATION      =")
    print("===================================================\n")

    # Initialize a new world
    world = LivingWorld(size=(10, 10))

    # --- Let's create the "Garden of Eden" for ALLA ---
    # A few interesting, discoverable objects.
    
    world.tick()  # Time starts at 1
    world.create_object(name="Old_Tree", shape="tree", color="brown", material="wood", size=20, weight=1000)
    world.create_object(name="River_Stone", shape="lump", color="grey", material="stone", size=5, weight=20)
    
    world.tick()  # Time is now 2
    world.create_object(name="Wooden_Chest", shape="box", color="brown", material="wood", size=10, weight=30, is_container=True)
    
    world.tick()  # Time is now 3
    world.create_object(name="Shiny_Gem", shape="crystal", color="blue", material="glass", size=1, weight=1)
    
    # Let's see the state
    print("\n--- INITIAL WORLD STATE ---")
    for obj in world.get_all_objects():
        print(obj)
    
    # Save this initial state so our ALLA engine can load it
    world.save_state("genesis_world.json")
    
    print("\n===================================================")
    print("=   'genesis_world.json' has been created.      =")
    print("=   The world is ready for an inhabitant.       =")
    print("===================================================")
