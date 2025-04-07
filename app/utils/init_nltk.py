"""Initialize NLTK data."""
import os
import nltk
from pathlib import Path

def init_nltk():
    """Initialize NLTK data if not already downloaded."""
    nltk_data_dir = str(Path.home() / 'nltk_data')
    
    # Create NLTK data directory if it doesn't exist
    os.makedirs(nltk_data_dir, exist_ok=True)
    
    # Check if required data exists
    punkt_dir = os.path.join(nltk_data_dir, 'tokenizers', 'punkt')
    punkt_tab_dir = os.path.join(nltk_data_dir, 'tokenizers', 'punkt_tab')
    
    # Only download if not already present
    if not os.path.exists(punkt_dir):
        nltk.download('punkt', quiet=True)
    if not os.path.exists(punkt_tab_dir):
        nltk.download('punkt_tab', quiet=True) 