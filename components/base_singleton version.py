# file: podcastfy_component.py

from langflow.custom import CustomComponent
from podcastfy.client import generate_podcast

class PodcastfyComponent(CustomComponent):
    display_name = "Podcast Generator"
    description = "Generate a podcast audio file from input text"
    
    def build(self, text: str) -> str:
        conversation_config = {
            "text_to_speech": {
                "default_tts_model": "openai",
                "output_directories": {
                    "transcripts": "./outputs/transcripts",
                    "audio": "./outputs/audio"
                },
                "openai": {
                    "default_voices": {
                        "question": "alloy",
                        "answer": "shimmer"
                    },
                    "model": "tts-1-hd"
                },
                "temp_audio_dir": "./outputs/audio/tmp/",
            },
            "conversation": {
                "model": "gpt-4.1-turbo"
            }
        }

        audio_path = generate_podcast(
            text=text,
            tts_model="openai",
            conversation_config=conversation_config,
            llm_model_name="gpt-4o-mini",
            api_key_label="OPENAI_API_KEY"
        )
        return audio_path
