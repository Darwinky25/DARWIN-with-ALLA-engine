#!/usr/bin/env python3
"""
ALLA v18.0 - English Grammar Engine
Fundamental understanding of English language structure
"""

from typing import Dict, List, Optional, Any
from enum import Enum

class WordClass(Enum):
    NOUN = "noun"
    VERB = "verb" 
    ADJECTIVE = "adjective"
    ADVERB = "adverb"
    PRONOUN = "pronoun"
    PREPOSITION = "preposition"
    CONJUNCTION = "conjunction"
    INTERJECTION = "interjection"
    DETERMINER = "determiner"
    AUXILIARY = "auxiliary"

class GrammaticalRole(Enum):
    SUBJECT = "subject"
    OBJECT = "object"
    PREDICATE = "predicate"
    MODIFIER = "modifier"
    COMPLEMENT = "complement"

class SentenceType(Enum):
    DECLARATIVE = "statement"
    INTERROGATIVE = "question"
    IMPERATIVE = "command"
    EXCLAMATORY = "exclamation"

class GrammarEngine:
    """Core English grammar understanding"""
    
    def __init__(self):
        self.word_class_rules = {
            WordClass.NOUN: {
                "can_be": [GrammaticalRole.SUBJECT, GrammaticalRole.OBJECT],
                "can_be_modified_by": [WordClass.ADJECTIVE, WordClass.DETERMINER],
                "can_modify": [],
                "requires": [],
                "semantic_function": "entity_reference"
            },
            WordClass.VERB: {
                "can_be": [GrammaticalRole.PREDICATE],
                "can_be_modified_by": [WordClass.ADVERB],
                "can_modify": [],
                "requires": [GrammaticalRole.SUBJECT],
                "semantic_function": "action_or_state"
            },
            WordClass.ADJECTIVE: {
                "can_be": [GrammaticalRole.MODIFIER, GrammaticalRole.COMPLEMENT],
                "can_be_modified_by": [WordClass.ADVERB],
                "can_modify": [WordClass.NOUN],
                "requires": [],
                "semantic_function": "property_description"
            },
            WordClass.PRONOUN: {
                "can_be": [GrammaticalRole.SUBJECT, GrammaticalRole.OBJECT],
                "can_be_modified_by": [],
                "can_modify": [],
                "requires": [],
                "semantic_function": "entity_substitution"
            },
            WordClass.INTERJECTION: {
                "can_be": [],
                "can_be_modified_by": [],
                "can_modify": [],
                "requires": [],
                "semantic_function": "emotion_expression"
            }
        }
        
        self.sentence_patterns = {
            "subject_verb": ["SUBJECT", "VERB"],
            "subject_verb_object": ["SUBJECT", "VERB", "OBJECT"],
            "subject_be_complement": ["SUBJECT", "BE", "COMPLEMENT"],
            "question_word_verb_subject": ["QUESTION_WORD", "VERB", "SUBJECT"],
            "greeting": ["INTERJECTION"],
            "command": ["VERB", "OBJECT"]
        }
    
    def analyze_word_function(self, word: str, word_class: WordClass, context: List[str]) -> Dict[str, Any]:
        """Analyze how a word functions in its context"""
        rules = self.word_class_rules.get(word_class, {})
        
        analysis = {
            "word": word,
            "class": word_class,
            "possible_roles": rules.get("can_be", []),
            "semantic_function": rules.get("semantic_function", "unknown"),
            "context_requirements": rules.get("requires", []),
            "can_modify": rules.get("can_modify", []),
            "can_be_modified_by": rules.get("can_be_modified_by", [])
        }
        
        return analysis
    
    def determine_sentence_type(self, words: List[Dict]) -> SentenceType:
        """Determine sentence type based on word structure"""
        if not words:
            return SentenceType.DECLARATIVE
            
        first_word = words[0]
        
        # Question words at start = question
        if first_word.get("class") == WordClass.PRONOUN and first_word.get("subtype") == "interrogative":
            return SentenceType.INTERROGATIVE
            
        # Interjection only = exclamation
        if len(words) == 1 and first_word.get("class") == WordClass.INTERJECTION:
            return SentenceType.EXCLAMATORY
            
        # Verb at start without subject = command
        if first_word.get("class") == WordClass.VERB:
            return SentenceType.IMPERATIVE
            
        return SentenceType.DECLARATIVE
    
    def validate_sentence_structure(self, word_sequence: List[Dict]) -> Dict[str, Any]:
        """Check if sentence structure follows English grammar rules"""
        sentence_type = self.determine_sentence_type(word_sequence)
        
        validation = {
            "is_valid": True,
            "sentence_type": sentence_type,
            "errors": [],
            "required_elements": [],
            "optional_elements": []
        }
        
        # Check for required elements based on sentence type
        if sentence_type == SentenceType.DECLARATIVE:
            has_subject = any(word.get("role") == GrammaticalRole.SUBJECT for word in word_sequence)
            has_verb = any(word.get("class") == WordClass.VERB for word in word_sequence)
            
            if not has_subject:
                validation["errors"].append("Missing subject")
                validation["is_valid"] = False
            if not has_verb:
                validation["errors"].append("Missing verb")
                validation["is_valid"] = False
        
        return validation
    
    def suggest_response_structure(self, input_type: SentenceType, input_words: List[Dict]) -> Dict[str, Any]:
        """Suggest appropriate response structure based on input"""
        if input_type == SentenceType.EXCLAMATORY:
            # Greeting -> Greeting back
            return {
                "type": SentenceType.EXCLAMATORY,
                "pattern": ["INTERJECTION"],
                "semantic_intent": "reciprocal_greeting"
            }
        
        elif input_type == SentenceType.INTERROGATIVE:
            # Question -> Answer (declarative)
            return {
                "type": SentenceType.DECLARATIVE,
                "pattern": ["SUBJECT", "VERB", "COMPLEMENT"],
                "semantic_intent": "provide_information"
            }
        
        elif input_type == SentenceType.IMPERATIVE:
            # Command -> Acknowledgment
            return {
                "type": SentenceType.DECLARATIVE,
                "pattern": ["SUBJECT", "VERB"],
                "semantic_intent": "acknowledge_action"
            }
        
        else:
            # Statement -> Related statement or question
            return {
                "type": SentenceType.DECLARATIVE,
                "pattern": ["SUBJECT", "VERB", "COMPLEMENT"],
                "semantic_intent": "continue_conversation"
            }
    
    def classify_word(self, word: str) -> Dict[str, Any]:
        """Determine word class and properties"""
        # Basic classification rules (this would be expanded)
        
        if word.lower() in ["hi", "hello", "hey", "goodbye", "bye"]:
            return {
                "class": WordClass.INTERJECTION,
                "subtype": "greeting",
                "semantic_function": "social_contact"
            }
        
        elif word.lower() in ["what", "where", "when", "who", "why", "how"]:
            return {
                "class": WordClass.PRONOUN,
                "subtype": "interrogative", 
                "semantic_function": "information_request"
            }
        
        elif word.lower() in ["i", "you", "he", "she", "it", "we", "they"]:
            return {
                "class": WordClass.PRONOUN,
                "subtype": "personal",
                "semantic_function": "entity_reference"
            }
        
        elif word.lower() in ["the", "a", "an"]:
            return {
                "class": WordClass.DETERMINER,
                "subtype": "article",
                "semantic_function": "specificity_marker"
            }
            
        elif word.lower() in ["red", "blue", "green", "big", "small", "happy", "sad"]:
            return {
                "class": WordClass.ADJECTIVE,
                "subtype": "descriptive",
                "semantic_function": "property_attribution"
            }
        
        elif word.lower() in ["go", "take", "give", "make", "see", "help"]:
            return {
                "class": WordClass.VERB,
                "subtype": "action",
                "semantic_function": "action_description"
            }
            
        # Default classification for unknown words
        return {
            "class": WordClass.NOUN,  # Default assumption
            "subtype": "unknown",
            "semantic_function": "entity_reference"
        }

if __name__ == "__main__":
    # Test the grammar engine
    grammar = GrammarEngine()
    
    # Test word understanding
    test_words = ["hi", "I", "am", "happy"]
    
    print("=== Word Analysis ===")
    for word in test_words:
        classification = grammar.classify_word(word)
        if classification:
            analysis = grammar.analyze_word_function(word, classification["class"], test_words)
            print(f"{word}: {classification}")
            print(f"  Function: {analysis['semantic_function']}")
            print(f"  Possible roles: {analysis['possible_roles']}")
        else:
            print(f"{word}: Unknown word")
        print()
