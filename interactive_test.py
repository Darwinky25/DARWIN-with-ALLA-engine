#!/usr/bin/env python3
"""
ALLA v17.0 - Interactive Test Interface
======================================

Quick and easy way to test ALLA's features interactively.
"""

from alla_engine import AllaEngine

def interactive_test():
    """Run a quick interactive test of ALLA features."""
    print("🚀 ALLA v17.0 - INTERACTIVE TEST")
    print("=" * 35)
    
    try:
        engine = AllaEngine()
        
        print("✅ ALLA initialized successfully!")
        print("\n🧪 Running predefined tests...")
        print("-" * 40)
        
        # Predefined test commands
        test_commands = [
            ("what is red", "Testing basic knowledge query"),
            ("create big blue sphere as test_ball", "Testing object creation"),
            ("what do I have", "Testing inventory check"),
            ("take the mysterious_object", "Testing curiosity system"),
            ("what do you know about blue", "Testing semantic memory"),
            ('teach property "shiny" as "obj.material == \'metal\'"', "Testing learning system")
        ]
        
        for i, (command, description) in enumerate(test_commands, 1):
            print(f"\n{i}. {description}")
            print(f"   Command: '{command}'")
            
            try:
                feedback, result = engine.process_command(command)
                print(f"   ALLA: {feedback}")
                
                if result is not None:
                    if isinstance(result, list):
                        print(f"   Found: {len(result)} items")
                    elif isinstance(result, bool):
                        print(f"   Answer: {'Yes' if result else 'No'}")
                    elif isinstance(result, str):
                        print(f"   Result: {result}")
                
                # Let ALLA think
                engine.tick()
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        print("\n" + "=" * 40)
        print("🎉 INTERACTIVE TEST COMPLETE!")
        print("=" * 40)
        print("Want to chat with ALLA? Run: python chat_with_alla.py")
        print("Want to see learning demo? Run: python demo_natural_learning.py")
        print("Want full interface? Run: python natural_interface.py")
        
        engine.shutdown()
        
    except Exception as e:
        print(f"❌ Interactive test failed: {e}")
        print("Please ensure alla_engine.py and world.py are available.")

if __name__ == "__main__":
    interactive_test()
