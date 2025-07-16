#!/usr/bin/env python3
"""
Interactive Human-Like Learning Demonstration

This script provides an interactive terminal session to demonstrate
ALLA's genuine human-like learning behavior in real-time.
"""

import json
import os
from alla_engine import AllaEngine

def clear_specific_concepts():
    """Clear specific learned concepts for demonstration"""
    memory_file = "alla_memory.json"
    if os.path.exists(memory_file):
        try:
            with open(memory_file, 'r') as f:
                memory = json.load(f)
            
            # Remove specific concepts we want to demonstrate learning
            concepts_to_clear = ['friendship', 'howdy', 'favorite', 'dream', 'happy', 'sad']
            for concept in concepts_to_clear:
                if concept in memory:
                    del memory[concept]
            
            with open(memory_file, 'w') as f:
                json.dump(memory, f, indent=2)
            print(f"✓ Cleared demonstration concepts: {concepts_to_clear}")
        except Exception as e:
            print(f"Note: {e}")

def interactive_demo():
    """Run interactive demonstration of ALLA's learning"""
    print("="*70)
    print("INTERACTIVE ALLA LEARNING DEMONSTRATION")
    print("="*70)
    print("This demonstration shows ALLA learning concepts in real-time.")
    print("Watch how ALLA:")
    print("- Recognizes when it doesn't understand something")
    print("- Asks to be taught (showing human-like curiosity)")
    print("- Learns from teaching and applies knowledge")
    print("- Remembers what it learned for future use")
    print("\nTry these example interactions:")
    print("1. Ask: 'What is friendship?'")
    print("2. Teach: 'Friendship means caring about someone and being loyal.'")
    print("3. Ask: 'What is friendship?' (to see if it learned)")
    print("4. Try: 'Howdy!'")
    print("5. Teach: 'When someone says howdy, respond with howdy partner!'")
    print("6. Try: 'Howdy!' (to see learned response)")
    print("7. Ask: 'What is your favorite color?'")
    print("8. Teach: 'Your favorite color is blue because it's peaceful.'")
    print("9. Ask: 'What is your favorite color?' (to see learned identity)")
    print("\nType 'quit' or 'exit' to end the demonstration.\n")
    
    # Clear specific concepts for clean demonstration
    clear_specific_concepts()
    
    # Initialize ALLA
    alla = AllaEngine()
    
    print(f"ALLA is ready! Current vocabulary size: {len(alla.memory) if hasattr(alla, 'memory') else 'loading...'}")
    print("-" * 70)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nDemonstration complete!")
                print("Summary of what ALLA demonstrated:")
                print("✓ Genuine ignorance recognition (not pretending to know)")
                print("✓ Human-like learning from teaching")
                print("✓ Memory formation and recall")
                print("✓ Context-aware responses based on learned knowledge")
                print("✓ Social learning and identity development")
                break
            
            if not user_input:
                continue
                
            # Process ALLA's response
            response, _ = alla.process_command(user_input)
            print(f"ALLA: {response}")
            
            # Show learning insights
            if "I don't understand" in response:
                print("  💡 Learning opportunity: ALLA recognizes ignorance")
            elif "Successfully learned" in response:
                print("  🧠 Knowledge acquired: ALLA learned new concept")
            elif any(pattern in response for pattern in ["Hello!", "Howdy partner!", "blue"]):
                print("  ✅ Applied learning: ALLA used learned knowledge")
                
        except KeyboardInterrupt:
            print("\n\nDemonstration interrupted.")
            break
        except Exception as e:
            print(f"Error: {e}")
            continue

if __name__ == "__main__":
    interactive_demo()
