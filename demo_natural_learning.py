#!/usr/bin/env python3
"""
ALLA v17.0 - Natural Learning Demonstration
==========================================

Demonstrate how ALLA learns language naturally through interaction
without any hardcoded translations or mappings.
"""

from alla_engine import AllaEngine

def demonstrate_natural_learning():
    """Show how ALLA learns language naturally through interaction."""
    
    print("="*70)
    print("🧠 ALLA v17.0 - NATURAL LANGUAGE LEARNING DEMONSTRATION")
    print("="*70)
    print("This demo shows how ALLA learns language naturally")
    print("without any hardcoded translations or mappings.")
    print("ALLA uses its curiosity system to ask about unknown words.")
    print("="*70)
    
    engine = AllaEngine()
    
    print("\n📚 SCENARIO 1: ALLA encounters an unknown word")
    print("-" * 50)
    print("Command: 'take the mysterious_gadget'")
    feedback, result = engine.process_command("take the mysterious_gadget")
    print(f"ALLA: {feedback}")
    
    # Let ALLA think and potentially ask a question
    print("\n💭 ALLA thinks about the unknown word...")
    engine.tick()
    
    print("\n📖 SCENARIO 2: User teaches ALLA the new word")
    print("-" * 50)
    teach_command = 'teach noun "mysterious_gadget" as "obj.shape == \'magical\'"'
    print(f"Command: {teach_command}")
    feedback, result = engine.process_command(teach_command)
    print(f"ALLA: {feedback}")
    
    print("\n🧠 SCENARIO 3: ALLA processes the learning")
    print("-" * 50)
    engine.tick()
    
    print("\n✅ SCENARIO 4: ALLA can now understand the word")
    print("-" * 50)
    print("Command: 'what is mysterious_gadget'")
    feedback, result = engine.process_command("what is mysterious_gadget")
    print(f"ALLA: {feedback}")
    if result:
        print(f"Result: {result}")
    
    print("\n🎯 SCENARIO 5: ALLA uses the learned word in context")
    print("-" * 50)
    print("Command: 'create big red mysterious_gadget as magic_tool'")
    feedback, result = engine.process_command("create big red mysterious_gadget as magic_tool")
    print(f"ALLA: {feedback}")
    
    print("\n📚 SCENARIO 6: Teaching more complex concepts")
    print("-" * 50)
    print("Command: teach property \"sparkling\" as \"obj.material == 'glitter'\"")
    feedback, result = engine.process_command('teach property "sparkling" as "obj.material == \'glitter\'"')
    print(f"ALLA: {feedback}")
    
    print("\n🔍 SCENARIO 7: ALLA understands and can explain new concepts")
    print("-" * 50)
    print("Command: 'what is sparkling'")
    feedback, result = engine.process_command("what is sparkling")
    print(f"ALLA: {feedback}")
    
    print("\n🎮 SCENARIO 8: Testing learned knowledge retention")
    print("-" * 50)
    print("Command: 'what do you know about mysterious_gadget'")
    feedback, result = engine.process_command("what do you know about mysterious_gadget")
    print(f"ALLA: {feedback}")
    
    print("\n📊 SCENARIO 9: Checking ALLA's vocabulary expansion")
    print("-" * 50)
    print("Command: 'list all properties'")
    feedback, result = engine.process_command("list all properties")
    print(f"ALLA: {feedback}")
    
    print("\n" + "="*70)
    print("🎉 DEMONSTRATION COMPLETE!")
    print("="*70)
    print("✨ Key Learning Points:")
    print("• ALLA learns words through natural teaching interaction")
    print("• No hardcoded language mappings or translations required")
    print("• ALLA asks questions when encountering unknown words")
    print("• Learning is persistent and builds upon previous knowledge")
    print("• ALLA uses learned words in future interactions naturally")
    print("• Curiosity-driven learning enables continuous vocabulary growth")
    print("="*70)
    
    engine.shutdown()

if __name__ == "__main__":
    try:
        demonstrate_natural_learning()
    except Exception as e:
        print(f"Demo failed: {e}")
        print("Please ensure alla_engine.py and world.py are available.")
