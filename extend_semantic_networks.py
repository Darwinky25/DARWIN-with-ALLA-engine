#!/usr/bin/env python3
"""
EXTENDED SEMANTIC NETWORK BUILDER
=================================

This script extends the semantic network for additional words that were 
missing in the first pass.
"""

import json
import os
from datetime import datetime

def extend_semantic_networks():
    """Add semantic networks for remaining words."""
    
    # Load current concept graph
    with open("concept_graph.json", 'r', encoding='utf-8') as f:
        concept_graph = json.load(f)
    
    print(f"Current concept graph has {len(concept_graph)} concepts")
    
    # Additional semantic relationships for missing words
    additional_relationships = {
        # Auxiliary verbs - connected to grammar, existence, possession
        "is": ["existence", "state", "identity", "being", "equality", "definition"],
        "are": ["existence", "plural_state", "identity", "being", "multiple", "group"],
        "was": ["past_existence", "previous_state", "history", "memory", "temporal"],
        "were": ["past_existence", "plural_past", "history", "group_past", "temporal"],
        "do": ["action", "performance", "execution", "activity", "verb_helper"],
        "does": ["action", "performance", "third_person", "execution", "activity"],
        "did": ["past_action", "completed", "history", "previous_activity", "temporal"],
        "have": ["possession", "ownership", "contain", "experience", "auxiliary"],
        "has": ["possession", "ownership", "third_person", "contain", "auxiliary"],
        "had": ["past_possession", "previous_ownership", "history", "temporal"],
        
        # Positive expressions - connected to evaluation, emotions
        "nice": ["pleasant", "agreeable", "positive", "good", "enjoyable", "approval"],
        "good": ["positive", "quality", "beneficial", "excellent", "satisfactory", "moral"],
        "great": ["excellent", "magnificent", "large", "important", "outstanding", "impressive"],
        "wonderful": ["amazing", "delightful", "excellent", "marvelous", "fantastic", "joy"],
        "fine": ["acceptable", "good", "satisfactory", "refined", "quality", "okay"],
        "alright": ["acceptable", "okay", "satisfactory", "agreement", "confirmation"],
        
        # Social interactions - connected to communication, relationships
        "meet": ["encounter", "introduction", "social_contact", "gathering", "appointment"],
        "talk": ["communicate", "speak", "conversation", "discussion", "dialogue", "verbal"],
        "care": ["concern", "attention", "love", "protection", "nurture", "responsibility"],
        "safe": ["secure", "protected", "danger_free", "risk_free", "sheltered", "stable"],
        "well": ["healthy", "good_condition", "properly", "satisfactorily", "adequately"],
        "farewell": ["goodbye", "departure", "leaving", "separation", "ending", "parting"],
        "welcome": ["greeting", "acceptance", "hospitality", "invitation", "reception"],
        "problem": ["difficulty", "issue", "challenge", "obstacle", "trouble", "complication"],
        "pleasure": ["enjoyment", "satisfaction", "happiness", "delight", "gratification"],
        
        # Colors - connected to visual perception, nature
        "brown": ["color", "earth", "wood", "natural", "warm_color", "organic"],
        "grey": ["color", "neutral", "clouds", "stone", "balanced", "subdued"],
        
        # Shapes - connected to geometry, form, structure
        "cube": ["shape", "square", "geometric", "six_faces", "regular", "solid"],
        "sphere": ["shape", "round", "ball", "circular", "three_dimensional", "globe"],
        "circle": ["shape", "round", "geometry", "curved", "loop", "ring"],
        "crystal": ["structure", "mineral", "geometric", "transparent", "formation", "solid"],
        "globe": ["sphere", "world", "earth", "round", "map", "planet"]
    }
    
    timestamp = datetime.now().timestamp()
    words_added = 0
    
    for word, related_concepts in additional_relationships.items():
        if word not in concept_graph:
            concept_entry = {
                "definition": f"Extended semantic concept: {word}",
                "word_type": "auxiliary" if word in ["is", "are", "was", "were", "do", "does", "did", "have", "has", "had"] else "general",
                "bootstrap_depth": 0,
                "confidence": 1.0,
                "source": "extended_semantic_builder",
                "related_concepts": related_concepts,
                "parent_concepts": [],
                "learned_timestamp": timestamp,
                "semantic_category": "extended_vocabulary"
            }
            
            concept_graph[word] = concept_entry
            words_added += 1
            print(f"✅ Added semantic network for '{word}' -> {len(related_concepts)} connections")
    
    # Save updated graph
    with open("concept_graph.json", 'w', encoding='utf-8') as f:
        json.dump(concept_graph, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 EXTENDED SEMANTIC NETWORK COMPLETE:")
    print(f"   - Words added: {words_added}")
    print(f"   - Total concepts in graph: {len(concept_graph)}")
    
    return len(concept_graph)

if __name__ == "__main__":
    print("🔗 EXTENDING SEMANTIC NETWORKS")
    print("=" * 40)
    total_concepts = extend_semantic_networks()
    print(f"\n🎯 SUCCESS! ALLA now has {total_concepts} interconnected concepts!")
