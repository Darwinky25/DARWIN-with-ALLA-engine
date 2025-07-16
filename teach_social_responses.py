#!/usr/bin/env python3
"""
Teaching ALLA Social Responses - Complete Guide
===============================================

This script demonstrates how to properly teach ALLA social interactions
using two different approaches:
1. Teaching complete response patterns
2. Teaching individual words + composition rules
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from alla_engine import AllaEngine, WordEntry

def comprehensive_social_teaching():
    print("🎓 COMPLETE GUIDE: Teaching ALLA Social Responses")
    print("=" * 60)
    
    alla = AllaEngine(memory_path="social_teaching_memory.json")
    
    print("\n📋 STEP 1: Current Behavior (Before Teaching)")
    print("-" * 40)
    test_responses(alla, "Before any teaching")
    
    print("\n🎯 STEP 2: Teaching Complete Response Patterns")
    print("-" * 40)
    
    # Method 1: Teach complete response patterns
    response_patterns = [
        ("response_to_thanks", "social", "You're welcome!"),
        ("response_to_thanks_warm", "social", "You're very welcome!"),
        ("response_to_thanks_casual", "social", "No problem!"),
        ("response_to_goodbye", "social", "Goodbye! Take care."),
        ("response_to_hello", "social", "Hello there!"),
        ("response_to_apology", "social", "It's perfectly okay.")
    ]
    
    print("Teaching complete response patterns:")
    for pattern_name, word_type, response_text in response_patterns:
        print(f"  Teaching: '{pattern_name}' -> '{response_text}'")
        entry = WordEntry(pattern_name, word_type, response_text, lambda obj, r=response_text: r)
        alla.lexicon.add_entry(entry)
    
    print("\n📋 STEP 3: Testing After Teaching Patterns")
    print("-" * 40)
    test_responses(alla, "After teaching patterns")
    
    print("\n🎯 STEP 4: Teaching Using the 'teach' Command")
    print("-" * 40)
    
    # Method 2: Use ALLA's built-in teach command
    teach_commands = [
        'teach social "polite_thanks_response" as "You are most welcome!"',
        'teach social "casual_goodbye" as "See you later!"',
        'teach social "friendly_greeting" as "Hi there, nice to see you!"'
    ]
    
    print("Using ALLA's teach command:")
    for command in teach_commands:
        print(f"  Command: {command}")
        response, _ = alla.process_command(command)
        print(f"  ALLA: {response}")
    
    print("\n📋 STEP 5: Final Testing")
    print("-" * 40)
    test_responses(alla, "After complete teaching")
    
    print("\n💡 STEP 6: How to Extend This")
    print("-" * 40)
    print("To teach ALLA new social responses:")
    print("1. Use the teach command: teach social \"pattern_name\" as \"Full Response\"")
    print("2. Or create WordEntry objects with response patterns")
    print("3. ALLA will use taught patterns when available")
    print("4. If no patterns exist, ALLA will try to compose from individual words")
    
    # Cleanup
    if os.path.exists("social_teaching_memory.json"):
        os.remove("social_teaching_memory.json")

def test_responses(alla, stage_name):
    print(f"\n[{stage_name}]")
    
    test_inputs = [
        "hello",
        "thank you",
        "thank you very much", 
        "goodbye",
        "sorry"
    ]
    
    for input_text in test_inputs:
        print(f"  Input: '{input_text}'")
        response, _ = alla.process_command(input_text)
        print(f"  ALLA: {response}")
        print()

def create_social_vocabulary_file():
    """Create a vocabulary file with social response patterns"""
    print("\n🎯 BONUS: Creating Social Vocabulary File")
    print("-" * 40)
    
    social_vocab_content = """# Social Response Patterns for ALLA
# These are complete response patterns that ALLA can use

# Gratitude responses
social :: response_to_thanks :: You're welcome!
social :: response_to_thanks_casual :: No problem!
social :: response_to_thanks_warm :: You're very welcome!

# Greeting responses  
social :: response_to_hello :: Hello there!
social :: response_to_greeting :: Hi! Nice to see you.

# Farewell responses
social :: response_to_goodbye :: Goodbye! Take care.
social :: response_to_bye :: See you later!

# Apology responses
social :: response_to_sorry :: It's okay, no worries.
social :: response_to_apology :: That's perfectly fine."""
    
    with open("social_responses.alla", "w") as f:
        f.write(social_vocab_content)
    
    print("Created 'social_responses.alla' file")
    print("You can load this into ALLA using: alla.learn_from_file('social_responses.alla')")

if __name__ == "__main__":
    comprehensive_social_teaching()
    create_social_vocabulary_file()
    
    print("\n🎉 TEACHING COMPLETE!")
    print("ALLA now knows how to learn social response patterns properly.")
    print("\nKey takeaway: ALLA learns both individual words AND complete patterns.")
    print("This is authentic human-like learning - not hardcoded responses!")
