#!/usr/bin/env python3
"""
Interactive ALLA Test Session
Direct communication with ALLA v17.0
"""

from alla_engine import AllaEngine
import sys

def interactive_alla_session():
    print("=== ALLA v17.0 Interactive Test Session ===")
    print("Type 'quit', 'exit', or 'bye' to end the session")
    print("Type 'status' to see ALLA's current vocabulary size")
    print("Type 'help' to see available commands")
    print("=" * 50)
    
    # Initialize ALLA
    print("\nInitializing ALLA...")
    alla = AllaEngine()
    print(f"ALLA is ready! Loaded {alla.lexicon.get_word_count()} words from memory.\n")
    
    # Interactive loop
    try:
        while True:
            # Get user input
            user_input = input("You: ").strip()
            
            # Handle special commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print("ALLA: Goodbye! Thank you for testing with me.")
                break
            elif user_input.lower() == 'status':
                print(f"ALLA: I currently know {alla.lexicon.get_word_count()} words.")
                continue
            elif user_input.lower() == 'help':
                print("ALLA: Available commands:")
                print("  - Social: hello, thanks, sorry, happy, sad, etc.")
                print("  - Questions: what is red, what is box, where is X")
                print("  - Actions: take box, create red box as mybox, destroy X")
                print("  - Inventory: do I have box, what do you have")
                print("  - Learning: teach property \"purple\" as \"obj.color == 'purple'\"")
                print("  - Properties: red, blue, big, small, etc.")
                print("  - Objects: box, ball, book, table, etc.")
                continue
            elif user_input == '':
                continue
            
            # Process the command with ALLA
            try:
                print("ALLA: ", end="", flush=True)
                feedback, result = alla.process_command(user_input)
                print(feedback)
                
                # Show results if any
                if result:
                    if isinstance(result, list):
                        if len(result) > 0:
                            print(f"      Found {len(result)} objects:")
                            for obj in result[:3]:  # Show first 3 objects
                                if hasattr(obj, 'name'):
                                    print(f"      - {obj.name} ({getattr(obj, 'shape', 'unknown')}, {getattr(obj, 'color', 'unknown')})")
                                else:
                                    print(f"      - {obj}")
                            if len(result) > 3:
                                print(f"      ... and {len(result) - 3} more")
                        else:
                            print("      No objects found.")
                    elif hasattr(result, 'name'):
                        print(f"      Result: {result.name}")
                    else:
                        print(f"      Result: {result}")
                        
            except Exception as e:
                print(f"ALLA: Error processing command: {e}")
                
    except KeyboardInterrupt:
        print("\n\nALLA: Session interrupted by user.")
    except Exception as e:
        print(f"\n\nError during session: {e}")
    finally:
        # Save ALLA's state
        print("\nSaving ALLA's memory...")
        alla.shutdown()
        print("Session ended. ALLA's memory has been saved.")

if __name__ == "__main__":
    interactive_alla_session()
