import re
from typing import List


class PreprocessingUtils:
    @staticmethod
    def clean_text(text: str) -> str:
        text = re.sub(r"\s+", " ", text)
        text = text.strip()
        return text

    @staticmethod
    def chunk_text(text: str, max_length: int = 512, overlap: int = 50) -> List[str]:
        words = text.split()
        chunks = []

        for i in range(0, len(words), max_length - overlap):
            chunk = " ".join(words[i : i + max_length])
            chunks.append(chunk)

            if i + max_length >= len(words):
                break

        return chunks

    @staticmethod
    def extract_speakers(text: str) -> List[str]:
        speaker_pattern = r"^([A-Z][a-z]+(?:\s[A-Z][a-z]+)*):"
        speakers = re.findall(speaker_pattern, text, re.MULTILINE)
        return list(set(speakers))

    @staticmethod
    def split_by_speaker(text: str) -> dict:
        lines = text.split("\n")
        speaker_texts = {}

        current_speaker = None
        for line in lines:
            match = re.match(r"^([A-Z][a-z]+(?:\s[A-Z][a-z]+)*):\s*(.+)", line)
            if match:
                current_speaker = match.group(1)
                content = match.group(2)
                if current_speaker not in speaker_texts:
                    speaker_texts[current_speaker] = []
                speaker_texts[current_speaker].append(content)
            elif current_speaker and line.strip():
                speaker_texts[current_speaker].append(line.strip())

        return {speaker: " ".join(texts) for speaker, texts in speaker_texts.items()}
