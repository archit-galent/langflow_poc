# Component 1: Transcript Generator
from langflow.custom import Component
from langflow.io import MessageTextInput, Output
from langflow.schema import Message
import openai
import os

class TranscriptGeneratorComponent(Component):
    display_name = "Transcript Generator"
    description = "Generate a conversational transcript from input text"
    icon = "file-text"
    name = "TranscriptGenerator"
    
    inputs = [
        MessageTextInput(
            name="input_text",
            display_name="Input Text",
            info="Text to convert into podcast transcript"
        )
    ]
    
    outputs = [
        Output(
            display_name="Transcript",
            name="transcript",
            method="generate_transcript"
        )
    ]
    
    def generate_transcript(self) -> Message:
        try:
            # Get the input text
            text_content = self.input_text
            
            # Initialize OpenAI client
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            
            # Create a prompt for generating conversational transcript
            prompt = f"""
            Convert the following text into a natural conversational transcript between two podcast hosts discussing the topic. 
            Make it engaging, informative, and suitable for audio consumption. Format it as a dialogue with Host A and Host B.
            
            Text to convert:
            {text_content}
            
            Create a natural conversation that covers the key points in an engaging way.
            """
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.7
            )
            
            transcript = response.choices[0].message.content
            self.status = f"Generated transcript with {len(transcript)} characters"
            return Message(text=transcript)
            
        except Exception as e:
            self.status = f"Error: {str(e)}"
            return Message(text=f"Error generating transcript: {str(e)}")