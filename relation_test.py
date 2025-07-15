#!/usr/bin/env python3

from alla_engine import AllaEngine
from pathlib import Path

# Test the relation fixes
print("Testing ALLA Engine v10.0 relational comparisons...")

engine = AllaEngine()

# Test curriculum with relations
curr = Path('relation_test.alla')
curriculum_content = """
property :: red :: obj.color == 'red'
property :: blue :: obj.color == 'blue'
property :: big :: obj.size > 5
property :: small :: obj.size <= 5
noun :: box :: obj.shape == 'box'
noun :: circle :: obj.shape == 'circle'
relation :: bigger_than :: obj1.size > obj2.size
relation :: smaller_than :: obj1.size < obj2.size
action :: create :: none
inquiry :: is :: none
"""
curr.write_text(curriculum_content.strip())
engine.learn_from_file(curr)

# Test object creation and comparison
feedback, result = engine.process_command('create a big red box as A')
print(f'Create A: {result is not None}')

feedback, result = engine.process_command('create a small blue circle as B')
print(f'Create B: {result is not None}')

feedback, result = engine.process_command('is A bigger_than B')
print(f'A bigger than B: {feedback} -> {result}')

feedback, result = engine.process_command('is B smaller_than A')
print(f'B smaller than A: {feedback} -> {result}')

curr.unlink()
print('Relation test complete!')
