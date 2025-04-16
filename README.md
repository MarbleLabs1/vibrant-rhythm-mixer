
# Vibrant Rhythm Mixer

A colorful, feature-rich DJ application built with Python and PyQt6. This application provides a modern interface for mixing tracks, adding effects, and triggering samples in a live performance environment.

## Features

- Dual deck mixing with crossfader
- Colorful performance pads for sample triggering
- Real-time waveform visualization
- 3-band EQ per deck
- Volume controls with VU meters
- Beat-synced effects
- Sample bank management

## Screenshots

![Application Screenshot](screenshot.png)

## Installation

### Requirements

- Python 3.8 or higher
- PyQt6
- PyAudio
- NumPy
- Pydub

### Setup

1. Clone this repository:
```
git clone https://github.com/yourusername/vibrant-rhythm-mixer.git
cd vibrant-rhythm-mixer
```

2. Create a virtual environment (recommended):
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```
pip install pyqt6 pyaudio numpy pydub
```

4. Run the application:
```
python main.py
```

## Usage Guide

### Loading Tracks

Click the "LOAD TRACK" button on either deck to open an audio file. The application supports common audio formats including MP3, WAV, AIFF, and FLAC.

### Mixing Controls

- **Crossfader**: Slide to transition between Deck A and Deck B
- **Volume Sliders**: Adjust the volume of each deck independently
- **EQ Knobs**: Adjust the low, mid, and high frequencies for each deck
- **Tempo Controls**: Adjust the playback speed to beat-match tracks

### Performance Pads

The 16 colorful pads at the bottom can be assigned samples for triggering during your performance:

1. Right-click on a pad to assign a sample
2. Click on the pad during performance to trigger the sample
3. Use the pad banks to organize different sample sets

### BPM Control

- Use the BPM control to set the tempo for beat-synced effects
- The tap tempo button can be used to manually set the BPM by tapping in time with the music

## Open Source Sounds

This application is designed to work with open source sound samples. Here are some recommended resources for high-quality free samples:

- [Freesound.org](https://freesound.org/) - A collaborative database of Creative Commons Licensed sounds
- [SampleSwap](https://sampleswap.org/) - Free and legal sample sharing community
- [Looperman](https://www.looperman.com/) - Royalty-free loops and samples

## Development

This application is structured as follows:

- `main.py` - Entry point for the application
- `dj_pad.py` - Main application window and UI
- `audio_engine.py` - Audio processing and playback
- `sample_manager.py` - Sample management and organization
- `components/` - UI components (pads, mixers, etc.)
- `styles.py` - Application styling and colors
- `resources/` - Sample files and assets

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by professional DJ software like Serato, Traktor, and VirtualDJ
- Utilizes the excellent PyQt6 framework for the UI
- Thanks to the open source audio community for sample resources
