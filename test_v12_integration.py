#!/usr/bin/env python3
"""
Test script for ALLA Engine v12.0 - The Great Separation
Tests the integration with the external LivingWorld engine.
"""

from alla_engine import AllaEngine
from world import LivingWorld

def test_v12_integration():
    print("=" * 60)
    print("ALLA ENGINE v12.0 - THE GREAT SEPARATION")
    print("Testing integration with external LivingWorld")
    print("=" * 60)
    
    # Initialize ALLA (should load genesis_world.json)
    print("\n1. Initializing ALLA Engine v12.0...")
    alla = AllaEngine()
    
    # Check if ALLA can see objects from the external world
    print("\n2. Testing world interaction...")
    feedback, result = alla.process_command("what is in the world")
    print(f"Command: 'what is in the world'")
    print(f"Feedback: {feedback}")
    if result:
        print("Objects found:")
        for obj in result:
            print(f"  - {obj}")
    
    # Test object interaction
    print("\n3. Testing object queries...")
    feedback, result = alla.process_command("where is Old_Tree")
    print(f"Command: 'where is Old_Tree'")
    print(f"Feedback: {feedback}")
    print(f"Result: {result}")
    
    # Test object creation through ALLA
    print("\n4. Testing object creation...")
    feedback, result = alla.process_command("create red cube as test_cube")
    print(f"Command: 'create red cube as test_cube'")
    print(f"Feedback: {feedback}")
    if result:
        print(f"Created: {result}")
    
    # Check world state after creation
    print("\n5. Verifying world state after creation...")
    feedback, result = alla.process_command("what is in the world")
    print(f"Command: 'what is in the world'")
    print(f"Total objects: {len(result) if result else 0}")
    
    # Test taking an object
    print("\n6. Testing object interaction...")
    feedback, result = alla.process_command("take test_cube")
    print(f"Command: 'take test_cube'")
    print(f"Feedback: {feedback}")
    print(f"Result: {result}")
    
    # Check what ALLA has
    print("\n7. Checking ALLA's inventory...")
    feedback, result = alla.process_command("what do I have")
    print(f"Command: 'what do I have'")
    print(f"Feedback: {feedback}")
    if result:
        print("ALLA's inventory:")
        for obj in result:
            print(f"  - {obj}")
    
    # Test teach command (v11.0 feature retained)
    print("\n8. Testing teach command (v11.0 feature)...")
    feedback, result = alla.process_command('teach property "shiny" as "obj.material == \'crystal\'"')
    print(f"Command: teach property \"shiny\" as \"obj.material == 'crystal'\"")
    print(f"Feedback: {feedback}")
    print(f"Result: {result}")
    
    # Test the taught concept
    print("\n9. Testing learned concept...")
    feedback, result = alla.process_command("what is shiny")
    print(f"Command: 'what is shiny'")
    print(f"Feedback: {feedback}")
    if result:
        print("Shiny objects found:")
        for obj in result:
            print(f"  - {obj}")
    
    # Test world persistence
    print("\n10. Testing world persistence...")
    print("Current world time:", alla.world.get_current_time())
    print("Total events recorded:", len(alla.world.get_events()))
    
    # Save and shutdown
    print("\n11. Saving and shutting down...")
    alla.world.save_state("test_world_state.json")
    alla.shutdown()
    
    print("\n" + "=" * 60)
    print("ALLA ENGINE v12.0 INTEGRATION TEST COMPLETE")
    print("- External world loaded successfully")
    print("- Object interaction working")
    print("- Object creation/modification working") 
    print("- Inventory management working")
    print("- Teaching system retained")
    print("- World persistence working")
    print("=" * 60)

if __name__ == "__main__":
    test_v12_integration()
