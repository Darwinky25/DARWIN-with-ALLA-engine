#!/usr/bin/env python3
"""
Check which words from ALLA memory are missing from concept graph
"""

import json

def main():
    # Load ALLA memory
    with open('alla_memory.json', 'r', encoding='utf-8') as f:
        alla_memory = json.load(f)
    
    # Load concept graph
    with open('concept_graph.json', 'r', encoding='utf-8') as f:
        concept_graph = json.load(f)
    
    # Find missing words
    missing_words = []
    for word in alla_memory.keys():
        if word not in concept_graph:
            missing_words.append(word)
    
    print(f'Total words in ALLA memory: {len(alla_memory)}')
    print(f'Total concepts in graph: {len(concept_graph)}')
    print(f'Missing words ({len(missing_words)}): {missing_words[:30]}...' if len(missing_words) > 30 else f'Missing words ({len(missing_words)}): {missing_words}')
    
    if missing_words:
        print(f"\nFirst 20 missing words to build semantic networks for:")
        for i, word in enumerate(missing_words[:20]):
            word_info = alla_memory.get(word, {})
            print(f"{i+1}. {word} - {word_info.get('word_type', 'unknown')} - {word_info.get('meaning_expression', 'no meaning')}")

if __name__ == "__main__":
    main()
