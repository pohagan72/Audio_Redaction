# Audio Redaction Tool

A streamlined and powerful tool that automatically redacts sensitive words from your audio recordings by replacing them with a beep tone. Leveraging the state-of-the-art Stable-Whisper [Stable-Whisper](https://github.com/jianfch/stable-ts/tree/main) asdf 

(https://github.com/jianfch/stable-ts/tree/main) transcription engine in SRT mode, this application pinpoints the exact timestamps for each word, then seamlessly overlays a beep sound over the sensitive segments.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Audio Redaction Tool makes it easy to remove, censor, or redact specific words in any audio file. The app:
- Transcribes the entire audio using the Whisper ASR engine.
- Generates an SRT file with precise timestamps for every word.
- Identifies user-specified words and replaces those segments with a natural-sounding beep tone.
- Outputs a new audio file with redacted content so you never have to worry about accidentally sharing sensitive audio.

---

## Features

- **Accurate Transcription:** Uses Whisper's SRT transcription mode to ensure every word is timed precisely.
- **Custom Redaction:** Specify any words (e.g., profanity, sensitive information) to redact automatically.
- **Audio Processing:** Efficient audio editing with Python's `pydub` library to overlay a beep sound.
- **Streamlit Interface:** A clean and interactive web interface allowing quick uploads and immediate redacted playback.
- **Easy Integration:** Ideal for journalists, podcasters, educators, or anyone looking to protect sensitive information.

---

## Requirements

Before you begin, ensure you have met the following requirements:

- **Python 3.7+**
- **FFmpeg:** Required by `pydub` for processing audio. Download and install it from [FFmpeg Official Site](https://ffmpeg.org/download.html).
- **System Dependencies:**  
  - [PyTorch](https://pytorch.org/)
  - [Torchvision](https://pytorch.org/vision/stable/index.html)
  - [Torchaudio](https://pytorch.org/audio/stable/)
  
---

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your_username/Audio_Redaction.git
   cd Audio_Redaction/repos/Audio_Redaction
   ```

2. **Install Python Dependencies:**

   ```bash
   pip install streamlit stable_whisper pydub torch torchvision torchaudio
   ```

3. **Install FFmpeg:**

   - Download from [FFmpeg Downloads](https://ffmpeg.org/download.html) and install according to your OS instructions.
   - Ensure FFmpeg is added to your system's PATH.

---

## Usage

1. **Launch the Streamlit Application:**

   ```bash
   streamlit run Audio_Redaction.py
   ```

2. **Interact with the App:**
   - **Upload:** Choose your audio file (supported formats: WAV, MP3, OGG, FLAC).
   - **Specify Terms:** Input the words you intend to redact (one per line).
   - **Start Process:** Click on the "Start Transcription and Redaction" button. The app will:
     - Transcribe the audio and generate an SRT file.
     - Search the SRT for the terms provided.
     - Replace corresponding audio sections with a beep.
   - **Playback:** Listen to your redacted audio directly within the app.

---

## How It Works

1. **Transcription:**
   - Uses the `stable_whisper` model to transcribe your audio with detailed SRT output.
   - Each subtitle block includes start and end timestamps.

2. **Word Detection:**
   - Processes the SRT file to identify occurrences of the user-specified sensitive words.
   - Extracts precise timestamps for each match using regular expressions.

3. **Audio Redaction:**
   - Loads the original audio using the `pydub` library.
   - For each identified segment, generates a beep sound (a 1000 Hz sine wave with slight volume reduction) lasting exactly as long as the word or phrase.
   - Replaces the segment in the original audio with the generated beep.
   - Exports the final redacted audio file.

---

## Troubleshooting

- **FFmpeg Not Found:** Ensure that FFmpeg is correctly installed and available in your system path.
- **Audio Upload Issues:** Confirm your audio file is in one of the supported formats: WAV, MP3, OGG, or FLAC.
- **Transcription Accuracy:** For best results, use clear audio recordings. Background noise may affect transcription performance.

For more detailed error messages, check the Streamlit app's debug logs.
