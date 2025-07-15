#!/usr/bin/env python3
"""
Final demonstration of ALLA Engine v11.0 - The Self-Educating Agent
This showcases the revolutionary teach command and persistent memory.
"""

from alla_engine import AllaEngine
from pathlib import Path
import os

def final_demo():
    print("ALLA ENGINE v11.0 - THE SELF-EDUCATING AGENT")
    print("=" * 60)
    
    # Clean start
    memory_file = Path("alla_memory.json")
    if memory_file.exists():
        memory_file.unlink()
    
    # Initialize with minimal curriculum
    engine = AllaEngine()
    
    # Minimal base curriculum
    base_curriculum = Path("base.alla")
    base_curriculum.write_text("""
action :: create :: none
inquiry :: what :: none
inquiry :: is :: none
""")
    engine.learn_from_file(base_curriculum)
    
    print(f"\nDEMONSTRATION: Teaching ALLA new concepts on-the-fly!")
    
    # Teaching session
    teach_commands = [
        'teach property "magical" as "obj.material == \'enchanted\'"',
        'teach noun "unicorn" as "obj.shape == \'unicorn\'"',
        'teach property "tiny" as "obj.size <= 2"',
        'teach property "giant" as "obj.size >= 9"',
    ]
    
    print("\nTEACHING PHASE:")
    for i, cmd in enumerate(teach_commands, 1):
        print(f"   [{i}] {cmd}")
        feedback, result = engine.process_command(cmd)
        if "Successfully learned" in str(result):
            print(f"       SUCCESS: {result}")
        else:
            print(f"       FAILED: {result}")
    
    # Test the learned concepts
    print("\nTESTING LEARNED CONCEPTS:")
    test_commands = [
        "create a magical tiny unicorn as Sparkle",
        "create a giant magical unicorn as Thunder", 
        "what is magical",
        "what is tiny",
        "what is giant",
    ]
    
    for i, cmd in enumerate(test_commands, 1):
        print(f"   [{i}] {cmd}")
        feedback, result = engine.process_command(cmd)
        if isinstance(result, list) and len(result) > 0:
            print(f"       Found {len(result)} objects:")
            for obj in result:
                print(f"           • {obj.name} ({obj.shape}, size {obj.size}, {obj.material})")
        elif result and hasattr(result, 'name'):
            print(f"       Created: {result.name}")
        else:
            print(f"       {feedback}")
    
    # Save and restart
    print("\nMEMORY PERSISTENCE TEST:")
    print("   Shutting down and saving memory...")
    engine.shutdown()
    
    print("   Restarting engine (should load saved knowledge)...")
    engine2 = AllaEngine()
    
    print("   Testing if concepts were remembered...")
    persistence_test = "what is magical"
    feedback, result = engine2.process_command(persistence_test)
    
    if isinstance(result, list) and len(result) > 0:
        print(f"   SUCCESS! Remembered {len(result)} magical objects:")
        for obj in result:
            print(f"       • {obj.name}")
    else:
        print(f"   FAILED: Could not remember learned concepts")
    
    # Final shutdown
    engine2.shutdown()
    
    # Show memory file
    print(f"\nPERSISTENT MEMORY FILE: {memory_file}")
    if memory_file.exists():
        with open(memory_file, 'r') as f:
            content = f.read()
            word_count = content.count('"word_type"')
            print(f"   Contains {word_count} learned concepts")
    
    # Cleanup
    base_curriculum.unlink()
    
    print("\n" + "=" * 60)
    print("ALLA ENGINE v11.0 DEMONSTRATION COMPLETE!")
    print("ALLA can now learn and remember forever!")
    print("=" * 60)

if __name__ == "__main__":
    final_demo()
