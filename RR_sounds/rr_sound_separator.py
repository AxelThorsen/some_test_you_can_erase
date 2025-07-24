#!/usr/bin/env python3
"""
Portuguese RR Sound Detector
Finds and highlights syllables containing R sounds in Portuguese text for educational purposes.
"""

import re
import sys
import os
from typing import List, Dict, Tuple
from dataclasses import dataclass

# Add the parent directory to import the syllabifier
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from portuguese_syllabifier_nltk import PortugueseSyllabifierNLTK

@dataclass
class RRSyllable:
    """Represents a syllable containing an R sound."""
    word: str
    syllable: str
    syllable_start: int
    syllable_end: int
    difficulty: str
    pronunciation: str
    example: str
    pattern_type: str  # 'double_rr' or 'single_r'

class RRSoundDetector:
    """
    Detects syllables containing R sounds in Portuguese text for educational purposes.
    """
    
    def __init__(self):
        # Initialize the syllabifier
        self.syllabifier = PortugueseSyllabifierNLTK()
        
        # Define R sound patterns with difficulty levels
        self.r_patterns = {
            # Double R (most difficult)
            'rr': {
                'difficulty': 'hard',
                'pronunciation': 'Strong trilled R sound',
                'examples': ['carro', 'ferro', 'guerra', 'terra', 'correio']
            },
            # Single R (difficult)
            'r': {
                'difficulty': 'hard',
                'pronunciation': 'Trilled R sound',
                'examples': ['rato', 'rosa', 'rua', 'rio', 'rei', 'porta', 'carta']
            }
        }
    
    def tokenize_text(self, text: str) -> List[str]:
        """
        Tokenize text into words using simple string splitting.
        
        Args:
            text: Text to tokenize
            
        Returns:
            List of words
        """
        # Simple word tokenization using regex
        import re
        words = re.findall(r'\b[a-zA-ZáâãàéêèíîìóôõòúûùçÇ]+\b', text)
        return words
    
    def detect_rr_syllables(self, text: str) -> List[RRSyllable]:
        """
        Detect syllables containing R sounds in the given text.
        
        Args:
            text: Portuguese text to analyze
            
        Returns:
            List of RRSyllable objects with detected syllables
        """
        syllables_with_r = []
        words = self.tokenize_text(text)
        
        # Process each word individually
        for word in words:
            word_syllables = self._analyze_word_syllables(word, text)
            syllables_with_r.extend(word_syllables)
        
        # Sort by position in text
        syllables_with_r.sort(key=lambda x: x.syllable_start)
        return syllables_with_r
    
    def _analyze_word_syllables(self, word: str, original_text: str) -> List[RRSyllable]:
        """
        Analyze a single word's syllables for R sounds.
        
        Args:
            word: Word to analyze
            original_text: Original text for position calculation
            
        Returns:
            List of RRSyllable objects found in the word
        """
        syllables_with_r = []
        
        # Get syllables for the word
        syllables = self.syllabifier.syllabify(word)
        
        # Find the word position in the original text (case-insensitive)
        word_lower = word.lower()
        text_lower = original_text.lower()
        word_start = text_lower.find(word_lower)
        
        if word_start == -1:
            return syllables_with_r
        
        # Check if the original word contains double RR pattern
        word_has_double_rr = 'rr' in word_lower
        
        # Analyze each syllable for R sounds
        current_pos = word_start
        for syllable in syllables:
            syllable_lower = syllable.lower()
            
            # Check if this syllable contains any R sound
            if 'r' in syllable_lower:
                # Calculate syllable position in original text
                syllable_start = current_pos
                syllable_end = current_pos + len(syllable)
                
                # Verify the syllable exists in the original text at this position
                original_syllable = original_text[syllable_start:syllable_end]
                if original_syllable.lower() == syllable_lower:
                    # Determine difficulty and pattern type
                    if word_has_double_rr:
                        # This syllable is part of a word with double RR
                        pattern_info = self.r_patterns['rr']
                        pattern_type = 'double_rr'
                    else:
                        # This syllable has single R
                        pattern_info = self.r_patterns['r']
                        pattern_type = 'single_r'
                    
                    rr_syllable = RRSyllable(
                        word=word,
                        syllable=syllable,
                        syllable_start=syllable_start,
                        syllable_end=syllable_end,
                        difficulty=pattern_info['difficulty'],
                        pronunciation=pattern_info['pronunciation'],
                        example=pattern_info['examples'][0] if pattern_info['examples'] else '',
                        pattern_type=pattern_type  # Add pattern type for differentiation
                    )
                    syllables_with_r.append(rr_syllable)
            
            current_pos += len(syllable)
        
        return syllables_with_r
    
    def highlight_text(self, text: str, syllables: List[RRSyllable]) -> str:
        """
        Create highlighted text with syllables containing RR patterns marked.
        Preserves original word structure, only highlights syllables with R sounds.
        
        Args:
            text: Original text
            syllables: List of detected syllables with RR patterns
            
        Returns:
            Text with syllables containing RR patterns highlighted
        """
        if not syllables:
            return text
        
        # Sort syllables by position (reverse order to avoid index shifting)
        sorted_syllables = sorted(syllables, key=lambda x: x.syllable_start, reverse=True)
        
        highlighted_text = text
        
        for syllable in sorted_syllables:
            # Verify the syllable position is valid
            if (syllable.syllable_start >= 0 and 
                syllable.syllable_end <= len(text) and 
                syllable.syllable_start < syllable.syllable_end):
                
                # Extract the actual syllable from the original text
                original_syllable = text[syllable.syllable_start:syllable.syllable_end]
                
                # Create highlight based on pattern type
                if syllable.pattern_type == 'double_rr':
                    highlight = f"**{original_syllable}**"  # Dark red for double RR
                elif syllable.pattern_type == 'single_r':
                    highlight = f"*{original_syllable}*"    # Red for single R
                else:
                    highlight = f"`{original_syllable}`"    # Green for other patterns
                
                # Replace the syllable in the text with highlighted version
                highlighted_text = (
                    highlighted_text[:syllable.syllable_start] + 
                    highlight + 
                    highlighted_text[syllable.syllable_end:]
                )
        
        return highlighted_text
    
    def get_statistics(self, syllables: List[RRSyllable]) -> Dict:
        """
        Get statistics about detected syllables with R sounds.
        
        Args:
            syllables: List of detected syllables with R sounds
            
        Returns:
            Dictionary with statistics
        """
        stats = {
            'total_patterns': len(syllables),
            'by_difficulty': {},
            'by_pattern_type': {'double_rr': 0, 'single_r': 0},
            'unique_words': set()
        }
        
        for syllable in syllables:
            # Count by difficulty
            stats['by_difficulty'][syllable.difficulty] = stats['by_difficulty'].get(syllable.difficulty, 0) + 1
            
            # Count by pattern type
            stats['by_pattern_type'][syllable.pattern_type] += 1
            
            # Collect unique words
            stats['unique_words'].add(syllable.word.lower())
        
        stats['unique_words'] = len(stats['unique_words'])
        return stats
    
    def analyze_text(self, text: str) -> Dict:
        """
        Complete analysis of syllables containing RR patterns in text.
        
        Args:
            text: Portuguese text to analyze
            
        Returns:
            Dictionary with analysis results
        """
        syllables = self.detect_rr_syllables(text)
        highlighted = self.highlight_text(text, syllables)
        stats = self.get_statistics(syllables)
        
        return {
            'original_text': text,
            'highlighted_text': highlighted,
            'patterns': syllables,
            'statistics': stats
        }

def test_rr_detector():
    """Test the RR sound detector with sample Portuguese text."""
    detector = RRSoundDetector()
    
    # Test text with various R patterns
    test_text = """
    O carro vermelho correu pela rua estreita.
    A porta da casa estava aberta.
    O trabalho foi difícil mas gratificante.
    A guerra acabou e a paz voltou.
    O correio chegou com uma carta importante.
    """
    
    print("🇵🇹 PORTUGUESE RR SOUND DETECTOR (SYLLABLE-BASED)")
    print("=" * 50)
    print("Original text:")
    print(test_text)
    
    # Analyze the text
    analysis = detector.analyze_text(test_text)
    
    print("\n📊 ANALYSIS RESULTS:")
    print(f"Total syllables with R sounds: {analysis['statistics']['total_patterns']}")
    print(f"Unique words with R: {analysis['statistics']['unique_words']}")
    
    print("\n📈 By difficulty:")
    for difficulty, count in analysis['statistics']['by_difficulty'].items():
        print(f"  {difficulty}: {count}")
    
    print("\n✨ Highlighted text:")
    print(analysis['highlighted_text'])
    
    print("\n📝 Detected syllables with R sounds:")
    for i, syllable in enumerate(analysis['patterns'], 1):
        print(f"  {i}. '{syllable.word}' -> '{syllable.syllable}' ({syllable.difficulty})")
        print(f"     Pronunciation: {syllable.pronunciation}")
        print(f"     Example: {syllable.example}")
    
    return detector

if __name__ == "__main__":
    test_rr_detector() 