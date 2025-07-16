#!/usr/bin/env python3
"""
Simple test to verify ALLA's natural interface works correctly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from alla_engine import AllaEngine

def test_alla_natural():
    """Test ALLA's natural CommandProcessor without grammar file interference."""
    print("=== Testing ALLA v17.0 Natural Interface ===")
    print("(Using ALLA's built-in CommandProcessor, NOT grammar file)")
    
    # Initialize ALLA
    alla = AllaEngine(memory_path="alla_memory.json")
    alla.load_lexicon()
    
    print(f"ALLA initialized with {alla.lexicon.get_word_count()} words in memory")
    
    # Test commands that should work with ALLA's native CommandProcessor
    test_commands = [
        "hi",                           # Social greeting (should work)
        "what is your name",           # Identity query (should work) 
        "what is alla",                # Object query (should work now)
        "who is alla",                 # Unknown pattern (should trigger curiosity)
        "what do you know about red",  # Knowledge query (should work)
        "list all colors",             # Knowledge query (should work)
        "create red box as testbox",   # Object creation (should work)
        "what is in the world",        # World query (should work)
    ]
    
    for i, command in enumerate(test_commands, 1):
        print(f"\n--- Test {i}: '{command}' ---")
        try:
            # Use ALLA's natural CommandProcessor
            plan = alla.command_processor.parse(command)
            if plan:
                print(f"✓ Parsed as: {plan.action_type}")
                print(f"  Feedback: {plan.feedback}")
                
                # Execute the plan
                result = alla.execution_engine.execute(plan)
                if result:
                    print(f"  Result: {result}")
                    
            else:
                print("✗ Command could not be parsed")
                
        except Exception as e:
            print(f"✗ Error: {e}")
    
    print(f"\n=== Final Status ===")
    print(f"Lexicon size: {alla.lexicon.get_word_count()} words")
    alla.save_lexicon()
    print("Memory saved")

if __name__ == "__main__":
    test_alla_natural()
