#!/usr/bin/env python3
"""
Simple test script to verify Portuguese syllabification
"""

from portuguese_syllabifier_nltk import PortugueseSyllabifierNLTK

def test_syllabification():
    """Test the syllabification with key Portuguese words."""
    
    syllabifier = PortugueseSyllabifierNLTK()
    
    print("🧪 TESTING PORTUGUESE SYLLABIFICATION")
    print("=" * 50)
    
    # Test "qu" words (should be fixed)
    print("\n✅ Testing 'qu' words:")
    qu_words = ['AQUARELA', 'AQUARELISTA', 'AQUARIO', 'AQUATICO', 'AQUECER']
    for word in qu_words:
        syllables = syllabifier.syllabify(word)
        print(f"  {word} → {'-'.join(syllables)}")
    
    # Test "cao" words (should be fixed)
    print("\n✅ Testing 'cao' words:")
    cao_words = ['ADMINISTRACAO', 'EDUCACAO', 'COMUNICACAO', 'APLICACAO', 'VERIFICACAO']
    for word in cao_words:
        syllables = syllabifier.syllabify(word)
        print(f"  {word} → {'-'.join(syllables)}")
    
    # Test "ção" words with proper accents
    print("\n✅ Testing 'ção' words with accents:")
    cao_accent_words = ['coração', 'Coração', 'administração', 'Administração', 'educação', 'Educação']
    for word in cao_accent_words:
        syllables = syllabifier.syllabify(word)
        print(f"  {word} → {'-'.join(syllables)}")
    
    # Test regular Portuguese words
    print("\n✅ Testing regular Portuguese words:")
    regular_words = ['CASA', 'TEMPO', 'PESSOA', 'TRABALHO', 'PORTUGAL']
    for word in regular_words:
        syllables = syllabifier.syllabify(word)
        print(f"  {word} → {'-'.join(syllables)}")
    
    # Test complex words
    print("\n✅ Testing complex words:")
    complex_words = ['ABACATEIRO', 'ABADESSA', 'ABAFAMENTO', 'ABALROAMENTO']
    for word in complex_words:
        syllables = syllabifier.syllabify(word)
        print(f"  {word} → {'-'.join(syllables)}")
    
    # Test words with other Portuguese accents
    print("\n✅ Testing words with other accents:")
    accent_words = ['café', 'Café', 'português', 'Português', 'história', 'História', 'música', 'Música']
    for word in accent_words:
        syllables = syllabifier.syllabify(word)
        print(f"  {word} → {'-'.join(syllables)}")
    
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    test_syllabification() 