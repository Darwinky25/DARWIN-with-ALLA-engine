#!/usr/bin/env python3
"""
SEMANTIC NETWORK BUILDER FOR EXISTING ALLA VOCABULARY
====================================================

This script builds semantic connections for all words that ALLA already knows
from alla_memory.json but don't have semantic networks in concept_graph.json yet.

It creates rich semantic relationships between concepts to enable true 
semantic reasoning and understanding.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Set

class SemanticNetworkBuilder:
    """Builds semantic networks for existing ALLA vocabulary."""
    
    def __init__(self):
        self.alla_memory_path = "alla_memory.json"
        self.concept_graph_path = "concept_graph.json"
        self.semantic_relationships = {}
        
    def load_existing_data(self):
        """Load existing ALLA memory and concept graph."""
        # Load ALLA memory
        try:
            with open(self.alla_memory_path, 'r', encoding='utf-8') as f:
                self.alla_memory = json.load(f)
                print(f"Loaded {len(self.alla_memory)} words from ALLA memory")
        except FileNotFoundError:
            print("ERROR: alla_memory.json not found!")
            return False
            
        # Load existing concept graph
        try:
            with open(self.concept_graph_path, 'r', encoding='utf-8') as f:
                self.concept_graph = json.load(f)
                print(f"Loaded {len(self.concept_graph)} existing concepts from graph")
        except FileNotFoundError:
            self.concept_graph = {}
            print("No existing concept graph found, creating new one")
            
        return True
    
    def define_semantic_relationships(self):
        """Define rich semantic relationships for each word category."""
        
        # SOCIAL WORDS - Connected to emotions, communication, human interaction
        social_network = {
            "hello": ["greeting", "acknowledgment", "communication", "social_interaction", "politeness", "beginning", "recognition"],
            "goodbye": ["farewell", "departure", "ending", "communication", "social_interaction", "closure", "separation"],
            "hi": ["greeting", "informal_communication", "friendly", "casual", "acknowledgment"],
            "hey": ["attention_seeking", "informal_greeting", "casual", "calling", "alerting"],
            "bye": ["farewell", "informal_departure", "casual", "ending", "separation"],
            "thanks": ["gratitude", "appreciation", "acknowledgment", "politeness", "social_courtesy", "positive_emotion"],
            "thank": ["gratitude", "appreciation", "acknowledgment", "recognition", "positive_feedback"],
            "please": ["request", "politeness", "courtesy", "asking", "social_etiquette", "respectful"],
            "sorry": ["apology", "regret", "acknowledgment_of_error", "remorse", "social_repair", "empathy"],
            "help": ["assistance", "support", "cooperation", "aid", "problem_solving", "collaboration"],
            "yes": ["affirmation", "agreement", "positive_response", "confirmation", "acceptance"],
            "no": ["negation", "disagreement", "negative_response", "refusal", "denial"],
            "okay": ["agreement", "acceptance", "confirmation", "understanding", "consent"],
            "ok": ["agreement", "acceptance", "informal_confirmation", "understanding"],
            "happy": ["joy", "positive_emotion", "contentment", "satisfaction", "well_being", "pleasure"],
            "sad": ["sorrow", "negative_emotion", "unhappiness", "melancholy", "grief", "disappointment"],
            "angry": ["rage", "frustration", "negative_emotion", "annoyance", "hostility", "irritation"],
            "excited": ["enthusiasm", "high_energy", "anticipation", "positive_emotion", "arousal", "eagerness"],
            "tired": ["fatigue", "exhaustion", "low_energy", "physical_state", "rest_needed", "weariness"],
            "hungry": ["appetite", "need_for_food", "physical_sensation", "biological_drive", "emptiness"]
        }
        
        # ACTION WORDS - Connected to movement, manipulation, creation
        action_network = {
            "go": ["movement", "locomotion", "travel", "displacement", "journey", "transportation"],
            "move": ["motion", "displacement", "change_position", "relocate", "shift", "transport"],
            "take": ["acquire", "grasp", "obtain", "pickup", "possession", "gather", "collect"],
            "get": ["acquire", "obtain", "retrieve", "fetch", "gain", "receive"],
            "give": ["transfer", "donate", "offer", "provide", "share", "hand_over", "bestow"],
            "put": ["place", "position", "locate", "set", "deposit", "arrange"],
            "place": ["position", "locate", "set", "arrange", "situate", "install"],
            "find": ["discover", "locate", "search", "identify", "uncover", "detect"],
            "look": ["observe", "watch", "examine", "gaze", "inspect", "view"],
            "see": ["perceive", "visual_perception", "observe", "notice", "witness", "detect"],
            "make": ["create", "construct", "build", "manufacture", "produce", "fabricate"],
            "create": ["generate", "produce", "construct", "form", "design", "invent"],
            "destroy": ["demolish", "break", "ruin", "eliminate", "dismantle", "obliterate"],
            "delete": ["remove", "erase", "eliminate", "cancel", "clear", "destroy"],
            "stop": ["halt", "cease", "end", "terminate", "pause", "discontinue"],
            "wait": ["pause", "delay", "stay", "remain", "hold", "standby"]
        }
        
        # PROPERTY WORDS - Connected to characteristics, appearance, qualities
        property_network = {
            "red": ["color", "warm_color", "visible_spectrum", "blood", "fire", "passion", "danger"],
            "blue": ["color", "cool_color", "sky", "water", "ocean", "calm", "sadness"],
            "green": ["color", "nature", "plants", "growth", "life", "environment", "freshness"],
            "yellow": ["color", "bright", "sun", "warmth", "happiness", "caution", "gold"],
            "big": ["size", "large", "magnitude", "dimension", "scale", "significant"],
            "small": ["size", "tiny", "compact", "little", "minimal", "insignificant"],
            "large": ["size", "big", "massive", "substantial", "expansive", "significant"],
            "tiny": ["size", "miniature", "microscopic", "small", "minimal", "compact"],
            "hot": ["temperature", "heat", "warm", "thermal_energy", "burning", "fire"],
            "cold": ["temperature", "cool", "chill", "freezing", "ice", "winter"],
            "new": ["fresh", "recent", "modern", "unused", "latest", "novel"],
            "old": ["aged", "ancient", "worn", "vintage", "experienced", "mature"]
        }
        
        # NOUN WORDS - Connected to objects, spaces, functions
        noun_network = {
            "box": ["container", "storage", "rectangular", "package", "enclosure", "object"],
            "ball": ["sphere", "round", "toy", "sports", "circular", "object"],
            "book": ["reading", "knowledge", "pages", "text", "literature", "information"],
            "table": ["furniture", "surface", "flat", "dining", "work_space", "horizontal"],
            "chair": ["furniture", "sitting", "support", "comfort", "seating", "rest"],
            "door": ["entrance", "barrier", "opening", "access", "portal", "passage"],
            "window": ["opening", "glass", "view", "light", "transparency", "aperture"],
            "wall": ["barrier", "structure", "vertical", "boundary", "separation", "protection"],
            "floor": ["surface", "ground", "horizontal", "foundation", "base", "walking"],
            "room": ["space", "enclosure", "area", "interior", "chamber", "compartment"]
        }
        
        # SPATIAL RELATIONS - Connected to position, location, geometry
        spatial_network = {
            "in": ["inside", "within", "contained", "interior", "enclosed", "internal"],
            "on": ["above", "surface", "contact", "supported", "top", "resting"],
            "under": ["below", "beneath", "lower", "covered", "hidden", "subordinate"],
            "near": ["close", "proximity", "adjacent", "nearby", "accessible", "local"],
            "far": ["distant", "remote", "separated", "inaccessible", "away", "removed"],
            "bigger_than": ["larger", "greater", "superior_size", "exceeding", "dominant"],
            "smaller_than": ["lesser", "inferior_size", "compact", "reduced", "minimal"]
        }
        
        # LOGICAL OPERATORS - Connected to reasoning, logic, computation
        logical_network = {
            "and": ["conjunction", "combination", "both", "addition", "logic", "union"],
            "or": ["disjunction", "alternative", "choice", "option", "either", "selection"],
            "not": ["negation", "opposite", "denial", "inverse", "contradiction", "absence"],
            "if": ["condition", "hypothesis", "assumption", "possibility", "logic", "causation"],
            "then": ["consequence", "result", "implication", "sequence", "logic", "conclusion"],
            "else": ["alternative", "otherwise", "different_option", "exception", "backup"]
        }
        
        # TEMPORAL CONCEPTS - Connected to time, sequence, chronology
        temporal_network = {
            "before": ["earlier", "prior", "preceding", "past", "sequence", "chronology"],
            "after": ["later", "subsequent", "following", "future", "sequence", "chronology"],
            "now": ["present", "current", "immediate", "contemporary", "this_moment"]
        }
        
        # INQUIRY WORDS - Connected to questions, investigation, knowledge
        inquiry_network = {
            "what": ["identity", "definition", "nature", "essence", "question", "inquiry"],
            "where": ["location", "position", "place", "geography", "space", "site"],
            "when": ["time", "moment", "timing", "chronology", "schedule", "occurrence"],
            "why": ["reason", "cause", "purpose", "motivation", "explanation", "justification"],
            "how": ["method", "process", "procedure", "technique", "way", "mechanism"],
            "who": ["person", "identity", "individual", "agent", "character", "actor"]
        }
        
        # PRONOUNS - Connected to reference, identity, deixis
        pronoun_network = {
            "i": ["self", "speaker", "first_person", "identity", "ego", "subject"],
            "you": ["addressee", "second_person", "other", "listener", "recipient"],
            "me": ["self_object", "first_person_object", "speaker_as_object", "target"],
            "my": ["possession", "ownership", "belonging", "first_person_possessive"],
            "your": ["other_possession", "second_person_possessive", "belonging_to_other"],
            "it": ["object", "thing", "third_person_neuter", "item", "entity"],
            "this": ["near_reference", "proximal", "current", "present", "close"],
            "that": ["far_reference", "distal", "distant", "previous", "remote"]
        }
        
        # COMPARISON RELATIONS - Connected to evaluation, judgment
        comparison_network = {
            "same": ["identical", "equal", "equivalent", "similar", "matching", "uniform"],
            "different": ["distinct", "unique", "varied", "contrasting", "dissimilar", "diverse"]
        }
        
        # IDENTITY CONCEPTS - Connected to self-awareness, recognition
        identity_network = {
            "name": ["identifier", "label", "designation", "title", "signature", "identity"],
            "alla": ["artificial_intelligence", "learning_agent", "cognitive_system", "AI", "self"]
        }
        
        # AUXILIARY VERBS - Connected to grammar, existence, action completion
        auxiliary_network = {
            "is": ["existence", "being", "state", "present_tense", "singular", "identity", "copula"],
            "are": ["existence", "being", "state", "present_tense", "plural", "identity", "copula"],
            "was": ["existence", "being", "state", "past_tense", "singular", "history", "copula"],
            "were": ["existence", "being", "state", "past_tense", "plural", "history", "copula"],
            "do": ["action", "perform", "execute", "accomplish", "auxiliary", "present_tense"],
            "does": ["action", "perform", "execute", "accomplish", "auxiliary", "third_person"],
            "did": ["action", "perform", "execute", "accomplish", "auxiliary", "past_tense"],
            "have": ["possession", "ownership", "auxiliary", "perfect_aspect", "present_tense"],
            "has": ["possession", "ownership", "auxiliary", "perfect_aspect", "third_person"],
            "had": ["possession", "ownership", "auxiliary", "perfect_aspect", "past_tense"]
        }
        
        # ADDITIONAL SOCIAL/QUALITY WORDS
        extended_social_network = {
            "nice": ["pleasant", "agreeable", "kind", "good", "positive", "attractive", "enjoyable"],
            "good": ["positive", "beneficial", "quality", "virtuous", "excellent", "favorable"],
            "great": ["excellent", "magnificent", "superior", "outstanding", "impressive", "large"],
            "wonderful": ["amazing", "marvelous", "excellent", "delightful", "extraordinary"],
            "meet": ["encounter", "gather", "introduce", "assemble", "convene", "social_interaction"],
            "talk": ["speak", "communicate", "converse", "discuss", "chat", "verbal_communication"],
            "care": ["concern", "attention", "compassion", "responsibility", "nurture", "protection"],
            "safe": ["secure", "protected", "harmless", "reliable", "danger_free", "trustworthy"],
            "well": ["healthy", "good", "properly", "satisfactorily", "thoroughly", "adequately"],
            "farewell": ["goodbye", "departure", "parting", "leave_taking", "separation", "ending"],
            "welcome": ["greeting", "reception", "hospitality", "acceptance", "invitation", "arrival"],
            "problem": ["issue", "difficulty", "challenge", "obstacle", "complication", "trouble"],
            "pleasure": ["enjoyment", "satisfaction", "delight", "happiness", "gratification", "joy"],
            "fine": ["good", "acceptable", "excellent", "thin", "delicate", "precise", "penalty"],
            "alright": ["okay", "acceptable", "satisfactory", "fine", "adequate", "approved"]
        }
        
        # ADDITIONAL COLORS
        extended_color_network = {
            "brown": ["color", "earth_tone", "wood", "soil", "natural", "warm_color", "chocolate"],
            "grey": ["color", "neutral", "ash", "storm", "intermediate", "dull", "subdued"]
        }
        
        # GEOMETRIC SHAPES
        geometry_network = {
            "cube": ["shape", "3D", "six_faces", "square_faces", "geometric", "solid", "rectangular"],
            "sphere": ["shape", "3D", "round", "ball", "geometric", "circular", "perfect_symmetry"],
            "circle": ["shape", "2D", "round", "curved", "geometric", "circumference", "radius"],
            "crystal": ["structure", "geometric", "faceted", "mineral", "transparent", "lattice"],
            "globe": ["sphere", "world", "earth", "round", "map", "planetary", "global"]
        }

        # Combine all networks
        self.semantic_relationships.update(social_network)
        self.semantic_relationships.update(action_network)
        self.semantic_relationships.update(property_network)
        self.semantic_relationships.update(noun_network)
        self.semantic_relationships.update(spatial_network)
        self.semantic_relationships.update(logical_network)
        self.semantic_relationships.update(temporal_network)
        self.semantic_relationships.update(inquiry_network)
        self.semantic_relationships.update(pronoun_network)
        self.semantic_relationships.update(comparison_network)
        self.semantic_relationships.update(identity_network)
        self.semantic_relationships.update(auxiliary_network)
        self.semantic_relationships.update(extended_social_network)
        self.semantic_relationships.update(extended_color_network)
        self.semantic_relationships.update(geometry_network)
        self.semantic_relationships.update(auxiliary_network)
        self.semantic_relationships.update(extended_social_network)
        self.semantic_relationships.update(extended_color_network)
        self.semantic_relationships.update(geometry_network)
        
        print(f"Defined semantic relationships for {len(self.semantic_relationships)} words")
    
    def build_semantic_networks(self):
        """Build semantic networks for words not yet in concept graph."""
        words_processed = 0
        words_already_exist = 0
        
        timestamp = datetime.now().timestamp()
        
        for word, word_data in self.alla_memory.items():
            # Skip if word already has semantic network
            if word in self.concept_graph:
                words_already_exist += 1
                continue
                
            # Get semantic relationships for this word
            related_concepts = self.semantic_relationships.get(word, [])
            
            if related_concepts:
                # Create concept entry
                concept_entry = {
                    "definition": f"Semantic concept: {word_data.get('meaning_expression', 'unknown')}",
                    "word_type": word_data.get('word_type', 'unknown'),
                    "bootstrap_depth": 0,
                    "confidence": 1.0,
                    "source": "semantic_network_builder",
                    "related_concepts": related_concepts,
                    "parent_concepts": [],
                    "learned_timestamp": timestamp,
                    "semantic_category": self._categorize_word(word_data.get('word_type', 'unknown'))
                }
                
                self.concept_graph[word] = concept_entry
                words_processed += 1
                print(f"✅ Built semantic network for '{word}' -> {len(related_concepts)} connections")
            else:
                print(f"⚠️  No semantic relationships defined for '{word}'")
        
        print(f"\n📊 SEMANTIC NETWORK BUILDING COMPLETE:")
        print(f"   - Words processed: {words_processed}")
        print(f"   - Words already had networks: {words_already_exist}")
        print(f"   - Total concepts in graph: {len(self.concept_graph)}")
    
    def _categorize_word(self, word_type: str) -> str:
        """Categorize words into semantic domains."""
        category_map = {
            'social': 'human_interaction',
            'action': 'activity_movement',
            'property': 'characteristics_qualities',
            'noun': 'objects_entities',
            'relation': 'spatial_logical_relations',
            'temporal': 'time_sequence',
            'inquiry': 'questions_investigation',
            'pronoun': 'reference_identity',
            'operator': 'logical_operations',
            'conditional': 'logical_operations'
        }
        return category_map.get(word_type, 'general_concepts')
    
    def save_updated_graph(self):
        """Save the updated concept graph."""
        try:
            with open(self.concept_graph_path, 'w', encoding='utf-8') as f:
                json.dump(self.concept_graph, f, indent=2, ensure_ascii=False)
            print(f"✅ Updated concept graph saved to {self.concept_graph_path}")
            return True
        except Exception as e:
            print(f"❌ Error saving concept graph: {e}")
            return False
    
    def generate_summary_report(self):
        """Generate a summary report of the semantic network."""
        categories = {}
        total_connections = 0
        
        for word, data in self.concept_graph.items():
            if data.get('source') == 'semantic_network_builder':
                category = data.get('semantic_category', 'unknown')
                if category not in categories:
                    categories[category] = []
                categories[category].append(word)
                total_connections += len(data.get('related_concepts', []))
        
        print(f"\n🧠 SEMANTIC NETWORK SUMMARY:")
        print(f"   Total semantic connections: {total_connections}")
        print(f"   Semantic categories created: {len(categories)}")
        
        for category, words in categories.items():
            print(f"   📂 {category}: {len(words)} words")
            print(f"      Examples: {', '.join(words[:5])}")
        
        return categories

def main():
    """Main function to build semantic networks."""
    print("🔗 BUILDING SEMANTIC NETWORKS FOR ALLA VOCABULARY")
    print("=" * 60)
    
    builder = SemanticNetworkBuilder()
    
    # Load existing data
    if not builder.load_existing_data():
        return
    
    # Define semantic relationships
    builder.define_semantic_relationships()
    
    # Build semantic networks
    builder.build_semantic_networks()
    
    # Save updated graph
    if builder.save_updated_graph():
        # Generate summary report
        builder.generate_summary_report()
        print("\n🎯 SEMANTIC NETWORK BUILDING SUCCESS!")
        print("ALLA now has rich semantic connections for all known words!")
    else:
        print("\n❌ Failed to save semantic networks")

if __name__ == "__main__":
    main()
