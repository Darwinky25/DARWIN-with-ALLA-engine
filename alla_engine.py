# ==============================================================================
# alla_engine.py
# Version 16.0 - The Inquisitive Agent: Curiosity-Driven Learning
#
# Changes from v15.0:
# - NEW UNDERSTAND GOAL TYPE: ALLA now generates inquiry goals for unknown concepts
# - CURIOSITY-DRIVEN BEHAVIOR: Unknown words trigger learning goals instead of failures
# - ENHANCED PLANNER: Added support for OUTPUT_QUESTION plans to ask users about unknowns
# - PROACTIVE LEARNING: ALLA actively seeks understanding through targeted questions
# - MYSTERY OBJECT CAPABILITY: Can discover, learn about, and interact with new objects
#
# Previous Features (maintained from v15.0):
# - CRITICAL BUG FIXES: Fixed knowledge retrieval (B11) and goal parsing regression (B12)
# - ENHANCED PLANNER: Added CREATE goal support and container-aware multi-step planning
# - HARDENED PARSER: Improved error handling and command pattern robustness
# - UNIFIED ARCHITECTURE: Single, stable foundational mind ready for expansion
# - COMPREHENSIVE TESTING: All previous features validated and working together
#
# Previous Features (maintained from v14.0):
# - Semantic Memory and Abstract Knowledge Formation with ReflectionCycle
# - SemanticNode and SemanticEdge datastructures for knowledge graphs
# - Knowledge query commands for accessing abstract understanding
# - ALLA forms general concepts from specific experiences
#
# Previous Features (maintained from v13.0):
# - Goal and Planning System with proactive thinking cycles
# - Autonomous goal pursuit and plan execution
# - Internal drive and purpose-oriented behavior
#
# Previous Features (maintained from v12.0):
# - External LivingWorld integration (world.py)
# - All v11.0 self-education and teaching capabilities
# - World state completely separated from agent logic
# - Fixed all integration bugs (B6-B10) from v12.0
#
# Previous Features (maintained from v11.0):
# - teach command for on-the-fly vocabulary expansion
# - Persistent lexicon with JSON memory file storage
# - Load/save learned concepts between sessions
# - Enhanced CommandProcessor with teach intent parsing
# - Enhanced ExecutionEngine with LEARN_NEW_WORD handler
# - Revolutionary self-education capabilities
#
# Previous Features (maintained from v10.0):
# - Richer WorldObject model with size and material properties
# - Enhanced create command parser for multi-property object creation
# - New relational concepts: bigger_than, smaller_than based on size comparison
# - Advanced temporal reasoning with "when" queries for event history
# - Expanded curriculum with physical properties (big, small, stone, wood)
# - Full backward compatibility with all v9.0 conditional reasoning features
#
# Previous Critical Bug Fixes (maintained in v10.0):
# - B5: Parser fails immediately if unknown nouns/properties are in logical queries
# - B4: "what is <WORD>" fails if <WORD> is not in Lexicon
# - B2: Create command parser ignores articles ('a', 'an', 'the') properly
# - B1: Hypothetical queries fail gracefully if unknown concepts are present
# ==============================================================================

# --- Important Security Warning ---
# This engine uses `eval()` to translate text into logic.
# This provides extraordinary power for procedural synthesis from language.
# However, this is NOT SAFE if curriculum files (.alla) come from untrusted
# sources. In this project, we assume all curriculum files are created by
# us (Cognitive Architects) and are safe to evaluate.
# ------------------------------------------------------------------------------

import os
import json
from pathlib import Path
from typing import List, Callable, Tuple, Dict, Any, Optional
from dataclasses import dataclass, field
import random
import re
from world import LivingWorld, WorldObject, Event  # NEW v12.0: Import from external world engine

# ==============================================================================
# PART 1: CORE DATA STRUCTURES (Models)
# ==============================================================================

@dataclass
class WordEntry:
    """Represents the AI's 'understanding' of a single word."""
    word: str
    word_type: str  # 'noun', 'property', 'relation', 'action', 'inquiry', 'operator', 'temporal', 'conditional', 'pronoun'
    meaning_expression: str
    meaning_function: Callable = field(repr=False)

@dataclass
class ExecutionPlan:
    """A structured plan for the engine to run, with conditional execution support."""
    action_type: str
    details: Dict[str, Any]
    feedback: str  # A natural language string to report back to the user
    
    # --- NEW v7.0: Conditional Execution Support ---
    condition: Optional[Dict[str, Any]] = None  # For conditional plans
    sub_plan_true: Optional['ExecutionPlan'] = None  # Plan to execute if condition is true
    sub_plan_false: Optional['ExecutionPlan'] = None  # Plan to execute if condition is false
    is_hypothetical: bool = False  # For "what if" queries that don't modify the world

@dataclass
class Goal:
    """(UPGRADED v16.0) Represents a desired state or knowledge the agent wants to achieve."""
    id: int
    description: str  # e.g., "I have the red box", "I understand 'flute'"
    # The condition that must be true for the goal to be complete.
    # This reuses our existing parsing logic!
    completion_condition: ExecutionPlan 
    goal_type: str = 'POSSESSION'  # NEW v16.0: 'POSSESSION', 'EXISTENCE', 'UNDERSTAND' 
    status: str = 'active'  # 'active', 'completed', 'failed'
    # NEW v16.0: For UNDERSTAND goals, the question to ask the user
    inquiry_question: Optional[str] = None

@dataclass
class Plan:
    """(NEW v13.0) A sequence of steps to achieve a goal."""
    goal_id: int
    steps: List[ExecutionPlan]
    current_step: int = 0

@dataclass
class SemanticNode:
    """(NEW v14.0) Represents an abstract concept in the knowledge graph."""
    id: str  # e.g., "concept:red", "property:color", "action:take"
    concept_type: str  # 'property', 'value', 'action', 'object_type', 'relation'
    name: str  # e.g., "red", "color", "take"
    observations: int = 0  # How many times this concept has been observed
    confidence: float = 1.0  # Confidence in this concept (0.0 to 1.0)
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional data

@dataclass
class SemanticEdge:
    """(NEW v14.0) Represents a relationship between concepts in the knowledge graph."""
    from_node: str  # Node ID
    to_node: str    # Node ID
    relationship: str  # e.g., "is_type_of", "has_property", "causes_change_in"
    strength: float = 1.0  # Strength of the relationship (0.0 to 1.0)
    observations: int = 1  # How many times this relationship has been observed

# ==============================================================================
# PART 2: CORE COGNITIVE COMPONENTS
# ==============================================================================

# NOTE v12.0: InternalWorld class removed - ALLA now uses external LivingWorld

class Lexicon:
    """(UPGRADED v11.0) The semantic memory with persistence support."""
    def __init__(self):
        self._word_dictionary: Dict[str, WordEntry] = {}
    
    def add_entry(self, entry: WordEntry):
        self._word_dictionary[entry.word] = entry
    
    def get_entry(self, word: str) -> Optional[WordEntry]:
        return self._word_dictionary.get(word)
    
    # NEW v11.0: Methods for persistence support
    def get_all_entries(self) -> Dict[str, WordEntry]:
        """Returns all word entries for saving to memory."""
        return self._word_dictionary.copy()
    
    def get_word_count(self) -> int:
        """Returns the number of words in the lexicon."""
        return len(self._word_dictionary)

class Planner:
    """(UPGRADED v16.0) Enhanced planner with CREATE goals, container-aware planning, and inquiry support."""
    def __init__(self, world: LivingWorld, lexicon: Lexicon):
        self._world = world
        self._lexicon = lexicon

    def create_plan_for_goal(self, goal: Goal) -> Optional[Plan]:
        """(UPGRADED v16.0) Analyzes a goal and creates comprehensive plans.
        
        New capabilities:
        - UNDERSTAND goals: Generate questions to learn about unknown concepts
        - CREATE goals: If object doesn't exist, plan to create it
        - Container-aware TAKE goals: Multi-step plans for objects in containers
        - Improved object matching with flexible descriptions
        """
        condition_type = goal.completion_condition.action_type
        condition_details = goal.completion_condition.details
        
        # --- NEW v16.0: Handle "understanding" goals ---
        if goal.goal_type == 'UNDERSTAND':
            unknown_word = condition_details.get('unknown_word', 'unknown')
            question = f"What is a '{unknown_word}'? Please describe it so I can understand."
            
            step1 = ExecutionPlan(
                action_type='OUTPUT_QUESTION',
                details={'question': question, 'unknown_word': unknown_word},
                feedback=f"Asking user about '{unknown_word}' to gain understanding..."
            )
            return Plan(goal_id=goal.id, steps=[step1])
        
        # --- UPGRADE 1: Handle "possession" goals with container awareness ---
        elif condition_type == 'VERIFY_INVENTORY':
            target_obj = self._find_object_matching_description(condition_details.get('filters', []))
            
            if target_obj:
                if target_obj.owner != 'alla':
                    # NEW: Check if object is in a container
                    container = self._find_container_of(target_obj)
                    if container:
                        # Multi-step plan: take from container, then take
                        step1 = ExecutionPlan(
                            action_type='TAKE_FROM_CONTAINER',
                            details={'object': target_obj, 'container': container},
                            feedback=f"Planning to remove {target_obj.name} from {container.name}..."
                        )
                        step2 = ExecutionPlan(
                            action_type='TRANSFER_OBJECT',
                            details={'object': target_obj, 'new_owner': 'alla'},
                            feedback=f"Planning to take {target_obj.name}..."
                        )
                        return Plan(goal_id=goal.id, steps=[step1, step2])
                    else:
                        # Simple one-step plan
                        step1 = ExecutionPlan(
                            action_type='TRANSFER_OBJECT',
                            details={'object': target_obj, 'new_owner': 'alla'},
                            feedback=f"Planning to take {target_obj.name} to achieve goal '{goal.description}'."
                        )
                        return Plan(goal_id=goal.id, steps=[step1])
            else:
                # Object doesn't exist - can we create it?
                create_plan = self._create_object_plan_from_filters(condition_details.get('filters', []), goal)
                if create_plan:
                    return create_plan
        
        # --- UPGRADE 2: Handle "existence" goals ---
        elif condition_type == 'VERIFY_EXISTENCE':
            if not self._find_object_matching_description(condition_details.get('filters', [])):
                # Object doesn't exist, create it
                create_plan = self._create_object_plan_from_filters(condition_details.get('filters', []), goal)
                if create_plan:
                    return create_plan
        
        return None  # Cannot find a plan

    def _find_object_matching_description(self, filters: List[Callable]) -> Optional[WorldObject]:
        """Find an object that matches all the given filter functions."""
        all_objects = self._world.get_all_objects()
        for obj in all_objects:
            if all(f(obj) for f in filters):
                return obj
        return None

    def _find_container_of(self, obj: WorldObject) -> Optional[WorldObject]:
        """Check if an object is inside a container."""
        all_objects = self._world.get_all_objects()
        for container in all_objects:
            if hasattr(container, 'contains') and obj.id in container.contains:
                return container
        return None

    def _create_object_plan_from_filters(self, filters: List[Callable], goal: Goal) -> Optional[Plan]:
        """Create a plan to make an object matching the given filters."""
        # Extract properties from filter functions by testing them
        # This is a heuristic approach - we test known property values
        
        color = 'red'  # Default
        shape = 'box'  # Default
        size = 5      # Default
        material = 'plastic'  # Default
        
        # Test common colors
        test_obj_colors = [
            (lambda: setattr(test_obj := WorldObject(id=0, name='test', shape='box', color='red', position=None, material='plastic', size=5, weight=5, hp=100), 'get_properties', lambda: {}), 'red'),
            (lambda: setattr(test_obj := WorldObject(id=0, name='test', shape='box', color='blue', position=None, material='plastic', size=5, weight=5, hp=100), 'get_properties', lambda: {}), 'blue'),
            (lambda: setattr(test_obj := WorldObject(id=0, name='test', shape='box', color='green', position=None, material='plastic', size=5, weight=5, hp=100), 'get_properties', lambda: {}), 'green'),
        ]
        
        # Test common shapes
        test_obj_shapes = [
            (lambda: setattr(test_obj := WorldObject(id=0, name='test', shape='box', color='red', position=None, material='plastic', size=5, weight=5, hp=100), 'get_properties', lambda: {}), 'box'),
            (lambda: setattr(test_obj := WorldObject(id=0, name='test', shape='circle', color='red', position=None, material='plastic', size=5, weight=5, hp=100), 'get_properties', lambda: {}), 'circle'),
            (lambda: setattr(test_obj := WorldObject(id=0, name='test', shape='sphere', color='red', position=None, material='plastic', size=5, weight=5, hp=100), 'get_properties', lambda: {}), 'sphere'),
        ]
        
        # For now, use a simple heuristic based on goal description
        goal_desc = goal.description.lower()
        if 'red' in goal_desc:
            color = 'red'
        elif 'blue' in goal_desc:
            color = 'blue'
        elif 'green' in goal_desc:
            color = 'green'
            
        if 'box' in goal_desc:
            shape = 'box'
        elif 'circle' in goal_desc:
            shape = 'circle'
        elif 'sphere' in goal_desc:
            shape = 'sphere'
        
        # Generate a unique name
        name = f"{color}_{shape}_{len(self._world.get_all_objects()) + 1}"
        
        step1 = ExecutionPlan(
            action_type='CREATE_OBJECT',
            details={'name': name, 'shape': shape, 'color': color, 'size': size, 'material': material},
            feedback=f"Planning to create a {color} {shape} to achieve goal '{goal.description}'."
        )
        return Plan(goal_id=goal.id, steps=[step1])

class SemanticMemory:
    """(NEW v14.0) Manages abstract knowledge, concepts, and relationships."""
    def __init__(self):
        self._nodes: Dict[str, SemanticNode] = {}
        self._edges: List[SemanticEdge] = []
    
    def add_node(self, node: SemanticNode):
        """Add or update a concept node."""
        if node.id in self._nodes:
            # Update existing node
            existing = self._nodes[node.id]
            existing.observations += node.observations
            existing.confidence = min(1.0, existing.confidence + 0.1)
        else:
            self._nodes[node.id] = node
    
    def add_edge(self, edge: SemanticEdge):
        """Add or strengthen a relationship edge."""
        # Check if edge already exists
        for existing_edge in self._edges:
            if (existing_edge.from_node == edge.from_node and 
                existing_edge.to_node == edge.to_node and 
                existing_edge.relationship == edge.relationship):
                # Strengthen existing edge
                existing_edge.observations += 1
                existing_edge.strength = min(1.0, existing_edge.strength + 0.1)
                return
        # Add new edge
        self._edges.append(edge)
    
    def get_concept(self, concept_id: str) -> Optional[SemanticNode]:
        """Retrieve a concept by ID."""
        return self._nodes.get(concept_id)
    
    def get_related_concepts(self, concept_id: str, relationship: Optional[str] = None) -> List[str]:
        """Get concepts related to the given concept."""
        related = []
        for edge in self._edges:
            if edge.from_node == concept_id:
                if relationship is None or edge.relationship == relationship:
                    related.append(edge.to_node)
        return related
    
    def query_knowledge(self, query: str) -> List[str]:
        """Answer knowledge queries about concepts and relationships."""
        results = []
        
        # Handle "what do you know about X" queries
        if "what do you know about" in query.lower():
            concept_word = query.lower().split("what do you know about")[-1].strip().strip("'\"?")
            concept_id = f"concept:{concept_word}"
            
            if concept_id in self._nodes:
                node = self._nodes[concept_id]
                results.append(f"I know about '{concept_word}': {node.concept_type}")
                results.append(f"Observed {node.observations} times (confidence: {node.confidence:.1f})")
                
                # Find related concepts
                related = self.get_related_concepts(concept_id)
                if related:
                    results.append(f"Related to: {', '.join([r.split(':')[-1] for r in related])}")
            else:
                results.append(f"I don't have abstract knowledge about '{concept_word}' yet.")
        
        # Handle "list all X" queries
        elif "list all" in query.lower():
            if "actions" in query.lower():
                actions = [node.name for node in self._nodes.values() if node.concept_type == 'action']
                results.append(f"Known actions: {', '.join(actions)}" if actions else "No actions learned yet.")
            elif "properties" in query.lower():
                properties = [node.name for node in self._nodes.values() if node.concept_type == 'property']
                results.append(f"Known properties: {', '.join(properties)}" if properties else "No properties learned yet.")
            elif "colors" in query.lower():
                colors = [node.name for node in self._nodes.values() 
                         if node.concept_type == 'value' and any(e.to_node == 'concept:color' for e in self._edges if e.from_node == node.id)]
                results.append(f"Known colors: {', '.join(colors)}" if colors else "No colors learned yet.")
        
        return results if results else ["I don't understand that knowledge query yet."]

class CommandProcessor:
    """(HEAVILY UPGRADED v8.0) Parses language including pronouns and interaction commands."""
    def __init__(self, lexicon: Lexicon, world: LivingWorld):
        self._lexicon = lexicon
        self._world = world

    def _resolve_pronoun(self, word: str) -> Optional[str]:
        """Converts pronouns to agent names or object references."""
        word = word.lower().strip()
        if word in ['i', 'me', 'alla']:
            return 'alla'
        if word in ['you']:
            return 'user'
        # Check if it's a direct object name
        if self._world.get_object(name=word):
            return word
        return None

    def _extract_property_filters(self, words: List[str]) -> Tuple[List[Callable], List[str]]:
        """(UPGRADED v16.0) Extracts property filter functions from a list of words.
        Returns (filters, unknown_words) tuple instead of failing completely."""
        filters = []
        unknown_words = []
        
        for word in words:
            entry = self._lexicon.get_entry(word)
            if entry and entry.word_type in ['property', 'noun']:
                filters.append(entry.meaning_function)
            else:
                unknown_words.append(word)
        
        # NEW v16.0: Return both successful filters and unknown words
        # Let the caller decide how to handle unknowns
        return filters, unknown_words

    def _resolve_agent(self, agent_word: str) -> Optional[str]:
        """Resolves agent references to standard agent names."""
        return self._resolve_pronoun(agent_word)

    def _parse_teach_command(self, command: str) -> ExecutionPlan:
        """Improved teach command parser with robust quote handling."""
        import re
        
        # Improved regex pattern to handle quoted strings with nested quotes
        # Pattern: teach [type] "word" as "expression"
        # This pattern handles nested single quotes within double quotes
        pattern = r'teach\s+(\w+)\s+"([^"]+)"\s+as\s+"([^"]+)"'
        match = re.search(pattern, command, re.IGNORECASE)
        
        if match:
            word_type = match.group(1).lower()
            word_to_learn = match.group(2)
            expression = match.group(3)
            
            # Validate word type
            valid_types = ['property', 'noun', 'relation', 'action', 'inquiry', 'operator', 'temporal', 'conditional', 'pronoun']
            if word_type in valid_types:
                return ExecutionPlan(
                    action_type='LEARN_NEW_WORD',
                    details={'word': word_to_learn, 'type': word_type, 'expression': expression},
                    feedback=f"Learning new {word_type}: '{word_to_learn}' with meaning '{expression}'..."
                )
            else:
                return ExecutionPlan(
                    action_type='PARSE_ERROR',
                    details={'error_type': 'invalid_word_type', 'word_type': word_type},
                    feedback=f"Invalid word type '{word_type}'. Valid types: {', '.join(valid_types)}"
                )
        
        # Fallback: Try the old method with enhanced error detection
        try:
            command_parts = command.split()
            
            # More robust validation
            if len(command_parts) < 5:
                return ExecutionPlan(
                    action_type='PARSE_ERROR',
                    details={'error_type': 'insufficient_arguments'},
                    feedback="Teach command requires at least 5 parts: teach [type] \"word\" as \"expression\""
                )
            
            # Find word type 
            word_type = command_parts[1].lower()
            
            # Find the "as" keyword
            as_index = -1
            for i, part in enumerate(command_parts):
                if part.lower() == 'as':
                    as_index = i
                    break
            
            if as_index == -1:
                return ExecutionPlan(
                    action_type='PARSE_ERROR',
                    details={'error_type': 'missing_as_keyword'},
                    feedback="Teach command must include 'as' keyword: teach [type] \"word\" as \"expression\""
                )
            
            if as_index <= 2:
                return ExecutionPlan(
                    action_type='PARSE_ERROR',
                    details={'error_type': 'malformed_structure'},
                    feedback="Invalid teach command structure. Expected: teach [type] \"word\" as \"expression\""
                )
            
            # Extract parts more carefully
            word_part = ' '.join(command_parts[2:as_index]).strip()
            expression_part = ' '.join(command_parts[as_index+1:]).strip()
            
            # Handle quotes more robustly
            if (word_part.startswith('"') and word_part.endswith('"')) or \
               (word_part.startswith("'") and word_part.endswith("'")):
                word_to_learn = word_part[1:-1]
            else:
                word_to_learn = word_part
            
            if (expression_part.startswith('"') and expression_part.endswith('"')) or \
               (expression_part.startswith("'") and expression_part.endswith("'")):
                expression = expression_part[1:-1]
            else:
                expression = expression_part
            
            # Validate that we have meaningful content
            if not word_to_learn:
                return ExecutionPlan(
                    action_type='PARSE_ERROR',
                    details={'error_type': 'empty_word'},
                    feedback="Word to learn cannot be empty"
                )
            
            if not expression:
                return ExecutionPlan(
                    action_type='PARSE_ERROR',
                    details={'error_type': 'empty_expression'},
                    feedback="Expression cannot be empty"
                )
            
            # Validate word type
            valid_types = ['property', 'noun', 'relation', 'action', 'inquiry', 'operator', 'temporal', 'conditional', 'pronoun']
            if word_type not in valid_types:
                return ExecutionPlan(
                    action_type='PARSE_ERROR',
                    details={'error_type': 'invalid_word_type', 'word_type': word_type},
                    feedback=f"Invalid word type '{word_type}'. Valid types: {', '.join(valid_types)}"
                )
            
            return ExecutionPlan(
                action_type='LEARN_NEW_WORD',
                details={'word': word_to_learn, 'type': word_type, 'expression': expression},
                feedback=f"Learning new {word_type}: '{word_to_learn}' with meaning '{expression}'..."
            )
            
        except Exception as e:
            return ExecutionPlan(
                action_type='PARSE_ERROR',
                details={'error_type': 'parsing_exception', 'exception': str(e)},
                feedback=f"Error parsing teach command: {str(e)}. Use: teach [type] \"word\" as \"expression\""
            )

    def parse(self, command: str) -> Optional[ExecutionPlan]:
        """Analyzes commands including interaction and ownership operations."""
        words = command.lower().replace('?', '').split()
        if not words: return None

        # --- INTENT 0: Learning Command (HIGHEST PRIORITY - NEW v11.0) ---
        # Pattern: teach [type] "word" as "expression"
        if words[0] == 'teach' and len(words) >= 5 and 'as' in words:
            return self._parse_teach_command(command)
            
        # Pattern: "help teach" - show teach command syntax
        if words == ['help', 'teach']:
            return ExecutionPlan(
                action_type='SHOW_HELP',
                details={'help_type': 'teach'},
                feedback="Showing help for the teach command..."
            )

        # --- INTENT 0.5: Knowledge Query Commands (NEW v14.0) ---
        # Pattern: "what do you know about X" or "list all [actions/properties/colors]"
        if ('what' in words and 'know' in words and 'about' in words) or ('list' in words and 'all' in words):
            return ExecutionPlan(
                action_type='KNOWLEDGE_QUERY',
                details={'query': command},
                feedback="Accessing abstract knowledge..."
            )

        # Pattern: "help teach" - show teach command syntax
        if words == ['help', 'teach']:
            return ExecutionPlan(
                action_type='SHOW_HELP',
                details={'help_type': 'teach'},
                feedback="Showing help for the teach command..."
            )

        # --- INTENT 1: Temporal Queries (v6.0) ---
        
        # Pattern: "list events"
        if words == ['list', 'events']:
            return ExecutionPlan(action_type='LIST_EVENTS', details={}, 
                               feedback="Listing all recorded events in chronological order...")

        # Pattern: "what happened before event <ID>" or "what happened after event <ID>"
        if len(words) == 5 and words[0] == 'what' and words[1] == 'happened' and words[3] == 'event':
            try:
                event_id = int(words[4])
                temporal_op = words[2]  # 'before' or 'after'
                
                if temporal_op in ['before', 'after']:
                    return ExecutionPlan(action_type='QUERY_EVENTS', 
                                       details={'operator': temporal_op, 'event_id': event_id}, 
                                       feedback=f"Finding events that happened {temporal_op} event {event_id}...")
            except (ValueError, IndexError):
                pass  # Not a valid temporal query

        # --- INTENT 2: Conditional Reasoning (v7.0) ---
        
        # Pattern: "if <CONDITION> then <ACTION>"
        if 'if' in words and 'then' in words:
            try:
                if_index = words.index('if')
                then_index = words.index('then')
                
                if if_index < then_index:
                    condition_words = words[if_index + 1:then_index]
                    action_words = words[then_index + 1:]
                    
                    # Parse the condition
                    condition_plan = self._parse_condition(condition_words)
                    if condition_plan:
                        # Parse the action
                        action_command = ' '.join(action_words)
                        action_plan = self.parse(action_command)
                        
                        if action_plan:
                            return ExecutionPlan(
                                action_type='CONDITIONAL_EXECUTION',
                                details={'condition_text': ' '.join(condition_words), 'action_text': action_command},
                                feedback=f"Setting up conditional: IF {' '.join(condition_words)} THEN {action_command}",
                                condition=condition_plan,
                                sub_plan_true=action_plan
                            )
            except (ValueError, IndexError):
                pass

        # Pattern: "what if <CONDITION>"
        if len(words) >= 3 and words[0] == 'what' and words[1] == 'if':
            condition_words = words[2:]
            condition_plan = self._parse_condition(condition_words)
            
            if condition_plan:
                return ExecutionPlan(
                    action_type='HYPOTHETICAL_QUERY',
                    details={'condition_text': ' '.join(condition_words)},
                    feedback=f"Evaluating hypothetical: What if {' '.join(condition_words)}?",
                    condition=condition_plan,
                    is_hypothetical=True
                )
            else:
                # CRITICAL: Fail the query if condition parsing failed due to unknown words
                return ExecutionPlan(
                    action_type='PARSE_ERROR',
                    details={'error_type': 'unknown_condition', 'condition_text': ' '.join(condition_words)},
                    feedback=f"Cannot evaluate hypothetical condition with unknown concepts: {' '.join(condition_words)}"
                )

        # --- INTENT 3: Interaction Commands (NEW v8.0) ---
        
        # Pattern: "give <OBJECT> to <RECIPIENT>"
        action_entry = self._lexicon.get_entry(words[0])
        if action_entry and action_entry.word == 'give' and 'to' in words:
            try:
                to_index = words.index('to')
                obj_words = words[1:to_index]
                recipient_word = words[to_index + 1] if to_index + 1 < len(words) else None
                
                # Resolve object name (handle multiple words like "red box")
                obj_name = None
                for word in obj_words:
                    resolved = self._resolve_pronoun(word)
                    if resolved and self._world.get_object(name=resolved):
                        obj_name = resolved
                        break
                
                # Resolve recipient
                recipient_name = self._resolve_pronoun(recipient_word) if recipient_word else None
                
                target_obj = self._world.get_object(name=obj_name) if obj_name else None
                
                if target_obj and recipient_name:
                    return ExecutionPlan(
                        action_type='TRANSFER_OBJECT',
                        details={'object': target_obj, 'new_owner': recipient_name},
                        feedback=f"Attempting to give {target_obj.name} to {recipient_name}..."
                    )
            except (ValueError, IndexError):
                pass

        # Pattern: "take <OBJECT>"
        if len(words) >= 2 and words[0] == 'take':
            action_entry = self._lexicon.get_entry(words[0])
            if action_entry and action_entry.word == 'take':
                obj_words = words[1:]
                
                # Find the object by trying each word
                target_obj = None
                for word in obj_words:
                    resolved = self._resolve_pronoun(word)
                    if resolved:
                        target_obj = self._world.get_object(name=resolved)
                        if target_obj:
                            break
                
                if target_obj:
                    return ExecutionPlan(
                        action_type='TRANSFER_OBJECT',
                        details={'object': target_obj, 'new_owner': 'alla'},
                        feedback=f"I am taking {target_obj.name}..."
                    )

        # --- INTENT 4: Inventory Verification (UPGRADED v16.0) ---
        
        # Pattern: "do I have <OBJECT_SPEC>?" - Critical for v9.0 conditional reasoning
        if words[0] == 'do' and words[1] == 'i' and words[2] == 'have' and len(words) >= 4:
            # Extract property filters from the object specification
            obj_spec_words = words[3:]  # e.g., ["a", "red", "box"] or ["red", "box"]
            
            # Remove articles like "a", "an", "the"
            filtered_words = [w for w in obj_spec_words if w not in ['a', 'an', 'the']]
            
            # Check if there are any words left after filtering articles
            if not filtered_words:
                return None  # No meaningful content
            
            property_filters, unknown_words = self._extract_property_filters(filtered_words)
            
            if property_filters and not unknown_words:
                # All words understood - proceed normally
                return ExecutionPlan(
                    action_type='VERIFY_INVENTORY',
                    details={'owner': 'alla', 'filters': property_filters, 'description': ' '.join(filtered_words)},
                    feedback=f"Checking if I have {' '.join(filtered_words)}..."
                )
            elif unknown_words:
                # NEW v16.0: Generate inquiry goal instead of failing
                first_unknown = unknown_words[0]  # Focus on first unknown word
                return ExecutionPlan(
                    action_type='TRIGGER_UNDERSTAND_GOAL',
                    details={'unknown_word': first_unknown, 'context': ' '.join(filtered_words)},
                    feedback=f"I don't understand '{first_unknown}'. Let me ask about it..."
                )
            else:
                # No meaningful words found
                return ExecutionPlan(
                    action_type='PARSE_ERROR',
                    details={'error_type': 'no_meaningful_words'},
                    feedback="I don't understand what you're asking about."
                )

        # --- INTENT 5: Inventory Queries (v8.0) ---
        
        # Pattern: "what do <AGENT> have?" or "what does <AGENT> have?"
        if words[0] == 'what' and ('have' in words or 'has' in words):
            # Find the agent reference
            agent_word = None
            if len(words) >= 3:
                if words[1] == 'do' and len(words) >= 4:
                    agent_word = words[2]
                elif words[1] == 'does' and len(words) >= 4:
                    agent_word = words[2]
                
            agent_name = self._resolve_pronoun(agent_word) if agent_word else None
            
            if agent_name:
                return ExecutionPlan(
                    action_type='QUERY_INVENTORY', 
                    details={'owner': agent_name}, 
                    feedback=f"Checking inventory of {agent_name}..."
                )

        # Pattern: "what do I have?" or "what do you have?"
        if words == ['what', 'do', 'i', 'have']:
            return ExecutionPlan(
                action_type='QUERY_INVENTORY',
                details={'owner': 'alla'},
                feedback="Checking my inventory..."
            )
        
        if words == ['what', 'do', 'you', 'have']:
            return ExecutionPlan(
                action_type='QUERY_INVENTORY',
                details={'owner': 'user'},
                feedback="Checking your inventory..."
            )

        # Pattern: "what is in the world"
        if words == ['what', 'is', 'in', 'the', 'world']:
            return ExecutionPlan(
                action_type='QUERY_INVENTORY',
                details={'owner': 'world'},
                feedback="Checking what objects are in the world..."
            )

        # --- INTENT 5: Comparison Operations ---
        # Pattern: "is <OBJ_A> same as <OBJ_B>" or "is <OBJ_A> different from <OBJ_B>"
        if words[0] == 'is' and len(words) >= 4:
            if 'same' in words and 'as' in words and len(words) == 5:
                obj_a_name, obj_b_name = words[1], words[4]
                obj_a = self._world.get_object(name=obj_a_name)
                obj_b = self._world.get_object(name=obj_b_name)
                if obj_a and obj_b:
                    return ExecutionPlan(action_type='VERIFY_COMPARISON', 
                                       details={'type': 'same', 'obj1': obj_a, 'obj2': obj_b}, 
                                       feedback=f"Comparing if '{obj_a.name}' is the same as '{obj_b.name}'...")
            
            elif 'different' in words and 'from' in words and len(words) == 5:
                obj_a_name, obj_b_name = words[1], words[4]
                obj_a = self._world.get_object(name=obj_a_name)
                obj_b = self._world.get_object(name=obj_b_name)
                if obj_a and obj_b:
                    return ExecutionPlan(action_type='VERIFY_COMPARISON', 
                                       details={'type': 'different', 'obj1': obj_a, 'obj2': obj_b}, 
                                       feedback=f"Comparing if '{obj_a.name}' is different from '{obj_b.name}'...")

        # --- INTENT 3: Logical Queries ---
        # Pattern: "what is <...> and/or/not <...>"
        if len(words) >= 3 and words[0] == 'what' and words[1] == 'is':
            query_words = words[2:]
            logical_plan = self._build_logical_filter_plan(query_words)
            if logical_plan:
                return logical_plan

        # --- INTENT 4: Interrogative (Question) - v4.0 functionality ---
        first_word_entry = self._lexicon.get_entry(words[0])
        if first_word_entry and first_word_entry.word_type == 'inquiry':
            intent_word = first_word_entry.word
            
            # Pattern: "what is <PROPERTY/NOUN>..." (simple, non-logical)
            if intent_word == 'what' and len(words) > 2 and words[1] == 'is':
                filter_words = words[2:]
                # Check if this contains logical operators
                has_logic = any(
                    entry and entry.word_type == 'operator' 
                    for w in filter_words 
                    if (entry := self._lexicon.get_entry(w))
                )
                if not has_logic:  # Simple query without logic
                    # Check if ALL words are known properties/nouns
                    found_filters = []
                    unknown_words = []
                    
                    for w in filter_words:
                        entry = self._lexicon.get_entry(w)
                        if entry and entry.word_type in ['property', 'noun']:
                            found_filters.append(entry.meaning_function)
                        else:
                            unknown_words.append(w)
                    
                    # CRITICAL: Fail if ANY word is unknown
                    if unknown_words:
                        return ExecutionPlan(
                            action_type='PARSE_ERROR',
                            details={'error_type': 'unknown_words', 'unknown_words': unknown_words},
                            feedback=f"Cannot search for unknown concepts: {', '.join(unknown_words)}"
                        )
                    
                    if found_filters:
                        return ExecutionPlan(action_type='FILTER_OBJECTS', details={'filters': found_filters}, feedback=f"Searching for what is '{' '.join(filter_words)}'...")

            # Pattern: "where is <OBJECT_NAME>"
            elif intent_word == 'where' and len(words) == 3 and words[1] == 'is':
                obj_name = words[2]
                target_obj = self._world.get_object(name=obj_name)
                if target_obj:
                    return ExecutionPlan(action_type='QUERY_PROPERTY', details={'target': target_obj, 'property_name': 'position'}, feedback=f"Locating '{target_obj.name}'...")

            # NEW v10.0: Pattern: "when was <OBJECT_NAME> <ACTION_PAST_TENSE>"
            elif intent_word == 'when' and len(words) >= 4 and words[1] == 'was':
                try:
                    # Extract object name and action
                    obj_name = words[2]
                    action_verb = words[3]  # e.g., created, destroyed
                    
                    # Map past tense verbs to action types
                    action_map = {
                        'created': 'CREATE',
                        'destroyed': 'DESTROY',
                        'made': 'CREATE',
                        'built': 'CREATE',
                        'removed': 'DESTROY',
                        'deleted': 'DESTROY'
                    }
                    
                    action_type = action_map.get(action_verb)
                    
                    if action_type:
                        # For CREATE queries, object might not exist yet but could be in history
                        # For DESTROY queries, object might not exist but could be in history
                        # We'll let the execution engine handle validation
                        return ExecutionPlan(
                            action_type='QUERY_EVENT',
                            details={'target_name': obj_name, 'event_action_type': action_type},
                            feedback=f"Searching event history for when '{obj_name}' was {action_verb}..."
                        )
                except (ValueError, IndexError):
                    pass

            # Pattern: "is <OBJECT_NAME> <PROPERTY>"
            elif intent_word == 'is' and len(words) == 3:
                obj_name = words[1]
                prop_word = words[2]
                target_obj = self._world.get_object(name=obj_name)
                prop_entry = self._lexicon.get_entry(prop_word)
                if target_obj and prop_entry and prop_entry.word_type in ['noun', 'property']:
                    return ExecutionPlan(action_type='VERIFY_PROPERTY', details={'target': target_obj, 'property_func': prop_entry.meaning_function}, feedback=f"Verifying if '{target_obj.name}' is {prop_word}...")

        # --- INTENT 5: Imperative (Action) ---
        action_entry = self._lexicon.get_entry(words[0])
        if action_entry and action_entry.word_type == 'action':
            if action_entry.word == 'create' and 'as' in words:
                try:
                    name_index = words.index('as') + 1
                    name = words[name_index]
                    prop_words = words[1:name_index-1]
                    
                    # Filter out articles first (critical fix for Bug B2)
                    filtered_prop_words = [w for w in prop_words if w not in ['a', 'an', 'the']]
                    
                    # Enhanced v10.0: Categorize properties by type
                    colors = []
                    shapes = []
                    sizes = []
                    materials = []
                    unknown_words = []
                    
                    for w in filtered_prop_words:
                        entry = self._lexicon.get_entry(w)
                        if entry and entry.word_type == 'property':
                            # Try to determine the property category based on word itself and meaning
                            word_lower = w.lower()
                            meaning_lower = entry.meaning_expression.lower()
                            
                            # Size-related properties
                            if word_lower in ['big', 'large', 'huge', 'small', 'tiny'] or 'size' in meaning_lower:
                                sizes.append(w)
                            # Material-related properties  
                            elif word_lower in ['stone', 'wood', 'metal', 'glass'] or 'material' in meaning_lower:
                                materials.append(w)
                            # Color-related properties (check meaning expression for color pattern)
                            elif 'color' in meaning_lower:
                                colors.append(w)
                            else:
                                # If it's a property but doesn't match size/material/color patterns, assume it's a color
                                colors.append(w)
                        elif entry and entry.word_type == 'noun':
                            shapes.append(w)
                        else:
                            unknown_words.append(w)
                    
                    # Extract properties with intelligent defaults
                    color = colors[0] if colors else 'red'  # Default to red if no color specified
                    shape = shapes[0] if shapes else 'cube'  # Default to cube if no shape specified
                    
                    # NEW v10.0: Handle size and material
                    # For size, we'll use a simple mapping or default to medium (5)
                    size = 5  # Default medium size
                    if sizes:
                        # Map size words to numeric values
                        size_map = {'big': 8, 'large': 8, 'huge': 10, 'small': 3, 'tiny': 1}
                        size = size_map.get(sizes[0], 5)
                    
                    material = materials[0] if materials else 'plastic'  # Default to plastic instead of unknown
                    
                    # Build feedback message
                    properties_desc = f"{color} {shape}"
                    if sizes:
                        properties_desc = f"{sizes[0]} {properties_desc}"
                    if materials:
                        properties_desc = f"{properties_desc} made of {material}"
                    
                    if unknown_words:
                        feedback = f"Attempting to create a {properties_desc} named '{name}' (ignoring unknown words: {', '.join(unknown_words)})"
                    else:
                        feedback = f"Attempting to create a {properties_desc} named '{name}'..."
                            
                    return ExecutionPlan(action_type='CREATE_OBJECT', details={'name': name, 'shape': shape, 'color': color, 'size': size, 'material': material}, feedback=feedback)
                except (ValueError, IndexError): pass
            
            elif action_entry.word == 'destroy' and len(words) == 2:
                name = words[1]
                if self._world.get_object(name=name):
                    return ExecutionPlan(action_type='DESTROY_OBJECT', details={'name': name}, feedback=f"Attempting to destroy '{name}'...")

        # --- INTENT 6: Relational Query ---
        # Pattern: "X relation Y" (3 words)
        if len(words) == 3:
            relation_entry = self._lexicon.get_entry(words[1])
            if relation_entry and relation_entry.word_type == 'relation':
                obj1 = self._world.get_object(name=words[0].lower())
                obj2 = self._world.get_object(name=words[2].lower())
                if obj1 and obj2:
                    return ExecutionPlan(action_type='VERIFY_RELATION', details={'relation_func': relation_entry.meaning_function, 'obj1': obj1, 'obj2': obj2}, feedback=f"Verifying if {obj1.name} is {relation_entry.word} {obj2.name}...")

        # NEW v10.0: Pattern: "is X bigger_than Y" or "is X smaller_than Y" (4 words)
        if len(words) == 4 and words[0] == 'is':
            relation_word = words[2]
            relation_entry = self._lexicon.get_entry(relation_word)
            if relation_entry and relation_entry.word_type == 'relation':
                obj1 = self._world.get_object(name=words[1].lower())
                obj2 = self._world.get_object(name=words[3].lower())
                if obj1 and obj2:
                    return ExecutionPlan(action_type='VERIFY_RELATION', details={'relation_func': relation_entry.meaning_function, 'obj1': obj1, 'obj2': obj2}, feedback=f"Comparing: Is {obj1.name} {relation_word.replace('_', ' ')} {obj2.name}?")

        # NEW v10.0: Pattern: "is X bigger than Y" or "is X smaller than Y" (5 words with space)
        if len(words) == 5 and words[0] == 'is' and words[3] == 'than':
            # Convert "bigger than" to "bigger_than" to match lexicon
            relation_base = words[2]  # "bigger" or "smaller"
            relation_word = f"{relation_base}_than"
            relation_entry = self._lexicon.get_entry(relation_word)
            if relation_entry and relation_entry.word_type == 'relation':
                obj1 = self._world.get_object(name=words[1].lower())
                obj2 = self._world.get_object(name=words[4].lower())
                if obj1 and obj2:
                    return ExecutionPlan(action_type='VERIFY_RELATION', details={'relation_func': relation_entry.meaning_function, 'obj1': obj1, 'obj2': obj2}, feedback=f"Comparing: Is {obj1.name} {relation_base} than {obj2.name}?")

        # --- INTENT 7: Simple Filtering (Fallback) ---
        found_filters = []
        unknown_words = []
        for w in words:
            entry = self._lexicon.get_entry(w)
            if entry and entry.word_type in ['noun', 'property']:
                found_filters.append(entry.meaning_function)
            else:
                # Check if it's not a pronoun, article, or common word
                if w not in ['a', 'an', 'the', 'i', 'you', 'me', 'my', 'your', 'is', 'are', 'was', 'were', 'do', 'does', 'did', 'have', 'has', 'had']:
                    unknown_words.append(w)
        
        if found_filters:
            return ExecutionPlan(action_type='FILTER_OBJECTS', details={'filters': found_filters}, feedback="Searching for objects...")
        
        # NEW v16.0: Instead of failing completely, check for unknown words and ask about them
        if unknown_words:
            first_unknown = unknown_words[0]  # Focus on the first unknown word
            return ExecutionPlan(
                action_type='TRIGGER_UNDERSTAND_GOAL',
                details={'unknown_word': first_unknown, 'context': ' '.join(words)},
                feedback=f"I don't understand '{first_unknown}'. Let me ask about it..."
            )
            
        return None

    def _build_logical_filter_plan(self, query_words: List[str]) -> Optional[ExecutionPlan]:
        """Builds a logical filter plan from query words containing operators."""
        # Handle complex "X and not Y" patterns first
        if 'and' in query_words and 'not' in query_words:
            and_index = query_words.index('and')
            not_index = query_words.index('not')
            
            if and_index < not_index:  # Pattern: "X and not Y"
                left_words = query_words[:and_index]
                not_word = query_words[not_index + 1] if not_index + 1 < len(query_words) else None
                
                # Build left side conditions
                left_conditions = []
                for w in left_words:
                    entry = self._lexicon.get_entry(w)
                    if entry and entry.word_type in ['property', 'noun']:
                        left_conditions.append({'operator': 'filter', 'function': entry.meaning_function})
                
                # Build NOT condition for right side
                if not_word:
                    not_entry = self._lexicon.get_entry(not_word)
                    if not_entry and not_entry.word_type in ['property', 'noun']:
                        not_condition = {'operator': 'not', 'condition': {'operator': 'filter', 'function': not_entry.meaning_function}}
                        
                        # Combine with AND
                        all_conditions = left_conditions + [not_condition]
                        condition = {'operator': 'and', 'conditions': all_conditions}
                        return ExecutionPlan(action_type='COMPLEX_FILTER', details=condition, 
                                           feedback=f"Searching for objects that are {' '.join(left_words)} AND NOT {not_word}...")
        
        # Handle simple 'not' operator (highest precedence for simple cases)
        if 'not' in query_words and 'and' not in query_words and 'or' not in query_words:
            not_index = query_words.index('not')
            if not_index + 1 < len(query_words):
                negated_word = query_words[not_index + 1]
                entry = self._lexicon.get_entry(negated_word)
                if entry and entry.word_type in ['property', 'noun']:
                    condition = {'operator': 'not', 'condition': {'operator': 'filter', 'function': entry.meaning_function}}
                    return ExecutionPlan(action_type='COMPLEX_FILTER', details=condition, feedback=f"Searching for objects that are NOT {negated_word}...")
        
        # Handle 'and' operator
        if 'and' in query_words and 'not' not in query_words:
            and_index = query_words.index('and')
            left_words = query_words[:and_index]
            right_words = query_words[and_index + 1:]
            
            left_filters = []
            for w in left_words:
                entry = self._lexicon.get_entry(w)
                if entry and entry.word_type in ['property', 'noun']:
                    left_filters.append({'operator': 'filter', 'function': entry.meaning_function})
            
            right_filters = []
            for w in right_words:
                entry = self._lexicon.get_entry(w)
                if entry and entry.word_type in ['property', 'noun']:
                    right_filters.append({'operator': 'filter', 'function': entry.meaning_function})
            
            if left_filters and right_filters:
                all_conditions = left_filters + right_filters
                condition = {'operator': 'and', 'conditions': all_conditions}
                return ExecutionPlan(action_type='COMPLEX_FILTER', details=condition, feedback=f"Searching for objects that match ALL conditions: {' AND '.join(query_words)}...")
        
        # Handle 'or' operator
        if 'or' in query_words:
            or_index = query_words.index('or')
            left_words = query_words[:or_index]
            right_words = query_words[or_index + 1:]
            
            left_filters = []
            for w in left_words:
                entry = self._lexicon.get_entry(w)
                if entry and entry.word_type in ['property', 'noun']:
                    left_filters.append({'operator': 'filter', 'function': entry.meaning_function})
            
            right_filters = []
            for w in right_words:
                entry = self._lexicon.get_entry(w)
                if entry and entry.word_type in ['property', 'noun']:
                    right_filters.append({'operator': 'filter', 'function': entry.meaning_function})
            
            if left_filters and right_filters:
                all_conditions = left_filters + right_filters
                condition = {'operator': 'or', 'conditions': all_conditions}
                return ExecutionPlan(action_type='COMPLEX_FILTER', details=condition, feedback=f"Searching for objects that match ANY condition: {' OR '.join(query_words)}...")
        
        return None

    def _parse_condition(self, condition_words: List[str]) -> Optional[Dict[str, Any]]:
        """Parses a condition phrase into a structured condition for evaluation."""
        if not condition_words:
            return None
        
        # Pattern: "I have <OBJECT_SPEC>" (NEW v9.0 - inventory-based conditions)
        if len(condition_words) >= 3 and condition_words[0] == 'i' and condition_words[1] == 'have':
            obj_spec_words = condition_words[2:]  # e.g., ["a", "red", "box"]
            
            # Remove articles
            filtered_words = [w for w in obj_spec_words if w not in ['a', 'an', 'the']]
            
            # CRITICAL: Check for unknown words first - fail if any unknown words are present
            unknown_words = []
            for w in filtered_words:
                entry = self._lexicon.get_entry(w)
                if not entry or entry.word_type not in ['property', 'noun']:
                    unknown_words.append(w)
            
            # If unknown words found, this condition parsing fails
            if unknown_words:
                return None  # Fail condition parsing for unknown concepts
            
            # Extract property filters
            property_filters, _unused_unknown = self._extract_property_filters(filtered_words)
            
            if property_filters:
                return {
                    'operator': 'inventory_check',
                    'owner': 'alla',
                    'filters': property_filters,
                    'description': ' '.join(filtered_words)
                }
        
        # Pattern: "you have <OBJECT_SPEC>" (NEW v9.0 - hypothetical inventory checks for other agents)
        if len(condition_words) >= 3 and condition_words[0] == 'you' and condition_words[1] == 'have':
            obj_spec_words = condition_words[2:]  # e.g., ["a", "red", "box"]
            
            # Remove articles
            filtered_words = [w for w in obj_spec_words if w not in ['a', 'an', 'the']]
            
            # CRITICAL: Check for unknown words first - fail if any unknown words are present
            unknown_words = []
            for w in filtered_words:
                entry = self._lexicon.get_entry(w)
                if not entry or entry.word_type not in ['property', 'noun']:
                    unknown_words.append(w)
            
            # If unknown words found, this condition parsing fails
            if unknown_words:
                return None  # Fail condition parsing for unknown concepts
            
            # Extract property filters
            property_filters, _unused_unknown = self._extract_property_filters(filtered_words)
            
            if property_filters:
                return {
                    'operator': 'inventory_check',
                    'owner': 'user',
                    'filters': property_filters,
                    'description': ' '.join(filtered_words)
                }
        
        # Pattern: "<OBJECT> is <PROPERTY>" (e.g., "a is red")
        if len(condition_words) == 3 and condition_words[1] == 'is':
            obj_name = condition_words[0]
            property_word = condition_words[2]
            
            # Check if object exists
            target_obj = self._world.get_object(name=obj_name)
            if not target_obj:
                # Return a condition that will always evaluate to False for non-existent objects
                return {
                    'operator': 'property_check',
                    'object_name': obj_name,
                    'property_function': lambda obj: False,  # Non-existent object condition
                    'property_word': property_word,
                    'object_exists': False
                }
                
            # Check if property is valid
            prop_entry = self._lexicon.get_entry(property_word)
            if prop_entry and prop_entry.word_type in ['property', 'noun']:
                return {
                    'operator': 'property_check',
                    'object_name': obj_name,
                    'property_function': prop_entry.meaning_function,
                    'property_word': property_word,
                    'object_exists': True
                }
        
        # Pattern: "<OBJECT> <RELATION> <OBJECT>" (e.g., "a above b")
        if len(condition_words) == 3:
            obj1_name = condition_words[0]
            relation_word = condition_words[1]
            obj2_name = condition_words[2]
            
            obj1 = self._world.get_object(name=obj1_name)
            obj2 = self._world.get_object(name=obj2_name)
            relation_entry = self._lexicon.get_entry(relation_word)
            
            if obj1 and obj2 and relation_entry and relation_entry.word_type == 'relation':
                return {
                    'operator': 'relation_check',
                    'object1_name': obj1_name,
                    'object2_name': obj2_name,
                    'relation_function': relation_entry.meaning_function,
                    'relation_word': relation_word
                }
        
        # Pattern: "there is a <PROPERTY> <NOUN>" (e.g., "there is a red box")
        if len(condition_words) >= 4 and condition_words[0] == 'there' and condition_words[1] == 'is' and condition_words[2] == 'a':
            filter_words = condition_words[3:]
            found_filters = []
            
            for w in filter_words:
                entry = self._lexicon.get_entry(w)
                if entry and entry.word_type in ['property', 'noun']:
                    found_filters.append(entry.meaning_function)
            
            if found_filters:
                return {
                    'operator': 'existence_check',
                    'filters': found_filters,
                    'description': ' '.join(filter_words)
                }
        
        return None

class ExecutionEngine:
    """(UPGRADED v11.0) Acts on a wider variety of plans including learning operations."""
    def __init__(self, world: LivingWorld, lexicon: Lexicon, engine_reference=None):
        self._world = world
        self._lexicon = lexicon  # NEW v11.0: Access to lexicon for learning
        self._engine_reference = engine_reference  # NEW v11.0: Reference to main engine for teaching

    def execute(self, plan: ExecutionPlan) -> Any:
        """Executes a plan and returns a result."""
        action_type = plan.action_type
        details = plan.details

        if action_type == 'FILTER_OBJECTS':
            current_objects = self._world.get_all_objects()
            for f in details.get('filters', []):
                current_objects = [obj for obj in current_objects if f(obj)]
            return current_objects
        
        elif action_type == 'VERIFY_RELATION':
            return details['relation_func'](details['obj1'], details['obj2'])

        elif action_type == 'CREATE_OBJECT':
            return self._world.create_object(details['name'], details['shape'], details['color'], details.get('size', 5), details.get('material', 'unknown'))

        elif action_type == 'DESTROY_OBJECT':
            return self._world.destroy_object(details['name'])

        elif action_type == 'QUERY_PROPERTY':
            # e.g., "where is A"
            target_obj = details['target']
            prop_name = details['property_name']
            return getattr(target_obj, prop_name, "Property not found.")

        elif action_type == 'VERIFY_PROPERTY':
            # e.g., "is A red?"
            target_obj = details['target']
            property_func = details['property_func']
            return property_func(target_obj) # Returns True or False

        elif action_type == 'VERIFY_COMPARISON':
            # e.g., "is A same as B?"
            obj1 = details['obj1']
            obj2 = details['obj2']
            if details['type'] == 'same':
                return obj1.get_properties() == obj2.get_properties()
            elif details['type'] == 'different':
                return obj1.get_properties() != obj2.get_properties()
            return False

        elif action_type == 'COMPLEX_FILTER':
            # Recursive logical evaluation
            all_objects = self._world.get_all_objects()
            return [obj for obj in all_objects if self._evaluate_condition(obj, details)]

        # --- NEW v6.0 TEMPORAL HANDLERS ---
        elif action_type == 'LIST_EVENTS':
            # Return all events in chronological order
            return self._world.get_events()

        # NEW v10.0: Enhanced event querying
        elif action_type == 'QUERY_EVENT':
            # Query for specific events involving an object
            target_name = details['target_name']
            event_action_type = details['event_action_type']
            
            # Search through events backwards to find the most recent matching event
            for event in reversed(self._world.get_events()):
                event_details = event.details
                event_target = event_details.get('name', '').lower()
                
                if event.type == event_action_type and event_target == target_name.lower():
                    return event  # Return the entire event object
            
            # No matching event found - create a helpful error message
            return f"No {event_action_type.lower()} event found for object '{target_name}' in the event history."

        elif action_type == 'QUERY_EVENTS':
            # Query events based on temporal operators
            operator = details['operator']
            event_id = details['event_id']
            all_events = self._world.get_events()
            
            if operator == 'before':
                return [event for event in all_events if event.id < event_id]
            elif operator == 'after':
                return [event for event in all_events if event.id > event_id]
            else:
                return []

        # --- NEW v7.0 CONDITIONAL HANDLERS (UPGRADED v9.0) ---
        elif action_type == 'CONDITIONAL_EXECUTION':
            # Execute conditional logic: IF condition THEN action
            condition_result = self._evaluate_condition_plan(plan.condition)
            
            if condition_result:
                # Condition is true, execute the true branch
                if plan.sub_plan_true:
                    return self.execute(plan.sub_plan_true)
            else:
                # Condition is false, execute the false branch if it exists
                if plan.sub_plan_false:
                    return self.execute(plan.sub_plan_false)
            
            return f"Condition evaluated to: {'True' if condition_result else 'False'}"

        elif action_type == 'HYPOTHETICAL_QUERY':
            # Evaluate "what if" without modifying the world
            condition_result = self._evaluate_condition_plan(plan.condition)
            condition_text = details.get('condition_text', 'unknown condition')
            
            return f"If {condition_text}: {'This condition would be True' if condition_result else 'This condition would be False'}"

        # --- NEW v8.0 INTERACTION HANDLERS ---
        elif action_type == 'TRANSFER_OBJECT':
            # Transfer ownership of an object
            obj = details['object']
            new_owner = details['new_owner']
            success = self._world.transfer_ownership(obj, new_owner)
            return obj if success else None

        elif action_type == 'QUERY_INVENTORY':
            # Query objects owned by a specific agent
            owner_name = details['owner']
            return self._world.get_objects_by_owner(owner_name)

        # --- ERROR HANDLING ---
        elif action_type == 'PARSE_ERROR':
            # Handle parsing errors with detailed feedback - return None so test scripts work properly
            return None

        # --- NEW v11.0 LEARNING HANDLER ---
        elif action_type == 'LEARN_NEW_WORD':
            # Delegate the learning to the main engine which has the teaching logic
            if self._engine_reference:
                word = details['word']
                word_type = details['type']
                expression = details['expression']
                return self._engine_reference._teach_word(word, word_type, expression)
            else:
                return "Learning failed: No engine reference available"
        
        # --- HELP SYSTEM ---
        elif action_type == 'SHOW_HELP':
            help_type = details.get('help_type', 'general')
            if help_type == 'teach':
                return """
TEACH COMMAND SYNTAX:
teach [type] "word" as "expression"

Valid types: property, noun, relation, action, inquiry, operator, temporal, conditional, pronoun

Examples:
- teach property "sparkly" as "obj.material == 'glitter'"
- teach noun "sphere" as "obj.shape == 'sphere'"
- teach relation "next_to" as "abs(obj1.position[0] - obj2.position[0]) <= 1"
- teach action "jump" as "none"

Use double quotes around words and expressions. Escape internal quotes with backslash (\").
"""

        # --- NEW v9.0 INVENTORY VERIFICATION HANDLER ---
        elif action_type == 'VERIFY_INVENTORY':
            # Check if an agent possesses objects matching specific criteria
            owner_name = details['owner']
            filters = details.get('filters', [])
            description = details.get('description', 'object')
            
            # Get all objects owned by the agent
            owned_objects = self._world.get_objects_by_owner(owner_name)
            
            # Check if any owned object matches all the filters
            for obj in owned_objects:
                if all(f(obj) for f in filters):
                    return True  # Found a matching object
            
            return False  # No matching object found

        elif action_type == 'KNOWLEDGE_QUERY':
            # NEW v14.0: Answer abstract knowledge queries using SemanticMemory
            query = details.get('query', '')
            if self._engine_reference and hasattr(self._engine_reference, 'semantic_memory'):
                results = self._engine_reference.semantic_memory.query_knowledge(query)
                return '\n'.join(results)
            else:
                return "Semantic memory not available."

        # --- NEW v15.0 ENHANCED PLANNING HANDLERS ---
        elif action_type == 'TAKE_FROM_CONTAINER':
            # Remove object from container first
            obj = details['object']
            container = details['container']
            if hasattr(container, 'contains') and obj.id in container.contains:
                container.contains.remove(obj.id)
                obj.position = None  # Object is now free-floating
                return f"Removed {obj.name} from {container.name}"
            else:
                return f"Failed: {obj.name} is not in {container.name}"

        elif action_type == 'VERIFY_EXISTENCE':
            # Check if objects matching criteria exist in the world
            filters = details.get('filters', [])
            all_objects = self._world.get_all_objects()
            for obj in all_objects:
                if all(f(obj) for f in filters):
                    return True
            return False

        # --- NEW v16.0 INQUIRY-DRIVEN LEARNING HANDLERS ---
        elif action_type == 'TRIGGER_UNDERSTAND_GOAL':
            # Create a new UNDERSTAND goal for an unknown word
            if self._engine_reference:
                unknown_word = details['unknown_word']
                context = details.get('context', '')
                return self._engine_reference._create_understand_goal(unknown_word, context)
            else:
                return "Failed to create understanding goal: No engine reference available"

        elif action_type == 'OUTPUT_QUESTION':
            # Output a question to the user interface
            question = details['question']
            unknown_word = details.get('unknown_word', 'unknown')
            print(f"\n[ALLA ASKS] {question}")
            return f"Question asked about '{unknown_word}'"

        elif action_type == 'VERIFY_UNDERSTANDING':
            # Check if ALLA now understands a word (i.e., it's in the lexicon)
            unknown_word = details['unknown_word']
            entry = self._lexicon.get_entry(unknown_word)
            return entry is not None  # True if word is now in lexicon, False otherwise

    def _evaluate_condition(self, obj: WorldObject, condition: Dict[str, Any]) -> bool:
        """Recursively evaluates a nested logical condition for a single object."""
        op = condition['operator']
        
        if op == 'and':
            # Returns true if ALL sub-conditions are true
            return all(self._evaluate_condition(obj, sub_cond) for sub_cond in condition['conditions'])
        
        elif op == 'or':
            # Returns true if ANY sub-condition is true
            return any(self._evaluate_condition(obj, sub_cond) for sub_cond in condition['conditions'])

        elif op == 'not':
            # Negates the result of the sub-condition
            return not self._evaluate_condition(obj, condition['condition'])
            
        elif op == 'filter':
            # This is the base case: a simple filter function
            filter_func = condition['function']
            return filter_func(obj)

        return False

    def _evaluate_condition_plan(self, condition: Optional[Dict[str, Any]]) -> bool:
        """Evaluates a condition plan and returns True or False."""
        if not condition:
            return False
        
        operator = condition['operator']
        
        if operator == 'inventory_check':
            # NEW v9.0: Check if an agent possesses objects matching criteria
            owner = condition['owner']
            filters = condition['filters']
            
            owned_objects = self._world.get_objects_by_owner(owner)
            
            # Check if any owned object matches all the filters
            for obj in owned_objects:
                if all(f(obj) for f in filters):
                    return True
            return False
        
        elif operator == 'property_check':
            # Check if an object has a specific property
            obj_name = condition['object_name']
            property_function = condition['property_function']
            
            # Handle non-existent objects explicitly
            if not condition.get('object_exists', True):
                return False
            
            target_obj = self._world.get_object(name=obj_name)
            if target_obj:
                return property_function(target_obj)
            return False
        
        elif operator == 'relation_check':
            # Check if two objects have a specific relationship
            obj1_name = condition['object1_name']
            obj2_name = condition['object2_name']
            relation_function = condition['relation_function']
            
            obj1 = self._world.get_object(name=obj1_name)
            obj2 = self._world.get_object(name=obj2_name)
            
            if obj1 and obj2:
                return relation_function(obj1, obj2)
            return False
        
        elif operator == 'existence_check':
            # Check if there exists an object matching the filters
            filters = condition['filters']
            current_objects = self._world.get_all_objects()
            
            for obj in current_objects:
                if all(f(obj) for f in filters):
                    return True
            return False
        
        return False

# ==============================================================================
# PART 3: THE MAIN ORCHESTRATOR (THE ENGINE)
# ==============================================================================

class AllaEngine:
    """(UPGRADED v11.0) The core engine with self-education and persistent memory."""

    def __init__(self, memory_path: str = "alla_memory.json"):
        """(UPGRADED v15.0) Initializes the integrated and stable foundational mind."""
        print("[AllaEngine v15.0] Initializing cognitive components...")
        self.world = LivingWorld()
        self.world.load_state("genesis_world.json")  # Load the external world
        self.lexicon = Lexicon()
        self.command_processor = CommandProcessor(self.lexicon, self.world)
        self.execution_engine = ExecutionEngine(self.world, self.lexicon, self)  # Pass self as engine reference
        self.planner = Planner(self.world, self.lexicon)  # UPGRADED v15.0: Enhanced planning
        self.semantic_memory = SemanticMemory()  # NEW v14.0: Abstract knowledge
        self.memory_path = Path(memory_path)
        
        # NEW v13.0: Goal and Planning System
        self.active_goals: List[Goal] = []
        self.active_plans: Dict[int, Plan] = {}  # Maps goal_id to a plan
        
        # NEW v14.0: Reflection System
        self.last_reflection_event = 0  # Track when we last reflected
        self.reflection_interval = 5  # Reflect every 5 events
        
        self.load_lexicon()  # Load learned knowledge on startup
        print("[AllaEngine v15.0] Ready. The integrated and stable foundational mind is online!")

    def _create_function_from_expression(self, word_type: str, meaning_expression: str) -> Callable:
        """(UPGRADED v8.0) Now supports 'pronoun' types."""
        try:
            if word_type in ['property', 'noun']:
                return eval(f"lambda obj: {meaning_expression}")
            elif word_type == 'relation':
                return eval(f"lambda obj1, obj2: {meaning_expression}")
            elif word_type in ['action', 'inquiry', 'operator', 'temporal', 'conditional', 'pronoun']:
                # Actions, inquiries, operators, temporal, conditional, and pronoun words don't have lambdas; they are identified by their name.
                return lambda: None 
            else:
                raise ValueError(f"Word type '{word_type}' is not supported.")
        except SyntaxError as e:
            raise SyntaxError(f"Invalid meaning expression: '{meaning_expression}' -> {e}")

    # NEW v11.0: Teaching and Memory Management Methods
    def _teach_word(self, word: str, word_type: str, expression: str) -> str:
        """Internal method to teach a new word and add it to the lexicon."""
        try:
            # Create the function from the expression
            meaning_function = self._create_function_from_expression(word_type, expression)
            
            # Create and add the word entry
            entry = WordEntry(word, word_type, expression, meaning_function)
            self.lexicon.add_entry(entry)
            
            return f"Successfully learned new {word_type}: '{word}' with meaning '{expression}'"
        except Exception as e:
            return f"Failed to learn word '{word}': {e}"

    def load_lexicon(self):
        """Loads the lexicon from the memory file."""
        print(f"[AllaEngine] Attempting to load memory from '{self.memory_path}'...")
        if not self.memory_path.is_file():
            print("[AllaEngine] No memory file found. Starting with a blank slate.")
            return
        try:
            with self.memory_path.open('r') as f:
                learned_words = json.load(f)
                count = 0
                for word, data in learned_words.items():
                    self._teach_word(word, data['word_type'], data['meaning_expression'])
                    count += 1
                print(f"[AllaEngine] Successfully loaded {count} concepts from memory.")
        except Exception as e:
            print(f"[ERROR] Failed to load memory file: {e}")

    def save_lexicon(self):
        """Saves the current state of the lexicon to a file."""
        print(f"\n[AllaEngine] Saving {self.lexicon.get_word_count()} concepts to '{self.memory_path}'...")
        to_save = {}
        for word, entry in self.lexicon.get_all_entries().items():
            to_save[word] = {
                'word_type': entry.word_type,
                'meaning_expression': entry.meaning_expression
            }
        try:
            with self.memory_path.open('w') as f:
                json.dump(to_save, f, indent=4)
            print("[AllaEngine] Memory saved successfully.")
        except Exception as e:
            print(f"[ERROR] Failed to save memory: {e}")

    def shutdown(self):
        """Properly shuts down the engine and saves memory."""
        print("\n[AllaEngine] Shutting down...")
        self.save_lexicon()
        print("[AllaEngine] Goodbye!")

    def learn_from_file(self, file_path: Path):
        """Reads a .alla curriculum file and implants concepts into the Lexicon."""
        print(f"\n[AllaEngine] Starting learning session from: '{file_path}'")
        if not file_path.is_file():
            print(f"[ERROR] Curriculum file not found at '{file_path}'")
            return

        with file_path.open('r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'): continue
                parts = [p.strip() for p in line.split('::')]
                if len(parts) != 3: continue
                word_type, word, expression = parts
                try:
                    meaning_function = self._create_function_from_expression(word_type, expression)
                    self.lexicon.add_entry(WordEntry(word, word_type, expression, meaning_function))
                except Exception as e:
                    print(f"[ERROR] Could not learn word '{word}': {e}")
        print("[AllaEngine] Learning session complete.")

    def process_command(self, command_text: str) -> Tuple[str, Any]:
        """A high-level API to process a command and return a tuple of (feedback, result)."""
        plan = self.command_processor.parse(command_text)
        if not plan:
            return ("Command not understood or invalid.", None)
        result = self.execution_engine.execute(plan)
        return (plan.feedback, result)

    # =====================================================================
    # NEW v13.0: GOAL AND PLANNING SYSTEM
    # =====================================================================

    def set_goal(self, goal_description: str) -> Optional[Goal]:
        """(FIXED v15.0) High-level command to give the agent a new goal with improved parsing."""
        # CRITICAL FIX B12: Improved goal parsing logic
        
        # Handle "i have X" pattern
        if goal_description.lower().startswith('i have'):
            condition_command = f"do {goal_description.lower()}"
            condition_plan = self.command_processor.parse(condition_command)
            
            if condition_plan and condition_plan.action_type == 'VERIFY_INVENTORY':
                new_goal = Goal(
                    id=len(self.active_goals) + 1,
                    description=goal_description,
                    completion_condition=condition_plan
                )
                self.active_goals.append(new_goal)
                print(f"[ALLA] New goal accepted: '{goal_description}'")
                return new_goal
        
        # Handle "there is X" pattern (existence goals)
        elif 'exists' in goal_description.lower() or goal_description.lower().startswith('there is'):
            # Convert to existence check
            if 'exists' in goal_description.lower():
                obj_desc = goal_description.lower().replace('exists', '').strip()
            else:
                obj_desc = goal_description.lower().replace('there is', '').strip().replace('a ', '')
            
            # Create a verification plan for existence
            words = obj_desc.split()
            found_filters = []
            for w in words:
                entry = self.lexicon.get_entry(w)
                if entry and entry.word_type in ['property', 'noun']:
                    found_filters.append(entry.meaning_function)
            
            if found_filters:
                condition_plan = ExecutionPlan(
                    action_type='VERIFY_EXISTENCE',
                    details={'filters': found_filters},
                    feedback=f"Checking if {obj_desc} exists..."
                )
                new_goal = Goal(
                    id=len(self.active_goals) + 1,
                    description=goal_description,
                    completion_condition=condition_plan
                )
                self.active_goals.append(new_goal)
                print(f"[ALLA] New goal accepted: '{goal_description}'")
                return new_goal
        
        print(f"[ALLA] Could not understand goal: '{goal_description}'")
        print(f"[ALLA] Supported patterns: 'i have X', 'X exists', 'there is X'")
        return None

    def _create_understand_goal(self, unknown_word: str, context: str = '') -> str:
        """(NEW v16.0) Creates an UNDERSTAND goal for learning about an unknown word."""
        goal_description = f"I understand '{unknown_word}'"
        
        # Create a simple condition plan for UNDERSTAND goals
        condition_plan = ExecutionPlan(
            action_type='VERIFY_UNDERSTANDING',
            details={'unknown_word': unknown_word, 'context': context},
            feedback=f"Checking if I understand '{unknown_word}'..."
        )
        
        new_goal = Goal(
            id=len(self.active_goals) + 1,
            description=goal_description,
            completion_condition=condition_plan,
            goal_type='UNDERSTAND',
            inquiry_question=f"What is a '{unknown_word}'? Please describe it so I can understand."
        )
        
        self.active_goals.append(new_goal)
        print(f"[ALLA] New inquiry goal created: '{goal_description}'")
        return f"Created understanding goal for '{unknown_word}'"

    def tick(self):
        """(NEW v13.0) A single 'thought' cycle for the agent."""
        print("\n--- ALLA's Turn (Thinking...) ---")
        
        # Step 1: Review active goals
        for goal in self.active_goals:
            if goal.status == 'active':
                # Is the goal already complete?
                is_complete = self.execution_engine.execute(goal.completion_condition)
                if is_complete:
                    goal.status = 'completed'
                    print(f"[ALLA] Goal '{goal.description}' has been completed!")
                    # Remove the plan since goal is done
                    if goal.id in self.active_plans:
                        del self.active_plans[goal.id]
                    continue

                # Do I have a plan for this goal?
                if goal.id not in self.active_plans:
                    print(f"[ALLA] No plan for goal '{goal.description}'. Creating one...")
                    plan = self.planner.create_plan_for_goal(goal)
                    if plan:
                        self.active_plans[goal.id] = plan
                        print(f"[ALLA] New plan created with {len(plan.steps)} step(s).")
                    else:
                        print(f"[ALLA] Could not create a plan for goal '{goal.description}'.")
                
                # If I have a plan, execute the next step
                if goal.id in self.active_plans:
                    plan = self.active_plans[goal.id]
                    if plan.current_step < len(plan.steps):
                        step = plan.steps[plan.current_step]
                        print(f"[ALLA] Executing step {plan.current_step + 1} of plan for goal '{goal.description}':")
                        print(f"[ALLA] -> {step.feedback}")
                        result = self.execution_engine.execute(step)
                        if result:
                            print(f"[ALLA] Step completed successfully: {result}")
                        plan.current_step += 1
                    else:
                        # Plan is finished, let the next tick re-evaluate the goal status
                        del self.active_plans[goal.id]
                        print(f"[ALLA] Plan for goal '{goal.description}' is complete. Re-evaluating on next tick.")

        # Finally, advance the world time
        self.world.tick()
        
        # NEW v14.0: Check if it's time to reflect on recent experiences
        self._check_and_reflect()

    def _check_and_reflect(self):
        """(NEW v14.0) Check if it's time to run a reflection cycle."""
        event_count = len(self.world.get_events())
        
        if event_count - self.last_reflection_event >= self.reflection_interval:
            print(f"\n[ALLA] Time to reflect... (processed {event_count - self.last_reflection_event} new events)")
            self._reflection_cycle()
            self.last_reflection_event = event_count

    def _reflection_cycle(self):
        """(NEW v14.0) Analyze recent events to form abstract knowledge."""
        # Get recent events for analysis
        all_events = self.world.get_events()
        recent_events = all_events[self.last_reflection_event:]
        
        print(f"[ALLA] Reflecting on {len(recent_events)} recent experiences...")
        
        insights = 0
        for event in recent_events:
            insights += self._extract_concepts_from_event(event)
        
        if insights > 0:
            print(f"[ALLA] Formed {insights} new abstract insights!")
        else:
            print("[ALLA] No new patterns detected in this reflection cycle.")

    def _extract_concepts_from_event(self, event) -> int:
        """(FIXED v15.0) Extract abstract concepts and relationships from a single event."""
        insights_formed = 0
        details = getattr(event, 'details', {})
        obj_id = details.get('object_id')
        obj = self.world.get_object(obj_id) if obj_id is not None else None
        
        # CRITICAL FIX B11: Also check for objects that were just created
        if not obj and details.get('name'):
            obj_name = details.get('name')
            if obj_name:
                obj = self.world.get_object(name=obj_name)
        
        if obj:
            # Extract color concept
            if hasattr(obj, 'color') and obj.color:
                color = obj.color
                color_node = SemanticNode(
                    id=f"concept:{color}",
                    concept_type="value",
                    name=color,
                    observations=1
                )
                self.semantic_memory.add_node(color_node)
                color_prop_node = SemanticNode(
                    id="concept:color",
                    concept_type="property",
                    name="color",
                    observations=1
                )
                self.semantic_memory.add_node(color_prop_node)
                self.semantic_memory.add_edge(SemanticEdge(
                    from_node=f"concept:{color}",
                    to_node="concept:color",
                    relationship="is_value_of"
                ))
                insights_formed += 1
                print(f"[REFLECTION] Learned about color: {color}")
            
            # Extract shape concept
            if hasattr(obj, 'shape') and obj.shape:
                shape = obj.shape
                shape_node = SemanticNode(
                    id=f"concept:{shape}",
                    concept_type="value",
                    name=shape,
                    observations=1
                )
                self.semantic_memory.add_node(shape_node)
                shape_prop_node = SemanticNode(
                    id="concept:shape",
                    concept_type="property",
                    name="shape",
                    observations=1
                )
                self.semantic_memory.add_node(shape_prop_node)
                self.semantic_memory.add_edge(SemanticEdge(
                    from_node=f"concept:{shape}",
                    to_node="concept:shape",
                    relationship="is_value_of"
                ))
                insights_formed += 1
                print(f"[REFLECTION] Learned about shape: {shape}")
            
            # Extract material concept
            if hasattr(obj, 'material') and obj.material and obj.material != 'unknown':
                material = obj.material
                material_node = SemanticNode(
                    id=f"concept:{material}",
                    concept_type="value",
                    name=material,
                    observations=1
                )
                self.semantic_memory.add_node(material_node)
                material_prop_node = SemanticNode(
                    id="concept:material",
                    concept_type="property",
                    name="material",
                    observations=1
                )
                self.semantic_memory.add_node(material_prop_node)
                self.semantic_memory.add_edge(SemanticEdge(
                    from_node=f"concept:{material}",
                    to_node="concept:material",
                    relationship="is_value_of"
                ))
                insights_formed += 1
                print(f"[REFLECTION] Learned about material: {material}")
        
        # Extract action concepts from event type
        event_type = getattr(event, 'type', '').lower()
        if event_type in ['create', 'transfer', 'destroy']:
            action_node = SemanticNode(
                id=f"concept:{event_type}",
                concept_type="action",
                name=event_type,
                observations=1
            )
            self.semantic_memory.add_node(action_node)
            insights_formed += 1
            print(f"[REFLECTION] Learned about action: {event_type}")
        
        return insights_formed

    def main_loop(self):
        """(NEW v13.0) The proactive main loop where ALLA thinks and acts autonomously."""
        import time
        
        print("\n" + "="*60)
        print("STARTING ALLA v13.0 AUTONOMOUS THINKING LOOP")
        print("ALLA will now think and act on its own goals.")
        print("Press Ctrl+C to stop.")
        print("="*60)
        
        try:
            tick_count = 0
            while True:
                tick_count += 1
                print(f"\n=== TICK {tick_count} ===")
                
                # Agent's own thought cycle
                self.tick()
                
                # Brief pause between thoughts
                time.sleep(2)
                
        except KeyboardInterrupt:
            print("\n[ALLA] Autonomous thinking loop stopped by user.")
            self.shutdown()
