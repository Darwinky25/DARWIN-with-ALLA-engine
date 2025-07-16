#!/usr/bin/env python3
"""
Test ALLA v18.0 with integrated grammar understanding
"""

from alla_engine import AllaEngine
from grammar_engine import GrammarEngine, WordUnderstanding

def test_grammar_integration():
    print("=== ALLA v18.0 Grammar Integration Test ===")
    
    # Initialize ALLA and Grammar Engine
    alla = AllaEngine()
    grammar = GrammarEngine()
    
    print(f"ALLA loaded {alla.lexicon.get_word_count()} words")
    
    # Test sentence understanding
    test_sentences = [
        "hi",
        "I am happy", 
        "you are good",
        "what is red",
        "can you help"
    ]
    
    for sentence in test_sentences:
        print(f"\n--- Analyzing: '{sentence}' ---")
        words = sentence.split()
        
        # Analyze each word
        word_analyses = []
        for word in words:
            classification = WordUnderstanding.classify_word(word)
            analysis = grammar.analyze_word_function(word, classification["class"], words)
            word_analyses.append({
                "word": word,
                "classification": classification,
                "analysis": analysis
            })
            print(f"  {word}: {classification['class'].value} ({classification['semantic_function']})")
        
        # Determine sentence type
        sentence_type = grammar.determine_sentence_type([w["classification"] for w in word_analyses])
        print(f"  Sentence type: {sentence_type.value}")
        
        # Suggest response structure
        response_structure = grammar.suggest_response_structure(sentence_type, [w["classification"] for w in word_analyses])
        print(f"  Suggested response: {response_structure['semantic_intent']}")
        print(f"  Response pattern: {response_structure['pattern']}")
        
        # Test ALLA's actual response
        try:
            feedback, result = alla.process_command(sentence)
            print(f"  ALLA's response: {feedback}")
        except Exception as e:
            print(f"  ALLA error: {e}")
    
    alla.shutdown()

if __name__ == "__main__":
    test_grammar_integration()
