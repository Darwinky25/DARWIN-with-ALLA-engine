#!/usr/bin/env python3
"""
Quick test script for ALLA Engine v5.0 complex logical operations.
"""

from pathlib import Path
import os
import sys

# Import the engine
sys.path.append(os.path.dirname(__file__))
from alla_engine import AllaEngine

def test_complex_logic():
    """Test complex logical operations that might need fixing."""
    
    # Setup curriculum
    curriculum_path = Path("test_concepts.alla")
    curriculum_content = """
property :: red :: obj.color == 'red'
property :: blue :: obj.color == 'blue'
noun :: box :: obj.shape == 'box'
noun :: circle :: obj.shape == 'circle'
inquiry :: what :: none
operator :: and :: none
operator :: or :: none
operator :: not :: none
operator :: same :: none
operator :: different :: none
action :: create :: none
    """
    curriculum_path.write_text(curriculum_content.strip())
    
    # Initialize engine
    engine = AllaEngine()
    engine.learn_from_file(curriculum_path)
    
    # Create test objects
    print("Creating test objects...")
    engine.process_command("create a red box as A")
    engine.process_command("create a blue circle as B")
    engine.process_command("create a red circle as C")
    
    # Test complex queries
    test_queries = [
        "what is red and not box",  # Should find C (red circle)
        "what is blue and not circle",  # Should find nothing
        "what is not not red",  # Double negation - should find A and C
    ]
    
    for query in test_queries:
        print(f"\n>>> Testing: '{query}'")
        feedback, result = engine.process_command(query)
        print(f"    Feedback: {feedback}")
        if isinstance(result, list):
            if result:
                print(f"    Found {len(result)} objects:")
                for obj in result:
                    print(f"        {obj}")
            else:
                print("    Found: No objects")
        else:
            print(f"    Result: {result}")
    
    # Cleanup
    os.remove(curriculum_path)
    print(f"\nTest complete. Curriculum file removed.")

if __name__ == "__main__":
    test_complex_logic()
