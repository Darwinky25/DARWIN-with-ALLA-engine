#!/usr/bin/env python3
"""
Simple test to debug the "what is your name" query parsing issue.
"""

from alla_engine import AllaEngine

def test_conversational_query():
    """Test conversational queries after learning words."""
    print("=== Testing Conversational Query Parsing ===")
    
    # Create ALLA instance
    alla = AllaEngine(memory_path="alla_memory.json")
    alla.load_lexicon()
    
    print(f"Current lexicon size: {alla.lexicon.get_word_count()} words")
    
    # Check if words exist
    words_to_check = ["what", "is", "your", "name"]
    for word in words_to_check:
        entry = alla.lexicon.get_entry(word)
        if entry:
            print(f"✓ Word '{word}' found: {entry.word_type} - {entry.meaning_expression}")
        else:
            print(f"✗ Word '{word}' NOT found in lexicon")
    
    # Try to parse the query
    print(f"\n--- Parsing Query: 'what is your name' ---")
    try:
        plan = alla.command_processor.parse("what is your name")
        if plan:
            print(f"✓ Parse successful:")
            print(f"  Action: {plan.action_type}")
            print(f"  Details: {plan.details}")
            print(f"  Feedback: {plan.feedback}")
        else:
            print("✗ Parse returned None")
    except Exception as e:
        print(f"✗ Parse error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n=== Done ===")

if __name__ == "__main__":
    test_conversational_query()
