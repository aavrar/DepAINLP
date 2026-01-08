import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.services.model_loader import ModelLoader


async def test_models():
    print("Testing model loading...")
    loader = ModelLoader()

    try:
        await loader.load_all_models()
        print("\nAll models loaded successfully!")

        print("\nTesting emotion analysis...")
        emotion_pipeline = loader.get_emotion_pipeline()
        test_text = "I am very happy about this project!"
        result = emotion_pipeline(test_text)
        print(f"Input: {test_text}")
        print(f"Result: {result}")

        print("\nTesting topic classification...")
        topic_pipeline = loader.get_topic_pipeline()
        result = topic_pipeline(
            "We need to discuss the new feature implementation",
            ["technical", "business", "general"],
        )
        print(f"Result: {result}")

        print("\nTesting summarization...")
        summary_pipeline = loader.get_summary_pipeline()
        long_text = (
            "In today's meeting, we discussed the new feature implementation. "
            "The team agreed that we should prioritize user authentication first. "
            "We also talked about the database schema and decided to use PostgreSQL. "
            "The frontend team will start working on the UI mockups next week."
        )
        result = summary_pipeline(long_text, max_length=50, min_length=10)
        print(f"Input length: {len(long_text.split())} words")
        print(f"Summary: {result[0]['summary_text']}")

        loader.cleanup()
        print("\nAll tests passed!")

    except Exception as e:
        print(f"\nError: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(test_models())
