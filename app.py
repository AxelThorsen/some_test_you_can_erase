import streamlit as st
from portuguese_syllabifier_nltk import PortugueseSyllabifierNLTK

# Page configuration
st.set_page_config(
    page_title="Portuguese Syllabifier",
    page_icon="🇵🇹",
    layout="centered"
)

# Initialize the syllabifier
@st.cache_resource
def get_syllabifier():
    return PortugueseSyllabifierNLTK()

def main():
    st.title("🇵🇹 Portuguese Syllabifier")
    st.markdown("*Separate Portuguese words into syllables*")
    st.markdown("---")
    
    # Initialize syllabifier
    syllabifier = get_syllabifier()
    
    # Input section
    st.subheader("Enter a Portuguese word:")
    
    # Text input with automatic processing on Enter
    word = st.text_input(
        "Word:",
        placeholder="e.g., coração, administração, água...",
        label_visibility="collapsed",
        key="word_input"
    )
    
    # Process automatically when word is entered
    if word.strip():
        try:
            # Get syllables
            syllables = syllabifier.syllabify(word.strip())
            
            # Display results
            st.markdown("---")
            st.subheader("📝 Results:")
            
            # Create a nice result display
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("**Original:**")
            with col2:
                st.markdown(f"`{word}`")
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("**Syllables:**")
            with col2:
                syllabified = "-".join(syllables)
                st.markdown(f"**`{syllabified}`**")
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("**Count:**")
            with col2:
                st.markdown(f"**{len(syllables)} syllables**")
            
            # Individual syllables in a nice format
            st.markdown("**Individual syllables:**")
            syllable_display = "  ".join([f"`{syl}`" for syl in syllables])
            st.markdown(syllable_display)
            
        except Exception as e:
            st.error(f"Error processing word: {str(e)}")
    
    # Simple footer
    st.markdown("---")
    st.markdown("*Portuguese (European) syllabification based on phonological rules*")

if __name__ == "__main__":
    main() 