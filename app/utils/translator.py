"""Utility module for Turkish to Kazakh translation."""
import os
import logging
from typing import Optional, Dict, Any
import nltk
import openai
from docx import Document
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from app.utils.init_nltk import init_nltk
from config import (
    DEFAULT_MODEL,
    TEMPERATURE,
    MAX_CHUNK_SIZE,
    SUPPORTED_INPUT_FORMATS,
    DEFAULT_ENCODING,
    TRANSLATION_SYSTEM_MESSAGE
)


# Initialize logging
logger = logging.getLogger(__name__)


# Initialize NLTK data
init_nltk()


def read_api_key() -> str:
    """Read API key from the api file."""
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        api_file = os.path.join(base_dir, 'api')
        if os.path.exists(api_file):
            with open(api_file, 'r', encoding='utf-8') as f:
                return f.read().strip()
    except Exception as e:
        logger.error(f"Error reading API key: {str(e)}")
        return None
    return None


class TurkishToKazakhTranslator:
    """Turkish to Kazakh translator using OpenAI API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the translator with OpenAI API key."""
        load_dotenv()
        self.api_key = api_key or read_api_key() or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key not found. Please provide an API key either through "
                "the api file or OPENAI_API_KEY environment variable."
            )
        
        openai.api_key = self.api_key
        self.max_chunk_size = MAX_CHUNK_SIZE
    
    def read_input(self, input_path: str) -> str:
        """Read input from file or text."""
        if not os.path.exists(input_path):
            return input_path  # Treat as direct text input
        
        file_ext = os.path.splitext(input_path)[1].lower()
        if file_ext not in SUPPORTED_INPUT_FORMATS:
            logger.error(f"Unsupported file format: {file_ext}")
            raise ValueError(f"Unsupported file format: {file_ext}")
            
        if file_ext == '.txt':
            with open(input_path, 'r', encoding=DEFAULT_ENCODING) as f:
                return f.read()
        elif file_ext == '.docx':
            doc = Document(input_path)
            return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        elif file_ext == '.pdf':
            text_content = []
            try:
                logger.info(f"Opening PDF file: {input_path}")
                reader = PdfReader(input_path)
                if not reader.pages:
                    logger.error("PDF file is empty or corrupted")
                    raise ValueError("PDF file is empty or corrupted")
                
                logger.info(f"PDF has {len(reader.pages)} pages")
                for i, page in enumerate(reader.pages, 1):
                    logger.info(f"Extracting text from page {i}")
                    text = page.extract_text()
                    if text.strip():
                        text_content.append(text)
                    else:
                        logger.warning(f"Page {i} appears to be empty")
                
                if not text_content:
                    logger.error("No text content found in PDF")
                    raise ValueError("No text content found in PDF")
                
                return '\n\n'.join(text_content)
            except Exception as e:
                logger.error(f"Error reading PDF file {input_path}: {str(e)}")
                raise ValueError(f"Failed to read PDF file: {str(e)}")
    
    def split_into_chunks(self, text: str) -> list[str]:
        """Split text into chunks based on MAX_CHUNK_SIZE setting."""
        sentences = nltk.sent_tokenize(text, language='turkish')
        chunks = []
        current_chunk = []
        
        for sentence in sentences:
            current_chunk.append(sentence)
            if len(current_chunk) >= self.max_chunk_size:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    def translate_chunk(self, chunk: str) -> str:
        """Translate a single chunk using OpenAI API."""
        try:
            response = openai.ChatCompletion.create(
                model=DEFAULT_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": TRANSLATION_SYSTEM_MESSAGE
                    },
                    {"role": "user", "content": chunk}
                ],
                temperature=TEMPERATURE
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error translating chunk: {str(e)}")
            raise
    
    def translate(self, input_path: str, output_path: str) -> Dict[str, Any]:
        """Main translation function."""
        # Read input
        text = self.read_input(input_path)
        
        # Split into chunks
        chunks = self.split_into_chunks(text)
        total_chunks = len(chunks)
        
        # Translate chunks
        translated_chunks = []
        progress = {"current": 0, "total": total_chunks}
        
        for i, chunk in enumerate(chunks, 1):
            translated_chunk = self.translate_chunk(chunk)
            translated_chunks.append(translated_chunk)
            progress["current"] = i
            
            # Write intermediate results
            intermediate_translation = '\n\n'.join(translated_chunks)
            with open(output_path, 'w', encoding=DEFAULT_ENCODING) as f:
                f.write(intermediate_translation)
            
            # Return progress information
            yield {
                "progress": progress,
                "translation": intermediate_translation,
                "is_complete": i == total_chunks
            }

    def get_supported_formats(self) -> list:
        """Get list of supported file formats."""
        return SUPPORTED_INPUT_FORMATS 