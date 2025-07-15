#!/usr/bin/env python3

from alla_engine import AllaEngine
from pathlib import Path

# Debug test
print("Debugging ALLA Engine v9.0...")

engine = AllaEngine()

# Test curriculum
curr = Path('test.alla')
curr.write_text('property :: red :: obj.color == "red"\nnoun :: box :: obj.shape == "box"')
engine.learn_from_file(curr)

# Test basic functionality with debugging
feedback, result = engine.process_command('create a red box as TEST')
print(f'Create test - Feedback: "{feedback}", Result: {result}')

feedback, result = engine.process_command('what is red')
print(f'Query test - Feedback: "{feedback}", Result: {result}')

feedback, result = engine.process_command('what is unknown_word')
print(f'Unknown word test - Feedback: "{feedback}", Result: {result}')

curr.unlink()
print('Debug complete!')
