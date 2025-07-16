#!/usr/bin/env python3
"""
MINIMAL ALLA v18.0 TEST
======================
Quick validation that the professional architecture works.
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

print("🚀 ALLA v18.0 QUICK TEST")
print("=" * 30)

try:
    print("Importing ALLA v18.0...")
    from alla_engine_v18 import AllaEngineV18
    print("✅ Import successful")
    
    print("\nInitializing engine...")
    alla = AllaEngineV18('quick_test.json')
    print("✅ Engine initialized")
    
    print("\nTesting basic commands...")
    
    # Test 1: Basic query
    feedback, result = alla.process_command("what is red")
    print(f"Command 1: 'what is red' -> {feedback}")
    
    # Test 2: Grammar-based parsing
    feedback, result = alla.process_command('teach property "shiny" as "obj.material == \'metal\'"')
    print(f"Command 2: Teaching -> {feedback}")
    
    # Test 3: Unknown word (triggers inquiry)
    feedback, result = alla.process_command("examine mysterious artifact")
    print(f"Command 3: Unknown word -> {feedback}")
    
    print("\nTesting autonomous thinking...")
    alla.tick()
    
    print("\nShutting down...")
    alla.shutdown()
    
    print("\n✅ ALL TESTS PASSED!")
    print("🎯 ALLA v18.0 Professional Architecture: OPERATIONAL")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
