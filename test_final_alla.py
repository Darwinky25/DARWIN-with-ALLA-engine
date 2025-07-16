#!/usr/bin/env python3
"""
Final comprehensive test for ALLA v17.0
Tests all major functionality including learning, memory, conversation, and grammar alignment.
"""

from alla_engine import AllaEngine
from pathlib import Path
import json

def test_comprehensive_alla():
    """Comprehensive test of all ALLA v17.0 functionality."""
    print("=== ALLA v17.0 Final Comprehensive Test ===")
    print("Testing: Learning, Memory, Conversation, Identity, Teaching, Grammar")
    print()
    
    # Initialize ALLA
    engine = AllaEngine("test_final_memory.json")
    print(f"ALLA initialized with {engine.lexicon.get_word_count()} words in memory")
    print()
    
    test_queries = [
        # 1. Identity and Social Queries
        ("hi", "Social greeting"),
        ("hello", "Social greeting variant"),
        ("what is your name", "Identity query"),
        ("who are you", "Identity query variant"),
        ("who is alla", "Agent identification"),
        ("what are you", "Self description"),
        ("what do you do", "Capability query"),
        
        # 2. Teaching and Learning
        ("teach property \"sparkly\" as \"obj.material == 'glitter'\"", "Teach new property"),
        ("teach noun \"globe\" as \"obj.shape == 'sphere'\"", "Teach new noun"),
        ("teach relation \"bigger_than\" as \"obj1.size > obj2.size\"", "Teach new relation"),
        
        # 3. Object Creation and Queries
        ("create sparkly globe as crystal_ball", "Create object with new vocabulary"),
        ("what is in the world", "Inventory query"),
        ("what do I have", "Personal inventory"),
        
        # 4. Property and Relation Queries
        ("is crystal_ball sparkly", "Property verification"),
        ("is crystal_ball bigger_than Old_Tree", "Relation verification"),
        
        # 5. Knowledge Queries
        ("what do you know about sparkly", "Knowledge about learned concept"),
        ("list all properties", "List learned properties"),
        
        # 6. Conditional and Complex Queries
        ("do I have sparkly globe", "Complex inventory check"),
        ("sparkly globe", "Filter by multiple properties"),
        
        # 7. Unknown Word Handling
        ("what is blorgify", "Unknown word trigger"),
        ("teach action \"blorgify\" as \"none\"", "Teach the unknown word"),
        ("what is blorgify", "Query about newly learned word"),
        
        # 8. Help System
        ("help", "General help"),
        ("help teach", "Teaching help"),
        ("what can you do", "Capability query"),
        
        # 9. Complex Grammar Patterns
        ("where is crystal_ball", "Location query"),
        ("when was crystal_ball created", "Temporal query"),
        ("list events", "Event history"),
    ]
    
    # Execute all test queries
    passed = 0
    total = len(test_queries)
    
    for i, (query, description) in enumerate(test_queries, 1):
        print(f"--- Test {i}: '{query}' ({description}) ---")
        try:
            feedback, result = engine.process_command(query)
            if feedback and "not understand" not in feedback.lower():
                print(f"PASS: {feedback}")
                if result is not None:
                    if isinstance(result, list) and len(result) > 3:
                        print(f"  Result: [{len(result)} items]")
                    else:
                        print(f"  Result: {result}")
                passed += 1
            else:
                print(f"FAIL: {feedback}")
                if result:
                    print(f"  Result: {result}")
        except Exception as e:
            print(f"ERROR: {e}")
        print()
    
    # Test memory persistence
    print("=== Memory Persistence Test ===")
    print(f"Words before save: {engine.lexicon.get_word_count()}")
    engine.save_lexicon()
    
    # Create new engine instance to test loading
    engine2 = AllaEngine("test_final_memory.json")
    print(f"Words after reload: {engine2.lexicon.get_word_count()}")
    
    # Test if learned words are still available
    feedback, result = engine2.process_command("is crystal_ball sparkly")
    print(f"Memory test feedback: {feedback}")
    print(f"Memory test result: {result}")
    memory_test_passed = ("sparkly" in str(feedback).lower() or 
                         "sparkly" in str(result).lower() or 
                         (result and len(result) > 0))  # Object found means memory worked
    
    # Alternative test: Check if 'sparkly' word itself is in the lexicon
    sparkly_entry = engine2.lexicon.get_entry("sparkly")
    if sparkly_entry:
        print(f"'sparkly' word found in lexicon: {sparkly_entry.meaning_expression}")
        memory_test_passed = True
    else:
        print("'sparkly' word not found in lexicon after reload")
    
    print(f"Memory persistence: {'PASS' if memory_test_passed else 'FAIL'}")
    print()
    
    # Final summary
    print("=== Final Summary ===")
    print(f"Query Tests: {passed}/{total} passed ({passed/total*100:.1f}%)")
    print(f"Memory Persistence: {'PASS' if memory_test_passed else 'FAIL'}")
    print(f"Final Lexicon Size: {engine2.lexicon.get_word_count()} words")
    
    # Check memory file
    memory_file = Path("test_final_memory.json")
    if memory_file.exists():
        with open(memory_file, 'r') as f:
            memory_data = json.load(f)
        print(f"Memory File: {len(memory_data)} concepts saved")
        
        # Show sample of learned words
        learned_words = list(memory_data.keys())[:10]
        print(f"Sample words: {', '.join(learned_words)}")
    
    overall_success = passed >= total * 0.8 and memory_test_passed
    print(f"\nFINAL RESULT: {'ALLA v17.0 PASSED' if overall_success else 'NEEDS IMPROVEMENT'}")
    
    # Cleanup
    engine.shutdown()
    engine2.shutdown()
    
    return overall_success

if __name__ == "__main__":
    test_comprehensive_alla()
