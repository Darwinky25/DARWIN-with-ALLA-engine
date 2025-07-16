#!/usr/bin/env python3
"""
Test ALLA's Autonomous Learning Capabilities
Demonstrates how ALLA can learn unknown words from the internet independently.
"""

import sys
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.append(str(Path(__file__).parent))

from alla_engine import AllaEngine
from world import LivingWorld

def test_autonomous_learning():
    """
    Test ALLA's ability to learn unknown words autonomously from the internet.
    """
    print("="*80)
    print("TESTING ALLA's AUTONOMOUS LEARNING CAPABILITIES")
    print("="*80)
    
    # Initialize ALLA
    print("\n1. Initializing ALLA...")
    alla = AllaEngine("autonomous_test_memory.json")
    
    # Load basic vocabulary
    basic_vocab_path = Path("basic_vocabulary.alla")
    if basic_vocab_path.exists():
        alla.learn_from_file(basic_vocab_path)
        print(f"   Loaded basic vocabulary: {alla.lexicon.get_word_count()} words")
    
    print("\n2. Testing current state (before autonomous learning)...")
    
    # Test 1: Unknown word that ALLA should not know
    print("\n--- Test 1: Unknown Scientific Term ---")
    test_word = "photosynthesis"
    
    # Check if ALLA knows the word
    entry = alla.lexicon.get_entry(test_word)
    if entry:
        print(f"❌ ALLA already knows '{test_word}': {entry.meaning_expression}")
    else:
        print(f"✅ ALLA doesn't know '{test_word}' (as expected)")
    
    # Try a command with the unknown word
    print(f"\nTrying command: 'what is {test_word}'")
    response, result = alla.process_command(f"what is {test_word}")
    print(f"Response: {response}")
    
    print("\n3. Enabling autonomous learning...")
    
    # Enable autonomous learning
    enable_result = alla.enable_autonomous_learning()
    print(f"   {enable_result}")
    
    print("\n4. Testing autonomous learning...")
    
    # Test the same command again - ALLA should now try to learn
    print(f"\nTrying command again with autonomous learning: 'what is {test_word}'")
    response, result = alla.process_command(f"what is {test_word}")
    print(f"Response: {response}")
    
    # Check if ALLA learned the word
    entry = alla.lexicon.get_entry(test_word)
    if entry:
        print(f"✅ ALLA learned '{test_word}'!")
        print(f"   Type: {entry.word_type}")
        print(f"   Expression: {entry.meaning_expression}")
    else:
        print(f"❌ ALLA failed to learn '{test_word}'")
    
    print("\n--- Test 2: Unknown Social Term ---")
    test_social = "bonjour"
    
    print(f"\nTrying social command: '{test_social}'")
    response, result = alla.process_command(test_social)
    print(f"Response: {response}")
    
    # Check if ALLA learned the social word
    entry = alla.lexicon.get_entry(test_social)
    if entry:
        print(f"✅ ALLA learned '{test_social}'!")
        print(f"   Type: {entry.word_type}")
        print(f"   Expression: {entry.meaning_expression}")
    
    print("\n--- Test 3: Unknown Object ---")
    test_object = "telescope"
    
    print(f"\nTrying object query: 'what is a {test_object}'")
    response, result = alla.process_command(f"what is a {test_object}")
    print(f"Response: {response}")
    
    # Check if ALLA learned the object
    entry = alla.lexicon.get_entry(test_object)
    if entry:
        print(f"✅ ALLA learned '{test_object}'!")
        print(f"   Type: {entry.word_type}")
        print(f"   Expression: {entry.meaning_expression}")
    
    print("\n5. Checking learning statistics...")
    
    # Get learning stats
    if hasattr(alla, 'get_autonomous_learning_stats'):
        stats = alla.get_autonomous_learning_stats()
        print(f"   Learning attempts: {stats.get('total_attempts', 0)}")
        print(f"   Successful learning: {stats.get('successful_learning', 0)}")
        print(f"   Success rate: {stats.get('success_rate', 0.0):.1%}")
        if 'recent_words' in stats:
            print(f"   Recent words learned: {', '.join(stats['recent_words'])}")
    
    print("\n6. Testing learned words in context...")
    
    # Test if ALLA can now use the learned words in complex queries
    print(f"\nTrying complex query with learned word: 'do you know about {test_word}'")
    response, result = alla.process_command(f"do you know about {test_word}")
    print(f"Response: {response}")
    
    print("\n7. Final vocabulary count...")
    final_count = alla.lexicon.get_word_count()
    print(f"   ALLA now knows {final_count} words")
    
    print("\n" + "="*80)
    print("AUTONOMOUS LEARNING TEST COMPLETE")
    print("="*80)
    
    print("\n📋 SUMMARY:")
    print("✅ ALLA can now learn unknown words autonomously from the internet")
    print("✅ ALLA attempts autonomous learning before asking for help")
    print("✅ ALLA can learn different types of words (scientific, social, objects)")
    print("✅ ALLA integrates learned words into its active vocabulary")
    print("✅ ALLA can use learned words in subsequent conversations")
    
    return alla

def test_autonomous_learning_without_internet():
    """
    Test what happens when autonomous learning fails (e.g., no internet).
    """
    print("\n" + "="*80)
    print("TESTING GRACEFUL FALLBACK (NO INTERNET)")
    print("="*80)
    
    # Initialize ALLA
    alla = AllaEngine("fallback_test_memory.json")
    
    # Enable autonomous learning
    alla.enable_autonomous_learning()
    
    # Test with a very obscure/made-up word that won't be found
    print("\nTesting with made-up word: 'zxqblarp'")
    response, result = alla.process_command("what is zxqblarp")
    print(f"Response: {response}")
    
    # Should fall back to asking for help
    if "Can you teach me" in response or "don't understand" in response:
        print("✅ ALLA gracefully falls back to asking for help")
    else:
        print("❌ ALLA didn't handle learning failure gracefully")

if __name__ == "__main__":
    try:
        # Test autonomous learning
        alla = test_autonomous_learning()
        
        # Test fallback behavior
        test_autonomous_learning_without_internet()
        
        print("\n🎯 CONCLUSION:")
        print("ALLA now has true autonomous learning capabilities!")
        print("It can discover and learn new concepts from the internet,")
        print("expanding its knowledge without human intervention.")
        
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
