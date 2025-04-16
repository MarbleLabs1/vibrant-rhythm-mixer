
import os
import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QPushButton, QVBoxLayout, 
                           QHBoxLayout, QSlider, QLabel, QFileDialog, QGridLayout)
from PyQt6.QtCore import Qt, QUrl, QTimer
from PyQt6.QtGui import QColor, QLinearGradient, QBrush, QPalette, QFont, QIcon
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from audio_engine import AudioEngine
from sample_manager import SampleManager
from components.pad import DJPad
from components.mixer import Mixer
from components.waveform import WaveformDisplay
from styles import DarkStyle, Colors

class DJPadApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set application style
        self.setStyleSheet(DarkStyle.STYLESHEET)
        
        # Set window properties
        self.setWindowTitle("Vibrant Rhythm Mixer")
        self.setMinimumSize(1200, 800)
        
        # Initialize audio engine and sample manager
        self.audio_engine = AudioEngine()
        self.sample_manager = SampleManager("resources/samples")
        
        # Create UI
        self.init_ui()
        
    def init_ui(self):
        # Create central widget and main layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        
        # Create header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Create main content area
        content = QHBoxLayout()
        
        # Create deck A
        deck_a = self.create_deck("DECK A", Colors.PURPLE_GRADIENT)
        content.addLayout(deck_a, 3)
        
        # Create mixer section
        mixer = Mixer(self)
        content.addWidget(mixer, 2)
        
        # Create deck B
        deck_b = self.create_deck("DECK B", Colors.BLUE_GRADIENT)
        content.addLayout(deck_b, 3)
        
        main_layout.addLayout(content)
        
        # Create pad section
        pads_section = self.create_pads_section()
        main_layout.addLayout(pads_section)
        
        # Create footer with controls
        footer = self.create_footer()
        main_layout.addWidget(footer)
        
        # Set central widget
        self.setCentralWidget(central_widget)
        
        # Apply gradient background
        self.apply_gradient_background()
        
    def create_header(self):
        header = QWidget()
        header.setFixedHeight(80)
        header_layout = QHBoxLayout(header)
        
        # Logo/Title
        logo = QLabel("VIBRANT RHYTHM MIXER")
        logo.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        logo.setStyleSheet(f"color: {Colors.ACCENT};")
        
        # BPM control
        bpm_container = QWidget()
        bpm_layout = QVBoxLayout(bpm_container)
        bpm_label = QLabel("BPM")
        bpm_label.setStyleSheet(f"color: {Colors.TEXT_BRIGHT};")
        bpm_value = QLabel("128.0")
        bpm_value.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        bpm_value.setStyleSheet(f"color: {Colors.ACCENT};")
        bpm_layout.addWidget(bpm_label)
        bpm_layout.addWidget(bpm_value)
        
        # Add widgets to header
        header_layout.addWidget(logo)
        header_layout.addStretch()
        header_layout.addWidget(bpm_container)
        
        return header
    
    def create_deck(self, name, gradient):
        deck_layout = QVBoxLayout()
        
        # Deck header
        deck_header = QWidget()
        deck_header.setFixedHeight(60)
        deck_header.setStyleSheet(f"background: {gradient}; border-radius: 10px;")
        deck_header_layout = QHBoxLayout(deck_header)
        
        deck_title = QLabel(name)
        deck_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        deck_title.setStyleSheet(f"color: {Colors.TEXT_BRIGHT};")
        deck_header_layout.addWidget(deck_title)
        
        load_button = QPushButton("LOAD TRACK")
        load_button.setStyleSheet(
            f"background-color: {Colors.ACCENT}; color: {Colors.BG_DARK}; "
            f"padding: 8px 15px; border-radius: 5px; font-weight: bold;"
        )
        deck_header_layout.addWidget(load_button)
        
        # Waveform display
        waveform = WaveformDisplay()
        waveform.setMinimumHeight(200)
        
        # Playback controls
        playback = QWidget()
        playback_layout = QHBoxLayout(playback)
        
        play_button = QPushButton("▶ PLAY")
        play_button.setStyleSheet(
            f"background-color: {Colors.ACCENT_2}; color: {Colors.BG_DARK}; "
            f"padding: 10px 20px; border-radius: 5px; font-weight: bold;"
        )
        
        cue_button = QPushButton("CUE")
        cue_button.setStyleSheet(
            f"background-color: {Colors.ACCENT_3}; color: {Colors.BG_DARK}; "
            f"padding: 10px 20px; border-radius: 5px; font-weight: bold;"
        )
        
        playback_layout.addWidget(play_button)
        playback_layout.addWidget(cue_button)
        
        # Tempo slider
        tempo_widget = QWidget()
        tempo_layout = QVBoxLayout(tempo_widget)
        
        tempo_label = QLabel("TEMPO")
        tempo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tempo_label.setStyleSheet(f"color: {Colors.TEXT_BRIGHT};")
        
        tempo_slider = QSlider(Qt.Orientation.Vertical)
        tempo_slider.setMinimum(-100)
        tempo_slider.setMaximum(100)
        tempo_slider.setValue(0)
        tempo_slider.setStyleSheet(
            f"QSlider::groove:vertical {{ background: {Colors.BG_MEDIUM}; width: 10px; border-radius: 5px; }}"
            f"QSlider::handle:vertical {{ background: {Colors.ACCENT}; height: 20px; width: 20px; "
            f"margin: -5px 0; border-radius: 10px; }}"
        )
        
        tempo_layout.addWidget(tempo_label)
        tempo_layout.addWidget(tempo_slider, 1)
        
        # Assemble deck
        deck_layout.addWidget(deck_header)
        deck_layout.addWidget(waveform)
        deck_layout.addWidget(playback)
        
        # Create container for track info and tempo
        track_container = QHBoxLayout()
        
        # Track info
        track_info = QWidget()
        track_info_layout = QVBoxLayout(track_info)
        track_name = QLabel("No Track Loaded")
        track_name.setStyleSheet(f"color: {Colors.TEXT_BRIGHT}; font-weight: bold;")
        track_details = QLabel("--:--  / --:--")
        track_details.setStyleSheet(f"color: {Colors.TEXT_MEDIUM};")
        
        track_info_layout.addWidget(track_name)
        track_info_layout.addWidget(track_details)
        
        track_container.addWidget(track_info, 3)
        track_container.addWidget(tempo_widget, 1)
        
        deck_layout.addLayout(track_container)
        
        return deck_layout
    
    def create_pads_section(self):
        pads_layout = QVBoxLayout()
        
        # Section header
        section_title = QLabel("PERFORMANCE PADS")
        section_title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        section_title.setStyleSheet(f"color: {Colors.TEXT_BRIGHT}; margin-top: 10px;")
        pads_layout.addWidget(section_title)
        
        # Pad grid container
        pad_grid = QGridLayout()
        pad_grid.setSpacing(10)
        
        # Create 4x4 grid of pads with different colors
        colors = [
            Colors.PAD_1, Colors.PAD_2, Colors.PAD_3, Colors.PAD_4,
            Colors.PAD_5, Colors.PAD_6, Colors.PAD_7, Colors.PAD_8,
            Colors.PAD_1, Colors.PAD_2, Colors.PAD_3, Colors.PAD_4,
            Colors.PAD_5, Colors.PAD_6, Colors.PAD_7, Colors.PAD_8,
        ]
        
        pad_names = [
            "KICK 1", "SNARE 1", "HAT 1", "CLAP 1",
            "BASS 1", "FX 1", "VOX 1", "SYNTH 1",
            "KICK 2", "SNARE 2", "HAT 2", "CLAP 2",
            "BASS 2", "FX 2", "VOX 2", "SYNTH 2",
        ]
        
        for i in range(4):
            for j in range(4):
                index = i * 4 + j
                pad = DJPad(pad_names[index], colors[index])
                pad.clicked.connect(lambda checked, idx=index: self.pad_clicked(idx))
                pad_grid.addWidget(pad, i, j)
        
        pads_layout.addLayout(pad_grid)
        
        return pads_layout
    
    def create_footer(self):
        footer = QWidget()
        footer.setFixedHeight(50)
        footer_layout = QHBoxLayout(footer)
        
        status = QLabel("Ready to mix")
        status.setStyleSheet(f"color: {Colors.TEXT_MEDIUM};")
        
        version = QLabel("v1.0.0")
        version.setStyleSheet(f"color: {Colors.TEXT_DIM};")
        
        footer_layout.addWidget(status)
        footer_layout.addStretch()
        footer_layout.addWidget(version)
        
        return footer
    
    def apply_gradient_background(self):
        # Set gradient background via stylesheet
        self.setStyleSheet(
            self.styleSheet() +
            f"QMainWindow {{ background: {Colors.BG_GRADIENT}; }}"
        )
    
    def pad_clicked(self, pad_index):
        # Handle pad click event
        print(f"Pad {pad_index} clicked")
        # In a real app, this would trigger a sound
        # self.audio_engine.play_sample(pad_index)
