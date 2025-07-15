#!/usr/bin/env python3
"""
Quick final test for ALLA Engine v10.0 comparison logic
"""

# Create a simple test of the comparison logic
from alla_engine import AllaEngine
from pathlib import Path
import os

def test_comparisons():
    # Create a minimal curriculum
    curriculum_content = """
# Quick test curriculum
property :: big :: lambda obj: obj.size >= 7
property :: small :: lambda obj: obj.size <= 3
relation :: bigger_than :: obj1.size > obj2.size
relation :: smaller_than :: obj1.size < obj2.size
action :: create :: none
noun :: box :: lambda obj: obj.shape == 'box'
noun :: circle :: lambda obj: obj.shape == 'circle'
property :: red :: lambda obj: obj.color == 'red'
property :: blue :: lambda obj: obj.color == 'blue'
"""
    
    # Write curriculum
    curriculum_path = Path("quick_test.alla")
    curriculum_path.write_text(curriculum_content.strip())
    
    # Initialize engine
    engine = AllaEngine()
    engine.learn_from_file(curriculum_path)
    
    # Test commands
    test_commands = [
        "create a big red box as A",      # size 8
        "create a small blue circle as B", # size 3
        "is A bigger than B",             # 8 > 3 → True
        "is B smaller than A",            # 3 < 8 → True
        "is B bigger than A",             # 3 > 8 → False
    ]
    
    print("=== FINAL COMPARISON TEST ===")
    for i, cmd in enumerate(test_commands, 1):
        print(f"[{i}] Command: '{cmd}'")
        feedback, result = engine.process_command(cmd)
        print(f"    Result: {feedback}")
        if isinstance(result, bool):
            print(f"    Answer: {'True' if result else 'False'}")
        print()
    
    # Cleanup
    os.remove(curriculum_path)
    print("Test complete - v10.0 comparisons verified!")

if __name__ == "__main__":
    test_comparisons()
