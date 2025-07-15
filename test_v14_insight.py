"""
test_v14_insight.py - Demonstrates ALLA's abstract knowledge formation (v14.0)
"""
from alla_engine import AllaEngine

def run_insight_demo():
    alla = AllaEngine()
    print("\n--- Creating objects ---")
    alla.process_command("create a red box")
    alla.process_command("create a blue circle")
    alla.process_command("create a red sphere")
    print("\n--- Triggering Reflection ---")
    # Manually trigger reflection for demo
    alla._reflection_cycle()
    print("\n--- Abstract Knowledge Queries ---")
    feedback, result = alla.process_command("what do you know about 'red'?")
    print(feedback)
    print(result)
    feedback, result = alla.process_command("list all known actions")
    print(feedback)
    print(result)
    feedback, result = alla.process_command("list all colors")
    print(feedback)
    print(result)

if __name__ == "__main__":
    run_insight_demo()
