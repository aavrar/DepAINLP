from app.utils.preprocessing import PreprocessingUtils


def test_clean_text():
    utils = PreprocessingUtils()
    text = "This   has   extra    spaces   "
    cleaned = utils.clean_text(text)
    assert cleaned == "This has extra spaces"


def test_chunk_text():
    utils = PreprocessingUtils()
    text = " ".join(["word"] * 600)
    chunks = utils.chunk_text(text, max_length=100, overlap=10)
    assert len(chunks) > 1
    assert all(len(chunk.split()) <= 100 for chunk in chunks)


def test_extract_speakers():
    utils = PreprocessingUtils()
    text = """John Doe: Hello everyone
Jane Smith: Hi there
John Doe: How are you?"""
    speakers = utils.extract_speakers(text)
    assert "John Doe" in speakers
    assert "Jane Smith" in speakers
    assert len(speakers) == 2


def test_split_by_speaker():
    utils = PreprocessingUtils()
    text = """John Doe: Hello everyone
Jane Smith: Hi there
John Doe: How are you?"""
    speaker_texts = utils.split_by_speaker(text)
    assert "John Doe" in speaker_texts
    assert "Jane Smith" in speaker_texts
    assert "Hello everyone" in speaker_texts["John Doe"]
    assert "Hi there" in speaker_texts["Jane Smith"]
