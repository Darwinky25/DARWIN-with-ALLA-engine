#!/usr/bin/env python3
"""
ISOLATION TEST FOR ALLA v18.0
=============================
Test imports without Neo4j to isolate the hanging issue.
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

print("🔍 ISOLATION TEST: Testing import without Neo4j initialization")
print("=" * 60)

try:
    print("1. Testing basic imports...")
    from lark import Lark, Transformer
    import networkx as nx
    print("   ✅ External libraries imported successfully")
    
    print("2. Testing ALLA components...")
    # Import but don't initialize engine
    import alla_engine_v18
    print("   ✅ ALLA module imported successfully")
    
    print("3. Testing individual classes...")
    from alla_engine_v18 import WordEntry, Goal, Plan, SemanticNode, SemanticEdge
    print("   ✅ Data classes imported successfully")
    
    from alla_engine_v18 import ALLATransformer, ProfessionalCommandProcessor
    print("   ✅ Grammar classes imported successfully")
    
    print("4. Testing semantic memory with fallback only...")
    from alla_engine_v18 import ProfessionalSemanticMemory
    semantic_mem = ProfessionalSemanticMemory(neo4j_uri=None, use_fallback=True)
    print("   ✅ SemanticMemory (fallback only) initialized successfully")
    
    print("5. Testing full engine initialization (no Neo4j)...")
    # Patch the constructor to skip Neo4j
    from alla_engine_v18 import AllaEngineV18
    
    # This should work since we pass neo4j_uri=None
    engine = AllaEngineV18('test_isolation.json', neo4j_uri=None)
    print("   ✅ Full engine initialized successfully")
    
    print("6. Testing basic command processing...")
    response, result = engine.process_command("what is red")
    print(f"   ✅ Command processed: {response}")
    
    engine.shutdown()
    print("\n🎉 ISOLATION TEST PASSED: All components work without Neo4j!")
    print("   Issue must be in Neo4j connection test logic.")

except Exception as e:
    import traceback
    print(f"\n❌ ISOLATION TEST FAILED: {e}")
    print("Traceback:")
    traceback.print_exc()
