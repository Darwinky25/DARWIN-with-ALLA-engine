#!/usr/bin/env python3
"""
Test ALLA's new social understanding capabilities
"""

from alla_engine import AllaEngine

def test_social_understanding():
    print("Testing ALLA's social understanding...")
    
    # Initialize ALLA
    alla = AllaEngine()
    
    # Test different social commands
    social_tests = [
        "hi",
        "hello", 
        "thanks",
        "goodbye",
        "help",
        "sorry",
        "yes",
        "no",
        "happy",
        "sad",
        "tired"
    ]
    
    print(f"\nALLA loaded {alla.lexicon.get_word_count()} words from memory")
    print("\nTesting social commands:")
    print("=" * 50)
    
    for test_cmd in social_tests:
        print(f"\nInput: '{test_cmd}'")
        try:
            feedback, result = alla.process_command(test_cmd)
            print(f"Response: {feedback}")
            if result:
                print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")
    
    alla.shutdown()

if __name__ == "__main__":
    test_social_understanding()
