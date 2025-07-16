#!/usr/bin/env python3
"""
Debug memory loading issue
"""

from alla_engine import AllaEngine
import json

def debug_memory_loading():
    print("=== DEBUGGING MEMORY LOADING ===")
    
    # Check file directly
    with open("alla_memory.json", "r") as f:
        file_data = json.load(f)
    
    print(f"File contains {len(file_data)} words total")
    
    social_in_file = [word for word, info in file_data.items() if info.get('word_type') == 'social']
    print(f"Social words in file: {len(social_in_file)}")
    for word in social_in_file[:5]:  # Show first 5
        print(f"  - {word}: {file_data[word]['meaning_expression']}")
    
    # Initialize ALLA and check what gets loaded
    print("\nInitializing ALLA...")
    alla = AllaEngine()
    
    print(f"ALLA lexicon contains {alla.lexicon.get_word_count()} words")
    
    # Check specific social words
    test_words = ['hi', 'hello', 'thanks', 'happy']
    print(f"\nChecking specific words in lexicon:")
    for word in test_words:
        entry = alla.lexicon.get_entry(word)
        if entry:
            print(f"  ✓ {word}: {entry.word_type} - {entry.meaning_expression}")
        else:
            print(f"  ✗ {word}: NOT FOUND")
    
    alla.shutdown()

if __name__ == "__main__":
    debug_memory_loading()
