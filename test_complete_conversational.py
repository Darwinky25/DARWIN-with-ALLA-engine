#!/usr/bin/env python3
"""
Complete test to verify both parsing and execution of conversational queries.
"""

from alla_engine import AllaEngine

def test_complete_conversational_flow():
    """Test the complete flow: parsing + execution of conversational queries."""
    print("=== Complete Conversational Flow Test ===")
    
    # Create ALLA instance
    alla = AllaEngine(memory_path="alla_memory.json")
    alla.load_lexicon()
    
    print(f"Current lexicon size: {alla.lexicon.get_word_count()} words")
    
    # Test the complete conversational flow
    test_queries = [
        "what is your name",
        "who are you",  # This should fail gracefully
        "hello",        # This should work as social greeting
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Test {i}: '{query}' ---")
        
        try:
            # Parse the query
            plan = alla.command_processor.parse(query)
            if plan:
                print(f"✓ Parse successful:")
                print(f"  Action: {plan.action_type}")
                print(f"  Details: {plan.details}")
                print(f"  Feedback: {plan.feedback}")
                
                # Execute the plan
                result = alla.execution_engine.execute(plan)
                print(f"✓ Execution result: {result}")
            else:
                print("✗ Parse returned None")
                
        except Exception as e:
            print(f"✗ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_complete_conversational_flow()
