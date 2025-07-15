#!/usr/bin/env python3

from alla_engine import AllaEngine
from pathlib import Path

# Quick test for non-existent object handling
curriculum_path = Path('test_concepts.alla')
curriculum_content = '''
property :: red :: obj.color == 'red'
action :: create :: none
action :: destroy :: none
conditional :: if :: none
conditional :: then :: none
'''
curriculum_path.write_text(curriculum_content.strip())

print("Testing conditional reasoning with non-existent objects...")
engine = AllaEngine()
engine.learn_from_file(curriculum_path)

# Test with non-existent object
print("\n1. Creating object A...")
engine.process_command('create a red box as A')

print("2. Testing conditional with non-existent object X...")
feedback, result = engine.process_command('if X is red then destroy A')
print(f"   Feedback: {feedback}")
print(f"   Result: {result}")

print("3. Checking if A still exists...")
obj_a = engine.world.get_object_by_name("a")
print(f"   Object A still exists: {obj_a is not None}")
if obj_a:
    print(f"   A details: {obj_a}")

# Cleanup
curriculum_path.unlink()
print("\nTest completed successfully!")
