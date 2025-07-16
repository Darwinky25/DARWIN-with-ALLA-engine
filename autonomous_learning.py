# ==============================================================================
# autonomous_learning.py
# ALLA Autonomous Learning System with Internet Access
# ==============================================================================

import requests
import json
import re
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from urllib.parse import quote_plus
import time

@dataclass
class LearningSource:
    """Represents a source of learning information."""
    source_type: str  # 'web_search', 'wikipedia', 'dictionary'
    url: str
    title: str
    content: str
    confidence: float = 0.8

@dataclass
class LearningResult:
    """Result of an autonomous learning attempt."""
    word: str
    definition: str
    word_type: str
    confidence: float
    sources: List[LearningSource]
    learned_successfully: bool = False

class AutonomousLearner:
    """Enables ALLA to learn new concepts independently via internet search."""
    
    def __init__(self):
        self.search_engines = {
            'duckduckgo': 'https://api.duckduckgo.com/',
            'wikipedia': 'https://en.wikipedia.org/api/rest_v1/page/summary/'
        }
        self.learning_history = []
        
    def learn_unknown_word(self, word: str, context: str = "") -> LearningResult:
        """
        Autonomously learn about an unknown word using internet resources.
        
        Args:
            word: The unknown word to learn about
            context: Context where the word appeared (helps disambiguation)
            
        Returns:
            LearningResult with definition and classification
        """
        print(f"🔍 ALLA is autonomously learning about: '{word}'")
        if context:
            print(f"   Context: {context}")
        
        sources = []
        
        # Try multiple learning strategies
        try:
            # Strategy 1: Wikipedia search (most reliable)
            wiki_source = self._search_wikipedia(word)
            if wiki_source:
                sources.append(wiki_source)
            
            # Strategy 2: DuckDuckGo instant answers
            ddg_source = self._search_duckduckgo(word)
            if ddg_source:
                sources.append(ddg_source)
            
            # Strategy 3: Basic web search for definitions
            web_sources = self._search_web_definitions(word)
            sources.extend(web_sources)
            
        except Exception as e:
            print(f"❌ Error during autonomous learning: {e}")
            return LearningResult(
                word=word,
                definition=f"Unknown concept: {word}",
                word_type="unknown",
                confidence=0.0,
                sources=[],
                learned_successfully=False
            )
        
        if not sources:
            print(f"❌ No learning sources found for '{word}'")
            return LearningResult(
                word=word,
                definition=f"Unknown concept: {word}",
                word_type="unknown",
                confidence=0.0,
                sources=[],
                learned_successfully=False
            )
        
        # Analyze sources and extract learning
        definition, word_type, confidence = self._analyze_sources(word, sources, context)
        
        result = LearningResult(
            word=word,
            definition=definition,
            word_type=word_type,
            confidence=confidence,
            sources=sources,
            learned_successfully=confidence > 0.5
        )
        
        self.learning_history.append(result)
        
        if result.learned_successfully:
            print(f"✅ ALLA learned: '{word}' = {definition} (type: {word_type}, confidence: {confidence:.2f})")
        else:
            print(f"Warning: ALLA struggled to learn '{word}' (confidence: {confidence:.2f})")
            
        return result
    
    def _search_wikipedia(self, word: str) -> Optional[LearningSource]:
        """Search Wikipedia for word definition."""
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote_plus(word)}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if 'extract' in data and data['extract']:
                    return LearningSource(
                        source_type='wikipedia',
                        url=url,
                        title=data.get('title', word),
                        content=data['extract'],
                        confidence=0.9
                    )
        except Exception as e:
            print(f"Wikipedia search failed: {e}")
        return None
    
    def _search_duckduckgo(self, word: str) -> Optional[LearningSource]:
        """Search DuckDuckGo instant answers."""
        try:
            url = f"https://api.duckduckgo.com/?q={quote_plus(word)}&format=json&no_html=1&skip_disambig=1"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check for abstract (definition)
                if data.get('Abstract'):
                    return LearningSource(
                        source_type='duckduckgo',
                        url=url,
                        title=f"DuckDuckGo: {word}",
                        content=data['Abstract'],
                        confidence=0.8
                    )
                
                # Check for definition in answer
                if data.get('Answer'):
                    return LearningSource(
                        source_type='duckduckgo',
                        url=url,
                        title=f"DuckDuckGo Answer: {word}",
                        content=data['Answer'],
                        confidence=0.7
                    )
                        
        except Exception as e:
            print(f"DuckDuckGo search failed: {e}")
        return None
    
    def _search_web_definitions(self, word: str) -> List[LearningSource]:
        """Search for definitions using basic web patterns."""
        sources = []
        
        # This is a simplified example - in a real implementation,
        # you might use Google Custom Search API or other services
        
        try:
            # Try Free Dictionary API
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    entry = data[0]
                    if 'meanings' in entry:
                        for meaning in entry['meanings']:
                            if 'definitions' in meaning:
                                for definition in meaning['definitions']:
                                    sources.append(LearningSource(
                                        source_type='dictionary',
                                        url=url,
                                        title=f"Dictionary: {word}",
                                        content=definition.get('definition', ''),
                                        confidence=0.8
                                    ))
                                    break  # Just take the first definition
                                break
                            break
                        
        except Exception as e:
            print(f"Dictionary API search failed: {e}")
        
        return sources
    
    def _analyze_sources(self, word: str, sources: List[LearningSource], context: str) -> tuple[str, str, float]:
        """
        Analyze learning sources to extract definition and classify word type.
        
        Returns:
            (definition, word_type, confidence)
        """
        if not sources:
            return f"Unknown concept: {word}", "unknown", 0.0
        
        # Combine content from all sources
        combined_content = []
        total_confidence = 0
        
        for source in sources:
            if source.content:
                combined_content.append(source.content)
                total_confidence += source.confidence
        
        if not combined_content:
            return f"Unknown concept: {word}", "unknown", 0.0
        
        # Use the first good source as primary definition
        primary_definition = combined_content[0]
        
        # Clean up the definition (remove extra whitespace, limit length)
        definition = ' '.join(primary_definition.split())
        if len(definition) > 200:
            definition = definition[:197] + "..."
        
        # Classify word type based on definition patterns
        word_type = self._classify_word_type(word, definition, context)
        
        # Calculate confidence based on source quality and content
        avg_confidence = total_confidence / len(sources)
        content_confidence = min(1.0, len(definition) / 50)  # More content = higher confidence
        final_confidence = (avg_confidence + content_confidence) / 2
        
        return definition, word_type, final_confidence
    
    def _classify_word_type(self, word: str, definition: str, context: str) -> str:
        """
        Classify the word type based on definition and context.
        
        Returns word type suitable for ALLA's lexicon.
        """
        definition_lower = definition.lower()
        word_lower = word.lower()
        context_lower = context.lower()
        
        # Social/greeting patterns
        if any(pattern in definition_lower for pattern in [
            'greeting', 'salutation', 'hello', 'goodbye', 'thank', 'please',
            'expression of', 'polite', 'courtesy'
        ]):
            return 'social'
        
        # Action/verb patterns
        if any(pattern in definition_lower for pattern in [
            'to do', 'to make', 'to create', 'to move', 'to go', 'to be',
            'action of', 'process of', 'act of', 'verb'
        ]) or word_lower.endswith('ing'):
            return 'action'
        
        # Property/adjective patterns
        if any(pattern in definition_lower for pattern in [
            'having the quality', 'characterized by', 'adjective',
            'color', 'size', 'shape', 'texture', 'quality of'
        ]):
            return 'property'
        
        # Question words
        if word_lower in ['what', 'where', 'when', 'why', 'how', 'who']:
            return 'inquiry'
        
        # Relation words
        if any(pattern in definition_lower for pattern in [
            'relationship', 'connection', 'preposition', 'between'
        ]):
            return 'relation'
        
        # Default to noun for concrete objects/concepts
        if any(pattern in definition_lower for pattern in [
            'a type of', 'a kind of', 'an object', 'a thing', 'a person',
            'refers to', 'noun'
        ]):
            return 'noun'
        
        # Default classification
        return 'noun'
    
    def generate_alla_expression(self, word: str, definition: str, word_type: str) -> str:
        """
        Generate an ALLA-compatible expression for the learned word.
        
        This converts natural language definitions into executable Python code
        that ALLA can use in its lexicon.
        """
        if word_type == 'social':
            # For social words, create recognition expressions
            if any(greeting in definition.lower() for greeting in ['hello', 'hi', 'greeting']):
                return "lambda: 'greeting_recognition'"
            elif any(farewell in definition.lower() for farewell in ['goodbye', 'bye', 'farewell']):
                return "lambda: 'farewell_recognition'"
            elif any(thanks in definition.lower() for thanks in ['thank', 'gratitude']):
                return "lambda: 'gratitude_expression'"
            else:
                return f"lambda: 'social_recognition'"
        
        elif word_type == 'property':
            # Create property checking functions
            if any(color in definition.lower() for color in ['red', 'blue', 'green', 'yellow', 'black', 'white']):
                # Extract the color from definition
                for color in ['red', 'blue', 'green', 'yellow', 'black', 'white', 'purple', 'orange']:
                    if color in definition.lower():
                        return f"lambda obj: getattr(obj, 'color', None) == '{color}'"
                return f"lambda obj: getattr(obj, 'color', None) == '{word.lower()}'"
            elif any(size in definition.lower() for size in ['big', 'large', 'small', 'tiny', 'huge']):
                return f"lambda obj: getattr(obj, 'size', 5) > 6"  # Assume big means size > 6
            else:
                return f"lambda obj: hasattr(obj, '{word.lower()}')"
        
        elif word_type == 'noun':
            # Create object type checking functions
            return f"lambda obj: getattr(obj, 'shape', None) == '{word.lower()}'"
        
        elif word_type == 'action':
            # Create action functions
            return f"lambda: print('Performing action: {word}')"
        
        elif word_type == 'inquiry':
            # Inquiry words are just markers
            return f"lambda: '{word.lower()}'"
        
        else:
            # Generic fallback
            return f"lambda: '{definition}'"


class ALLAAutonomousSystem:
    """
    Integration layer between ALLA's main engine and autonomous learning.
    """
    
    def __init__(self, alla_engine):
        self.alla = alla_engine
        self.learner = AutonomousLearner()
        self.learning_enabled = True
    
    def handle_unknown_word(self, word: str, context: str = "") -> bool:
        """
        Handle an unknown word by attempting autonomous learning.
        
        Returns True if learning was successful, False otherwise.
        """
        if not self.learning_enabled:
            return False
        
        print(f"\nALLA detected unknown word: '{word}'")
        print("🔄 Initiating autonomous learning...")
        
        # Attempt to learn the word
        result = self.learner.learn_unknown_word(word, context)
        
        if result.learned_successfully:
            # Add the learned word to ALLA's lexicon
            alla_expression = self.learner.generate_alla_expression(
                result.word, 
                result.definition, 
                result.word_type
            )
            
            try:
                # Create the meaning function from the expression
                meaning_function = eval(alla_expression)
                
                # Create WordEntry for ALLA
                from alla_engine import WordEntry
                new_entry = WordEntry(
                    word=result.word,
                    word_type=result.word_type,
                    meaning_expression=alla_expression,
                    meaning_function=meaning_function
                )
                
                # Add to ALLA's lexicon
                self.alla.lexicon.add_entry(new_entry)
                
                print(f"✅ Successfully taught ALLA: '{word}' ({result.word_type})")
                print(f"   Definition: {result.definition}")
                print(f"   ALLA Expression: {alla_expression}")
                
                return True
                
            except Exception as e:
                print(f"❌ Failed to integrate learned word into ALLA: {e}")
                return False
        else:
            print(f"❌ Autonomous learning failed for '{word}'")
            return False
    
    def enable_autonomous_learning(self):
        """Enable autonomous learning mode."""
        self.learning_enabled = True
        print("🔓 Autonomous learning ENABLED - ALLA can now learn from the internet")
    
    def disable_autonomous_learning(self):
        """Disable autonomous learning mode."""
        self.learning_enabled = False
        print("🔒 Autonomous learning DISABLED - ALLA will ask for help with unknown words")
    
    def get_learning_history(self) -> List[LearningResult]:
        """Get the history of autonomous learning attempts."""
        return self.learner.learning_history
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Get statistics about autonomous learning performance."""
        history = self.learner.learning_history
        if not history:
            return {"total_attempts": 0, "success_rate": 0.0}
        
        successful = sum(1 for result in history if result.learned_successfully)
        return {
            "total_attempts": len(history),
            "successful_learning": successful,
            "success_rate": successful / len(history),
            "recent_words": [r.word for r in history[-5:]]
        }
