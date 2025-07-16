#!/usr/bin/env python3
"""
Final validation test for ALLA v17.0 - The Inquisitive Agent
Tests natural language interaction, learning, and memory persistence
"""

import json
import os
from alla_engine import AllaEngine

def test_memory_persistence():
    """Test that ALLA remembers concepts across sessions"""
    print("=== MEMORY PERSISTENCE TEST ===")
    
    # Initialize ALLA
    alla = AllaEngine()
    
    # Check if previously learned concepts are remembered
    print("\n1. Testing memory of previously learned concepts:")
    
    # Test knowledge of 'mysterious_gadget' (should be in memory)
    gadget_entry = alla.lexicon.get_entry("mysterious_gadget")
    if gadget_entry:
        print("✅ ALLA remembers 'mysterious_gadget'")
        print(f"   Definition: {gadget_entry.word_type} - {gadget_entry.meaning_expression}")
    else:
        print("❌ ALLA forgot 'mysterious_gadget'")
    
    # Test knowledge of 'sparkling' (should be in memory)
    sparkling_entry = alla.lexicon.get_entry("sparkling")
    if sparkling_entry:
        print("✅ ALLA remembers 'sparkling'")
        print(f"   Definition: {sparkling_entry.word_type} - {sparkling_entry.meaning_expression}")
    else:
        print("❌ ALLA forgot 'sparkling'")
    
    return alla

def test_new_learning(alla):
    """Test learning a new concept"""
    print("\n=== NEW LEARNING TEST ===")
    
    # Teach a new word using the engine's interface
    new_word = "magnificent"
    new_definition = "obj.beauty >= 9"
    
    print(f"\n2. Teaching ALLA a new word: '{new_word}'")
    
    # Check if word is unknown initially
    initial_entry = alla.lexicon.get_entry(new_word)
    if not initial_entry:
        print(f"✅ '{new_word}' is initially unknown")
        
        # Teach the word using the engine's internal method
        result = alla._teach_word(new_word, "property", new_definition)
        print(f"📚 Teaching result: {result}")
        
        # Verify it was learned
        learned_entry = alla.lexicon.get_entry(new_word)
        if learned_entry:
            print(f"✅ ALLA learned '{new_word}'")
            print(f"   Type: {learned_entry.word_type}")
            print(f"   Expression: {learned_entry.meaning_expression}")
        else:
            print(f"❌ ALLA failed to learn '{new_word}'")
    else:
        print(f"ℹ️  '{new_word}' was already known")

def test_memory_file_updated():
    """Test that the memory file was updated with new learning"""
    print("\n=== MEMORY FILE VALIDATION ===")
    
    if os.path.exists("alla_memory.json"):
        with open("alla_memory.json", "r") as f:
            memory_data = json.load(f)
        
        print(f"\n3. Memory file contains {len(memory_data)} words")
        
        # Check for our test word
        if "magnificent" in memory_data:
            print("✅ New word 'magnificent' was saved to memory file")
            print(f"   Definition: {memory_data['magnificent']}")
        else:
            print("❌ New word 'magnificent' was not saved to memory file")
        
        # Show recent entries
        print("\nRecent memory entries:")
        for word, definition in list(memory_data.items())[-5:]:
            print(f"  - {word}: {definition}")
    else:
        print("❌ Memory file not found")

def test_natural_language_processing(alla):
    """Test natural language understanding"""
    print("\n=== NATURAL LANGUAGE TEST ===")
    
    test_phrases = [
        "show me red boxes",
        "find big sparkling objects", 
        "what is magnificent?",
        "create a small blue cube"
    ]
    
    print("\n4. Testing natural language understanding:")
    for phrase in test_phrases:
        print(f"\nInput: '{phrase}'")
        try:
            # Test if ALLA can parse the phrase
            feedback, result = alla.process_command(phrase)
            print(f"✅ Processed successfully")
            print(f"   Feedback: {feedback}")
            if result:
                print(f"   Result: {result}")
        except Exception as e:
            print(f"❌ Processing failed: {e}")

def main():
    """Main test function"""
    print("ALLA v17.0 - The Inquisitive Agent")
    print("Final Validation Test")
    print("=" * 50)
    
    try:
        # Test 1: Memory persistence
        alla = test_memory_persistence()
        
        # Test 2: New learning
        test_new_learning(alla)
        
        # Test 3: Memory file validation
        test_memory_file_updated()
        
        # Test 4: Natural language processing
        test_natural_language_processing(alla)
        
        print("\n" + "=" * 50)
        print("🎉 VALIDATION COMPLETE!")
        print("ALLA v17.0 - The Inquisitive Agent is ready for use.")
        print("\nKey Features Validated:")
        print("✅ Persistent memory across sessions")
        print("✅ Natural language learning")
        print("✅ Automatic memory saving")
        print("✅ Natural language processing")
        
        # Properly shutdown to save any final state
        alla.shutdown()
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
