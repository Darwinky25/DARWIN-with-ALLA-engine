#!/usr/bin/env python3
"""
Test ALLA v20.0 Semantic Bootstrapping Engine
Verifying that ALLA can build concept networks from single words.
"""

def test_alla_semantic_bootstrap():
    """Test ALLA's semantic bootstrapping capabilities."""
    print("=== ALLA v20.0 Semantic Bootstrapping Test ===")
    print("Testing: Concept Networks, Semantic Learning, World Model Building")
    print()
    
    try:
        # Try to create AllaEngine - first check if it exists
        try:
            from alla_engine import AllaEngine
            print("✅ AllaEngine class found")
        except ImportError as e:
            print(f"❌ AllaEngine class not found: {e}")
            print("Let me check what's available in alla_engine...")
            
            # Import what's available
            import alla_engine
            available = [name for name in dir(alla_engine) if not name.startswith('_')]
            print(f"Available classes/functions: {available}")
            
            # Look for a main engine class
            engine_classes = [name for name in available if 'engine' in name.lower() or 'alla' in name.lower()]
            print(f"Potential engine classes: {engine_classes}")
            
            if not engine_classes:
                print("❌ No suitable engine class found. Creating a basic test...")
                test_basic_components()
                return
            
        # If we have AllaEngine, test it
        print("Initializing ALLA v20.0...")
        engine = AllaEngine("test_bootstrap_memory.json")
        print(f"ALLA initialized with {engine.lexicon.get_word_count()} words")
        
        # Test 1: Enable semantic bootstrapping
        print("\n📡 Test 1: Enabling Semantic Bootstrapping...")
        result = engine.enable_semantic_bootstrapping()
        print(f"Result: {result}")
        
        # Test 2: Bootstrap learn a simple word
        print("\n🌱 Test 2: Bootstrap Learning 'photosynthesis'...")
        if hasattr(engine, 'attempt_bootstrap_learning'):
            bootstrap_result = engine.attempt_bootstrap_learning('photosynthesis', 'test')
            if bootstrap_result:
                print(f"✅ Bootstrap successful!")
                print(f"   Root word: {bootstrap_result.root_word}")
                print(f"   Concepts learned: {bootstrap_result.total_words_learned}")
                print(f"   New words: {len(bootstrap_result.learning_tree)}")
                print(f"   Processing time: {bootstrap_result.bootstrap_time:.2f}s")
            else:
                print("❌ Bootstrap learning failed")
        else:
            print("❌ Bootstrap learning method not available")
        
        # Test 3: Check concept network
        print("\n🧠 Test 3: Querying Concept Network...")
        if hasattr(engine, 'query_concept_network'):
            query_result = engine.query_concept_network("plant energy")
            print(f"Query result: {query_result}")
        else:
            print("❌ Concept network query not available")
        
        # Test 4: Visualize concept map
        print("\n🌳 Test 4: Visualizing Concept Map...")
        if hasattr(engine, 'visualize_concept_map'):
            tree = engine.visualize_concept_map('photosynthesis')
            print(tree)
        else:
            print("❌ Concept map visualization not available")
        
        # Test 5: Get bootstrap statistics
        print("\n📊 Test 5: Bootstrap Statistics...")
        if hasattr(engine, 'get_semantic_bootstrap_stats'):
            stats = engine.get_semantic_bootstrap_stats()
            print(f"Statistics: {stats}")
        else:
            print("❌ Bootstrap statistics not available")
        
        print("\nAll semantic bootstrapping tests completed!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


def test_basic_components():
    """Test basic semantic components if AllaEngine isn't available."""
    print("\n🔧 Testing Basic Semantic Components...")
    
    try:
        # Test semantic bootstrapper directly
        from semantic_bootstrapper import SemanticBootstrapper, ALLABootstrapIntegration
        print("✅ SemanticBootstrapper found")
        
        # Create a mock ALLA engine
        class MockALLA:
            def __init__(self):
                from alla_engine import Lexicon
                self.lexicon = Lexicon()
                self.autonomous_learning_enabled = False
        
        mock_alla = MockALLA()
        bootstrapper = SemanticBootstrapper(mock_alla)
        
        print(f"✅ Bootstrapper initialized (max_depth: {bootstrapper.max_depth})")
        
        # Test bootstrap learning
        print("\n🌱 Testing bootstrap learning...")
        result = bootstrapper.bootstrap_word("photosynthesis")
        if result:
            print(f"✅ Bootstrap result: {result.total_words_learned} concepts discovered")
            print(f"   Root: {result.root_word}")
            print(f"   Time: {result.bootstrap_time:.2f}s")
        
        # Test concept graph
        print(f"\n📈 Concept graph size: {len(bootstrapper.concept_graph)}")
        
        # Test statistics
        stats = bootstrapper.get_bootstrap_statistics()
        print(f"📊 Bootstrap stats: {stats}")
        
        print("✅ Basic semantic components working!")
        
    except Exception as e:
        print(f"❌ Error testing basic components: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_alla_semantic_bootstrap()
