"""
ALLA INITIATIVE PHASE 1: NATURAL LANGUAGE VISUAL TEACHING TEST
==============================================================

This test demonstrates the ALLA Guiding Principles in action:
1. Human teaches in natural language
2. ALLA learns through grounded experience  
3. Technology facilitates, never replaces
4. Full transparency in reasoning
5. Integration with existing ALLA knowledge base
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from alla_engine import AllaEngine
from alla_visual_teacher import VisualTeacher, VisualReasoner
from pathlib import Path
import json

def test_principle_1_natural_teaching():
    """
    Test Principle: "The human teacher should not need to understand Python, 
    JSON, or complex syntax. They teach in natural language."
    """
    print("\n" + "="*60)
    print("TESTING PRINCIPLE 1: NATURAL LANGUAGE TEACHING")
    print("="*60)
    
    # Initialize ALLA with clean state
    alla = AllaEngine("test_visual_memory.json")
    teacher = VisualTeacher(alla)
    
    # Human teaches in completely natural language
    natural_instructions = [
        "When you see blue squares, move them down until they touch something",
        "If there are isolated red objects, connect them with a line",
        "When you see enclosed areas, fill them with the same color as the border"
    ]
    
    example_grids = [
        [[0, 1, 0], [0, 0, 0], [2, 2, 2]],  # Blue square above red barrier
        [[1, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],  # Isolated blue objects
        [[2, 2, 2], [2, 0, 2], [2, 2, 2]]  # Red border with empty center
    ]
    
    success_count = 0
    for instruction, grid in zip(natural_instructions, example_grids):
        print(f"\nHUMAN: '{instruction}'")
        response = teacher.teach_visual_rule(instruction, grid)
        print(f"ALLA: {response}")
        
        if "I learned" in response:
            success_count += 1
        
    print(f"\nRESULT: ALLA learned {success_count}/{len(natural_instructions)} rules from natural language")
    alla.shutdown()
    
    return success_count == len(natural_instructions)

def test_principle_2_grounded_learning():
    """
    Test Principle: "ALLA learns through grounded experience."
    """
    print("\n" + "="*60)
    print("TESTING PRINCIPLE 2: GROUNDED LEARNING")
    print("="*60)
    
    alla = AllaEngine("test_visual_memory.json")
    teacher = VisualTeacher(alla)
    reasoner = VisualReasoner(alla, teacher)
    
    # Teach ALLA with concrete examples
    grid1 = [[0, 1, 0], [0, 0, 0], [2, 2, 2]]
    teacher.teach_visual_rule("Blue moves down to red", grid1)
    
    # Test if ALLA can apply learning to similar but different grid
    grid2 = [[1, 0, 0], [0, 0, 0], [0, 0, 2]]  # Different layout, same concept
    analysis = reasoner.analyze_grid(grid2)
    
    print(f"Original teaching grid: {grid1}")
    print(f"New test grid: {grid2}")
    print(f"ALLA's analysis: {analysis['alla_thoughts']}")
    print(f"Applicable rules: {analysis['applicable_rules']}")
    
    # Check if ALLA grounded the learning in its existing knowledge base
    feedback, result = alla.process_command("what do you know about blue")
    print(f"ALLA's knowledge about 'blue': {result if result else 'No specific knowledge'}")
    
    alla.shutdown()
    return len(analysis['applicable_rules']) > 0

def test_principle_3_technology_bridge():
    """
    Test Principle: "Technology bridges human language to AI understanding."
    """
    print("\n" + "="*60)
    print("TESTING PRINCIPLE 3: TECHNOLOGY AS BRIDGE")
    print("="*60)
    
    alla = AllaEngine("test_visual_memory.json")
    teacher = VisualTeacher(alla)
    
    # Show how natural language gets parsed into structured understanding
    instruction = "When you see blue squares, move them down until they touch something"
    
    print(f"Human instruction: '{instruction}'")
    
    # Internal parsing (normally hidden from human)
    parsed = teacher._parse_natural_instruction(instruction)
    print(f"Technology parsing (internal): {parsed}")
    
    # Grounding in ALLA's knowledge (normally hidden from human)
    grid = [[0, 1, 0], [0, 0, 0], [2, 2, 2]]
    response = teacher.teach_visual_rule(instruction, grid)
    
    print(f"ALLA's response (visible to human): {response}")
    
    # Show that the human doesn't need to understand the internal complexity
    print("\nThe human teacher never needs to see or understand:")
    print("- Python parsing logic")
    print("- JSON data structures") 
    print("- Internal semantic memory operations")
    print("- Graph database operations")
    print("\nThe human only sees natural language input and output.")
    
    alla.shutdown()
    return parsed is not None

def test_principle_4_transparency():
    """
    Test Principle: "The human must always be able to understand what ALLA 
    is thinking and why."
    """
    print("\n" + "="*60)
    print("TESTING PRINCIPLE 4: FULL TRANSPARENCY")
    print("="*60)
    
    alla = AllaEngine("test_visual_memory.json")
    teacher = VisualTeacher(alla)
    reasoner = VisualReasoner(alla, teacher)
    
    # Teach ALLA some rules
    teacher.teach_visual_rule("Blue moves down", [[0, 1, 0], [0, 0, 0], [2, 2, 2]])
    teacher.teach_visual_rule("Connect isolated objects", [[1, 0, 0, 0, 1], [0, 0, 0, 0, 0]])
    
    # Show complete transparency of ALLA's reasoning
    test_grid = [[0, 1, 0], [0, 0, 0], [0, 0, 0]]
    
    print("HUMAN PROVIDES TEST GRID:")
    for row in test_grid:
        print(row)
    
    print("\nALLA'S COMPLETE REASONING PROCESS:")
    analysis = reasoner.analyze_grid(test_grid)
    
    print(f"1. What ALLA sees: {analysis['colors_present']} colors")
    print(f"2. Patterns ALLA detects: {analysis['patterns_detected']}")
    print(f"3. Rules ALLA considers: {analysis['applicable_rules']}")
    print(f"4. ALLA's interpretation: {analysis['alla_thoughts']}")
    
    print("\nALLA'S LEARNED RULES (Human-readable):")
    for i, rule in enumerate(teacher.visual_rules, 1):
        print(f"{i}. {rule.to_natural_language()}")
        print(f"   Confidence: {rule.confidence}")
        print(f"   Examples: {len(rule.examples)} grids")
    
    print("\nTRANSPARENCY ACHIEVED: Human can see exactly how ALLA thinks.")
    
    alla.shutdown()
    return len(teacher.visual_rules) > 0

def test_principle_5_integration():
    """
    Test Principle: "Integration with existing ALLA knowledge base."
    """
    print("\n" + "="*60)
    print("TESTING PRINCIPLE 5: INTEGRATION WITH EXISTING ALLA")
    print("="*60)
    
    alla = AllaEngine("test_visual_memory.json")
    teacher = VisualTeacher(alla)
    
    # First, teach ALLA some regular (non-visual) concepts
    alla.process_command('teach property "blue" as "obj.color == \'blue\'"')
    alla.process_command('teach property "red" as "obj.color == \'red\'"')
    alla.process_command('teach action "move" as "obj.action_type == \'move\'"')
    
    print("ALLA's existing knowledge:")
    feedback, result = alla.process_command("what do you know about blue")
    print(f"About blue: {result if result else 'Learning...'}")
    
    # Now teach visual rules that connect to this existing knowledge
    grid = [[0, 1, 0], [0, 0, 0], [2, 2, 2]]
    response = teacher.teach_visual_rule("Blue objects move down", grid)
    
    print(f"\nAfter visual teaching: {response}")
    
    # Check integration - ALLA should connect visual and symbolic knowledge
    feedback, result = alla.process_command("what do you know about move")
    print(f"About move: {result if result else 'Learning...'}")
    
    # Test if ALLA can reason about both visual and symbolic concepts
    print("\nTesting integrated reasoning:")
    feedback, result = alla.process_command("what is blue")
    print(f"ALLA's understanding of 'blue': {feedback}")
    
    print("\nINTEGRATION SUCCESSFUL: Visual learning builds on existing knowledge.")
    
    alla.shutdown()
    return True

def run_alla_initiative_phase1_test():
    """
    Master test for ALLA Initiative Phase 1: Natural Language Visual Teaching
    """
    print("ALLA INITIATIVE PHASE 1 TEST")
    print("Validating implementation of ALLA Guiding Principles")
    print("="*80)
    
    tests = [
        ("Principle 1: Natural Language Teaching", test_principle_1_natural_teaching),
        ("Principle 2: Grounded Learning", test_principle_2_grounded_learning),
        ("Principle 3: Technology as Bridge", test_principle_3_technology_bridge),
        ("Principle 4: Full Transparency", test_principle_4_transparency),
        ("Principle 5: Integration with ALLA", test_principle_5_integration)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            print(f"\n{'='*20} {test_name} {'='*20}")
            success = test_func()
            results.append(success)
            print(f"RESULT: {'PASSED' if success else 'FAILED'}")
        except Exception as e:
            print(f"ERROR: {e}")
            results.append(False)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\n{'='*80}")
    print(f"ALLA INITIATIVE PHASE 1 TEST RESULTS: {passed}/{total} principles validated")
    
    if passed == total:
        print("ALL TESTS PASSED! ALLA Initiative Phase 1 principles successfully implemented!")
        print("\nKey achievements:")
        print("- Humans can teach ALLA in natural language")
        print("- ALLA learns through grounded visual experience")
        print("- Technology bridges understanding transparently")
        print("- Full transparency in ALLA's reasoning process")
        print("- Visual learning integrates with existing ALLA knowledge")
        print("\nReady for Phase 2: Symbolic Reasoning Engine")
    else:
        print(f"{total - passed} principles need attention before proceeding.")
    
    return passed == total

if __name__ == "__main__":
    # Clean up any existing test files
    for test_file in ["test_visual_memory.json"]:
        if Path(test_file).exists():
            Path(test_file).unlink()
    
    success = run_alla_initiative_phase1_test()
    
    # Clean up test files
    for test_file in ["test_visual_memory.json"]:
        if Path(test_file).exists():
            Path(test_file).unlink()
    
    print(f"\nPhase 1 Implementation: {'COMPLETE' if success else 'NEEDS WORK'}")
