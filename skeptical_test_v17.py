#!/usr/bin/env python3
"""
ALLA v17.0 SKEPTICAL REALITY TEST
===============================

This test is designed to be skeptical and test ALLA against real human logic and expectations.
We will test edge cases, logical consistency, and realistic behavior patterns.

Test Philosophy:
- Be skeptical of "success" that doesn't make logical sense
- Test edge cases that could reveal flaws
- Verify that responses align with human reasoning
- Check for consistent behavior across similar scenarios
- Ensure the system fails gracefully when it should
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from alla_engine import AllaEngine
import traceback

def skeptical_test():
    print("=" * 60)
    print("ALLA v17.0 SKEPTICAL REALITY TEST")
    print("Testing against human logic and realistic expectations")
    print("=" * 60)
    
    alla = AllaEngine('skeptical_test.json')
    
    # Test 1: Logic Consistency - Does ALLA understand what "unknown" means?
    print("\n🔍 TEST 1: Logic Consistency")
    print("Testing if ALLA truly understands the concept of 'unknown'")
    
    # First, let's see what happens with a truly unknown word
    feedback1, result1 = alla.process_command("examine flibbertigibbet")
    print(f"Command: 'examine flibbertigibbet'")
    print(f"Response: {feedback1}")
    
    # Now test with another unknown word - should behave consistently
    feedback2, result2 = alla.process_command("investigate zyphonqlix")  
    print(f"Command: 'investigate zyphonqlix'")
    print(f"Response: {feedback2}")
    
    # SKEPTICAL CHECK: Are both responses logically consistent?
    if "understand" in feedback1.lower() and "understand" in feedback2.lower():
        print("✓ CONSISTENT: Both unknown words trigger understanding goals")
    else:
        print("❌ INCONSISTENT: Different responses to unknown words")
        print(f"  Response 1: {feedback1}")
        print(f"  Response 2: {feedback2}")
    
    # Test 2: Realistic Behavior - Does it handle mixed scenarios properly?
    print("\n🔍 TEST 2: Realistic Mixed Scenarios")
    print("Testing mixed known/unknown word combinations")
    
    # Teach ALLA one word first
    alla.process_command('teach noun "apple" as "obj.shape == \'round\'"')
    
    # Now test mixed scenario: one known, one unknown
    feedback3, result3 = alla.process_command("examine the sparkly apple")
    print(f"Command: 'examine the sparkly apple' (apple=known, sparkly=unknown)")
    print(f"Response: {feedback3}")
    
    # SKEPTICAL CHECK: Does it focus on the unknown word logically?
    if "sparkly" in feedback3.lower() and "unknown" in feedback3.lower():
        print("✓ LOGICAL: Correctly identifies the unknown word in mixed context")
    else:
        print("❌ ILLOGICAL: Should focus on 'sparkly' as the unknown word")
    
    # Test 3: Edge Case - Empty or nonsensical commands
    print("\n🔍 TEST 3: Edge Cases")
    print("Testing how ALLA handles problematic inputs")
    
    edge_cases = [
        "",  # Empty command
        "    ",  # Just spaces
        "the the the",  # Only grammar words
        "a an the is to from",  # Only articles and prepositions
    ]
    
    for i, cmd in enumerate(edge_cases, 1):
        try:
            feedback, result = alla.process_command(cmd)
            print(f"Edge case {i}: '{cmd}' -> {feedback}")
            if feedback and "understand" in feedback.lower():
                print(f"❌ ILLOGICAL: Shouldn't create understanding goals for '{cmd}'")
        except Exception as e:
            print(f"Edge case {i}: '{cmd}' -> Exception: {e}")
    
    # Test 4: Autonomous Thinking - Does it actually ask questions?
    print("\n🔍 TEST 4: Autonomous Question Generation")
    print("Testing if ALLA actually generates and asks questions")
    
    # Trigger an unknown word
    alla.process_command("study the mysterious artifact")
    
    # Capture what ALLA "says" during thinking
    print("ALLA is thinking...")
    original_print = print
    captured_output = []
    
    def capture_print(*args, **kwargs):
        captured_output.append(' '.join(str(arg) for arg in args))
        original_print(*args, **kwargs)
    
    # Temporarily replace print to capture ALLA's questions
    import builtins
    builtins.print = capture_print
    
    try:
        alla.tick()  # Let ALLA think
    finally:
        builtins.print = original_print
    
    # SKEPTICAL CHECK: Did ALLA actually ask a question?
    asked_question = any("ALLA ASKS" in output for output in captured_output)
    if asked_question:
        print("✓ REALISTIC: ALLA actually asked a question autonomously")
    else:
        print("❌ NOT REALISTIC: ALLA didn't ask any questions")
        print("Captured output:", captured_output)
    
    # Test 5: Learning Integration - Does teaching actually work?
    print("\n🔍 TEST 5: Learning Integration Reality Check")
    print("Testing if teaching actually changes ALLA's behavior")
    
    # First, trigger unknown word
    feedback_before, _ = alla.process_command("find the crystals")
    print(f"Before teaching 'find': {feedback_before}")
    
    # Teach the word
    teach_feedback, _ = alla.process_command('teach action "find" as "none"')
    print(f"Teaching 'find': {teach_feedback}")
    
    # Test again - should behave differently now
    feedback_after, _ = alla.process_command("find the crystals")
    print(f"After teaching 'find': {feedback_after}")
    
    # SKEPTICAL CHECK: Did behavior actually change?
    if feedback_before != feedback_after:
        print("✓ REALISTIC: Teaching changed ALLA's behavior")
        if "understand" not in feedback_after.lower():
            print("✓ LOGICAL: No longer asks about 'find' after learning")
        else:
            print("❌ ILLOGICAL: Still asking about 'find' after teaching")
    else:
        print("❌ NOT REALISTIC: Teaching had no effect on behavior")
    
    # Test 6: Goal Completion - Do goals actually complete?
    print("\n🔍 TEST 6: Goal Completion Reality Check")
    print("Testing if understanding goals actually get completed")
    
    # Check active goals before teaching
    active_goals_before = len([g for g in alla.active_goals if g.status == 'active'])
    print(f"Active goals before: {active_goals_before}")
    
    # Teach a word that should complete a goal
    alla.process_command('teach noun "artifact" as "obj.material == \'stone\'"')
    
    # Let ALLA think to process goal completion
    alla.tick()
    
    # Check active goals after
    active_goals_after = len([g for g in alla.active_goals if g.status == 'active'])
    completed_goals = len([g for g in alla.active_goals if g.status == 'completed'])
    
    print(f"Active goals after: {active_goals_after}")
    print(f"Completed goals: {completed_goals}")
    
    # SKEPTICAL CHECK: Do goals actually complete?
    if completed_goals > 0:
        print("✓ REALISTIC: Goals actually get completed")
    else:
        print("❌ NOT REALISTIC: No goals completed despite learning")
    
    # Test 7: Logical Word Priority - Multiple unknowns
    print("\n🔍 TEST 7: Multiple Unknown Words Priority")
    print("Testing ALLA's logic when multiple unknown words are present")
    
    feedback_multi, _ = alla.process_command("utilize the phantasmagorical contraption")
    print(f"Multiple unknowns: {feedback_multi}")
    
    # SKEPTICAL CHECK: Does it handle multiple unknowns logically?
    if "utilize" in feedback_multi or "phantasmagorical" in feedback_multi or "contraption" in feedback_multi:
        print("✓ LOGICAL: Focuses on one unknown word at a time")
    else:
        print("❌ ILLOGICAL: Doesn't handle multiple unknowns properly")
    
    # Final Assessment
    print("\n" + "=" * 60)
    print("SKEPTICAL ASSESSMENT SUMMARY")
    print("=" * 60)
    
    # Run a final reality check
    print("🧠 FINAL REALITY CHECK:")
    print("If ALLA truly understands 'unknown' concepts, it should:")
    print("1. Consistently detect unknown words")
    print("2. Ask logical questions about them") 
    print("3. Learn from teaching")
    print("4. Complete goals when learning occurs")
    print("5. Handle edge cases gracefully")
    
    # Test the most basic logic: known vs unknown
    known_response, _ = alla.process_command("examine apple")  # Should know this
    unknown_response, _ = alla.process_command("examine blorginator")  # Definitely unknown
    
    print(f"\nKnown word response: {known_response}")
    print(f"Unknown word response: {unknown_response}")
    
    if known_response != unknown_response:
        print("✅ PASSES BASIC LOGIC: Treats known and unknown words differently")
    else:
        print("❌ FAILS BASIC LOGIC: Same response for known and unknown words")
    
    alla.shutdown()
    
    print("\n🎯 VERDICT: Review the above tests for logical consistency and realistic behavior")

if __name__ == "__main__":
    skeptical_test()
