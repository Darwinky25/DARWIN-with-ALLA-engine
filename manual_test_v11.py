#!/usr/bin/env python3
"""
Manual test of ALLA Engine v11.0 teach command
"""

from alla_engine import AllaEngine
from pathlib import Path

def manual_test():
    print("=== ALLA ENGINE v11.0 MANUAL TEST ===")
    
    # Initialize with basic concepts
    engine = AllaEngine()
    
    # Basic curriculum
    curriculum_path = Path("manual_test.alla")
    curriculum_content = """
property :: red :: obj.color == 'red'
property :: blue :: obj.color == 'blue'
noun :: box :: obj.shape == 'box'
noun :: circle :: obj.shape == 'circle'
action :: create :: none
inquiry :: what :: none
inquiry :: is :: none
"""
    curriculum_path.write_text(curriculum_content.strip())
    engine.learn_from_file(curriculum_path)
    
    # Test commands
    test_commands = [
        "help teach",
        'teach property "sparkly" as "obj.material == \'glitter\'"',
        "create a sparkly blue box as test1",
        "what is sparkly",
        'teach relation "bigger_than" as "obj1.size > obj2.size"',
        "create a big red box as big1",
        "create a small blue circle as small1", 
        "is big1 bigger_than small1",
    ]
    
    for i, cmd in enumerate(test_commands, 1):
        print(f"\n[{i}] Command: '{cmd}'")
        feedback, result = engine.process_command(cmd)
        print(f"    Feedback: {feedback}")
        
        if isinstance(result, bool):
            print(f"    Answer: {'Yes' if result else 'No'}")
        elif isinstance(result, list) and len(result) > 0:
            print(f"    Found {len(result)} items:")
            for item in result:
                print(f"        {item}")
        elif isinstance(result, list):
            print("    Found: No items")
        elif result:
            print(f"    Result: {result}")
    
    # Cleanup
    engine.shutdown()
    curriculum_path.unlink()
    print("\n=== TEST COMPLETE ===")

if __name__ == "__main__":
    manual_test()
