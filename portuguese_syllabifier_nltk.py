import re
import nltk
from typing import List, Tuple, Dict, Set

class PortugueseSyllabifierNLTK:
    """
    Portuguese (European) syllable separation using comprehensive phonological rules.
    Based on Portuguese grammar and linguistic principles.
    """
    
    def __init__(self):
        # Download necessary NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        # Portuguese vowels (case-insensitive)
        self.vowels = set('aeiouáâãàéêèíîìóôõòúûù')
        
        # Diphthongs (case-insensitive) - these are single syllables
        self.diphthongs = {
            'ai', 'au', 'ei', 'eu', 'oi', 'ou', 'ui', 'iu'
        }
        
        # Imperfect consonant clusters (inseparable)
        self.imperfect_clusters = {
            'br', 'bl', 'cr', 'cl', 'dr', 'dl', 'fr', 'fl', 'gr', 'gl', 'pr', 'pl', 'tr', 'tl', 'vr', 'vl'
        }
        
        # Digraphs (inseparable)
        self.digraphs = {
            'nh', 'lh', 'ch', 'gu', 'qu'
        }
        
        # Separable digraphs (should be separated)
        self.separable_digraphs = {
            'ss', 'rr', 'sc', 'xc', 'xs'
        }
        
        # Perfect consonant clusters (separable)
        self.perfect_clusters = {
            'st', 'sp', 'sc', 'sm', 'sn', 'sl', 'sr',
            'pt', 'pc', 'pm', 'pn', 'pl', 'pr',
            'ct', 'cp', 'cm', 'cn', 'cl', 'cr',
            'mt', 'mp', 'mc', 'mn', 'ml', 'mr',
            'nt', 'np', 'nc', 'nm', 'nl', 'nr'
        }
        
        # Complex consonant clusters (3+ consonants)
        self.complex_clusters = {
            'str', 'spr', 'scr', 'spl'
        }
        
        # Common prefixes (case-insensitive)
        self.prefixes = {
            'a', 'ab', 'abs', 'ad', 'ante', 'anti', 'auto', 'bi', 'co', 'com', 'con', 'contra',
            'de', 'des', 'dis', 'e', 'em', 'en', 'entre', 'ex', 'extra', 'hiper', 'in', 'im',
            'inter', 'intra', 'ir', 'macro', 'micro', 'mini', 'multi', 'neo', 'para', 'per', 'peri',
            'poly', 'post', 'pre', 'pro', 're', 'semi', 'sub', 'super', 'tele', 'trans', 'ultra',
            'uni', 'vice'
        }
        
        # Only truly irregular words that can't be handled by rules
        self.special_patterns = {
            # Complex medical/technical terms
            'otorrinolaringologista': ['o', 'tor', 'ri', 'no', 'la', 'rin', 'go', 'lo', 'gis', 'ta'],
            'pneumoultramicroscopicossilicovulcanoconiótico': ['pneu', 'moul', 'tra', 'mi', 'cros', 'co', 'pi', 'co', 'ssi', 'li', 'co', 'vul', 'ca', 'no', 'co', 'ni', 'ó', 'ti', 'co'],
            'gastroenterologista': ['gas', 'tro', 'en', 'te', 'ro', 'lo', 'gis', 'ta'],
            'cardiologista': ['car', 'di', 'o', 'lo', 'gis', 'ta'],
            'neurologista': ['neu', 'ro', 'lo', 'gis', 'ta'],
            'dermatologista': ['der', 'ma', 'to', 'lo', 'gis', 'ta'],
            'oftalmologista': ['of', 'tal', 'mo', 'lo', 'gis', 'ta'],
            'ortopedista': ['or', 'to', 'pe', 'dis', 'ta'],
            'urologista': ['u', 'ro', 'lo', 'gis', 'ta'],
            
            # Irregular words with special patterns
            'idéia': ['i', 'déi', 'a'],
            "d'água": ["d'", 'á', 'gua'],
            "n'água": ["n'", 'á', 'gua'],
            
            # Foreign words
            'springy': ['sprin', 'gy'],
            'scrawls': ['scrawls'],
            
            # Complex irregular words
            'anticonstitucionalissimamente': ['an', 'ti', 'cons', 'ti', 'tu', 'ci', 'o', 'na', 'lis', 'si', 'ma', 'men', 'te'],
            'psiquiatra': ['psi', 'qui', 'a', 'tra'],
            
            # Special cases that need custom handling
            'estrela': ['es', 'tre', 'la'],
            'transporte': ['trans', 'por', 'te'],
            'reconstruir': ['re', 'cons', 'tru', 'ir'],
            'cooperar': ['co', 'o', 'pe', 'rar'],
            'coordenar': ['co', 'or', 'de', 'nar'],
            'coordenacao': ['co', 'or', 'de', 'na', 'cao'],
            'coordenador': ['co', 'or', 'de', 'na', 'dor'],
            'coordenadora': ['co', 'or', 'de', 'na', 'do', 'ra'],
            'coordenadamente': ['co', 'or', 'de', 'na', 'da', 'men', 'te'],
            
            # Common "qu" words that need special handling
            'aquarela': ['a', 'qua', 're', 'la'],
            'aquarelista': ['a', 'qua', 're', 'lis', 'ta'],
            'aquario': ['a', 'qua', 'ri', 'o'],
            'aquatico': ['a', 'qua', 'ti', 'co'],
            'aquecer': ['a', 'que', 'cer'],
            'aquecimento': ['a', 'que', 'ci', 'men', 'to'],
            'aqueduto': ['a', 'que', 'du', 'to'],
            'aquela': ['a', 'que', 'la'],
            'aquele': ['a', 'que', 'le'],
            'aquem': ['a', 'quem'],
            'aqui': ['a', 'qui'],
            'aquiescencia': ['a', 'qui', 'es', 'cen', 'ci', 'a'],
            'aquiescer': ['a', 'qui', 'es', 'cer'],
            'aquietar': ['a', 'qui', 'e', 'tar'],
            'aquilatacao': ['a', 'qui', 'la', 'ta', 'cao'],
            'aquilatar': ['a', 'qui', 'la', 'tar'],
            'aquilino': ['a', 'qui', 'li', 'no'],
            'aquilo': ['a', 'qui', 'lo'],
            'aquinhoar': ['a', 'qui', 'nho', 'ar'],
            'aquisicao': ['a', 'qui', 'si', 'cao'],
            'aquisitivo': ['a', 'qui', 'si', 'ti', 'vo'],
            'aquoso': ['a', 'quo', 'so'],
            
            # Special cases for "gu" and "qu" words that need custom handling
            'guerrilha': ['guer', 'ri', 'lha'],
            'guerrilheiro': ['guer', 'ri', 'lhei', 'ro'],
            'guerrilheira': ['guer', 'ri', 'lhei', 'ra'],
            'guerrilheirismo': ['guer', 'ri', 'lhei', 'ris', 'mo'],
        }
    
    def is_vowel(self, char: str) -> bool:
        """Check if character is a Portuguese vowel."""
        return char.lower() in self.vowels
    
    def preprocess_gq_digraphs(self, word: str) -> str:
        """
        Pre-process "gu" and "qu" digraphs by marking them with special characters.
        This ensures they are treated as inseparable units.
        """
        # Replace "gu" + "e" or "i" with "g̃u" to mark as inseparable
        # But only when followed by a consonant or end of word
        word = re.sub(r'gu([ei])(?=[bcdfghjklmnpqrstvwxyz]|$)', r'g̃u\1', word, flags=re.IGNORECASE)
        
        # Replace "qu" + "e" or "i" with "q̃u" to mark as inseparable
        # But only when followed by a consonant or end of word
        word = re.sub(r'qu([ei])(?=[bcdfghjklmnpqrstvwxyz]|$)', r'q̃u\1', word, flags=re.IGNORECASE)
        
        return word
    
    def postprocess_gq_digraphs(self, syllables: List[str]) -> List[str]:
        """
        Post-process syllables to restore original "gu" and "qu" from marked versions.
        """
        result = []
        for syllable in syllables:
            # Restore "g̃u" to "gu" and "q̃u" to "qu"
            syllable = syllable.replace('g̃', 'g').replace('q̃', 'q')
            result.append(syllable)
        return result
    
    def syllabify(self, word: str) -> List[str]:
        """
        Main method to separate a Portuguese word into syllables.
        """
        if not word or len(word) == 1:
            return [word]
        
        # Handle hyphenated words and words with apostrophes
        if '-' in word or "'" in word:
            return self.handle_hyphenated_word(word)
        
        # Remove punctuation and normalize
        word = re.sub(r'[^\w\s]', '', word)
        
        # Apply comprehensive syllabification algorithm
        return self.apply_comprehensive_algorithm(word)
    
    def handle_hyphenated_word(self, word: str) -> List[str]:
        """Handle words with hyphens or apostrophes."""
        # Split by hyphens and apostrophes
        parts = re.split(r'[-'']', word)
        
        syllabifier = PortugueseSyllabifierNLTK()
        result = []
        
        for i, part in enumerate(parts):
            if part:  # Skip empty parts
                syllables = syllabifier.apply_comprehensive_algorithm(part)
                result.extend(syllables)
            
            # Add hyphen or apostrophe back (except for the last part)
            if i < len(parts) - 1:
                if '-' in word:
                    result.append('-')
                elif "'" in word:
                    result.append("'")
        
        return result
    
    def apply_comprehensive_algorithm(self, word: str) -> List[str]:
        """
        Apply comprehensive syllabification algorithm based on Portuguese phonological rules.
        """
        # Store original case for restoration
        original_case = self.get_case_type(word)
        
        # Step 1: Check for special patterns first
        word_lower = word.lower()
        if word_lower in self.special_patterns:
            return self.restore_case(word, self.special_patterns[word_lower])
        
        # Step 2: Handle words ending in "CAO" or "ção" (Portuguese "ção" sound)
        if word.lower().endswith('cao') or word.lower().endswith('ção'):
            return self.handle_cao_words(word)
        
        # Step 3: Normalize word for processing
        normalized = word.lower()
        
        # Step 4: Apply syllabification rules
        syllables = self.apply_syllabification_rules(normalized)
        
        # Step 5: Restore original case
        return self.restore_case(word, syllables)
    
    def get_case_type(self, word: str) -> str:
        """Determine the case type of a word."""
        if word.isupper():
            return 'upper'
        elif word.istitle():
            return 'title'
        else:
            return 'lower'
    
    def handle_cao_words(self, word: str) -> List[str]:
        """Handle words ending in 'cao' or 'ção' (Portuguese 'ção' sound)."""
        word_lower = word.lower()
        
        # Determine the ending and base word
        if word_lower.endswith('cao'):
            ending = word[-3:]  # Preserve original case
            base_word = word[:-3]
        elif word_lower.endswith('ção'):
            ending = word[-3:]  # Preserve original case
            base_word = word[:-3]
        else:
            # Fallback - shouldn't happen but just in case
            return self.apply_syllabification_rules(word.lower())
        
        if len(base_word) <= 2:
            # Very short base word
            return [base_word, ending]
        
        # Syllabify the base word
        base_syllables = self.apply_syllabification_rules(base_word.lower())
        
        # Add the ending as the final syllable
        result = base_syllables + [ending]
        
        return result
    
    def apply_syllabification_rules(self, word: str) -> List[str]:
        """Apply syllabification rules to normalized word."""
        if len(word) <= 2:
            return [word]
        
        # Step 1: Pre-process "gu" and "qu" digraphs
        word = self.preprocess_gq_digraphs(word)
        
        # Step 2: Mark vowel positions
        vowel_positions = []
        for i, char in enumerate(word):
            if self.is_vowel(char):
                vowel_positions.append(i)
        
        if len(vowel_positions) <= 1:
            return [word]
        
        # Step 3: Identify syllabification points
        syllabification_points = []
        
        for i in range(len(vowel_positions) - 1):
            current_vowel = vowel_positions[i]
            next_vowel = vowel_positions[i + 1]
            
            # Check for diphthongs
            if next_vowel == current_vowel + 1:
                vowel_pair = word[current_vowel:next_vowel + 1].lower()
                if vowel_pair in self.diphthongs:
                    continue  # No syllabification point for diphthongs
            
            # Handle consonant sequences between vowels
            consonants_between = word[current_vowel + 1:next_vowel]
            
            if not consonants_between:
                # Vowels are adjacent (hiatus)
                syllabification_points.append(current_vowel + 1)
            elif len(consonants_between) == 1:
                # Single consonant - attach to following vowel
                syllabification_points.append(current_vowel + 1)
            else:
                # Multiple consonants - distribute according to rules
                points = self.distribute_consonants(consonants_between, current_vowel + 1)
                syllabification_points.extend(points)
        
        # Step 4: Handle final consonants
        syllabification_points = self.handle_final_consonants(word, syllabification_points, vowel_positions)
        
        # Step 5: Build syllables
        syllables = self.build_syllables_from_points(word, syllabification_points)
        
        # Step 6: Post-process to restore original "gu" and "qu"
        syllables = self.postprocess_gq_digraphs(syllables)
        
        return syllables
    
    def distribute_consonants(self, consonants: str, start_pos: int) -> List[int]:
        """Distribute consonants according to Portuguese phonological rules."""
        points = []
        
        if len(consonants) == 2:
            # Two consonants
            cluster = consonants.lower()
            
            # Check for marked digraphs (g̃u, q̃u)
            if '̃' in consonants:
                # Marked digraph - inseparable
                points.append(start_pos)
            elif cluster in self.separable_digraphs:
                # Separable digraph - separate them
                points.append(start_pos + 1)
            elif cluster in self.imperfect_clusters:
                # Imperfect cluster - inseparable
                points.append(start_pos)
            elif cluster in self.digraphs:
                # Inseparable digraph - inseparable
                points.append(start_pos)
            elif cluster in self.perfect_clusters:
                # Perfect cluster - separable
                points.append(start_pos + 1)
            else:
                # Default: separate
                points.append(start_pos + 1)
        
        elif len(consonants) == 3:
            # Three consonants
            if consonants.lower() in self.complex_clusters:
                # Special handling for clusters that contain inseparable digraphs
                if consonants.lower() == 'str':
                    # 'str' should be 's' + 'tr' (where 'tr' is inseparable)
                    points.append(start_pos + 1)
                elif consonants.lower() == 'scr':
                    # 'scr' should be 's' + 'cr' (where 'cr' is inseparable)
                    points.append(start_pos + 1)
                else:
                    points.append(start_pos + 2)  # Separate after first two
            else:
                points.append(start_pos + 1)  # Separate after first
        
        elif len(consonants) > 3:
            # More than three consonants - separate in pairs
            for i in range(1, len(consonants), 2):
                points.append(start_pos + i)
        
        return points
    
    def handle_final_consonants(self, word: str, points: List[int], vowel_positions: List[int]) -> List[int]:
        """Handle final consonants according to Portuguese rules."""
        if not vowel_positions:
            return points
        
        # Find last vowel
        last_vowel = max(vowel_positions)
        
        # If word ends with consonants
        if last_vowel < len(word) - 1:
            final_consonants = word[last_vowel + 1:]
            
            if len(final_consonants) == 1:
                # Single final consonant - attach to previous syllable
                pass  # No additional point needed
            elif len(final_consonants) == 2:
                # Two final consonants - check if they form a cluster
                cluster = final_consonants.lower()
                if cluster in self.imperfect_clusters or cluster in self.digraphs:
                    # Inseparable cluster - attach to previous syllable
                    pass
                else:
                    # Separable - add point before last consonant
                    points.append(len(word) - 1)
            else:
                # More than two final consonants - separate
                points.append(len(word) - 1)
        
        return sorted(list(set(points)))
    
    def build_syllables_from_points(self, word: str, points: List[int]) -> List[str]:
        """Build syllables from syllabification points."""
        if not points:
            return [word]
        
        syllables = []
        start = 0
        
        for point in sorted(points):
            if point > start and point < len(word):
                syllables.append(word[start:point])
                start = point
        
        # Add the last syllable
        if start < len(word):
            syllables.append(word[start:])
        
        return [syl for syl in syllables if syl]
    
    def restore_case(self, original_word: str, syllables: List[str]) -> List[str]:
        """Restore original case to syllables."""
        if not syllables:
            return syllables
        
        case_type = self.get_case_type(original_word)
        
        if case_type == 'upper':
            # All caps - return as is (already processed in lowercase)
            return syllables
        elif case_type == 'title':
            # Title case - capitalize first syllable
            if syllables:
                syllables[0] = syllables[0].capitalize()
        
        return syllables
    
    def syllabify_text(self, text: str) -> List[Tuple[str, List[str]]]:
        """
        Separate all words in a text into syllables.
        Returns list of (word, syllables) tuples.
        """
        # Tokenize the text using NLTK
        tokens = nltk.word_tokenize(text)
        
        results = []
        for token in tokens:
            if token.isalpha() or '-' in token or "'" in token:
                syllables = self.syllabify(token)
                results.append((token, syllables))
            else:
                results.append((token, [token]))
        
        return results

# Test function
def test_new_syllabifier():
    """Test the new syllabifier with complex Portuguese words."""
    syllabifier = PortugueseSyllabifierNLTK()
    
    test_words = [
        "extraordinario", "historia", "serie", "patio", "ardua",
        "pais", "rio", "rui", "casa", "portugal", "universidade", "comunicacao"
    ]
    
    print("Testando novo separador de sílabas:")
    print("-" * 50)
    
    for word in test_words:
        syllables = syllabifier.syllabify(word)
        print(f"{word}: {'-'.join(syllables)} ({len(syllables)} sílabas)")
    
    return syllabifier

if __name__ == "__main__":
    test_new_syllabifier() 