#!/usr/bin/env python3
"""
Test script to debug lexicon learning and saving issues in ALLA v17.0
"""

import sys
from pathlib import Path

# Add the current directory to the path
sys.path.append(str(Path(__file__).parent))

from alla_engine import AllaEngine
import json

def test_lexicon_operations():
    """Test basic lexicon operations to find the bug."""
    print("=== ALLA Lexicon Debug Test ===\n")
    
    # Initialize ALLA
    print("1. Initializing ALLA...")
    alla = AllaEngine()
    
    # Check initial lexicon state
    print(f"2. Initial lexicon count: {alla.lexicon.get_word_count()}")
    print(f"   Memory file exists: {alla.memory_path.exists()}")
    
    # Try to teach a basic word
    print("\n3. Teaching a basic word...")
    result = alla._teach_word("hello", "social", "acknowledge_greeting")
    print(f"   Result: {result}")
    
    # Check lexicon after teaching
    print(f"4. Lexicon count after teaching: {alla.lexicon.get_word_count()}")
    
    # List all entries
    print("\n5. All lexicon entries:")
    all_entries = alla.lexicon.get_all_entries()
    for word, entry in all_entries.items():
        print(f"   {word}: {entry.word_type} -> {entry.meaning_expression}")
    
    # Check memory file content
    print(f"\n6. Memory file content:")
    if alla.memory_path.exists():
        try:
            with alla.memory_path.open('r') as f:
                content = json.load(f)
                print(f"   {content}")
        except Exception as e:
            print(f"   Error reading memory file: {e}")
    else:
        print("   Memory file does not exist")
    
    # Try manual save
    print("\n7. Manually triggering save...")
    alla.save_lexicon()
    
    # Check memory file again
    print(f"\n8. Memory file content after manual save:")
    if alla.memory_path.exists():
        try:
            with alla.memory_path.open('r') as f:
                content = json.load(f)
                print(f"   {content}")
        except Exception as e:
            print(f"   Error reading memory file: {e}")
    
    # Test teaching multiple words
    print("\n9. Teaching more words...")
    words_to_teach = [
        ("goodbye", "social", "acknowledge_farewell"),
        ("red", "property", "color:red"),
        ("box", "object", "container")
    ]
    
    for word, word_type, expression in words_to_teach:
        result = alla._teach_word(word, word_type, expression)
        print(f"   Teaching '{word}': {result}")
    
    print(f"\n10. Final lexicon count: {alla.lexicon.get_word_count()}")
    
    # Final memory check
    print(f"\n11. Final memory file content:")
    if alla.memory_path.exists():
        try:
            with alla.memory_path.open('r') as f:
                content = json.load(f)
                print(f"    {content}")
        except Exception as e:
            print(f"    Error reading memory file: {e}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_lexicon_operations()
