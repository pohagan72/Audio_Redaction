# Audio_Redaction
Finds words in an audio file as specified by the user, and then generates a new version of the audio file with those words beeped out.

Uses Whisper as the transcription engine but in SRT mode so each word is extracted with it's specific timestamp.

pip install streamlit stable_whisper pydub torch torchvision torchaudio

Also, pydub requires FFmpeg and that needs to be downloaded and installed separately https://ffmpeg.org/download.html 
