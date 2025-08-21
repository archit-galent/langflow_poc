# Component 3: File Path Handler
from langflow.custom import Component
from langflow.io import MessageTextInput, Output
from langflow.schema import Message
import os

class FilePathHandlerComponent(Component):
    display_name = "File Path Handler"
    description = "Process audio file path and provide download information"
    icon = "folder"
    name = "FilePathHandler"
    
    inputs = [
        MessageTextInput(
            name="file_message",
            display_name="File Message",
            info="Message containing file path"
        )
    ]
    
    outputs = [
        Output(
            display_name="File Info",
            name="file_info",
            method="process_file_info"
        )
    ]
    
    def process_file_info(self) -> Message:
        try:
            # Get the file path from message
            file_path_text = self.file_message
            
            # The file path might be the direct path or need extraction
            if file_path_text.startswith("Error"):
                return Message(text=file_path_text)
            
            # Use the path directly if it exists
            audio_path = file_path_text.strip()
            
            # Check if file exists
            if os.path.exists(audio_path):
                file_size = os.path.getsize(audio_path)
                file_size_mb = round(file_size / (1024 * 1024), 2)
                
                result = f"""Podcast generated successfully!
File: {audio_path}
Size: {file_size_mb} MB
Status: Ready for download

You can find your podcast file at: {audio_path}"""
                
                self.status = f"File processed: {file_size_mb} MB"
                return Message(text=result)
            else:
                self.status = "File not found"
                return Message(text=f"Error: Audio file not found at {audio_path}")
                
        except Exception as e:
            self.status = f"Error: {str(e)}"
            return Message(text=f"Error processing file path: {str(e)}")