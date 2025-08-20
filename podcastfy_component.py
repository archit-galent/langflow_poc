from langflow.custom import Component
from langflow.io import StrInput, DropdownInput, BoolInput, Output
from langflow.schema import Data
from podcastfy.client import generate_podcast 

class PodcastfyGenerator(Component):
    display_name = "Podcastfy Generator"
    description = "Generate a podcast MP3 from URLs or raw text using Podcastfy."
    icon = "mic"
    name = "PodcastfyGenerator"

    inputs = [
        StrInput(name="input_text", display_name="Input Text", advanced=True),
        StrInput(name="url", display_name="Single URL", advanced=True),
        StrInput(name="urls_csv", display_name="URLs (comma-separated)", advanced=True),
        DropdownInput(
            name="tts_model",
            display_name="TTS Model",
            options=["openai", "elevenlabs", "edge"],
            value="openai",
            advanced=True,
        ),
        BoolInput(name="transcript_only", display_name="Transcript Only (no audio)", value=False, advanced=True),
    ]

    outputs = [
        Output(name="result", display_name="Result (Data)", method="build_result")
    ]

    def build_result(self, input_data: Data = None) -> Data:
        text_input = self.input_text or ""
        if input_data and "text" in input_data.data:
            text_input += "\n" + input_data.data["text"]

        urls = []
        if self.urls_csv:
            urls.extend([u.strip() for u in self.urls_csv.split(",") if u.strip()])
        if self.url:
            urls.append(self.url.strip())

        if not urls and not text_input:
            raise ValueError("Provide either a URL, Input Text, or connect transcript input.")

        path = generate_podcast(
            urls=urls or None,
            text=text_input or None,
            tts_model=self.tts_model or None,
            transcript_only=self.transcript_only or False,
        )

        return Data(data={"path": path, "kind": "audio", "text": f"Podcast saved: {path}"})

