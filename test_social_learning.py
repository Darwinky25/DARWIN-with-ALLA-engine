from alla_engine import AllaEngine
from pathlib import Path

engine = AllaEngine()
engine.learn_from_file(Path('basic_vocabulary.alla'))  # Ensure all patterns are loaded
print('=== Testing Human-Like Social Learning ===')
print()

result1 = engine.process_command('hello')
print(f'Hello: {result1[1]}')

result2 = engine.process_command('thanks')
print(f'Thanks: {result2[1]}')

result3 = engine.process_command('goodbye')
print(f'Goodbye: {result3[1]}')

print()
print('=== Testing Social Learning Opportunity ===')
result4 = engine.process_command('howdy')
print(f'Howdy (unknown): {result4}')

print()
print('=== Teaching ALLA a new social response ===')
teach_result = engine.process_command('teach social "howdy_response" as "Hey there, partner!"')
print(f'Teaching result: {teach_result}')

print()
print('=== Now teach the base social word ===')
teach_howdy = engine.process_command('teach social "howdy" as "acknowledge_greeting"')
print(f'Teaching howdy: {teach_howdy}')

print()
print('=== Testing newly learned response ===')
result5 = engine.process_command('howdy')
print(f'Howdy (after learning): {result5}')
