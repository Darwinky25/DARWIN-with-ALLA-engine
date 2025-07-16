#!/usr/bin/env python3
"""
Quick test to verify ALLA has learned and no longer shows hardcoded responses
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from alla_engine import AllaEngine

def quick_learning_test():
    print("🧪 Quick Learning Verification Test")
    print("=" * 40)
    
    # Test with default setup (basic vocabulary loaded)
    alla = AllaEngine(memory_path="quick_test_memory.json")
    
    print("\n📋 Testing Current Behavior:")
    
    test_inputs = [
        "hello",
        "thank you", 
        "thank you very much",
        "goodbye"
    ]
    
    for input_text in test_inputs:
        print(f"\nInput: '{input_text}'")
        response, _ = alla.process_command(input_text)
        print(f"Response: {response}")
        
        # Check for hardcoded patterns
        suspicious_patterns = [
            "You're welcome!",
            "You are welcome!",
            "No problem!"
        ]
        
        is_suspicious = any(pattern in response for pattern in suspicious_patterns)
        if is_suspicious:
            print("❌ STILL HARDCODED!")
        else:
            print("✅ Appears to be compositional")
    
    # Cleanup
    if os.path.exists("quick_test_memory.json"):
        os.remove("quick_test_memory.json")

if __name__ == "__main__":
    quick_learning_test()
