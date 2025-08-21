# Component 2: Podcast Audio Generator
from langflow.custom import Component
from langflow.io import MessageTextInput, Output
from langflow.schema import Message

class PodcastGeneratorComponent(Component):
    display_name = "Podcast Generator"
    description = "Generate a podcast audio file from transcript text"
    icon = "headphones"
    name = "PodcastGenerator"
    
    inputs = [
        MessageTextInput(
            name="transcript",
            display_name="Transcript",
            info="Conversational transcript to convert to audio"
        )
    ]
    
    outputs = [
        Output(
            display_name="Audio Path",
            name="audio_path",
            method="generate_audio"
        )
    ]
    
    def generate_audio(self) -> Message:
        try:
            from podcastfy.client import generate_podcast
            import os
            
            # Get the transcript text
            transcript_text = self.transcript
            
            # Ensure output directories exist
            os.makedirs("./outputs/transcripts", exist_ok=True)
            os.makedirs("./outputs/audio", exist_ok=True)
            os.makedirs("./outputs/audio/tmp", exist_ok=True)
            
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
                    "model": "gpt-4-turbo"
                }
            }
            
            audio_path = generate_podcast(
                text=transcript_text,
                tts_model="openai",
                conversation_config=conversation_config,
                llm_model_name="gpt-4o-mini",
                api_key_label="OPENAI_API_KEY"
            )
            
            self.status = f"Generated audio file: {audio_path}"
            return Message(text=str(audio_path))
            
        except Exception as e:
            self.status = f"Error: {str(e)}"
            return Message(text=f"Error generating podcast: {str(e)}")