#!/usr/bin/env python3
"""
Test script for ALLA Engine v13.0 - The Agent of Purpose
"The First Desire" - Witnessing ALLA's first autonomous goal pursuit.

This is the revolutionary test where we:
1. Start ALLA v13.0
2. Create a red box in the world 
3. Give ALLA its first goal: "I have the red box"
4. Watch it autonomously create a plan and execute it
5. Witness the moment ALLA becomes proactive, not reactive
"""

from alla_engine import AllaEngine
from world import LivingWorld

def test_first_desire():
    print("=" * 70)
    print("ALLA ENGINE v13.0 - THE AGENT OF PURPOSE")
    print("The First Desire Test: Witnessing Autonomous Goal Pursuit")
    print("=" * 70)
    
    # Initialize ALLA v13.0
    print("\n1. Initializing ALLA Engine v13.0...")
    alla = AllaEngine()
    
    # Add a red box to the world for ALLA to desire
    print("\n2. Creating a red box in the world...")
    red_box = alla.world.create_object("red_box", "box", "red", 3, "cardboard")
    print(f"Created: {red_box}")
    
    # Show current world state
    print("\n3. Current world state:")
    for obj in alla.world.get_all_objects():
        print(f"   {obj}")
    
    # Check ALLA's current inventory (should be empty)
    print("\n4. ALLA's current inventory:")
    alla_inventory = alla.world.get_objects_by_owner("alla")
    if alla_inventory:
        for obj in alla_inventory:
            print(f"   {obj}")
    else:
        print("   (empty)")
    
    # THE REVOLUTIONARY MOMENT: Give ALLA its first desire
    print("\n5. THE FIRST DESIRE - Giving ALLA a goal...")
    goal = alla.set_goal("red box")  # This should trigger "do i have red box"
    
    if goal:
        print(f"   Goal ID: {goal.id}")
        print(f"   Description: {goal.description}")
        print(f"   Status: {goal.status}")
        
        # Manual execution of a few thinking cycles to demonstrate
        print("\n6. MANUAL THINKING DEMONSTRATION (5 ticks):")
        for i in range(5):
            alla.tick()
            
            # Check if goal is completed
            if goal.status == 'completed':
                print(f"\n🎉 GOAL ACHIEVED! ALLA successfully obtained the red box!")
                break
        
        # Show final state
        print("\n7. Final world state:")
        for obj in alla.world.get_all_objects():
            print(f"   {obj}")
        
        print("\n8. ALLA's final inventory:")
        alla_inventory = alla.world.get_objects_by_owner("alla")
        if alla_inventory:
            for obj in alla_inventory:
                print(f"   {obj}")
        else:
            print("   (empty)")
    
    # Demonstrate autonomous loop (optional)
    print("\n9. Starting autonomous thinking loop...")
    print("   (This will run indefinitely until Ctrl+C)")
    print("   ALLA will continue to think and pursue any remaining goals.")
    
    # Create another goal for demonstration
    print("\n   Adding another goal for the autonomous loop...")
    alla.set_goal("blue crystal")  # Reference to the Shiny_Gem
    
    # Start the autonomous loop
    alla.main_loop()

if __name__ == "__main__":
    test_first_desire()
