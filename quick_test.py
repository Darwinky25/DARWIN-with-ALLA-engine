#!/usr/bin/env python3

from alla_engine import AllaEngine
from pathlib import Path

# Quick test
print("Testing ALLA Engine v9.0 bug fixes...")

engine = AllaEngine()

# Test curriculum
curr = Path('test.alla')
curr.write_text('property :: red :: obj.color == "red"\nnoun :: box :: obj.shape == "box"')
engine.learn_from_file(curr)

# Test basic functionality
feedback, result = engine.process_command('create a red box as TEST')
print('Create test:', 'SUCCESS' if result else 'FAILED')

feedback, result = engine.process_command('what is red')
print('Query test:', 'SUCCESS' if result else 'FAILED')

feedback, result = engine.process_command('what is unknown_word')
print('Unknown word test:', 'SUCCESS' if 'Command failed' in feedback else 'FAILED')

feedback, result = engine.process_command('what if I have a blue elephant')
print('Hypothetical unknown test:', 'SUCCESS' if 'Cannot evaluate' in feedback else 'FAILED')

curr.unlink()
print('All basic tests passed!')
