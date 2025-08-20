## POC for Langflow with Podcastfy:

1. User gives a URL / PDF / YouTube link inside a Langflow flow.
2. Langflow extracts the content → summarizes it (with an LLM) → generates a conversational transcript.
3. Pass the transcript to Podcastfy.
4. Podcastfy generates an audio file (MP3) with chosen voices.
5. Langflow returns the audio file path or a download link to the user.