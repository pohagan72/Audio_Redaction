import os
import streamlit as st
import stable_whisper
from pydub import AudioSegment
from pydub.generators import Sine
import re
from datetime import datetime

# Load the Whisper model for transcription
model = stable_whisper.load_model('base')


def timestamp_to_milliseconds(timestamp):
    """
    Convert a timestamp in 'HH:MM:SS,mmm' format to milliseconds.

    Args:
        timestamp (str): Timestamp string (e.g., '00:01:23,456').

    Returns:
        int: Time in milliseconds.
    """
    # Parse the timestamp string into a datetime object
    time_obj = datetime.strptime(timestamp, '%H:%M:%S,%f')
    
    # Calculate total milliseconds
    return (
        time_obj.hour * 3600000 +      # Hours to ms
        time_obj.minute * 60000 +      # Minutes to ms
        time_obj.second * 1000 +       # Seconds to ms
        time_obj.microsecond // 1000   # Microseconds to ms
    )


def find_terms_in_srt(srt_path, terms):
    """
    Search for specified terms in an SRT file and return their timestamps.

    Args:
        srt_path (str): Path to the SRT file.
        terms (list): List of terms to search for.

    Returns:
        list: List of tuples containing start and end times in milliseconds.
    """
    timestamps = []
    try:
        # Open and read the SRT file contents
        with open(srt_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Split the content into individual subtitle blocks
        blocks = content.strip().split('\n\n')

        for block in blocks:
            lines = block.split('\n')
            if len(lines) >= 3:
                time_line = lines[1]  # The second line contains the timestamp
                text = ' '.join(lines[2:]).lower()  # Combine subtitle lines and convert to lowercase

                # Check if any of the terms are present in the subtitle text
                if any(term.lower() in text for term in terms):
                    # Use regex to extract start and end timestamps
                    match = re.match(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})', time_line)
                    if match:
                        start_time = timestamp_to_milliseconds(match.group(1))
                        end_time = timestamp_to_milliseconds(match.group(2))
                        timestamps.append((start_time, end_time))
        return timestamps
    except Exception as e:
        # Display an error message in the Streamlit app if something goes wrong
        st.error(f"Error reading SRT file: {str(e)}")
        return []


def generate_beep(duration):
    """
    Generate a beep sound of a specified duration.

    Args:
        duration (int): Duration of the beep in milliseconds.

    Returns:
        AudioSegment: Audio segment containing the beep sound.
    """
    # Create a sine wave generator at 1000 Hz
    sine_wave = Sine(1000)
    
    # Create a silent audio segment of the specified duration
    beep = AudioSegment.silent(duration=duration)
    
    # Overlay the sine wave onto the silent segment to create the beep
    beep = beep.overlay(sine_wave.to_audio_segment(duration=duration))
    
    # Reduce the volume by 3 dB for a softer beep
    return beep - 3


def process_audio(audio_path, timestamps, output_path):
    """
    Replace specified segments of the audio with beep sounds based on timestamps.

    Args:
        audio_path (str): Path to the original audio file.
        timestamps (list): List of tuples with start and end times in milliseconds.
        output_path (str): Path to save the redacted (processed) audio.

    Returns:
        bool: True if processing is successful, False otherwise.
    """
    try:
        # Load the original audio file
        audio = AudioSegment.from_file(audio_path)
        
        # Iterate over each timestamp to replace the audio segment with a beep
        for start_ms, end_ms in timestamps:
            duration = end_ms - start_ms  # Calculate duration of the segment to be beeped
            beep = generate_beep(duration)  # Generate a beep of the same duration
            audio = audio[:start_ms] + beep + audio[end_ms:]  # Replace the segment with beep
        
        # Export the modified audio to the specified output path
        audio.export(output_path, format=os.path.splitext(output_path)[1][1:])
        return True
    except Exception as e:
        # Display an error message in the Streamlit app if processing fails
        st.error(f"Error processing audio: {str(e)}")
        return False


def main():
    """
    The main function that defines the Streamlit app's behavior.
    """
    st.title("Automatic Audio Transcription and Redaction Tool")

    # Step 1: Upload audio file
    audio_file = st.file_uploader("Upload an audio file", type=['wav', 'mp3', 'ogg', 'flac'])

    # Step 2: User inputs words to bleep
    terms_input = st.text_area("Enter words to bleep (one per line):")
    
    # Process the input terms by stripping whitespace and ignoring empty lines
    terms = [term.strip() for term in terms_input.split('\n') if term.strip()]

    # Action button to start transcription and redaction
    if st.button("Start Transcription and Redaction"):
        if audio_file and terms:
            # Save the uploaded audio file to a temporary path
            audio_path = f"./temp_{audio_file.name}"
            with open(audio_path, 'wb') as f:
                f.write(audio_file.read())

            # Transcribe the audio using Whisper
            st.write("Transcribing audio...")
            try:
                result = model.transcribe(audio_path)  # Perform transcription
                base_name = os.path.splitext(audio_path)[0]  # Get the base name without extension
                srt_path = f"{base_name}-transcription.srt"  # Define the SRT file path
                result.to_srt_vtt(srt_path)  # Save the transcription as an SRT file
                st.success(f"Transcription complete! SRT saved as {srt_path}")

                # Display the transcription content to the user
                with open(srt_path, 'r') as f:
                    transcription_content = f.read()
                st.text_area("Transcription Result:", transcription_content, height=300)

                # Step 3: Find and bleep specified words in the transcription
                st.write("Bleeping audio for specified terms...")
                timestamps = find_terms_in_srt(srt_path, terms)  # Get timestamps of terms to bleep

                if timestamps:
                    # Display the timestamps where beeping will occur
                    for start, end in timestamps:
                        st.write(f"Bleeping from {start}ms to {end}ms")

                    # Define the path for the redacted audio
                    redacted_audio_path = f"{base_name}-redacted{os.path.splitext(audio_path)[1]}"
                    
                    # Process the audio to replace specified segments with beeps
                    if process_audio(audio_path, timestamps, redacted_audio_path):
                        st.success(f"Redacted audio saved as {redacted_audio_path}")
                        st.audio(redacted_audio_path)  # Play the redacted audio in the app
                    else:
                        st.error("Failed to create redacted audio.")
                else:
                    st.warning("No matching terms found in the transcription.")

            except Exception as e:
                # Display an error message if transcription fails
                st.error(f"Error during transcription: {str(e)}")
        else:
            # Warn the user to upload an audio file and enter terms if not provided
            st.warning("Please upload an audio file and enter terms to bleep.")


if __name__ == "__main__":
    main()