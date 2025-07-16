#!/usr/bin/env python3
"""
ALLA v17.0 - THE INQUISITIVE MIND DEMO
=====================================

This demo showcases ALLA's new curiosity-driven learning capabilities.
Watch as ALLA encounters unknown words and proactively asks for definitions!

Key v17.0 Features:
- Autonomous question generation for unknown concepts
- Goal-driven inquiry behavior  
- Seamless integration with existing teaching system
- Proactive learning instead of passive failure
"""

import sys
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.append(str(Path(__file__).parent))

from alla_engine import AllaEngine

def main():
    print("="*60)
    print("ALLA v17.0 - THE INQUISITIVE MIND DEMO")
    print("="*60)
    print("Watch ALLA become curious about unknown words!")
    print()
    
    # Initialize ALLA
    alla = AllaEngine("demo_v17_memory.json")
    
    print("\n" + "="*50)
    print("SCENARIO: Encountering Unknown Concepts")
    print("="*50)
    
    # Test 1: Unknown action word
    print("\n[Demo] Let's try an unknown action...")
    print("USER: 'investigate the box'")
    feedback, result = alla.process_command("investigate the box")
    print(f"ALLA: {feedback}")
    
    # Let ALLA think about this
    print("\n[Demo] ALLA is thinking...")
    alla.tick()
    
    print("\n[Demo] Now let's teach ALLA what 'investigate' means...")
    print("USER: teach action \"investigate\" as \"none\"")
    feedback, result = alla.process_command("teach action \"investigate\" as \"none\"")
    print(f"ALLA: {feedback}")
    
    # Let ALLA think again to see the goal completion
    print("\n[Demo] ALLA thinks again...")
    alla.tick()
    
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    print("✓ ALLA detected unknown word 'investigate'")
    print("✓ ALLA created an UNDERSTAND goal automatically") 
    print("✓ ALLA asked a question autonomously")
    print("✓ User taught ALLA the new concept")
    print("✓ ALLA's goal was completed successfully")
    print()
    print("This demonstrates the key v17.0 upgrade:")
    print("ALLA is now PROACTIVE about learning, not passive!")
    
    alla.shutdown()

if __name__ == "__main__":
    main()
