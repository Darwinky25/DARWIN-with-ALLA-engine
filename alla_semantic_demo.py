#!/usr/bin/env python3
"""
ALLA Semantic Bootstrapping Demonstration
Shows how ALLA builds and uses concept networks from single words.
"""

from alla_engine import AllaEngine

def semantic_demo():
    """Demonstrate ALLA's semantic capabilities."""
    print("🌱 ALLA SEMANTIC BOOTSTRAPPING DEMO")
    print("=" * 50)
    
    # Initialize ALLA
    alla = AllaEngine()
    print(f"📚 ALLA initialized with {alla.lexicon.get_word_count()} words")
    
    # Enable semantic bootstrapping
    result = alla.enable_semantic_bootstrapping()
    print(f"✅ {result}")
    
    # Get bootstrap stats
    stats = alla.get_semantic_bootstrap_stats()
    print(f"\n📊 Current Bootstrap Statistics:")
    for key, value in stats.items():
        if key != 'current_session_words':  # Skip this as it's too long
            print(f"   {key}: {value}")
    
    print(f"\n🧠 SEMANTIC REASONING TESTS:")
    print("-" * 30)
    
    # Test 1: Query about photosynthesis concepts
    print("🔍 Query: 'What do plants use for photosynthesis?'")
    result1 = alla.query_concept_network("plants photosynthesis light")
    print(result1)
    
    print("\n🔍 Query: 'How do organisms get energy?'")
    result2 = alla.query_concept_network("organism energy")
    print(result2)
    
    print("\n🔍 Query: 'What is cellular respiration?'")
    result3 = alla.query_concept_network("cellular respiration")
    print(result3)
    
    # Test 2: Try teaching a new word and see how it connects
    print(f"\n🎓 LEARNING TEST:")
    print("-" * 20)
    print("Teaching ALLA a new concept: 'ecosystem'...")
    
    # Bootstrap learn a new word
    if hasattr(alla, 'bootstrap_system'):
        new_result = alla.bootstrap_system.bootstrap_learn_word("ecosystem", "user")
        if new_result:
            print(f"✅ Learned {new_result.total_words_learned} new concepts!")
            print(f"🌳 Concept tree for 'ecosystem':")
            tree = alla.bootstrap_system.visualize_concept_map("ecosystem")
            print(tree)
    
    print(f"\n🏆 FINAL STATISTICS:")
    final_stats = alla.get_semantic_bootstrap_stats()
    print(f"   Total concept graph size: {final_stats.get('concept_graph_size', 0)}")
    print(f"   Total bootstrap sessions: {final_stats.get('total_sessions', 0)}")
    
    print(f"\nDEMO COMPLETE!")
    print("ALLA now has a rich semantic network and can reason about concepts!")

if __name__ == "__main__":
    semantic_demo()
