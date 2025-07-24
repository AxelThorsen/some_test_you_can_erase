import streamlit as st
import sys
import os

# Add the RR_sounds directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'RR_sounds'))
from rr_sound_separator import RRSoundDetector

# Page configuration
st.set_page_config(
    page_title="RR Sound Detector",
    page_icon="🔤",
    layout="centered"
)

# Initialize the RR detector
@st.cache_resource
def get_rr_detector():
    return RRSoundDetector()

def main():
    st.title("🔤 Portuguese RR Sound Detector")
    st.markdown("*Find and highlight difficult R sounds for children*")
    st.markdown("---")
    
    # Initialize RR detector
    detector = get_rr_detector()
    
    # Input section
    st.subheader("Enter Portuguese text:")
    
    # Simple text input that responds to Enter key
    text = st.text_area(
        "Text:",
        placeholder="Enter Portuguese text to analyze for RR patterns... (Press Enter to submit)",
        height=150,
        key="text_input"
    )
    
    # Highlighting mode toggle
    st.markdown("**🎨 Highlighting Style:**")
    highlight_mode = st.radio(
        "Choose highlighting style:",
        ["Box Highlight", "Color Only"],
        horizontal=True,
        help="Box Highlight: Syllables with colored backgrounds. Color Only: Syllables with colored text only."
    )
    
    # Process when text is entered and Enter is pressed
    if text and text.strip():
        try:
            # Analyze the text
            analysis = detector.analyze_text(text.strip())
            
            # Highlighted text (moved to appear first)
            st.markdown("---")
            st.subheader("✨ Highlighted Text:")
            if highlight_mode == "Box Highlight":
                st.markdown("*Legend: 🔴 Dark Red Box = Double RR patterns, 🔴 Red Box = Single R patterns*")
            else:
                st.markdown("*Legend: 🔴 Dark Red Text = Double RR patterns, 🔴 Red Text = Single R patterns*")
            
            # Create better highlighted text with custom colors
            highlighted_html = analysis['highlighted_text']
            
            # Replace markdown formatting with custom HTML colors using a more robust approach
            import re
            
            # First, protect double asterisks by replacing them with a temporary marker
            highlighted_html = highlighted_html.replace('**', 'DOUBLE_ASTERISK')
            
            if highlight_mode == "Box Highlight":
                # Box highlighting mode - colored backgrounds
                # First, restore double asterisks and remove separator
                highlighted_html = highlighted_html.replace('DOUBLE_ASTERISK', '**')
                highlighted_html = highlighted_html.replace('X', '')
                
                # Process double asterisks first (dark red)
                while '**' in highlighted_html:
                    # Handle the case where there might be empty content between **
                    highlighted_html = re.sub(r'\*\*([^*]+?)\*\*', r'<span style="background-color: #d32f2f; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold;">\1</span>', highlighted_html, count=1)
                
                # Then process single asterisks (light red)
                highlighted_html = re.sub(r'\*(.*?)\*', r'<span style="background-color: #ff6b6b; color: white; padding: 2px 4px; border-radius: 3px;">\1</span>', highlighted_html)
                
                # Easy patterns: Green background (replace `text` with span)
                highlighted_html = re.sub(r'`(.*?)`', r'<span style="background-color: #66bb6a; color: white; padding: 2px 4px; border-radius: 3px; font-family: monospace;">\1</span>', highlighted_html)
            else:
                # Color only mode - colored text without backgrounds
                # First, restore double asterisks and remove separator
                highlighted_html = highlighted_html.replace('DOUBLE_ASTERISK', '**')
                highlighted_html = highlighted_html.replace('X', '')
                
                # Process double asterisks first (dark red)
                while '**' in highlighted_html:
                    # Handle the case where there might be empty content between **
                    highlighted_html = re.sub(r'\*\*([^*]+?)\*\*', r'<span style="color: #d32f2f; font-weight: bold;">\1</span>', highlighted_html, count=1)
                
                # Then process single asterisks (light red)
                highlighted_html = re.sub(r'\*(.*?)\*', r'<span style="color: #ff6b6b;">\1</span>', highlighted_html)
                
                # Easy patterns: Green text (replace `text` with span)
                highlighted_html = re.sub(r'`(.*?)`', r'<span style="color: #66bb6a; font-family: monospace;">\1</span>', highlighted_html)
            
            # Display highlighted text in a nice box
            st.markdown(f"""
            <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; border: 2px solid #e0e0e0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="font-size: 18px; line-height: 1.6; color: #333;">
            {highlighted_html.replace(chr(10), '<br>')}
            </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Analysis Results (moved to appear after highlighted text)
            st.markdown("---")
            st.subheader("📊 Analysis Results:")
            
            # Statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Patterns", analysis['statistics']['total_patterns'])
            with col2:
                st.metric("Unique Words", analysis['statistics']['unique_words'])
            with col3:
                hard_count = analysis['statistics']['by_difficulty'].get('hard', 0)
                st.metric("Hard Patterns", hard_count)
            
            # Difficulty breakdown
            st.markdown("**📈 By Difficulty:**")
            difficulty_cols = st.columns(len(analysis['statistics']['by_difficulty']))
            for i, (difficulty, count) in enumerate(analysis['statistics']['by_difficulty'].items()):
                with difficulty_cols[i]:
                    if difficulty == 'hard':
                        st.metric("Hard", count, help="Double RR, R at start/end")
                    elif difficulty == 'medium':
                        st.metric("Medium", count, help="R in consonant clusters")
                    else:
                        st.metric("Easy", count, help="R between vowels")
            
            # Pattern type breakdown
            st.markdown("**🔍 R Sound Types:**")
            col1, col2 = st.columns(2)
            with col1:
                # Safe access to pattern type statistics
                by_pattern_type = analysis['statistics'].get('by_pattern_type', {})
                single_r_count = by_pattern_type.get('single_r', 0)
                st.metric("Single R", single_r_count, help="Syllables with single R sound")
            with col2:
                double_rr_count = by_pattern_type.get('double_rr', 0)
                st.metric("Double RR", double_rr_count, help="Syllables from words with double RR pattern")
            
            # Detailed pattern list
            if analysis['patterns']:
                st.markdown("---")
                st.subheader("📝 Detected Patterns:")
                
                for i, syllable in enumerate(analysis['patterns'], 1):
                    # Safe access to pattern_type with fallback
                    pattern_type = getattr(syllable, 'pattern_type', 'single_r')
                    pattern_type_display = "Double RR" if pattern_type == 'double_rr' else "Single R"
                    with st.expander(f"{i}. '{syllable.word}' -> '{syllable.syllable}' ({pattern_type_display})"):
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.markdown("**Word:**")
                            st.markdown("**Syllable:**")
                            st.markdown("**Pattern Type:**")
                            st.markdown("**Difficulty:**")
                            st.markdown("**Pronunciation:**")
                            st.markdown("**Example:**")
                        with col2:
                            st.markdown(syllable.word)
                            st.markdown(syllable.syllable)
                            st.markdown(pattern_type_display)
                            st.markdown(syllable.difficulty)
                            st.markdown(syllable.pronunciation)
                            st.markdown(syllable.example)
            
        except Exception as e:
            st.error(f"Error processing text: {str(e)}")
    
    # Educational info
    st.markdown("---")
    st.markdown("**🎓 Educational Information:**")
    st.markdown("""
    This tool helps identify syllables containing R sounds that are challenging for Portuguese children:
    
    - **Hard patterns** (All R sounds): Difficult to pronounce for children
    - **Double RR** (carro, ferro, guerra): Most challenging R sound
    - **Single R** (rato, porta, carta): Also challenging but easier than double R
    
    Perfect for teachers and speech therapists working with Portuguese children! 🇵🇹
    """)

if __name__ == "__main__":
    main() 