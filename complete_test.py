#!/usr/bin/env python3

from alla_engine import AllaEngine
from pathlib import Path

# Complete test
print("Testing ALLA Engine v9.0 with complete curriculum...")

engine = AllaEngine()

# Test curriculum - including actions and inquiry words
curr = Path('complete_test.alla')
curriculum_content = """
property :: red :: obj.color == 'red'
noun :: box :: obj.shape == 'box'
action :: create :: none
inquiry :: what :: none
"""
curr.write_text(curriculum_content.strip())
engine.learn_from_file(curr)

# Test basic functionality with debugging
feedback, result = engine.process_command('create a red box as TEST')
print(f'Create test - Feedback: "{feedback}", Result: {result}')

feedback, result = engine.process_command('what is red')
print(f'Query test - Feedback: "{feedback}", Result: {result}')

feedback, result = engine.process_command('what is unknown_word')
print(f'Unknown word test - Feedback: "{feedback}", Result: {result}')

curr.unlink()
print('All tests complete!')
