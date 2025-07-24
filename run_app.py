#!/usr/bin/env python3
"""
Script to run the Portuguese Syllabifier Streamlit app
"""
import subprocess
import sys
import os

def main():
    print("🚀 Starting Portuguese Syllabifier App...")
    print("📱 Opening in your browser...")
    print("🌐 App will be available at: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the app")
    print("-" * 50)
    
    try:
        # Run the Streamlit app
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running app: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ Streamlit not found. Please install it with: pip install streamlit")
        sys.exit(1)

if __name__ == "__main__":
    main() 