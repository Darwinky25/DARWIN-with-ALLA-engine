#!/usr/bin/env python3
"""
Quick memory test - check if ALLA remembers learned words
"""

from alla_engine import AllaEngine

def test_memory():
    print("Testing ALLA's memory...")
    
    # Initialize ALLA
    alla = AllaEngine()
    
    # Check for 'hi' and 'greeting'
    hi_entry = alla.lexicon.get_entry('hi')
    greeting_entry = alla.lexicon.get_entry('greeting')
    
    print(f"'hi' in memory: {hi_entry is not None}")
    if hi_entry:
        print(f"  Type: {hi_entry.word_type}")
        print(f"  Expression: {hi_entry.meaning_expression}")
    
    print(f"'greeting' in memory: {greeting_entry is not None}")
    if greeting_entry:
        print(f"  Type: {greeting_entry.word_type}")
        print(f"  Expression: {greeting_entry.meaning_expression}")
    
    # Count total words
    total_words = alla.lexicon.get_word_count()
    print(f"Total words in memory: {total_words}")
    
    alla.shutdown()

if __name__ == "__main__":
    test_memory()
