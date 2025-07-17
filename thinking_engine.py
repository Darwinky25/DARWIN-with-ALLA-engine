#!/usr/bin/env python3
"""
🧠 ALLA THINKING ENGINE
======================
Transforms ALLA from data storage → cognitive reasoning agent
Implements structured thinking patterns and exploratory reasoning
"""

import json
import re
from typing import Dict, List, Set, Tuple, Optional, Any

class ConceptReasoner:
    """Handles concept-level reasoning: opposites, similarities, categories"""
    
    def __init__(self, alla_memory: Dict, concept_graph: Dict, concept_baseline: Dict):
        self.memory = alla_memory
        self.graph = concept_graph
        self.baseline = concept_baseline
        
    def find_opposites(self, word: str) -> List[str]:
        """Find conceptual opposites using semantic reasoning"""
        # Check direct opposites in baseline
        if 'opposites' in self.baseline and word in self.baseline['opposites']:
            return [self.baseline['opposites'][word]]
        
        # Check if word has emotional valence
        valence = self.get_emotional_valence(word)
        if valence:
            return self.find_concepts_with_opposite_valence(valence)
        
        # Check for opposites in logical_relations
        if word in self.baseline.get('logical_relations', {}):
            attrs = self.baseline['logical_relations'][word]
            for attr in attrs:
                if isinstance(attr, dict) and 'opposite' in attr:
                    return [attr['opposite']]
        
        # Check for explicit opposites in emotions
        if word in self.baseline.get('emotions', {}):
            attrs = self.baseline['emotions'][word]
            for attr in attrs:
                if isinstance(attr, dict) and 'opposite' in attr:
                    return [attr['opposite']]
        
        return []
    
    def get_emotional_valence(self, word: str) -> Optional[str]:
        """Determine emotional valence: positive, negative, neutral"""
        if word in self.baseline.get('emotions', {}):
            attrs = self.baseline['emotions'][word]
            # Check for structured valence data
            for attr in attrs:
                if isinstance(attr, dict) and 'valence' in attr:
                    return attr['valence']
            # Fallback to simple attribute checking
            if 'positive' in attrs:
                return 'positive'
            elif 'negative' in attrs:
                return 'negative'
            else:
                return 'neutral'
        return None
    
    def find_concepts_with_opposite_valence(self, valence: str) -> List[str]:
        """Find emotions with opposite valence"""
        target_valence = 'negative' if valence == 'positive' else 'positive'
        result = []
        
        for emotion, attrs in self.baseline.get('emotions', {}).items():
            if target_valence in attrs:
                result.append(emotion)
        
        return result
    
    def are_conceptual_opposites(self, attrs1: List[str], attrs2: List[str]) -> bool:
        """Check if two concept attribute lists represent opposites"""
        opposite_pairs = [
            ('positive', 'negative'),
            ('big', 'small'),
            ('fast', 'slow'),
            ('hot', 'cold'),
            ('light', 'dark'),
            ('up', 'down')
        ]
        
        for pair in opposite_pairs:
            if (pair[0] in attrs1 and pair[1] in attrs2) or \
               (pair[1] in attrs1 and pair[0] in attrs2):
                return True
        return False

class AnalogicalReasoner:
    """Handles analogical reasoning: A is to B as C is to ?"""
    
    def __init__(self, alla_memory: Dict, concept_graph: Dict, concept_baseline: Dict):
        self.memory = alla_memory
        self.graph = concept_graph
        self.baseline = concept_baseline
        
    def analogize(self, A: str, B: str, C: str) -> List[str]:
        """Solve analogy: A is to B as C is to ?"""
        # Find the relationship between A and B
        relationship = self.find_relationship(A, B)
        
        if relationship:
            # Apply same relationship to C
            return self.apply_relationship(C, relationship)
        
        return []
    
    def find_relationship(self, word1: str, word2: str) -> Optional[Dict]:
        """Find semantic relationship between two words"""
        # Check animal sounds
        if self.is_animal_sound_relationship(word1, word2):
            return {'type': 'makes_sound', 'sound': word2}
        
        # Check category membership
        if self.is_category_relationship(word1, word2):
            return {'type': 'is_category', 'category': word2}
        
        # Check action relationships
        if self.is_action_relationship(word1, word2):
            return {'type': 'performs_action', 'action': word2}
        
        return None
    
    def is_animal_sound_relationship(self, animal: str, sound: str) -> bool:
        """Check if animal-sound relationship exists"""
        if animal in self.baseline.get('animals', {}):
            attrs = self.baseline['animals'][animal]
            # Check structured sound data
            for attr in attrs:
                if isinstance(attr, dict) and attr.get('sound') == sound:
                    return True
            # Fallback to hardcoded mappings
            animal_sounds = {
                'dog': 'bark', 'cat': 'meow', 'cow': 'moo', 
                'pig': 'oink', 'lion': 'roar', 'bird': 'sing',
                'horse': 'neigh', 'elephant': 'trumpet'
            }
            return animal_sounds.get(animal) == sound
        return False
    
    def is_category_relationship(self, item: str, category: str) -> bool:
        """Check if item belongs to category"""
        for cat_name, concepts in self.baseline.items():
            if item in concepts and cat_name == category:
                return True
        return False
    
    def is_action_relationship(self, subject: str, action: str) -> bool:
        """Check if subject-action relationship exists"""
        action_mappings = {
            'bird': 'fly', 'fish': 'swim', 'horse': 'gallop', 
            'dog': 'run', 'cat': 'jump', 'pig': 'oink'
        }
        return action_mappings.get(subject) == action
    
    def apply_relationship(self, word: str, relationship: Dict) -> List[str]:
        """Apply discovered relationship to new word"""
        if relationship['type'] == 'makes_sound':
            # Check structured animal data first
            if word in self.baseline.get('animals', {}):
                attrs = self.baseline['animals'][word]
                for attr in attrs:
                    if isinstance(attr, dict) and 'sound' in attr:
                        return [attr['sound']]
            
            # Fallback to hardcoded mappings
            animal_sounds = {
                'dog': 'bark', 'cat': 'meow', 'cow': 'moo', 
                'pig': 'oink', 'lion': 'roar', 'bird': 'sing',
                'horse': 'neigh', 'elephant': 'trumpet', 'monkey': 'chatter'
            }
            sound = animal_sounds.get(word)
            return [sound] if sound else []
        
        elif relationship['type'] == 'performs_action':
            # Check for action relationships
            action_mappings = {
                'bird': 'fly', 'fish': 'swim', 'horse': 'gallop', 
                'dog': 'run', 'cat': 'jump', 'monkey': 'swing'
            }
            action = action_mappings.get(word)
            return [action] if action else []
        
        elif relationship['type'] == 'is_category':
            # Find category of this word
            for cat_name, concepts in self.baseline.items():
                if word in concepts:
                    return [cat_name]
        
        return []

class CausalReasoner:
    """Handles cause-effect reasoning and logical chains"""
    
    def __init__(self, alla_memory: Dict, concept_graph: Dict, concept_baseline: Dict):
        self.memory = alla_memory
        self.graph = concept_graph
        self.baseline = concept_baseline
        
        # Define causal patterns
        self.causal_patterns = {
            'biological_drives': {
                'hungry': ['eat', 'food', 'nutrition'],
                'thirsty': ['drink', 'water', 'liquid'],
                'tired': ['sleep', 'rest', 'recharge']
            },
            'emotional_triggers': {
                'loss': ['sadness', 'grief', 'sorrow'],
                'achievement': ['happiness', 'pride', 'joy'],
                'threat': ['fear', 'anxiety', 'worry']
            },
            'social_dynamics': {
                'friend_loss': ['grief', 'sadness', 'loneliness'],
                'help_received': ['gratitude', 'happiness', 'trust'],
                'betrayal': ['anger', 'sadness', 'distrust']
            }
        }
    
    def find_causal_chain(self, cause: str) -> List[str]:
        """Find what effects follow from a cause"""
        effects = []
        
        # Check biological drives
        if cause in self.causal_patterns['biological_drives']:
            effects.extend(self.causal_patterns['biological_drives'][cause])
        
        # Check emotional triggers
        if cause in self.causal_patterns['emotional_triggers']:
            effects.extend(self.causal_patterns['emotional_triggers'][cause])
        
        # Check social dynamics
        if cause in self.causal_patterns['social_dynamics']:
            effects.extend(self.causal_patterns['social_dynamics'][cause])
        
        return effects
    
    def explain_why(self, effect: str) -> List[str]:
        """Find possible causes for an effect"""
        causes = []
        
        for pattern_type, patterns in self.causal_patterns.items():
            for cause, effect_list in patterns.items():
                if effect in effect_list:
                    causes.append(cause)
        
        return causes

class EmpathyEngine:
    """Handles emotional understanding and empathy simulation"""
    
    def __init__(self, alla_memory: Dict, concept_graph: Dict, concept_baseline: Dict):
        self.memory = alla_memory
        self.graph = concept_graph
        self.baseline = concept_baseline
        self.causal_reasoner = CausalReasoner(alla_memory, concept_graph, concept_baseline)
    
    def simulate_empathy(self, situation: str) -> Dict[str, Any]:
        """Simulate emotional response to a situation"""
        # Parse the situation
        key_concepts = self.extract_key_concepts(situation)
        
        # Identify emotional triggers
        emotional_state = self.predict_emotional_state(key_concepts)
        
        # Generate empathetic response
        response = self.generate_empathetic_response(emotional_state, key_concepts)
        
        return {
            'key_concepts': key_concepts,
            'predicted_emotion': emotional_state,
            'empathetic_response': response,
            'reasoning_chain': self.build_reasoning_chain(key_concepts, emotional_state)
        }
    
    def extract_key_concepts(self, text: str) -> List[str]:
        """Extract key concepts from text"""
        words = re.findall(r'\b\w+\b', text.lower())
        key_concepts = []
        
        # Include important emotional and relational words even if not in memory
        important_words = ['dies', 'die', 'death', 'sad', 'happy', 'friend', 'loss', 'grief']
        
        for word in words:
            if word in self.memory or self.is_in_baseline(word) or word in important_words:
                key_concepts.append(word)
        
        return key_concepts
    
    def is_in_baseline(self, word: str) -> bool:
        """Check if word exists in concept baseline"""
        for category, concepts in self.baseline.items():
            if word in concepts:
                return True
        return False
    
    def predict_emotional_state(self, concepts: List[str]) -> str:
        """Predict emotional state from key concepts"""
        emotional_indicators = {
            'negative': ['loss', 'death', 'sad', 'anger', 'fear', 'die', 'dies', 'grief'],
            'positive': ['friend', 'happy', 'joy', 'love', 'success'],
            'neutral': ['think', 'know', 'see', 'hear']
        }
        
        scores = {'positive': 0, 'negative': 0, 'neutral': 0}
        
        for concept in concepts:
            for emotion_type, indicators in emotional_indicators.items():
                if concept in indicators:
                    scores[emotion_type] += 1
        
        return max(scores.keys(), key=lambda k: scores[k])
    
    def generate_empathetic_response(self, emotional_state: str, concepts: List[str]) -> str:
        """Generate empathetic response based on emotional state"""
        if emotional_state == 'negative':
            if 'friend' in concepts and ('die' in concepts or 'dies' in concepts or 'loss' in concepts):
                return "This would cause deep sadness and grief. Losing a friend is emotionally devastating."
            elif 'sad' in concepts:
                return "This situation would create feelings of sadness and sorrow."
            else:
                return "This situation would create negative emotions."
        
        elif emotional_state == 'positive':
            return "This would create positive emotions like happiness and joy."
        
        return "This situation would have emotional impact that requires understanding."
    
    def build_reasoning_chain(self, concepts: List[str], emotion: str) -> List[str]:
        """Build logical reasoning chain"""
        chain = []
        
        if 'friend' in concepts and emotion == 'negative':
            chain.append("friend_relationship_exists")
            if 'die' in concepts or 'loss' in concepts:
                chain.append("loss_event_occurs")
                chain.append("emotional_impact_follows")
                chain.append("grief_response_generated")
        
        return chain

class ThinkingEngine:
    """Main thinking engine that orchestrates all reasoning modules"""
    
    def __init__(self, alla_memory_path: str, concept_graph_path: str, concept_baseline_path: str):
        # Load data with proper UTF-8 encoding
        with open(alla_memory_path, 'r', encoding='utf-8') as f:
            self.alla_memory = json.load(f)
        with open(concept_graph_path, 'r', encoding='utf-8') as f:
            self.concept_graph = json.load(f)
        with open(concept_baseline_path, 'r', encoding='utf-8') as f:
            self.concept_baseline = json.load(f)
        
        # Initialize reasoning modules
        self.concept_reasoner = ConceptReasoner(self.alla_memory, self.concept_graph, self.concept_baseline)
        self.analogical_reasoner = AnalogicalReasoner(self.alla_memory, self.concept_graph, self.concept_baseline)
        self.causal_reasoner = CausalReasoner(self.alla_memory, self.concept_graph, self.concept_baseline)
        self.empathy_engine = EmpathyEngine(self.alla_memory, self.concept_graph, self.concept_baseline)
    
    def think(self, question: str, question_type: str = 'auto') -> Dict[str, Any]:
        """Main thinking method - routes questions to appropriate reasoning modules"""
        
        if question_type == 'auto':
            question_type = self.detect_question_type(question)
        
        result = {
            'question': question,
            'question_type': question_type,
            'reasoning_trace': [],
            'answer': None,
            'confidence': 0.0
        }
        
        if question_type == 'opposite':
            result['answer'] = self.handle_opposite_question(question)
            result['reasoning_trace'].append("Used conceptual reasoning for opposites")
            
        elif question_type == 'analogy':
            result['answer'] = self.handle_analogy_question(question)
            result['reasoning_trace'].append("Used analogical reasoning")
            
        elif question_type == 'causal':
            result['answer'] = self.handle_causal_question(question)
            result['reasoning_trace'].append("Used causal reasoning")
            
        elif question_type == 'empathy':
            result['answer'] = self.handle_empathy_question(question)
            result['reasoning_trace'].append("Used empathy simulation")
        
        else:
            result['answer'] = "I need to learn how to answer this type of question."
            result['reasoning_trace'].append("Question type not recognized")
        
        # Calculate confidence based on answer quality
        result['confidence'] = self.calculate_confidence(result['answer'])
        
        return result
    
    def detect_question_type(self, question: str) -> str:
        """Auto-detect question type from text patterns"""
        question_lower = question.lower()
        
        if 'opposite' in question_lower:
            return 'opposite'
        elif 'is to' in question_lower and 'as' in question_lower:
            return 'analogy'
        elif 'why' in question_lower or 'because' in question_lower or 'cause' in question_lower:
            return 'causal'
        elif 'feel' in question_lower or 'emotion' in question_lower or 'sad' in question_lower:
            return 'empathy'
        else:
            return 'general'
    
    def handle_opposite_question(self, question: str) -> str:
        """Handle questions about opposites"""
        # Extract the word to find opposite of
        words = re.findall(r'\b\w+\b', question.lower())
        
        for word in words:
            if word in ['what', 'is', 'the', 'opposite', 'of']:
                continue
            
            opposites = self.concept_reasoner.find_opposites(word)
            if opposites:
                return f"The opposite of '{word}' is '{opposites[0]}'."
        
        return "I couldn't identify what word you want the opposite of."
    
    def handle_analogy_question(self, question: str) -> str:
        """Handle analogical reasoning questions"""
        # Parse "A is to B as C is to ?" pattern
        pattern = r'(\w+)\s+is\s+to\s+(\w+)\s+as\s+(\w+)\s+is\s+to'
        match = re.search(pattern, question.lower())
        
        if match:
            A, B, C = match.groups()
            answers = self.analogical_reasoner.analogize(A, B, C)
            if answers:
                return f"{A} is to {B} as {C} is to {answers[0]}."
        
        return "I couldn't parse this analogy question."
    
    def handle_causal_question(self, question: str) -> str:
        """Handle causal reasoning questions"""
        words = re.findall(r'\b\w+\b', question.lower())
        
        for word in words:
            effects = self.causal_reasoner.find_causal_chain(word)
            if effects:
                return f"When someone is {word}, it typically leads to: {', '.join(effects)}."
        
        return "I couldn't identify the causal relationship in this question."
    
    def handle_empathy_question(self, question: str) -> str:
        """Handle empathy and emotional reasoning questions"""
        empathy_result = self.empathy_engine.simulate_empathy(question)
        
        if empathy_result['empathetic_response']:
            return empathy_result['empathetic_response']
        
        return "I recognize this has emotional implications but need more context to understand the feelings involved."
    
    def calculate_confidence(self, answer: str) -> float:
        """Calculate confidence score for the answer"""
        if answer and "I couldn't" not in answer and "I need to learn" not in answer:
            return 0.8
        elif answer:
            return 0.3
        else:
            return 0.0

def test_thinking_engine():
    """Test the thinking engine with various question types"""
    
    print("🧠 TESTING ALLA'S THINKING ENGINE")
    print("=" * 50)
    
    # Initialize thinking engine
    engine = ThinkingEngine(
        'alla_memory.json',
        'concept_graph.json', 
        'concept_baseline.json'
    )
    
    # Test questions
    test_questions = [
        ("What is the opposite of happy?", "opposite"),
        ("Dog is to bark as cat is to what?", "analogy"),
        ("Why does someone feel sad when their friend dies?", "empathy"),
        ("What happens when someone is hungry?", "causal")
    ]
    
    for question, q_type in test_questions:
        print(f"\n🤔 Question: {question}")
        print(f"📝 Type: {q_type}")
        
        result = engine.think(question, q_type)
        
        print(f"🎯 Answer: {result['answer']}")
        print(f"🔍 Reasoning: {', '.join(result['reasoning_trace'])}")
        print(f"📊 Confidence: {result['confidence']:.1%}")
        print("-" * 40)

if __name__ == "__main__":
    test_thinking_engine()
