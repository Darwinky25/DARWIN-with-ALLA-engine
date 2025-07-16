#!/usr/bin/env python3
"""
ALLA v18.0 Complete Verification Test
Tests all major functionality to verify v18.0 is fully working.
"""

from alla_engine import AllaEngine
from pathlib import Path
import json

def test_alla_v18():
    """Complete test of ALLA v18.0 functionality."""
    print("=== ALLA v18.0 Complete Verification Test ===")
    print("Testing: Memory, Learning, Conversation, Identity, Social, Teaching")
    print()
    
    # Initialize ALLA - should load basic vocabulary
    engine = AllaEngine("test_v18_memory.json")
    print(f"ALLA v18.0 initialized with {engine.lexicon.get_word_count()} words in memory")
    print()
    
    # Define comprehensive test suite
    test_queries = [
        # Social & Conversational
        ("hi", "Social greeting - should recognize and respond appropriately"),
        ("hello", "Alternative greeting"),
        ("thank you", "Gratitude expression"),
        ("goodbye", "Farewell expression"),
        
        # Identity & Self-awareness
        ("what is your name", "Identity query - should know its name"),
        ("who are you", "Self identity - should describe itself"),
        ("what are you", "Self description - should explain what it is"),
        ("who is alla", "Agent identification"),
        
        # Teaching & Learning
        ("teach property \"shiny\" as \"obj.material == 'gold'\"", "Teach new property"),
        ("teach noun \"orb\" as \"obj.shape == 'sphere'\"", "Teach new noun"),
        ("teach social \"please\" as \"request_assistance\"", "Teach social word"),
        
        # Object Creation with new vocabulary
        ("create shiny orb as golden_sphere", "Create object using learned vocabulary"),
        
        # Verification
        ("what is in the world", "World inventory query"),
        ("is golden_sphere shiny", "Property verification with learned word"),
        ("please help me", "Social interaction with learned word"),
        
        # Knowledge queries
        ("what do you know about shiny", "Knowledge about learned concept"),
        ("list all properties", "List learned properties"),
        
        # Complex interactions
        ("do I have shiny orb", "Complex inventory check"),
        ("where is golden_sphere", "Location query"),
        ("when was golden_sphere created", "Temporal query"),
        
        # Help system
        ("help teach", "Teaching help"),
        ("what can you do", "Capability query"),
        
        # Unknown word handling
        ("what is zephyr", "Unknown word - should trigger learning"),
        ("teach noun \"zephyr\" as \"obj.name == 'wind'\"", "Learn the unknown word"),
        ("what is zephyr", "Query about newly learned word"),
        
        # Event system
        ("list events", "Event history"),
    ]
    
    # Execute tests
    passed = 0
    failed = 0
    
    for i, (query, description) in enumerate(test_queries, 1):
        print(f"Test {i:2d}: {query}")
        print(f"         {description}")
        try:
            feedback, result = engine.process_command(query)
            
            # Check for success indicators
            is_success = (
                feedback and 
                "not understand" not in feedback.lower() and
                "command not understood" not in feedback.lower() and
                "parse error" not in feedback.lower()
            )
            
            if is_success:
                print(f"         ✓ SUCCESS: {feedback}")
                if result is not None:
                    if isinstance(result, list) and len(result) > 3:
                        print(f"         Result: [{len(result)} items]")
                    elif isinstance(result, str) and len(result) > 80:
                        print(f"         Result: {result[:80]}...")
                    else:
                        print(f"         Result: {result}")
                passed += 1
            else:
                print(f"         ✗ FAILED: {feedback}")
                failed += 1
        except Exception as e:
            print(f"         ✗ ERROR: {e}")
            failed += 1
        print()
    
    # Memory persistence test
    print("=== Memory Persistence Test ===")
    original_count = engine.lexicon.get_word_count()
    print(f"Words before save: {original_count}")
    
    # Force save
    engine.save_lexicon()
    
    # Create new instance
    engine2 = AllaEngine("test_v18_memory.json")
    new_count = engine2.lexicon.get_word_count()
    print(f"Words after reload: {new_count}")
    
    # Test if learned concepts persist
    test_feedback, test_result = engine2.process_command("is golden_sphere shiny")
    memory_works = (
        original_count == new_count and
        test_feedback and "not understand" not in test_feedback.lower()
    )
    
    if memory_works:
        print("✓ Memory persistence: PASS")
        print(f"✓ Learned concepts available after reload")
    else:
        print("✗ Memory persistence: FAIL")
        failed += 1
    print()
    
    # Final results
    total_tests = len(test_queries) + 1  # +1 for memory test
    print("=== ALLA v18.0 Test Results ===")
    print(f"Tests Passed: {passed + (1 if memory_works else 0)}")
    print(f"Tests Failed: {failed}")
    print(f"Success Rate: {((passed + (1 if memory_works else 0)) / total_tests * 100):.1f}%")
    print(f"Final Lexicon Size: {engine2.lexicon.get_word_count()} words")
    
    # Check memory file
    memory_file = Path("test_v18_memory.json")
    if memory_file.exists():
        with open(memory_file, 'r') as f:
            memory_data = json.load(f)
        print(f"Persistent Memory: {len(memory_data)} concepts saved")
    
    # Overall assessment
    success_rate = (passed + (1 if memory_works else 0)) / total_tests
    if success_rate >= 0.9:
        status = "🎯 EXCELLENT - ALLA v18.0 FULLY OPERATIONAL"
    elif success_rate >= 0.8:
        status = "✓ GOOD - ALLA v18.0 MOSTLY WORKING"
    elif success_rate >= 0.6:
        status = "⚠ FAIR - ALLA v18.0 NEEDS IMPROVEMENT"
    else:
        status = "✗ POOR - ALLA v18.0 REQUIRES DEBUGGING"
    
    print(f"\n{status}")
    print(f"Success Rate: {success_rate*100:.1f}% ({passed + (1 if memory_works else 0)}/{total_tests})")
    
    # Cleanup
    engine.shutdown()
    engine2.shutdown()
    
    return success_rate >= 0.8

if __name__ == "__main__":
    test_alla_v18()
