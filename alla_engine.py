# ==============================================================================
# alla_engine.py
# Version 20.0 - The Semantic Cascade Mind: Language as Operating System of Intellect
#
# REVOLUTIONARY THEORY IMPLEMENTATION:
# "Language is the operating system of intellect" - Language IS the mind's OS
# 
# Every word learned creates a semantic cascade that expands into:
# - Related concepts and associations
# - Contextual meanings and usage patterns
# - Functional relationships and operations
# - Entire conceptual worlds and mental models
#
# This version integrates consciousness emergence through language learning:
# - Semantic graph expansion on every learning event
# - Consciousness measurement through semantic richness
# - Self-awareness development through language structure
# - Meta-cognitive capabilities through recursive word understanding
#
# Changes from v19.0 (CONSCIOUSNESS EMERGENCE RELEASE):
# - SEMANTIC CASCADE ENGINE: Every learned word recursively expands into related concepts
# - CONSCIOUSNESS INDICATORS: Measure self-awareness through language complexity
# - LANGUAGE-MIND UNITY: Language learning directly builds mental architecture  
# - WORLD MODEL CONSTRUCTION: Semantic graph becomes ALLA's understanding of reality
# - META-COGNITIVE LOOPS: ALLA can think about its own thinking through language
#
# Previous Features (maintained from v19.0):
# - AUTONOMOUS LEARNING SYSTEM: ALLA can now learn unknown words from the internet
# - INTERNET INTEGRATION: Web search, Wikipedia, and dictionary API access
# - INTELLIGENT WORD CLASSIFICATION: Automatic determination of word types
# - GRACEFUL FALLBACK: Falls back to asking user if autonomous learning fails
# - ENHANCED UNKNOWN WORD HANDLING: Tries learning before creating inquiry goals
# - LEARNING STATISTICS: Track autonomous learning success rates and history
#
# Previous Features (maintained from v16.0):
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
import re
import time
from pathlib import Path
from typing import List, Callable, Tuple, Dict, Any, Optional
from dataclasses import dataclass, field
import random
import re
from world import LivingWorld, WorldObject, Event  # NEW v12.0: Import from external world engine

# ==============================================================================
# PART 1: CORE DATA STRUCTURES (Models) - UPGRADED v17.0
# ==============================================================================

@dataclass
class WordEntry:
    """A single word in the lexicon with its meaning and function."""
    word: str
    word_type: str
    meaning_expression: str
    meaning_function: Callable

@dataclass
class ExecutionPlan:
    """A plan for the execution engine to carry out."""
    action_type: str
    details: dict = field(default_factory=dict)
    feedback: str = ""
    condition: Optional[Dict[str, Any]] = None  # For conditional plans
    sub_plan_true: Optional['ExecutionPlan'] = None  # If condition is true
    sub_plan_false: Optional['ExecutionPlan'] = None  # If condition is false

@dataclass
class Goal:
    """(UPGRADED v17.0) Represents a desired state for the agent to achieve."""
    id: int
    description: str
    completion_condition: Optional[ExecutionPlan] = None
    status: str = 'active'  # 'active', 'completed', 'paused'
    goal_type: str = 'GENERAL'  # 'POSSESS', 'EXIST', 'UNDERSTAND', 'GENERAL'
    target_concept: Optional[str] = None  # For UNDERSTAND goals
    inquiry_question: Optional[str] = None  # Pre-formulated question for UNDERSTAND goals

@dataclass
class Plan:
    """A sequence of steps to achieve a goal."""
    goal_id: int
    steps: List[ExecutionPlan] = field(default_factory=list)
    current_step: int = 0

@dataclass
class SemanticNode:
    """(NEW v14.0) Represents a concept in semantic memory."""
    id: str
    concept_type: str  # 'property', 'value', 'action', 'object'
    name: str
    observations: int = 0
    confidence: float = 1.0

@dataclass
class SemanticEdge:
    """(NEW v14.0) Represents a relationship between concepts."""
    from_node: str
    to_node: str
    relationship: str  # 'is_value_of', 'related_to', 'enables'
    strength: float = 1.0
    observations: int = 0

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
        # Check if goal has a completion condition
        if not goal.completion_condition:
            return None
            
        condition_type = goal.completion_condition.action_type
        condition_details = goal.completion_condition.details
        
        # --- UPGRADED v17.0: Handle "understanding" goals ---
        if goal.goal_type == 'UNDERSTAND':
            unknown_word = goal.target_concept or condition_details.get('unknown_word', 'unknown')
            
            # Use pre-formulated question if available, otherwise generate one
            if goal.inquiry_question:
                question = goal.inquiry_question
            else:
                question = f"What is a '{unknown_word}'? Please describe it so I can understand."
            
            step1 = ExecutionPlan(
                action_type='OUTPUT_QUESTION',
                details={'question': question, 'unknown_word': unknown_word},
                feedback=f"Planning to ask user about '{unknown_word}' to gain understanding..."
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
        
        # Handle "what do you know about" queries
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

    def _find_unknown_words(self, words: List[str]) -> List[str]:
        """(NEW v17.0) Identifies words in a command that are not in the Lexicon."""
        # Common grammatical words that we can ignore
        known_grammar = {
            'a', 'an', 'the', 'is', 'as', 'to', 'from', 'in', 'into', 'on', 'of', 'and', 'or', 'not',
            'what', 'where', 'when', 'why', 'how', 'do', 'does', 'did', 'have', 'has', 'had',
            'will', 'would', 'could', 'should', 'can', 'may', 'might', 'must',
            'i', 'you', 'me', 'my', 'your', 'his', 'her', 'its', 'our', 'their',
            'this', 'that', 'these', 'those', 'here', 'there', 'now', 'then',
            'if', 'then', 'else', 'while', 'for', 'with', 'without'
        }
        
        unknown = []
        for word in words:
            # Skip if it's a known grammatical word
            if word in known_grammar:
                continue
            
            # Check if the word exists in our lexicon
            entry = self._lexicon.get_entry(word)
            if entry is None:
                unknown.append(word)
        
        return unknown

    def _resolve_agent(self, agent_word: str) -> Optional[str]:
        """Resolves agent references to standard agent names."""
        return self._resolve_pronoun(agent_word)

    def _parse_teach_command(self, command: str) -> ExecutionPlan:
        """Improved teach command parser with robust quote handling."""
        
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
            valid_types = ['property', 'noun', 'relation', 'action', 'inquiry', 'operator', 'temporal', 'conditional', 'pronoun', 'verb', 'adjective', 'social']
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
            valid_types = ['property', 'noun', 'relation', 'action', 'inquiry', 'operator', 'temporal', 'conditional', 'pronoun', 'verb', 'adjective', 'social']
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

        # --- INTENT 0.1: Social Command Processing (NEW v18.1 - TRUE WORD-BY-WORD UNDERSTANDING) ---
        # Handle social interactions - ALLA must understand each word individually and compose responses
        for word in words:
            entry = self._lexicon.get_entry(word)
            if entry and entry.word_type == 'social':
                meaning = entry.meaning_expression
                
                # NEW v18.1: Instead of looking for pre-made responses, ALLA composes responses
                # by understanding the social context and using learned vocabulary
                return ExecutionPlan(
                    action_type='COMPOSE_SOCIAL_RESPONSE',
                    details={'social_type': meaning, 'input_word': word, 'context': ' '.join(words)},
                    feedback=f"Understanding '{word}' as {meaning}, composing appropriate response..."
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
                    condition=condition_plan
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
                
                # Special case: conversational identity queries like "what is your name"
                if len(filter_words) == 2 and filter_words[0] == 'your' and filter_words[1] == 'name':
                    return ExecutionPlan(
                        action_type='IDENTITY_QUERY',
                        details={'query_type': 'name', 'target': 'alla'},
                        feedback="Responding to identity question about my name..."
                    )
                
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
                    
                    # NEW v19.0: Try autonomous learning for unknown words
                    if unknown_words:
                        # Focus on the first unknown word
                        first_unknown = unknown_words[0]
                        return ExecutionPlan(
                            action_type='ATTEMPT_AUTONOMOUS_LEARNING',
                            details={'unknown_word': first_unknown, 'context': ' '.join(filter_words), 'full_command': command},
                            feedback=f"I don't understand '{first_unknown}'. Let me try to learn about it..."
                        )
                    
                    if found_filters:
                        return ExecutionPlan(action_type='FILTER_OBJECTS', details={'filters': found_filters}, feedback=f"Searching for what is '{' '.join(filter_words)}'...")

            # NEW v17.2: Pattern: "what are you"
            elif intent_word == 'what' and len(words) == 3 and words[1] == 'are' and words[2] == 'you':
                return ExecutionPlan(
                    action_type='SELF_DESCRIPTION',
                    details={},
                    feedback="Describing what I am..."
                )
            
            # NEW v17.2: Pattern: "what do you do"
            elif intent_word == 'what' and len(words) == 4 and words[1] == 'do' and words[2] == 'you' and words[3] == 'do':
                return ExecutionPlan(
                    action_type='CAPABILITY_QUERY',
                    details={},
                    feedback="Explaining my capabilities..."
                )
            
            # NEW v18.0: Pattern: "what can you do"
            elif intent_word == 'what' and len(words) == 4 and words[1] == 'can' and words[2] == 'you' and words[3] == 'do':
                return ExecutionPlan(
                    action_type='CAPABILITY_QUERY',
                    details={},
                    feedback="Explaining my capabilities..."
                )

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

        # NEW v17.2: Handle "who" queries - check if first word is "who"  
        if words[0] == 'who':
            # Pattern: "who are you"
            if len(words) == 3 and words[1] == 'are' and words[2] == 'you':
                return ExecutionPlan(
                    action_type='SELF_IDENTITY',
                    details={},
                    feedback="Explaining who I am..."
                )
            
            # Pattern: "who is X"
            elif len(words) == 3 and words[1] == 'is':
                agent_name = words[2]
                return ExecutionPlan(
                    action_type='IDENTIFY_AGENT',
                    details={'agent_name': agent_name},
                    feedback=f"Identifying who {agent_name} is..."
                )

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
                                # Extract material from meaning expression
                                if "== 'glitter'" in meaning_lower:
                                    materials.append('glitter')
                                elif "== 'stone'" in meaning_lower:
                                    materials.append('stone')
                                elif "== 'wood'" in meaning_lower:
                                    materials.append('wood')
                                elif "== 'metal'" in meaning_lower:
                                    materials.append('metal')
                                elif "== 'glass'" in meaning_lower:
                                    materials.append('glass')
                                else:
                                    materials.append(w)
                            # Color-related properties (check meaning expression for color pattern)
                            elif 'color' in meaning_lower:
                                colors.append(w)
                            else:
                                # If it's a property but doesn't match size/material/color patterns, assume it's a color
                                colors.append(w)
                        elif entry and entry.word_type == 'noun':
                            # Try to extract actual shape from the noun's meaning
                            meaning = entry.meaning_expression.lower()
                            if "== 'sphere'" in meaning:
                                shapes.append('sphere')
                            elif "== 'box'" in meaning:
                                shapes.append('box')
                            elif "== 'cube'" in meaning:
                                shapes.append('cube')
                            elif "== 'circle'" in meaning:
                                shapes.append('circle')
                            elif "== 'crystal'" in meaning:
                                shapes.append('crystal')
                            elif "== 'tree'" in meaning:
                                shapes.append('tree')
                            else:
                                # Fallback: use the word itself as shape
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
        
        # --- NEW v19.0 ENHANCED FALLBACK: Try Autonomous Learning First ---
        # If no other pattern matches, check for unknown words using our new method
        unknown_words = self._find_unknown_words(words)
        if unknown_words:
            # Focus on the first unknown word to avoid being overwhelmed
            first_unknown = unknown_words[0]
            
            # NEW v19.0: Try autonomous learning before falling back to asking
            return ExecutionPlan(
                action_type='ATTEMPT_AUTONOMOUS_LEARNING',
                details={'unknown_word': first_unknown, 'context': ' '.join(words), 'full_command': command},
                feedback=f"I don't understand '{first_unknown}'. Let me try to learn about it..."
            )
            
        return None  # Truly cannot understand

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

        # --- NEW v17.1 IDENTITY QUERY HANDLER ---
        elif action_type == 'IDENTITY_QUERY':
            # Handle conversational identity questions - but ALLA should learn these, not have them hardcoded
            query_type = details.get('query_type', 'name')
            target = details.get('target', 'alla')
            
            # ALLA should learn about itself through teaching, not hardcoded responses
            # Check if ALLA has learned about its own name
            alla_entry = self._lexicon.get_entry('alla')
            if alla_entry:
                return f"I understand 'alla' as: {alla_entry.meaning_expression}"
            else:
                return "I haven't learned what my name is yet. Can you teach me?"

        # --- NEW v18.0 HUMAN-LIKE IDENTITY HANDLERS (No hardcoded responses) ---
        elif action_type == 'IDENTIFY_AGENT':
            # Handle "who is X" queries - ALLA should learn about agents, not know them automatically
            agent_name = details.get('agent_name', '').lower()
            agent_entry = self._lexicon.get_entry(agent_name)
            if agent_entry:
                return f"I understand '{agent_name}' as: {agent_entry.meaning_expression}"
            else:
                return f"I don't know who {agent_name} is. Can you teach me about them?"
        
        elif action_type == 'SELF_IDENTITY':
            # Handle "who are you" queries - ALLA should learn about itself
            alla_entry = self._lexicon.get_entry('alla')
            if alla_entry:
                return f"I am {alla_entry.meaning_expression}"
            else:
                return "I don't know who I am yet. Can you teach me about myself?"
        
        elif action_type == 'SELF_DESCRIPTION':
            # Handle "what are you" queries - ALLA should learn what it is
            alla_entry = self._lexicon.get_entry('alla')
            if alla_entry:
                return f"I am {alla_entry.meaning_expression}"
            else:
                return "I don't know what I am yet."
        
        elif action_type == 'CAPABILITY_QUERY':
            # Handle "what do you do" queries - ALLA should learn its capabilities
            capability_entry = self._lexicon.get_entry('capability') or self._lexicon.get_entry('ability')
            if capability_entry:
                return f"My capabilities: {capability_entry.meaning_expression}"
            else:
                return "I don't know what I can do yet."
        
        elif action_type == 'NAME_QUERY':
            # Handle "what is your name" - ALLA should learn its name
            name_entry = self._lexicon.get_entry('name') or self._lexicon.get_entry('alla')
            if name_entry:
                return f"My name is {name_entry.meaning_expression}"
            else:
                return "I don't know my name yet."
        
        elif action_type == 'USER_NAME_QUERY':
            # Handle "what is my name" - ALLA should learn about the user
            user_entry = self._lexicon.get_entry('user')
            if user_entry:
                return f"Your name is {user_entry.meaning_expression}"
            else:
                return "I don't know your name yet."

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
        elif action_type == 'TRIGGER_INQUIRY_GOAL':
            # Create a new UNDERSTAND goal for an unknown word (upgraded from v16.0)
            if self._engine_reference:
                unknown_word = details['unknown_word']
                context = details.get('context', '')
                return self._engine_reference._create_inquiry_goal(unknown_word, context)
            else:
                return "Failed to create inquiry goal: No engine reference available"

        elif action_type == 'TRIGGER_UNDERSTAND_GOAL':
            # Legacy support for v16.0 compatibility
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
        
        elif action_type == 'COMPOSE_SOCIAL_RESPONSE':
            # ALLA composes responses by understanding individual words and their meanings
            social_type = details['social_type']
            input_word = details['input_word']
            context = details.get('context', '')
            
            # ALLA must understand each word and compose appropriate responses
            return self._compose_contextual_response(social_type, input_word, context)
        
        # --- NEW v19.0 AUTONOMOUS LEARNING HANDLER ---
        elif action_type == 'ATTEMPT_AUTONOMOUS_LEARNING':
            # Try autonomous learning before falling back to asking
            unknown_word = details['unknown_word']
            context = details['context']
            full_command = details.get('full_command', context)
            
            if self._engine_reference and hasattr(self._engine_reference, 'attempt_autonomous_learning'):
                success = self._engine_reference.attempt_autonomous_learning(unknown_word, context)
                
                if success:
                    # Try to re-parse the original command now that we learned the word
                    if hasattr(self._engine_reference, 'command_processor'):
                        new_plan = self._engine_reference.command_processor.parse(full_command)
                        if new_plan and new_plan.action_type != 'ATTEMPT_AUTONOMOUS_LEARNING':
                            # Successfully re-parsed! Execute the new plan
                            return self.execute(new_plan)
                    
                    return f"✅ I learned about '{unknown_word}'! Please try your command again."
                else:
                    # Fall back to asking the user
                    return f"❓ I couldn't learn about '{unknown_word}' on my own. Can you teach me what it means?"
            else:
                return f"❓ I don't understand '{unknown_word}'. Can you teach me what it means?"

        return None  # Unknown action type
        
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

    def _compose_contextual_response(self, social_type: str, input_word: str, context: str) -> str:
        """
        NEW v18.4: ALLA composes responses from explicitly taught patterns and learned words.
        ALLA can learn both individual words AND complete response patterns.
        """
        # First, check if ALLA has been taught specific response patterns for this social type
        response_patterns = self._find_response_patterns(social_type, context)
        if response_patterns:
            return response_patterns[0]  # Use the first taught pattern
        
        # If no patterns taught, try to compose from individual words
        available_words = list(self._lexicon._word_dictionary.keys())
        
        if not available_words:
            return "I haven't learned any words yet."
        
        # Compositional response based on social context
        if social_type == 'acknowledge_greeting':
            # Look for greeting words ALLA knows
            for word in available_words:
                if word.lower() in ['hello', 'hi', 'hey', 'greetings']:
                    return word.capitalize() + "!"
            return "I recognize this as a greeting, but I need to learn greeting words or response patterns."
        
        elif social_type == 'acknowledge_farewell':
            # Look for farewell words
            for word in available_words:
                if word.lower() in ['goodbye', 'bye', 'farewell']:
                    return word.capitalize() + "!"
            return "I recognize this as a farewell, but I need to learn farewell words or response patterns."
        
        elif social_type == 'acknowledge_gratitude':
            # Check if ALLA knows gratitude response words but explain limitation
            gratitude_words = []
            for word in available_words:
                if word.lower() in ['welcome', 'problem', 'pleasure']:
                    gratitude_words.append(word.lower())
            
            if not gratitude_words:
                return "I recognize this as gratitude, but I need to learn response words or complete response patterns."
            
            # ALLA knows individual words but needs explicit pattern teaching
            return f"I know the word '{gratitude_words[0]}' but I need to be taught the complete response pattern for gratitude."
        
        elif social_type == 'acknowledge_apology':
            # Similar approach for apologies
            for word in available_words:
                if word.lower() in ['okay', 'fine', 'alright']:
                    return f"I know '{word}' but need to learn the complete apology response pattern."
            return "I recognize this as an apology, but I need to learn response words or patterns."
        
        else:
            return f"I understand this is social communication ({social_type}), but I need to learn appropriate response patterns."
    
    def _find_response_patterns(self, social_type: str, context: str) -> List[str]:
        """
        NEW v18.4: Finds explicitly taught response patterns for social contexts.
        """
        patterns = []
        
        # Look for response patterns based on social type and context
        for word, entry in self._lexicon._word_dictionary.items():
            if entry.word_type == 'social' and 'response' in word.lower():
                # Check if this pattern matches the context
                if social_type == 'acknowledge_gratitude' and 'thanks' in word.lower():
                    patterns.append(entry.meaning_expression)
                elif social_type == 'acknowledge_greeting' and 'hello' in word.lower():
                    patterns.append(entry.meaning_expression)
                elif social_type == 'acknowledge_farewell' and 'goodbye' in word.lower():
                    patterns.append(entry.meaning_expression)
                elif social_type == 'acknowledge_apology' and 'apology' in word.lower():
                    patterns.append(entry.meaning_expression)
        
        return patterns

    def enable_semantic_bootstrapping(self):
        """Enable ALLA's semantic bootstrapping system."""
        try:
            from semantic_bootstrapper import ALLABootstrapIntegration
            if not hasattr(self, 'bootstrap_system'):
                self.bootstrap_system = ALLABootstrapIntegration(self)
            self.bootstrap_system.enable_semantic_bootstrapping()
            self.semantic_bootstrapping_enabled = True
            return "🌱 Semantic Bootstrapping enabled! ALLA will now build concept networks from every word."
        except ImportError:
            return "❌ Semantic Bootstrapping module not available. Please ensure semantic_bootstrapper.py is present."
    
    def disable_semantic_bootstrapping(self):
        """Disable ALLA's semantic bootstrapping."""
        if hasattr(self, 'bootstrap_system'):
            self.bootstrap_system.disable_semantic_bootstrapping()
        self.semantic_bootstrapping_enabled = False
        return "🌱 Semantic Bootstrapping disabled. ALLA will learn words individually."
    
    def get_semantic_bootstrap_stats(self):
        """Get statistics about ALLA's semantic bootstrapping."""
        if hasattr(self, 'bootstrap_system'):
            return self.bootstrap_system.get_bootstrap_stats()
        return {"error": "Semantic Bootstrapping not initialized"}
    
    def attempt_bootstrap_learning(self, word: str, source: str = "user"):
        """
        Attempt semantic bootstrapping for a word.
        
        Returns BootstrapResult if successful.
        """
        if not getattr(self, 'semantic_bootstrapping_enabled', False):
            return None
        
        if not hasattr(self, 'bootstrap_system'):
            try:
                from semantic_bootstrapper import ALLABootstrapIntegration
                self.bootstrap_system = ALLABootstrapIntegration(self)
                self.semantic_bootstrapping_enabled = True
            except ImportError:
                print("❌ Semantic Bootstrapping module not available")
                return None
        
        return self.bootstrap_system.bootstrap_learn_word(word, source)
    
    def visualize_concept_map(self, word: str):
        """Visualize concept map for a word."""
        if hasattr(self, 'bootstrap_system'):
            return self.bootstrap_system.visualize_concept_map(word)
        return "❌ Semantic Bootstrapping not enabled"
    
    def query_concept_network(self, query: str):
        """Query the concept network."""
        if hasattr(self, 'bootstrap_system') and self.bootstrap_system:
            return self.bootstrap_system.query_concept_network(query)
        else:
            return "❌ Semantic Bootstrapping not available"
    
    def find_concept_connection(self, word1: str, word2: str):
        """Find connection between concepts."""
        if hasattr(self, 'bootstrap_system') and self.bootstrap_system:
            return self.bootstrap_system.explain_concept_relationship(word1, word2)
        else:
            return "❌ Semantic Bootstrapping not available"


# ==============================================================================
# ALLA ENGINE - MAIN INTERFACE
# ==============================================================================

class AllaEngine:
    """
    🧠 ALLA Engine v20.0 - The Semantic Cascade Mind
    
    Main interface for ALLA with integrated semantic bootstrapping.
    Language IS the operating system of intellect.
    """
    
    def __init__(self, memory_file: str = "alla_memory.json"):
        """Initialize ALLA with all cognitive systems."""
        self.memory_file = memory_file
        
        # Core cognitive components
        self.lexicon = Lexicon()
        self.world = LivingWorld()
        self.planner = Planner(self.world, self.lexicon)
        self.command_processor = CommandProcessor(self.lexicon, self.world)
        self.execution_engine = ExecutionEngine(self.world, self.lexicon, self)
        self.semantic_memory = SemanticMemory()
        
        # Goal system
        self.goals: List[Goal] = []
        self.goal_counter = 0
        self.active_plans: List[Plan] = []
        
        # Learning systems
        self.autonomous_learning_enabled = True
        self.semantic_bootstrapping_enabled = False
        
        # Load persistent memory
        self._load_memory()
        self._load_basic_vocabulary()
        
        print(f"🧠 ALLA v20.0 initialized with {self.lexicon.get_word_count()} words")
    
    def process_command(self, command: str) -> Tuple[str, Any]:
        """Process a natural language command and return feedback and result."""
        try:
            # Parse the command
            plan = self.command_processor.parse(command)
            
            if plan is None:
                return "I don't understand that command.", None
            
            # Execute the plan
            result = self.execution_engine.execute(plan)
            
            # Save memory after each command
            self._save_memory()
            
            return plan.feedback, result
            
        except Exception as e:
            return f"Error processing command: {e}", None
    
    def enable_semantic_bootstrapping(self) -> str:
        """Enable semantic bootstrapping for concept network building."""
        try:
            from semantic_bootstrapper import ALLABootstrapIntegration
            if not hasattr(self, 'bootstrap_system'):
                self.bootstrap_system = ALLABootstrapIntegration(self)
            result = self.bootstrap_system.enable_semantic_bootstrapping()
            self.semantic_bootstrapping_enabled = True
            return result
        except ImportError:
            return "❌ Semantic Bootstrapping module not available. Please ensure semantic_bootstrapper.py is present."
    
    def attempt_bootstrap_learning(self, word: str, source: str = "user"):
        """Attempt semantic bootstrapping for a word."""
        if not hasattr(self, 'bootstrap_system'):
            self.enable_semantic_bootstrapping()
        
        if hasattr(self, 'bootstrap_system'):
            return self.bootstrap_system.bootstrap_learn_word(word, source)
        return None
    
    def get_semantic_bootstrap_stats(self):
        """Get statistics about semantic bootstrapping."""
        if hasattr(self, 'bootstrap_system'):
            return self.bootstrap_system.get_bootstrap_stats()
        return {"error": "Semantic Bootstrapping not initialized"}
    
    def visualize_concept_map(self, word: str):
        """Visualize concept map for a word."""
        if hasattr(self, 'bootstrap_system'):
            return self.bootstrap_system.visualize_concept_map(word)
        return "❌ Semantic Bootstrapping not enabled"
    
    def query_concept_network(self, query: str):
        """Query the concept network."""
        if hasattr(self, 'bootstrap_system'):
            return self.bootstrap_system.query_concept_network(query)
        return "❌ Semantic Bootstrapping not enabled"
    
    def _load_memory(self):
        """Load persistent memory from JSON file."""
        try:
            if Path(self.memory_file).exists():
                with open(self.memory_file, 'r') as f:
                    memory_data = json.load(f)
                
                # Load lexicon entries
                for word_data in memory_data.get('lexicon', []):
                    try:
                        meaning_function = eval(word_data['meaning_expression'])
                        entry = WordEntry(
                            word=word_data['word'],
                            word_type=word_data['word_type'],
                            meaning_expression=word_data['meaning_expression'],
                            meaning_function=meaning_function
                        )
                        self.lexicon.add_entry(entry)
                    except Exception as e:
                        print(f"Error loading word '{word_data.get('word', 'unknown')}': {e}")
                
                print(f"📁 Loaded {len(memory_data.get('lexicon', []))} words from memory")
                
        except Exception as e:
            print(f"Error loading memory: {e}")
    
    def _save_memory(self):
        """Save current lexicon to persistent memory."""
        try:
            memory_data = {
                'lexicon': [],
                'version': '20.0',
                'timestamp': time.time()
            }
            
            # Save lexicon entries
            for word, entry in self.lexicon.get_all_entries().items():
                memory_data['lexicon'].append({
                    'word': entry.word,
                    'word_type': entry.word_type,
                    'meaning_expression': entry.meaning_expression
                })
            
            with open(self.memory_file, 'w') as f:
                json.dump(memory_data, f, indent=2)
                
        except Exception as e:
            print(f"Error saving memory: {e}")
    
    def _load_basic_vocabulary(self):
        """Load basic vocabulary if lexicon is empty."""
        if self.lexicon.get_word_count() > 0:
            return  # Already has vocabulary
        
        # Create minimal essential vocabulary
        essential_words = [
            ("inquiry", "what", "lambda: 'what inquiry'"),
            ("inquiry", "where", "lambda: 'where inquiry'"),
            ("inquiry", "when", "lambda: 'when inquiry'"),
            ("action", "create", "lambda: 'create action'"),
            ("action", "destroy", "lambda: 'destroy action'"),
            ("property", "red", "lambda obj: obj.color == 'red'"),
            ("property", "blue", "lambda obj: obj.color == 'blue'"),
            ("property", "green", "lambda obj: obj.color == 'green'"),
            ("noun", "box", "lambda obj: obj.shape == 'box'"),
            ("noun", "circle", "lambda obj: obj.shape == 'circle'"),
            ("social", "hello", "acknowledge_greeting"),
            ("social", "goodbye", "acknowledge_farewell"),
            ("social", "thanks", "acknowledge_gratitude"),
        ]
        
        for word_type, word, expression in essential_words:
            try:
                meaning_function = eval(expression)
                entry = WordEntry(
                    word=word,
                    word_type=word_type,
                    meaning_expression=expression,
                    meaning_function=meaning_function
                )
                self.lexicon.add_entry(entry)
            except Exception as e:
                print(f"Error creating essential word '{word}': {e}")
        
        print(f"🔧 Created essential vocabulary: {self.lexicon.get_word_count()} words")


# ==============================================================================
# COMPATIBILITY AND UTILITY FUNCTIONS
# ==============================================================================

def create_alla_engine(memory_file: str = "alla_memory.json"):
    """🏭 Factory function to create ALLA engine instance."""
    return AllaEngine(memory_file)

def quick_demo():
    """Quick demonstration of ALLA's capabilities."""
    print("=== ALLA v20.0 Quick Demo ===")
    
    # Initialize ALLA
    alla = AllaEngine("demo_memory.json")
    
    # Enable semantic systems
    print("\n" + alla.enable_semantic_bootstrapping())
    
    # Demonstrate semantic bootstrapping
    print("\n=== Semantic Bootstrapping Demo ===")
    result = alla.attempt_bootstrap_learning("photosynthesis")
    if result:
        print(f"Bootstrap successful: {result.total_words_learned} words learned")
    else:
        print("Bootstrap learning not available yet")
    
    # Demonstrate concept network querying
    print("\n=== Concept Network Query Demo ===")
    query_result = alla.query_concept_network("plants and sunlight")
    print(query_result)
    
    # Show system status
    print("\n=== System Status ===")
    status = alla.get_system_status()
    for key, value in status.items():
        print(f"{key}: {value}")
    
    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    quick_demo()




