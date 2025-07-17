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
            "room": ["space", "enclosure", "area", "interior", "chamber", "compartment"],
            "space": ["area", "volume", "dimension", "void", "cosmos", "universe", "emptiness", "expanse", "room", "gap"]
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
    
    def expand_alla_memory_with_concepts(self):
        """Add all semantic concepts to ALLA memory as learnable words."""
        concepts_added = 0
        timestamp = datetime.now().timestamp()
        
        # Collect all unique concepts from semantic relationships
        all_concepts = set()
        for word, related_concepts in self.semantic_relationships.items():
            all_concepts.update(related_concepts)
        
        print(f"📝 Found {len(all_concepts)} unique semantic concepts to add to ALLA memory")
        
        # Add each concept to ALLA memory if not already present
        for concept in all_concepts:
            if concept not in self.alla_memory:
                # Determine word type based on concept patterns
                word_type = self._infer_word_type(concept)
                
                # Create basic meaning expression
                meaning_expression = f"semantic_concept_{concept}"
                
                # Add to ALLA memory
                self.alla_memory[concept] = {
                    "word_type": word_type,
                    "meaning_expression": meaning_expression,
                    "source": "semantic_expansion",
                    "learned_timestamp": timestamp
                }
                concepts_added += 1
                print(f"✅ Added concept '{concept}' as {word_type} to ALLA memory")
        
        print(f"\n📊 MEMORY EXPANSION COMPLETE:")
        print(f"   - Concepts added to memory: {concepts_added}")
        print(f"   - Total words in ALLA memory: {len(self.alla_memory)}")
        
        return concepts_added
    
    def _infer_word_type(self, concept: str) -> str:
        """Infer word type from concept name patterns."""
        # Action patterns
        if any(pattern in concept for pattern in ['ing', 'tion', 'ment', 'process', 'action']):
            return 'action'
        
        # Property patterns  
        if any(pattern in concept for pattern in ['_color', 'temperature', 'size', 'quality', 'state']):
            return 'property'
        
        # Social/emotion patterns
        if any(pattern in concept for pattern in ['emotion', 'social', 'feeling', 'interaction']):
            return 'social'
        
        # Spatial/relation patterns
        if any(pattern in concept for pattern in ['position', 'location', 'spatial', 'relation']):
            return 'relation'
        
        # Temporal patterns
        if any(pattern in concept for pattern in ['time', 'temporal', 'sequence', 'chronology']):
            return 'temporal'
        
        # Logical patterns
        if any(pattern in concept for pattern in ['logic', 'reasoning', 'operation']):
            return 'operator'
        
        # Default to noun for most concepts
        return 'noun'
    
    def save_expanded_memory(self):
        """Save the expanded ALLA memory with new concepts."""
        try:
            with open(self.alla_memory_path, 'w', encoding='utf-8') as f:
                json.dump(self.alla_memory, f, indent=4, ensure_ascii=False)
            print(f"✅ Expanded ALLA memory saved to {self.alla_memory_path}")
            return True
        except Exception as e:
            print(f"❌ Error saving ALLA memory: {e}")
            return False

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

    def recursive_semantic_expansion(self, target_words=1000000):
        """Recursively expand ALLA vocabulary by generating new semantic concepts."""
        print(f"🚀 STARTING RECURSIVE SEMANTIC EXPANSION")
        print(f"Target: {target_words:,} words")
        print("=" * 60)
        
        iteration = 0
        while len(self.alla_memory) < target_words:
            iteration += 1
            initial_word_count = len(self.alla_memory)
            
            print(f"\n🔄 ITERATION {iteration}")
            print(f"Current vocabulary: {initial_word_count:,} words")
            print(f"Remaining to target: {target_words - initial_word_count:,} words")
            
            # Generate new concepts from existing words
            new_concepts = self._generate_derivative_concepts()
            
            if not new_concepts:
                print("⚠️  No new concepts generated. Creating synthetic concepts...")
                new_concepts = self._generate_synthetic_concepts(1000)
            
            # Add new concepts to memory
            concepts_added = self._add_concepts_to_memory(new_concepts)
            
            # Build semantic networks for new concepts
            self._build_networks_for_new_concepts(new_concepts)
            
            # Save progress every 10,000 words
            if len(self.alla_memory) % 10000 < concepts_added:
                self.save_expanded_memory()
                self.save_updated_graph()
                print(f"💾 Progress saved at {len(self.alla_memory):,} words")
            
            # Break if no progress
            if concepts_added == 0:
                print("⚠️  No new concepts added. Stopping expansion.")
                break
                
            print(f"✅ Added {concepts_added:,} new concepts")
            print(f"📊 Total vocabulary: {len(self.alla_memory):,} words")
            
            # Progress update every 50,000 words
            if len(self.alla_memory) % 50000 < concepts_added:
                progress = (len(self.alla_memory) / target_words) * 100
                print(f"🎯 Progress: {progress:.1f}% ({len(self.alla_memory):,}/{target_words:,})")
        
        print(f"\n🎉 EXPANSION COMPLETE!")
        print(f"Final vocabulary: {len(self.alla_memory):,} words")
        return len(self.alla_memory)

    def _generate_derivative_concepts(self):
        """Generate new concepts by combining and deriving from existing ones."""
        new_concepts = set()
        
        # Get existing concepts
        existing_concepts = set()
        for word, data in self.concept_graph.items():
            if 'related_concepts' in data:
                existing_concepts.update(data['related_concepts'])
        
        # Generate compound concepts
        concept_list = list(existing_concepts)
        for i, concept1 in enumerate(concept_list[:500]):  # Limit to prevent explosion
            for concept2 in concept_list[i+1:i+11]:  # Max 10 combinations per concept
                # Create compound concepts
                compounds = [
                    f"{concept1}_{concept2}",
                    f"{concept2}_{concept1}",
                    f"meta_{concept1}",
                    f"anti_{concept1}",
                    f"pseudo_{concept1}",
                    f"quasi_{concept1}",
                    f"super_{concept1}",
                    f"hyper_{concept1}",
                    f"ultra_{concept1}",
                    f"micro_{concept1}",
                    f"macro_{concept1}",
                    f"neo_{concept1}",
                    f"proto_{concept1}",
                    f"pre_{concept1}",
                    f"post_{concept1}",
                    f"trans_{concept1}",
                    f"inter_{concept1}",
                    f"intra_{concept1}",
                    f"extra_{concept1}",
                    f"multi_{concept1}",
                    f"sub_{concept1}",
                    f"over_{concept1}",
                    f"under_{concept1}",
                    f"counter_{concept1}",
                    f"re_{concept1}",
                    f"un_{concept1}",
                    f"non_{concept1}",
                    f"de_{concept1}",
                    f"co_{concept1}",
                    f"bi_{concept1}"
                ]
                
                for compound in compounds:
                    if compound not in self.alla_memory and len(compound) < 50:
                        new_concepts.add(compound)
                        if len(new_concepts) >= 5000:  # Limit per iteration
                            return list(new_concepts)
        
        return list(new_concepts)

    def _generate_synthetic_concepts(self, count=1000):
        """Generate synthetic concepts when derivative generation is exhausted."""
        synthetic_concepts = []
        
        # Base semantic domains
        domains = [
            "cognitive", "emotional", "physical", "temporal", "spatial", "logical",
            "social", "cultural", "linguistic", "mathematical", "scientific",
            "artistic", "musical", "architectural", "mechanical", "digital",
            "biological", "chemical", "astronomical", "geological", "meteorological",
            "philosophical", "psychological", "sociological", "anthropological"
        ]
        
        # Concept types
        types = [
            "pattern", "system", "process", "structure", "function", "relationship",
            "property", "attribute", "characteristic", "quality", "state", "condition",
            "phenomenon", "event", "action", "reaction", "interaction", "interface",
            "mechanism", "algorithm", "protocol", "framework", "model", "theory"
        ]
        
        # Modifiers
        modifiers = [
            "dynamic", "static", "complex", "simple", "abstract", "concrete",
            "linear", "nonlinear", "recursive", "iterative", "parallel", "sequential",
            "synchronized", "asynchronous", "distributed", "centralized", "hierarchical",
            "networked", "modular", "integrated", "adaptive", "responsive", "emergent"
        ]
        
        for i in range(count):
            # Generate random combinations
            import random
            domain = random.choice(domains)
            concept_type = random.choice(types)
            modifier = random.choice(modifiers)
            
            # Create different concept patterns
            patterns = [
                f"{modifier}_{domain}_{concept_type}",
                f"{domain}_{modifier}_{concept_type}",
                f"{concept_type}_{modifier}_{domain}",
                f"meta_{domain}_{concept_type}",
                f"proto_{modifier}_{concept_type}",
                f"hyper_{domain}_{modifier}",
                f"quantum_{domain}_{concept_type}",
                f"neural_{modifier}_{concept_type}",
                f"fractal_{domain}_{modifier}",
                f"holistic_{concept_type}_{domain}"
            ]
            
            concept = random.choice(patterns)
            if concept not in self.alla_memory:
                synthetic_concepts.append(concept)
        
        return synthetic_concepts[:count]

    def _add_concepts_to_memory(self, concepts):
        """Add new concepts to ALLA memory."""
        timestamp = datetime.now().timestamp()
        concepts_added = 0
        
        for concept in concepts:
            if concept not in self.alla_memory:
                word_type = self._infer_word_type(concept)
                
                self.alla_memory[concept] = {
                    "word_type": word_type,
                    "meaning_expression": f"generated_concept_{concept}",
                    "source": "recursive_expansion",
                    "learned_timestamp": timestamp,
                    "generation_method": "derivative" if "_" in concept else "synthetic"
                }
                concepts_added += 1
        
        return concepts_added

    def _build_networks_for_new_concepts(self, new_concepts):
        """Build semantic networks for newly added concepts."""
        timestamp = datetime.now().timestamp()
        
        for concept in new_concepts[:1000]:  # Limit network building for performance
            if concept in self.alla_memory and concept not in self.concept_graph:
                # Generate related concepts based on word structure
                related_concepts = self._generate_related_concepts(concept)
                
                concept_entry = {
                    "definition": f"Generated semantic concept: {concept}",
                    "word_type": self.alla_memory[concept]["word_type"],
                    "bootstrap_depth": 1,
                    "confidence": 0.8,
                    "source": "recursive_expansion",
                    "related_concepts": related_concepts,
                    "parent_concepts": self._find_parent_concepts(concept),
                    "learned_timestamp": timestamp
                }
                
                self.concept_graph[concept] = concept_entry

    def _generate_related_concepts(self, concept):
        """Generate related concepts for a given concept."""
        related = []
        
        # Split compound concepts
        if "_" in concept:
            parts = concept.split("_")
            related.extend(parts)
        
        # Add semantic neighbors based on existing graph
        for existing_concept, data in list(self.concept_graph.items())[:100]:  # Limit search
            if existing_concept != concept:
                # Check for semantic similarity (simple string matching)
                similarity_score = self._calculate_similarity(concept, existing_concept)
                if similarity_score > 0.3:
                    related.append(existing_concept)
                    if len(related) >= 10:  # Limit relations
                        break
        
        # Add some common semantic concepts
        common_concepts = ["concept", "entity", "property", "relation", "system", "process"]
        related.extend([c for c in common_concepts if c not in related])
        
        return related[:15]  # Limit to 15 relations

    def _find_parent_concepts(self, concept):
        """Find parent concepts for hierarchical relationships."""
        parents = []
        
        if "_" in concept:
            parts = concept.split("_")
            if len(parts) > 1:
                # First part is often the parent category
                parents.append(parts[0])
        
        return parents

    def _calculate_similarity(self, concept1, concept2):
        """Calculate semantic similarity between two concepts."""
        # Simple string-based similarity
        set1 = set(concept1.lower().split("_"))
        set2 = set(concept2.lower().split("_"))
        
        if not set1 or not set2:
            return 0.0
        
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0.0

    # ...existing code...
def main():
    """Main function to build semantic networks and expand to 1M words."""
    print("🔗 BUILDING SEMANTIC NETWORKS FOR ALLA VOCABULARY")
    print("🎯 TARGET: 1,000,000 WORDS")
    print("=" * 60)
    
    builder = SemanticNetworkBuilder()
    
    # Load existing data
    if not builder.load_existing_data():
        return
    
    # Define semantic relationships
    builder.define_semantic_relationships()
    
    # Initial expansion with semantic concepts
    print("\n📝 INITIAL SEMANTIC EXPANSION...")
    concepts_added = builder.expand_alla_memory_with_concepts()
    
    # Build initial semantic networks
    print("\n🧠 BUILDING INITIAL SEMANTIC NETWORKS...")
    builder.build_semantic_networks()
    
    print(f"\n🚀 STARTING RECURSIVE EXPANSION TO 1 MILLION WORDS...")
    print(f"Current vocabulary: {len(builder.alla_memory):,} words")
    
    # Recursive expansion to 1 million words
    final_word_count = builder.recursive_semantic_expansion(target_words=1000000)
    
    # Final save
    print("\n💾 SAVING FINAL RESULTS...")
    builder.save_expanded_memory()
    builder.save_updated_graph()
    
    # Generate final report
    builder.generate_summary_report()
    
    print(f"\n� EXPANSION COMPLETE!")
    print(f"Final vocabulary: {final_word_count:,} words")
    print(f"Concept networks: {len(builder.concept_graph):,} concepts")
    print("ALLA now has a massive semantic vocabulary!")

def quick_expansion_test():
    """Quick test with smaller target for testing."""
    print("🧪 QUICK EXPANSION TEST")
    print("🎯 TARGET: 10,000 WORDS")
    print("=" * 40)
    
    builder = SemanticNetworkBuilder()
    
    if not builder.load_existing_data():
        return
    
    builder.define_semantic_relationships()
    builder.expand_alla_memory_with_concepts()
    builder.build_semantic_networks()
    
    print(f"\nStarting vocabulary: {len(builder.alla_memory):,} words")
    final_count = builder.recursive_semantic_expansion(target_words=10000)
    
    builder.save_expanded_memory()
    builder.save_updated_graph()
    
    print(f"\n✅ Test complete! Final count: {final_count:,} words")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Quick test with 10K words
        quick_expansion_test()
    else:
        # Full expansion to 1M words
        main()
