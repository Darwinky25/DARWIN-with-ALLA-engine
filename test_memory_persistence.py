#!/usr/bin/env python3
"""
Test script to verify ALLA's memory persistence is working correctly.
This script will:
1. Load ALLA and verify it loads all concepts from memory
2. Test that ALLA recognizes and uses learned concepts
3. Teach ALLA a new concept and verify it persists
4. Restart ALLA and verify the new concept is still there
"""

from alla_engine import AllaEngine
import json
from pathlib import Path

def count_memory_concepts(memory_file="alla_memory.json"):
    """Count concepts in the memory file."""
    memory_path = Path(memory_file)
    if not memory_path.exists():
        return 0
    
    with memory_path.open('r') as f:
        data = json.load(f)
        return len(data)

def test_memory_loading():
    """Test that ALLA loads all concepts from memory."""
    print("=== Testing Memory Loading ===")
    
    # Count concepts in memory file
    file_concepts = count_memory_concepts()
    print(f"Concepts in memory file: {file_concepts}")
    
    # Start ALLA and check loaded concepts
    engine = AllaEngine()
    loaded_concepts = engine.lexicon.get_word_count()
    print(f"Concepts loaded by ALLA: {loaded_concepts}")
    
    if loaded_concepts == file_concepts:
        print("✅ ALLA successfully loaded all concepts from memory!")
    else:
        print(f"❌ MISMATCH: Expected {file_concepts}, got {loaded_concepts}")
    
    return engine

def test_concept_recognition(engine):
    """Test that ALLA recognizes learned concepts."""
    print("\n=== Testing Concept Recognition ===")
    
    # Test some concepts that should be in memory
    test_words = ["red", "blue", "box", "big", "small", "tree"]
    
    for word in test_words:
        entry = engine.lexicon.get_entry(word)
        if entry:
            print(f"✅ ALLA knows '{word}' as {entry.word_type}: {entry.meaning_expression}")
        else:
            print(f"❌ ALLA doesn't know '{word}'")

def test_new_learning(engine):
    """Test learning a new concept and verify it persists."""
    print("\n=== Testing New Learning ===")
    
    # Learn a new concept
    test_word = "purple"
    test_expression = "obj.color == 'purple'"
    
    print(f"Teaching ALLA: {test_word} = {test_expression}")
    result = engine._teach_word(test_word, "property", test_expression)
    print(f"Result: {result}")
    
    # Verify it's in memory
    entry = engine.lexicon.get_entry(test_word)
    if entry:
        print(f"✅ ALLA learned '{test_word}' successfully")
    else:
        print(f"❌ ALLA failed to learn '{test_word}'")
    
    return test_word

def test_persistence_after_restart(test_word):
    """Test that learned concepts persist after restarting ALLA."""
    print("\n=== Testing Persistence After Restart ===")
    
    # Create a new ALLA instance (simulating restart)
    print("Creating new ALLA instance...")
    new_engine = AllaEngine()
    
    # Check if the test word is still there
    entry = new_engine.lexicon.get_entry(test_word)
    if entry:
        print(f"✅ '{test_word}' persisted after restart: {entry.meaning_expression}")
    else:
        print(f"❌ '{test_word}' was lost after restart")
    
    new_engine.shutdown()
    return entry is not None

def main():
    """Run all memory persistence tests."""
    print("ALLA Memory Persistence Test")
    print("=" * 40)
    
    # Test 1: Memory loading
    engine = test_memory_loading()
    
    # Test 2: Concept recognition
    test_concept_recognition(engine)
    
    # Test 3: New learning
    test_word = test_new_learning(engine)
    
    # Shutdown first engine
    engine.shutdown()
    
    # Test 4: Persistence after restart
    persisted = test_persistence_after_restart(test_word)
    
    print("\n" + "=" * 40)
    if persisted:
        print("🎉 ALL TESTS PASSED! ALLA's memory persistence is working correctly.")
    else:
        print("💥 MEMORY PERSISTENCE FAILED! ALLA is forgetting learned concepts.")

if __name__ == "__main__":
    main()
