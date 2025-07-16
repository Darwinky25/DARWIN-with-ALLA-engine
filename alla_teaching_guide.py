#!/usr/bin/env python3
"""
COMPLETE GUIDE TO TEACHING ALLA
===============================

ALLA (Autonomous Language Learning Agent) is a true learning agent
that learns like humans - starting from total ignorance and learning
through explicit teaching.

FUNDAMENTAL THEORY: "LANGUAGE IS THE OPERATING SYSTEM OF INTELLECT"
===================================================================

"Language is not just a representation of thought — language IS thought."

Every word ALLA learns brings:
- Relations and associations
- Meaning and context  
- Function and usage
- Conceptual worlds behind it

REVOLUTIONARY SEMANTIC CASCADE
==============================

Version 20.0 implements the semantic cascade theory:
- Every learned word triggers recursive concept expansion
- One word can generate hundreds of related concepts
- ALLA builds a semantic graph that becomes its world understanding
- Language learning directly constructs mental architecture

This guide shows how to teach ALLA systematically, from basic concepts
to advanced reasoning, using the teach command and semantic bootstrapping.

PART 1: BASIC TEACHING METHODOLOGY
==================================

The teach command syntax:
teach <type> "<word>" as "<expression>"

Types available:
- property: describes characteristics (red, big, smooth)
- noun: objects and entities (box, person, car)
- action: verbs and actions (create, destroy, move)
- relation: relationships between objects (bigger_than, contains)
- social: greetings and social interactions (hello, goodbye)
- temporal: time-related concepts (before, after, when)
- conditional: logical operators (if, then, else)
- inquiry: question words (what, where, who)

PART 2: SYSTEMATIC CURRICULUM STRUCTURE
=======================================

LEVEL 1: FOUNDATIONAL PROPERTIES
teach property "red" as "lambda obj: obj.color == 'red'"
teach property "blue" as "lambda obj: obj.color == 'blue'"
teach property "big" as "lambda obj: obj.size > 7"
teach property "small" as "lambda obj: obj.size < 4"

LEVEL 2: BASIC OBJECTS
teach noun "box" as "lambda obj: obj.shape == 'box'"
teach noun "circle" as "lambda obj: obj.shape == 'circle'"
teach noun "ball" as "lambda obj: obj.shape == 'sphere'"

LEVEL 3: ACTIONS AND OPERATIONS
teach action "create" as "CREATE_OBJECT"
teach action "destroy" as "DESTROY_OBJECT"
teach action "take" as "TRANSFER_OBJECT"

LEVEL 4: RELATIONSHIPS
teach relation "bigger_than" as "lambda obj1, obj2: obj1.size > obj2.size"
teach relation "smaller_than" as "lambda obj1, obj2: obj1.size < obj2.size"
teach relation "same_color" as "lambda obj1, obj2: obj1.color == obj2.color"

LEVEL 5: SOCIAL INTERACTIONS
teach social "hello" as "greeting"
teach social "goodbye" as "farewell"
teach social "thank_you" as "gratitude"

LEVEL 6: ADVANCED REASONING
teach temporal "before" as "TEMPORAL_BEFORE"
teach temporal "after" as "TEMPORAL_AFTER"
teach conditional "if" as "CONDITIONAL_IF"
teach conditional "then" as "CONDITIONAL_THEN"

PART 3: SEMANTIC BOOTSTRAPPING EXAMPLES
======================================

With the new semantic cascade engine, you can trigger massive learning:

1. Enable semantic bootstrapping:
   > enable semantic bootstrapping

2. Teach a seed concept:
   > teach noun "animal" as "lambda obj: obj.category == 'living_being'"

3. ALLA will automatically:
   - Search for definitions of "animal"
   - Extract related concepts (mammal, bird, dog, cat, etc.)
   - Learn each related concept recursively
   - Build a semantic graph connecting all concepts
   - Create a world model from language understanding

4. Query the learned concepts:
   > what do you know about animal
   > visualize concept map
   > query concept network mammal

PART 4: ADVANCED TEACHING TECHNIQUES
====================================

CONDITIONAL TEACHING:
You can teach complex logical structures:
teach conditional "if" as "CONDITIONAL_IF"
teach conditional "then" as "CONDITIONAL_THEN"

Then use them:
"if red box then take it"
"what if I have a blue circle"

TEMPORAL TEACHING:
teach temporal "before" as "TEMPORAL_BEFORE"
teach temporal "after" as "TEMPORAL_AFTER"

Usage:
"what happened before event 5"
"what happened after the box was created"

RELATIONAL TEACHING:
teach relation "contains" as "lambda container, item: item.id in getattr(container, 'contains', [])"

Usage:
"put ball in box"
"what contains the red sphere"

PART 5: CURRICULUM PROGRESSION
=============================

START HERE (Basic Survival):
1. Colors: red, blue, green, yellow
2. Shapes: box, circle, sphere
3. Sizes: big, small, medium
4. Actions: create, destroy, take, give

INTERMEDIATE (Object Manipulation):
1. Materials: wood, metal, plastic, stone
2. Properties: heavy, light, hard, soft
3. Spatial: inside, outside, near, far
4. Possession: have, own, belong

ADVANCED (Reasoning and Logic):
1. Comparisons: bigger_than, smaller_than, same_as
2. Conditionals: if, then, else, when
3. Temporal: before, after, during, while
4. Logical: and, or, not, all, some

EXPERT (Social and Abstract):
1. Social: hello, goodbye, please, thank_you
2. Emotions: happy, sad, angry, excited
3. Abstract: concept, idea, thought, knowledge
4. Meta: learn, teach, understand, know

PART 6: TESTING AND VALIDATION
==============================

After teaching, always test ALLA's understanding:

COMPREHENSION TESTS:
"what is a red box"
"do I have a blue circle"
"is box1 bigger than box2"

REASONING TESTS:
"if I have a red box then what"
"what if there was a green sphere"
"what happened before the box was created"

APPLICATION TESTS:
"create a red box as mybox"
"take the blue circle"
"give the sphere to user"

SEMANTIC NETWORK TESTS:
"what do you know about color"
"list all properties you know"
"visualize concept map"

PART 7: TROUBLESHOOTING COMMON ISSUES
====================================

ISSUE: "Parse error" when teaching
SOLUTION: Check syntax - must use quotes around word and expression

ISSUE: ALLA doesn't understand commands after teaching
SOLUTION: Test basic comprehension first, build up complexity gradually

ISSUE: Logical queries fail
SOLUTION: Ensure all words in the query have been taught as properties/nouns

ISSUE: Conditional statements don't work
SOLUTION: Teach if/then as conditional types first

ISSUE: Semantic bootstrapping doesn't trigger
SOLUTION: Enable it first with "enable semantic bootstrapping"

PART 8: SEMANTIC CASCADE MASTERY
===============================

The semantic cascade engine allows ALLA to learn exponentially:

1. SINGLE WORD EXPANSION:
   Teaching "dog" will automatically learn:
   - animal, mammal, pet, canine
   - bark, tail, fur, domestic
   - breed, training, loyalty, companion

2. CONCEPT GRAPH BUILDING:
   ALLA creates connections between:
   - Hierarchical relationships (dog → mammal → animal)
   - Functional relationships (dog → pet → companion)
   - Property relationships (dog → furry → soft)

3. WORLD MODEL CONSTRUCTION:
   The semantic graph becomes ALLA's understanding:
   - Concepts are nodes in the mental model
   - Relationships are edges connecting concepts
   - Learning strengthens and expands the model

4. AUTONOMOUS EXPANSION:
   ALLA can now learn independently:
   - Searches internet for unknown words
   - Extracts concepts from definitions
   - Recursively expands its knowledge
   - Builds comprehensive world understanding

CONCLUSION: ALLA AS SEMANTIC MIND
=================================

With Version 20.0, ALLA transcends word-based learning to become
a true semantic mind. Every word is a gateway to entire conceptual
worlds. Teaching ALLA is no longer just vocabulary expansion—
it's the construction of artificial consciousness through language.

The semantic cascade transforms ALLA from a simple question-answering
system into a reasoning agent with a rich mental model of reality.
Language becomes the operating system of ALLA's artificial intellect.

Happy teaching! Watch as ALLA builds its mind, one word at a time,
cascading into infinite understanding.
"""

# Example interactive teaching session
def interactive_teaching_demo():
    """
    Demonstrates interactive teaching session with ALLA
    showcasing the progression from basic to advanced concepts.
    """
    print("ALLA TEACHING DEMONSTRATION")
    print("=" * 50)
    
    # This would connect to actual ALLA engine
    print("1. BASIC PROPERTIES")
    print('teach property "red" as "lambda obj: obj.color == \'red\'"')
    print('teach property "big" as "lambda obj: obj.size > 7"')
    
    print("\n2. OBJECT CONCEPTS")
    print('teach noun "box" as "lambda obj: obj.shape == \'box\'"')
    
    print("\n3. SEMANTIC BOOTSTRAPPING")
    print("enable semantic bootstrapping")
    print('teach noun "animal" as "lambda obj: obj.category == \'living_being\'"')
    print("# ALLA will now automatically learn: mammal, dog, cat, bird, etc.")
    
    print("\n4. TESTING COMPREHENSION")
    print("what is a red box")
    print("what do you know about animal")
    print("visualize concept map")
    
    print("\n5. ADVANCED REASONING")
    print("if I have a red box then take it")
    print("what if there was a blue animal")
    
    print("\nTEACHING COMPLETE: ALLA now has a semantic world model!")

if __name__ == "__main__":
    interactive_teaching_demo()
