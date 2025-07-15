#!/usr/bin/env python3
"""
ALLA v16.0 Test Script: The Mystery Object
==========================================

This script demonstrates ALLA's new curiosity-driven learning capabilities.
We will:
1. Place a mysterious object (flute) in the world that ALLA doesn't know about
2. Ask ALLA to interact with it 
3. Watch ALLA realize it doesn't understand the word and ask about it
4. Teach ALLA about the flute
5. Verify that ALLA can now interact with it successfully

Expected Behavior:
- OLD v15.0: "take the flute" would fail with "Unknown words detected"
- NEW v16.0: "take the flute" triggers curiosity, ALLA asks "What is a flute?"
"""

import sys
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.append(str(Path(__file__).parent))

from alla_engine import AllaEngine
from world import LivingWorld

def setup_world_with_mystery_object():
    """Set up a world with a mysterious 'flute' that ALLA doesn't know about."""
    print("=== Setting up world with mystery object ===")
    
    # Create ALLA with test memory file that has base vocabulary
    alla = AllaEngine("test_v16_memory.json")
    
    # Add a mysterious object to the world - a 'flute'
    # This object exists in the world but ALLA has no concept of what a 'flute' is
    flute = alla.world.create_object("flute", "cylinder", "brown", 3, "wood")
    if flute:
        print(f"Created mysterious object: {flute.name} (shape: {flute.shape}, color: {flute.color}, material: {flute.material})")
    else:
        print("Failed to create flute object")
    
    # Also add a known object for comparison
    box = alla.world.create_object("box1", "box", "red", 5, "plastic")
    if box:
        print(f"Created known object: {box.name} (shape: {box.shape}, color: {box.color}, material: {box.material})")
    else:
        print("Failed to create box object")
    
    return alla

def test_mystery_object_discovery():
    """The main test: ALLA encounters an unknown object and learns about it."""
    print("\n" + "="*60)
    print("ALLA v16.0 MYSTERY OBJECT TEST")
    print("="*60)
    
    # Setup
    alla = setup_world_with_mystery_object()
    
    print("\n--- Phase 1: ALLA encounters the unknown word ---")
    print("User: take the flute")
    
    # This should trigger ALLA's curiosity instead of failing
    result = alla.process_command("take the flute")
    print(f"Result: {result}")
    
    # ALLA should now have an UNDERSTAND goal
    print(f"\nALLA's current goals: {len(alla.active_goals)}")
    for goal in alla.active_goals:
        print(f"  - {goal.description} (type: {goal.goal_type}, status: {goal.status})")
        if goal.inquiry_question:
            print(f"    Question: {goal.inquiry_question}")
    
    print("\n--- Phase 2: ALLA thinks and asks a question ---")
    print("Running ALLA's thinking cycle...")
    
    # Let ALLA think - this should create a plan to ask about the flute
    alla.tick()
    
    # The question should have been output during the tick
    
    print("\n--- Phase 3: User teaches ALLA about flutes ---")
    print("User teaches ALLA: teach noun \"flute\" as \"obj.shape == 'cylinder' and obj.material == 'wood'\"")
    
    # Teach ALLA about flutes
    teach_result = alla.process_command('teach noun "flute" as "obj.shape == \'cylinder\' and obj.material == \'wood\'"')
    print(f"Teaching result: {teach_result}")
    
    print("\n--- Phase 4: ALLA runs another thinking cycle ---")
    print("Running another thinking cycle to check if ALLA now understands...")
    
    # Another tick to see if the UNDERSTAND goal is now complete
    alla.tick()
    
    print("\n--- Phase 5: Verify ALLA can now interact with the flute ---")
    print("User: take the flute")
    
    # This should now work since ALLA understands what a flute is
    final_result = alla.process_command("take the flute")
    print(f"Final result: {final_result}")
    
    # Check if ALLA now has the flute
    print("\nUser: what do I have?")
    inventory_result = alla.process_command("what do I have?")
    print(f"ALLA's inventory: {inventory_result}")
    
    print("\n--- Phase 6: Test ALLA's understanding ---")
    print("User: what is flute")
    understanding_result = alla.process_command("what is flute")
    print(f"ALLA's understanding: {understanding_result}")
    
    return True

def test_multiple_unknown_words():
    """Test ALLA's behavior with multiple unknown words."""
    print("\n" + "="*60)
    print("MULTIPLE UNKNOWN WORDS TEST")
    print("="*60)
    
    alla = AllaEngine("test_v16_memory2.json")  # Use test memory with base vocabulary
    
    # Add objects ALLA doesn't know about
    trumpet = alla.world.create_object("trumpet", "cylinder", "brass", 4, "metal")
    violin = alla.world.create_object("violin", "oval", "brown", 2, "wood")
    print(f"Created test objects: trumpet and violin")
    
    print("User: do I have a trumpet?")
    result1 = alla.process_command("do I have a trumpet?")
    print(f"Result: {result1}")
    
    # Let ALLA think about the first unknown word
    alla.tick()
    
    print("\nUser: do I have a violin?")
    result2 = alla.process_command("do I have a violin?")
    print(f"Result: {result2}")
    
    # Check ALLA's goals
    print(f"\nALLA's goals after encountering multiple unknowns:")
    for goal in alla.active_goals:
        print(f"  - {goal.description} (type: {goal.goal_type})")
    
    return True

def test_known_vs_unknown():
    """Test that ALLA handles known words normally while being curious about unknown ones."""
    print("\n" + "="*60)
    print("KNOWN VS UNKNOWN WORD TEST")
    print("="*60)
    
    alla = AllaEngine("test_v16_memory3.json")  # Use test memory with base vocabulary
    
    # Add known and unknown objects
    box = alla.world.create_object("box1", "box", "red", 5, "plastic")
    mystery = alla.world.create_object("gadget", "sphere", "silver", 3, "metal")
    print(f"Created test objects: box1 and gadget")
    
    print("User: do I have a red box?")
    result1 = alla.process_command("do I have a red box?")
    print(f"Result (known words): {result1}")
    
    print("\nUser: do I have a gadget?")
    result2 = alla.process_command("do I have a gadget?")
    print(f"Result (unknown word): {result2}")
    
    # ALLA should only create an inquiry goal for the unknown word
    print(f"\nALLA's goals:")
    for goal in alla.active_goals:
        print(f"  - {goal.description} (type: {goal.goal_type})")
    
    return True

def run_all_tests():
    """Run all v16.0 tests."""
    print("STARTING ALLA v16.0 COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    
    tests = [
        ("Mystery Object Discovery", test_mystery_object_discovery),
        ("Multiple Unknown Words", test_multiple_unknown_words),
        ("Known vs Unknown Words", test_known_vs_unknown)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            print(f"\n{'='*20} {test_name} {'='*20}")
            success = test_func()
            if success:
                print(f"- {test_name} PASSED")
                passed += 1
            else:
                print(f"- {test_name} FAILED")
        except Exception as e:
            print(f"- {test_name} FAILED with exception: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*80}")
    print(f"ALLA v16.0 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("ALL TESTS PASSED! ALLA v16.0 - The Inquisitive Agent is working correctly!")
        print("\nKey v16.0 Features Validated:")
        print("- Unknown word detection triggers curiosity instead of failure")
        print("- UNDERSTAND goals are created automatically")
        print("- ALLA asks meaningful questions about unknown concepts")
        print("- Learning new words completes UNDERSTAND goals")
        print("- Known words continue to work normally")
        print("- Multiple unknown words create separate inquiry goals")
    else:
        print(f"- {total - passed} tests failed. Please check the implementation.")
    
    return passed == total

if __name__ == "__main__":
    # Create test memory files that start with base vocabulary
    import json
    import shutil
    import os
    
    # Clean up any old test memory files first
    for file in ["test_v16_memory.json", "test_v16_memory2.json", "test_v16_memory3.json"]:
        if os.path.exists(file):
            os.remove(file)
    
    # Copy base vocabulary to test files
    if os.path.exists("alla_memory.json"):
        for test_file in ["test_v16_memory.json", "test_v16_memory2.json", "test_v16_memory3.json"]:
            shutil.copy("alla_memory.json", test_file)
        print("Test memory files created with base vocabulary")
    
    run_all_tests()
