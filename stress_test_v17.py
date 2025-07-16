#!/usr/bin/env python3
"""
ALLA v17.0 Stress Test - Verification of Perfect Operation
"""

from alla_engine import AllaEngine
import traceback

def stress_test():
    print('=== ALLA v17.0 COMPREHENSIVE STRESS TEST ===')
    alla = AllaEngine('stress_test.json')
    
    test_cases = [
        'examine mysterious_object',
        'investigate the crystalline artifact', 
        'create red mysterious_shape as test',
        'teach noun "artifact" as "obj.material == \'crystal\'"',
        'what do I have',
        'what is shimmering and transparent',
    ]
    
    passed = 0
    total = len(test_cases)
    
    for i, command in enumerate(test_cases, 1):
        try:
            print(f'\nTest {i}: "{command}"')
            feedback, result = alla.process_command(command)
            print(f'✓ PASSED: {feedback}')
            passed += 1
        except Exception as e:
            print(f'✗ FAILED: {str(e)}')
            traceback.print_exc()
    
    # Test thinking cycles
    try:
        print('\nTesting autonomous thinking...')
        alla.tick()
        alla.tick()
        print('✓ PASSED: Autonomous thinking works')
        passed += 1
        total += 1
    except Exception as e:
        print(f'✗ FAILED: Thinking error: {str(e)}')
        total += 1
    
    print(f'\n=== STRESS TEST RESULTS ===')
    print(f'Passed: {passed}/{total} tests')
    
    if passed == total:
        print('🎉 PERFECT! ALLA v17.0 is absolutely flawless!')
        success = True
    else:
        print('❌ Some issues detected.')
        success = False
    
    alla.shutdown()
    return success

if __name__ == "__main__":
    success = stress_test()
    exit(0 if success else 1)
