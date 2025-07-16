#!/usr/bin/env python3
"""
ALLA Autonomous Learning Demo
Shows how to enable ALLA's ability to learn from the internet.
"""

import sys
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.append(str(Path(__file__).parent))

from alla_engine import AllaEngine

def demo_autonomous_learning():
    """Simple demo of ALLA's autonomous learning."""
    
    print("ALLA Autonomous Learning Demo")
    print("=" * 50)
    
    # Initialize ALLA
    print("\n1. Initializing ALLA...")
    alla = AllaEngine("demo_memory.json")
    
    print(f"   ALLA knows {alla.lexicon.get_word_count()} words")
    
    # Enable autonomous learning
    print("\n2. Enabling autonomous learning...")
    result = alla.enable_autonomous_learning()
    print(f"   {result}")
    
    print("\n3. Testing autonomous learning...")
    print("   Try asking ALLA about words it doesn't know!")
    print("   Examples:")
    print("   - 'what is photosynthesis'")
    print("   - 'what is a telescope'") 
    print("   - 'hello' (in different languages)")
    print("   - 'what is democracy'")
    
    print("\n4. Interactive mode (type 'quit' to exit):")
    
    while True:
        try:
            user_input = input("\n>>> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                break
            
            if not user_input:
                continue
            
            # Process the command
            response, result = alla.process_command(user_input)
            print(f"ALLA: {response}")
            
            # Show learning stats
            if hasattr(alla, 'get_autonomous_learning_stats'):
                stats = alla.get_autonomous_learning_stats()
                if stats.get('total_attempts', 0) > 0:
                    print(f"📊 Learning Stats: {stats['successful_learning']}/{stats['total_attempts']} successful ({stats['success_rate']:.1%})")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n🎓 ALLA now knows {alla.lexicon.get_word_count()} words!")
    print("   Autonomous learning complete.")

if __name__ == "__main__":
    demo_autonomous_learning()
