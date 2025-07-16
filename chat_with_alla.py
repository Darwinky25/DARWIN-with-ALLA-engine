#!/usr/bin/env python3
"""
ALLA v17.0 - Simple Chat Interface
=================================

Simple, clean chat interface with ALLA for natural conversation.
"""

from alla_engine import AllaEngine

def chat_with_alla():
    """Simple chat interface with ALLA."""
    print("ALLA v17.0 - Ready to Chat!")
    print("=" * 40)
    print("Talk to me naturally. I'll ask if I don't understand something.")
    print("Examples: 'take the flibbertigibbet', 'what is red', 'create blue box'")
    print("Type 'exit' when you're done.\n")
    
    try:
        engine = AllaEngine()
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("ALLA: Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                # Process through ALLA's natural command processor
                feedback, result = engine.process_command(user_input)
                
                # Simple response formatting
                response = feedback
                if result is not None:
                    if isinstance(result, list) and result:
                        response += f" Found {len(result)} items."
                    elif isinstance(result, bool):
                        response += f" Answer: {'Yes' if result else 'No'}"
                    elif isinstance(result, str) and result:
                        response += f" Result: {result}"
                
                print(f"ALLA: {response}")
                
                # Let ALLA think if needed
                if engine.active_goals:
                    print("[ALLA thinking...]")
                    engine.tick()
                
            except KeyboardInterrupt:
                print("\nALLA: Chat ended.")
                break
            except Exception as e:
                print(f"Error: {e}")
                print("ALLA: Sorry, could you try again?")
        
        engine.shutdown()
        
    except Exception as e:
        print(f"Failed to start ALLA: {e}")
        print("Please ensure alla_engine.py and world.py are available.")

if __name__ == "__main__":
    chat_with_alla()
