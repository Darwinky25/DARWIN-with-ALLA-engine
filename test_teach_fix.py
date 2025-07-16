#!/usr/bin/env python3
"""
Test script to verify the teach command parsing fix.
"""

from alla_engine import AllaEngine
import json

def test_teach_command_fix():
    """Test that the teach command can now handle conversational words."""
    print("=== Testing ALLA Teach Command Fix ===")
    
    # Create ALLA instance
    alla = AllaEngine(memory_path="alla_memory.json")
    
    # Load existing memory
    alla.load_lexicon()
    print(f"Loaded {alla.lexicon.get_word_count()} existing words from memory")
    
    # Test teaching a new conversational word
    test_commands = [
        'teach pronoun "your" as "lambda obj: obj"',  # Possessive pronoun
        'teach noun "name" as "lambda obj: obj.get(\'name\', \'unknown\')"',  # Identity concept
        'teach noun "alla" as "ALLAEngine"',  # Self-identity
    ]
    
    for i, command in enumerate(test_commands, 1):
        print(f"\n--- Test {i}: {command} ---")
        
        try:
            # Parse the command
            plan = alla.command_processor.parse(command)
            
            if plan:
                print(f"✓ Parsing successful: {plan.action_type}")
                print(f"  Details: {plan.details}")
                print(f"  Feedback: {plan.feedback}")
                
                # Execute the plan
                if plan.action_type == 'LEARN_NEW_WORD':
                    result = alla.execution_engine.execute(plan)
                    print(f"✓ Execution result: {result}")
                    
                    # Verify the word was learned
                    word = plan.details['word']
                    if alla.lexicon.get_entry(word):
                        print(f"✓ Word '{word}' successfully added to lexicon")
                    else:
                        print(f"✗ Word '{word}' not found in lexicon after learning")
                else:
                    print(f"✗ Unexpected action type: {plan.action_type}")
            else:
                print("✗ Parsing failed - no plan returned")
                
        except Exception as e:
            print(f"✗ Error: {e}")
    
    # Test a conversational query after learning
    print(f"\n--- Testing conversational query ---")
    try:
        # Try a query that uses the learned words
        query = "what is your name"
        print(f"Query: {query}")
        
        plan = alla.command_processor.parse(query)
        if plan:
            print(f"✓ Query parsing successful: {plan.action_type}")
            result = alla.execution_engine.execute(plan)
            print(f"Result: {result}")
        else:
            print("✗ Query parsing failed")
            
    except Exception as e:
        print(f"✗ Query error: {e}")
    
    # Show final lexicon size
    print(f"\nFinal lexicon size: {alla.lexicon.get_word_count()} words")
    
    # Save memory
    alla.save_lexicon()
    print("Memory saved to file")

if __name__ == "__main__":
    test_teach_command_fix()
