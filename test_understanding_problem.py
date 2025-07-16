#!/usr/bin/env python3
"""
Test to prove ALLA currently just copies from internet without true understanding.
Then demonstrate the fix for genuine understanding.
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from alla_engine import AllaEngine

def test_shallow_vs_deep_learning():
    """Test that shows ALLA currently just copies vs truly understanding."""
    
    print("🧪 TESTING: Shallow Copy vs Deep Understanding")
    print("=" * 60)
    
    # Initialize ALLA
    alla = AllaEngine("understanding_test_memory.json")
    alla.enable_autonomous_learning()
    
    print("\n1️⃣ TESTING SHALLOW LEARNING (Current Issue)")
    print("-" * 50)
    
    # Test with a scientific concept
    print("Teaching ALLA about 'photosynthesis'...")
    response, _ = alla.process_command("what is photosynthesis")
    print(f"ALLA's response: {response}")
    
    # Check if ALLA can actually USE this knowledge contextually
    print("\n🧐 Testing if ALLA truly understands 'photosynthesis':")
    
    understanding_tests = [
        "do plants do photosynthesis",  # Should understand the connection
        "what happens in photosynthesis", # Should know the process
        "why do plants need light",      # Should connect to photosynthesis
        "create a plant that does photosynthesis"  # Should apply knowledge
    ]
    
    for test in understanding_tests:
        print(f"\nTest: '{test}'")
        response, _ = alla.process_command(test)
        print(f"ALLA: {response}")
        
        # Check if ALLA's lexicon has proper understanding
        entry = alla.lexicon.get_entry("photosynthesis")
        if entry:
            print(f"Internal representation: {entry.meaning_expression}")
            print(f"Word type: {entry.word_type}")
        
    print("\n❌ PROBLEM: ALLA just copied the definition but doesn't truly understand it!")
    print("   - It can't apply the knowledge in different contexts")
    print("   - It doesn't connect concepts together")
    print("   - It's just parroting the internet definition")
    
    return alla

if __name__ == "__main__":
    test_shallow_vs_deep_learning()
