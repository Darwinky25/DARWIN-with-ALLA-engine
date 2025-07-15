"""
test_v14_comprehensive.py - Full demonstration of ALLA's v14.0 abstract knowledge capabilities
"""
from alla_engine import AllaEngine

def run_comprehensive_demo():
    print("ALLA ENGINE v14.0 - THE THINKER")
    print("=" * 60)
    
    alla = AllaEngine()
    
    print("\nPHASE 1: Creating diverse objects...")
    commands = [
        "create a red box",
        "create a blue circle", 
        "create a red sphere",
        "create a green triangle",
        "take red box"
    ]
    
    for cmd in commands:
        print(f"   Command: {cmd}")
        feedback, result = alla.process_command(cmd)
        if result and hasattr(result, 'name'):
            print(f"   Created: {result.name} ({result.color} {result.shape})")
        else:
            print(f"   {feedback}")
    
    print("\nPHASE 2: Triggering reflection...")
    alla._reflection_cycle()
    
    print("\nPHASE 3: Abstract knowledge queries...")
    queries = [
        "what do you know about 'red'?",
        "what do you know about 'blue'?", 
        "list all known actions",
        "list all colors",
        "list all properties"
    ]
    
    for query in queries:
        print(f"\n   Query: {query}")
        feedback, result = alla.process_command(query)
        if result:
            lines = result.split('\n') if isinstance(result, str) else [str(result)]
            for line in lines:
                if line.strip():
                    print(f"   {line}")
    
    print("\nPHASE 4: Testing goal pursuit with reflection...")
    goal = alla.set_goal("i have green triangle")
    if goal:
        print(f"   Goal set: {goal.description}")
        # Run a few thinking cycles
        for i in range(3):
            print(f"   🤔 Thinking cycle {i+1}...")
            alla.tick()
    
    print("\nPHASE 5: Final knowledge summary...")
    final_queries = [
        "list all known actions",
        "list all colors"
    ]
    
    for query in final_queries:
        feedback, result = alla.process_command(query)
        if result:
            print(f"   {query}: {result}")
    
    alla.shutdown()
    print("\nv14.0 COMPREHENSIVE DEMO COMPLETE!")
    print("ALLA now forms abstract knowledge from experiences!")

if __name__ == "__main__":
    run_comprehensive_demo()
