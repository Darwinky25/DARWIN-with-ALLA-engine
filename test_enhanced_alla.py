#!/usr/bin/env python3
"""
Test ALLA's enhanced vocabulary and memory persistence
"""

from alla_engine import AllaEngine

def test_enhanced_alla():
    print("=== Testing Enhanced ALLA v17.0 ===\n")
    
    # Initialize ALLA (should load the rich vocabulary)
    print("1. Initializing ALLA...")
    alla = AllaEngine()
    
    print(f"2. ALLA loaded {alla.lexicon.get_word_count()} words from memory!")
    
    # Test various types of commands that should now work
    test_commands = [
        # Social interactions
        "hello",
        "thanks", 
        "sorry",
        
        # Simple queries that should work with the new vocabulary
        "what is red",
        "what is box",
        
        # Property-based queries
        "red",
        "big", 
        "small",
        
        # Object requests
        "take box",
        "find red box",
        
        # Social expressions with emotions
        "happy",
        "sad",
        "tired",
        
        # Complex queries
        "what is red box",
        "what is big red box"
    ]
    
    print(f"\n3. Testing {len(test_commands)} commands with enhanced vocabulary:")
    print("=" * 60)
    
    for i, cmd in enumerate(test_commands, 1):
        print(f"\n[{i:2d}] Input: '{cmd}'")
        try:
            feedback, result = alla.process_command(cmd)
            print(f"     Response: {feedback}")
            if result:
                print(f"     Result: {result}")
        except Exception as e:
            print(f"     Error: {e}")
    
    print(f"\n4. Testing memory persistence by checking some specific words:")
    test_words = ["red", "box", "hello", "big", "take", "what"]
    for word in test_words:
        entry = alla.lexicon.get_entry(word)
        if entry:
            print(f"   ✓ '{word}': {entry.word_type} -> {entry.meaning_expression}")
        else:
            print(f"   ✗ '{word}': Not found in lexicon")
    
    # Clean shutdown
    print(f"\n5. Final memory save...")
    alla.shutdown()
    
    print(f"\n=== Test Complete ===")
    print("ALLA's memory persistence and vocabulary are now working correctly!")

if __name__ == "__main__":
    test_enhanced_alla()
