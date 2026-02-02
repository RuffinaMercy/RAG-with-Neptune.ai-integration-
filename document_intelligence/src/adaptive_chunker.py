import re
from typing import List
import nltk
from nltk.tokenize import sent_tokenize
import os

# Download NLTK data if needed
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class AdaptiveChunker:
    def __init__(self):
        self.min_chunk_size = 100
        self.max_chunk_size = 1000
        self.target_chunk_size = 300
        
    def calculate_chunk_size(self, text: str, file_size: int = None, query_complexity: str = "medium") -> int:
        """Dynamically calculate chunk size based on document and query"""
        # Base on file size
        if file_size:
            if file_size < 100_000:  # Small file
                base_size = 200
            elif file_size < 1_000_000:  # Medium file
                base_size = 300
            else:  # Large file
                base_size = 150  # Smaller chunks for large files
        
        # Adjust based on text characteristics
        sentences = sent_tokenize(text[:5000])  # Analyze first 5000 chars
        avg_sentence_len = sum(len(s) for s in sentences) / max(len(sentences), 1)
        
        if avg_sentence_len > 150:  # Complex sentences
            chunk_size = base_size * 0.7
        elif avg_sentence_len < 50:  # Simple sentences
            chunk_size = base_size * 1.3
        else:
            chunk_size = base_size
        
        # Adjust for query complexity
        if query_complexity == "simple":
            chunk_size *= 1.2
        elif query_complexity == "complex":
            chunk_size *= 0.8
        
        # Apply limits
        return int(max(self.min_chunk_size, min(self.max_chunk_size, chunk_size)))
    
    def chunk_text(self, text: str, chunk_size: int = None, overlap: int = 50) -> List[str]:
        """Chunk text with semantic boundaries"""
        if not chunk_size:
            chunk_size = self.target_chunk_size
            
        # Clean text
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Split by sentences
        sentences = sent_tokenize(text)
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # If adding this sentence would exceed chunk size and current chunk is not empty
            if len(current_chunk) + len(sentence) > chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                # Start new chunk with overlap from previous chunk
                overlap_sentences = self._get_overlap_sentences(current_chunk, overlap)
                current_chunk = " ".join(overlap_sentences + [sentence])
            else:
                current_chunk += " " + sentence if current_chunk else sentence
        
        # Add the last chunk if not empty
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        print(f"[INFO] Created {len(chunks)} adaptive chunks (target size: {chunk_size})")
        return chunks
    
    def _get_overlap_sentences(self, text: str, overlap_chars: int) -> List[str]:
        """Get sentences for overlap from end of chunk"""
        sentences = sent_tokenize(text)
        overlap_text = ""
        overlap_sentences = []
        
        # Add sentences from the end until we reach overlap size
        for sentence in reversed(sentences):
            if len(overlap_text) + len(sentence) <= overlap_chars:
                overlap_sentences.insert(0, sentence)
                overlap_text = sentence + " " + overlap_text
            else:
                break
        
        return overlap_sentences
    
    def analyze_query_complexity(self, query: str) -> str:
        """Analyze query complexity to adjust chunking"""
        query = query.lower()
        
        # Simple queries (factual, short)
        simple_patterns = ['what is', 'who is', 'when was', 'where is', 'phone', 'email', 'date']
        
        # Complex queries (analytical, multi-part)
        complex_patterns = ['explain', 'analyze', 'compare', 'summarize', 'how does', 'why does']
        
        words = query.split()
        
        if any(pattern in query for pattern in complex_patterns):
            return "complex"
        elif len(words) <= 4 or any(pattern in query for pattern in simple_patterns):
            return "simple"
        else:
            return "medium"