#!/usr/bin/env python3
"""Simple test for autonomous learning integration."""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

try:
    from alla_engine import AllaEngine
    print("✅ Imported AllaEngine")
    
    alla = AllaEngine("test_autonomous.json")
    print("✅ Created ALLA instance")
    
    result = alla.enable_autonomous_learning()
    print(f"✅ Enabled autonomous learning: {result}")
    
    # Test a simple unknown word
    response, _ = alla.process_command("telescope")
    print(f"✅ Processed command: {response}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
