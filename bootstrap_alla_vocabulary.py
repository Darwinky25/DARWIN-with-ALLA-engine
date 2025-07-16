#!/usr/bin/env python3
"""
Bootstrap ALLA with a comprehensive basic vocabulary including grammar-aware entries.
This script will teach ALLA essential words needed for natural language interaction.
"""

import sys
from pathlib import Path

# Add the current directory to the path
sys.path.append(str(Path(__file__).parent))

from alla_engine import AllaEngine
from grammar_engine import GrammarEngine

def bootstrap_alla_vocabulary():
    """Bootstrap ALLA with essential vocabulary for natural language interaction."""
    print("=== ALLA Vocabulary Bootstrap ===\n")
    
    # Initialize ALLA and grammar engine
    print("1. Initializing ALLA...")
    alla = AllaEngine()
    grammar = GrammarEngine()
    
    print(f"2. Current lexicon size: {alla.lexicon.get_word_count()} words")
    
    # Define comprehensive basic vocabulary with grammar integration
    basic_vocabulary = [
        # Social/Greeting words
        ("hi", "social", "acknowledge_greeting"),
        ("hello", "social", "acknowledge_greeting"),
        ("hey", "social", "acknowledge_greeting"),
        ("goodbye", "social", "acknowledge_farewell"),
        ("bye", "social", "acknowledge_farewell"),
        ("thanks", "social", "acknowledge_gratitude"),
        ("thank", "social", "acknowledge_gratitude"),
        ("please", "social", "request_politeness"),
        ("sorry", "social", "acknowledge_apology"),
        ("help", "social", "request_assistance"),
        ("yes", "social", "affirmative_response"),
        ("no", "social", "negative_response"),
        ("okay", "social", "acknowledge_agreement"),
        ("ok", "social", "acknowledge_agreement"),
        
        # Emotional states
        ("happy", "social", "emotional_state_happy"),
        ("sad", "social", "emotional_state_sad"),
        ("angry", "social", "emotional_state_angry"),
        ("excited", "social", "emotional_state_excited"),
        ("tired", "social", "physical_state_tired"),
        ("hungry", "social", "physical_state_hungry"),
        
        # Basic actions (verbs)
        ("go", "action", "move_to_location"),
        ("move", "action", "change_position"),
        ("take", "action", "pickup_object"),
        ("get", "action", "pickup_object"),
        ("give", "action", "transfer_object"),
        ("put", "action", "place_object"),
        ("place", "action", "place_object"),
        ("find", "action", "locate_object"),
        ("look", "action", "observe_environment"),
        ("see", "action", "perceive_visual"),
        ("make", "action", "create_object"),
        ("create", "action", "create_object"),
        ("destroy", "action", "destroy_object"),
        ("delete", "action", "destroy_object"),
        ("stop", "action", "halt_execution"),
        ("wait", "action", "pause_execution"),
        
        # Properties/Adjectives (using valid lambda expressions)
        ("red", "property", "obj.color == 'red'"),
        ("blue", "property", "obj.color == 'blue'"),
        ("green", "property", "obj.color == 'green'"),
        ("yellow", "property", "obj.color == 'yellow'"),
        ("big", "property", "obj.size > 7"),
        ("small", "property", "obj.size < 4"),
        ("large", "property", "obj.size > 7"),
        ("tiny", "property", "obj.size < 2"),
        ("hot", "property", "hasattr(obj, 'temperature') and obj.temperature > 80"),
        ("cold", "property", "hasattr(obj, 'temperature') and obj.temperature < 20"),
        ("new", "property", "hasattr(obj, 'age') and obj.age < 1"),
        ("old", "property", "hasattr(obj, 'age') and obj.age > 10"),
        
        # Basic objects/nouns (using object shape/type checking)
        ("box", "noun", "obj.shape == 'box'"),
        ("ball", "noun", "obj.shape == 'sphere' or obj.shape == 'ball'"),
        ("book", "noun", "obj.shape == 'rectangular' and hasattr(obj, 'readable')"),
        ("table", "noun", "obj.shape == 'flat' and obj.size > 5"),
        ("chair", "noun", "obj.shape == 'chair'"),
        ("door", "noun", "obj.shape == 'barrier' and hasattr(obj, 'openable')"),
        ("window", "noun", "obj.material == 'glass'"),
        ("wall", "noun", "obj.shape == 'vertical_barrier'"),
        ("floor", "noun", "obj.shape == 'horizontal_surface'"),
        ("room", "noun", "obj.shape == 'enclosed_space'"),
        
        # Spatial/Location relations
        ("in", "relation", "obj1.position == obj2.position"),
        ("on", "relation", "obj1.position[2] > obj2.position[2]"),  # Assuming z-axis for height
        ("under", "relation", "obj1.position[2] < obj2.position[2]"),
        ("near", "relation", "abs(obj1.position[0] - obj2.position[0]) < 2 and abs(obj1.position[1] - obj2.position[1]) < 2"),
        ("far", "relation", "abs(obj1.position[0] - obj2.position[0]) > 5 or abs(obj1.position[1] - obj2.position[1]) > 5"),
        ("bigger_than", "relation", "obj1.size > obj2.size"),
        ("smaller_than", "relation", "obj1.size < obj2.size"),
        
        # Question words (inquiry type)
        ("what", "inquiry", "query_identity"),
        ("where", "inquiry", "query_location"),
        ("when", "inquiry", "query_time"),
        ("why", "inquiry", "query_reason"),
        ("how", "inquiry", "query_method"),
        ("who", "inquiry", "query_person"),
        
        # Pronouns
        ("i", "pronoun", "first_person_singular"),
        ("you", "pronoun", "second_person"),
        ("it", "pronoun", "third_person_object"),
        ("this", "pronoun", "demonstrative_near"),
        ("that", "pronoun", "demonstrative_far"),
        ("me", "pronoun", "first_person_object"),
        ("my", "pronoun", "first_person_possessive"),
        ("your", "pronoun", "second_person_possessive"),
        
        # Basic operators (logical connectors)
        ("and", "operator", "logical_and"),
        ("or", "operator", "logical_or"),
        ("not", "operator", "logical_not"),
        ("if", "conditional", "conditional_if"),
        ("then", "conditional", "conditional_then"),
        ("else", "conditional", "conditional_else"),
        
        # Temporal words
        ("when", "temporal", "temporal_when"),
        ("before", "temporal", "temporal_before"),
        ("after", "temporal", "temporal_after"),
        ("now", "temporal", "temporal_present"),
        ("then", "temporal", "temporal_past"),
        
        # Additional useful properties
        ("same", "relation", "obj1.name == obj2.name"),
        ("different", "relation", "obj1.name != obj2.name"),
    ]
    
    print(f"\n3. Teaching {len(basic_vocabulary)} essential words...")
    success_count = 0
    failed_words = []
    
    for i, (word, word_type, expression) in enumerate(basic_vocabulary, 1):
        try:
            # Check if word already exists
            existing_entry = alla.lexicon.get_entry(word)
            if existing_entry:
                print(f"   [{i:3d}] Skipping '{word}' (already known)")
                success_count += 1
                continue
            
            # Teach the word
            result = alla._teach_word(word, word_type, expression)
            if "Successfully learned" in result:
                print(f"   [{i:3d}] ✓ {word} ({word_type})")
                success_count += 1
            else:
                print(f"   [{i:3d}] ✗ {word} - {result}")
                failed_words.append((word, result))
        except Exception as e:
            print(f"   [{i:3d}] ✗ {word} - Exception: {e}")
            failed_words.append((word, str(e)))
    
    print(f"\n4. Vocabulary bootstrap complete!")
    print(f"   Successfully taught: {success_count} words")
    print(f"   Failed: {len(failed_words)} words")
    print(f"   Final lexicon size: {alla.lexicon.get_word_count()} words")
    
    if failed_words:
        print(f"\n5. Failed words:")
        for word, error in failed_words:
            print(f"   - {word}: {error}")
    
    # Test grammar-aware parsing for a few key words
    print(f"\n6. Testing grammar integration...")
    test_words = ["hello", "red", "go", "box", "what", "the"]
    for word in test_words:
        if word in [w[0] for w in basic_vocabulary]:
            # Get grammar classification
            grammar_info = grammar.classify_word(word)
            lexicon_entry = alla.lexicon.get_entry(word)
            if lexicon_entry:
                print(f"   {word}: {lexicon_entry.word_type} | Grammar: {grammar_info}")
    
    print(f"\n7. Testing basic interaction...")
    test_commands = ["hello", "what", "go", "red box"]
    for cmd in test_commands:
        try:
            feedback, result = alla.process_command(cmd)
            print(f"   '{cmd}' -> {feedback}")
        except Exception as e:
            print(f"   '{cmd}' -> Error: {e}")
    
    # Clean shutdown to save all learned words
    print(f"\n8. Saving vocabulary...")
    alla.shutdown()
    
    print(f"\n=== Bootstrap Complete ===")
    print(f"ALLA now has {success_count} words in its vocabulary!")

if __name__ == "__main__":
    bootstrap_alla_vocabulary()
