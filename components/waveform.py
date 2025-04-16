
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer, QRect
from PyQt6.QtGui import QPainter, QColor, QPen, QLinearGradient, QBrush
import random
from styles import Colors

class WaveformDisplay(QWidget):
    """
    Visual waveform display for audio tracks
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.waveform_data = []
        self.playhead_position = 0.0  # 0.0 to 1.0
        self.generate_dummy_waveform()  # For demonstration only
        
        # Animation timer for demonstration
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_playhead)
        self.animation_timer.start(30)  # ~30fps
    
    def generate_dummy_waveform(self, length=1000):
        """Generate dummy waveform data for demonstration"""
        self.waveform_data = []
        
        # Create dummy beat pattern
        # In a real app, this would be actual audio analysis data
        for i in range(length):
            # Create a beat pattern
            if i % 100 < 10:  # Beat peaks
                value = random.uniform(0.7, 1.0)
            elif i % 25 < 5:  # Sub beats
                value = random.uniform(0.4, 0.7)
            else:
                value = random.uniform(0.1, 0.4)
                
            # Add some variation
            value *= (1.0 + random.uniform(-0.2, 0.2))
            value = max(0.05, min(1.0, value))
            
            self.waveform_data.append(value)
    
    def update_playhead(self):
        """Update playhead position for animation"""
        self.playhead_position += 0.001
        if self.playhead_position > 1.0:
            self.playhead_position = 0.0
        self.update()
    
    def set_waveform_data(self, data):
        """Set actual waveform data from audio analysis"""
        self.waveform_data = data
        self.update()
    
    def set_playhead_position(self, position):
        """Set playhead position (0.0 to 1.0)"""
        self.playhead_position = max(0.0, min(1.0, position))
        self.update()
    
    def paintEvent(self, event):
        """Custom paint for waveform visualization"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Calculate dimensions
        width = self.width()
        height = self.height()
        center_y = height / 2
        
        # Draw background
        painter.setPen(Qt.PenStyle.NoPen)
        background_gradient = QLinearGradient(0, 0, 0, height)
        background_gradient.setColorAt(0.0, QColor(Colors.BG_MEDIUM))
        background_gradient.setColorAt(1.0, QColor(Colors.BG_DARK))
        painter.setBrush(QBrush(background_gradient))
        painter.drawRect(0, 0, width, height)
        
        # Draw grid lines
        painter.setPen(QPen(QColor(Colors.BG_LIGHT), 1, Qt.PenStyle.DotLine))
        
        # Horizontal center line
        painter.drawLine(0, center_y, width, center_y)
        
        # Vertical grid lines (beats)
        grid_spacing = width / 16  # 16 beat markers
        for i in range(17):
            x = i * grid_spacing
            painter.drawLine(x, 0, x, height)
        
        # Draw waveform if data available
        if self.waveform_data:
            # Calculate scaling
            data_length = len(self.waveform_data)
            x_scale = width / data_length
            
            # Create gradient for waveform
            waveform_gradient = QLinearGradient(0, 0, 0, height)
            waveform_gradient.setColorAt(0.0, QColor(Colors.ACCENT))
            waveform_gradient.setColorAt(0.5, QColor(Colors.ACCENT_2))
            waveform_gradient.setColorAt(1.0, QColor(Colors.ACCENT))
            
            # Draw waveform as mirrored gradient bars
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(waveform_gradient))
            
            for i in range(data_length):
                x = int(i * x_scale)
                value = self.waveform_data[i]
                bar_height = int(center_y * value)
                
                # Draw mirrored bars (top and bottom)
                painter.drawRect(x, center_y - bar_height, 
                               max(1, int(x_scale)), bar_height)
                painter.drawRect(x, center_y, 
                               max(1, int(x_scale)), bar_height)
        
        # Draw played section with different color
        if self.waveform_data:
            playhead_x = int(width * self.playhead_position)
            played_gradient = QLinearGradient(0, 0, 0, height)
            played_gradient.setColorAt(0.0, QColor(Colors.SECONDARY))
            played_gradient.setColorAt(0.5, QColor(Colors.PRIMARY))
            played_gradient.setColorAt(1.0, QColor(Colors.SECONDARY))
            
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(played_gradient))
            
            for i in range(int(data_length * self.playhead_position)):
                x = int(i * x_scale)
                value = self.waveform_data[i]
                bar_height = int(center_y * value)
                
                # Draw mirrored bars (top and bottom)
                painter.drawRect(x, center_y - bar_height, 
                               max(1, int(x_scale)), bar_height)
                painter.drawRect(x, center_y, 
                               max(1, int(x_scale)), bar_height)
        
        # Draw playhead line
        playhead_x = int(width * self.playhead_position)
        painter.setPen(QPen(QColor("#FFFFFF"), 2))
        painter.drawLine(playhead_x, 0, playhead_x, height)
        
        # Draw time markers
        painter.setPen(QColor(Colors.TEXT_MEDIUM))
        painter.drawText(5, height - 5, "0:00")
        painter.drawText(width - 40, height - 5, "3:30")  # Example duration
        
        # Draw current position
        minutes = int(self.playhead_position * 3.5)  # Example duration: 3:30
        seconds = int((self.playhead_position * 3.5 * 60) % 60)
        time_text = f"{minutes}:{seconds:02d}"
        painter.setPen(QColor(Colors.TEXT_BRIGHT))
        painter.drawText(playhead_x + 5, 15, time_text)
    
    def mousePressEvent(self, event):
        """Handle mouse press to set playhead position"""
        if event.button() == Qt.MouseButton.LeftButton:
            # Set playhead position based on click position
            self.playhead_position = event.position().x() / self.width()
            self.update()
    
    def mouseMoveEvent(self, event):
        """Handle mouse drag to set playhead position"""
        if event.buttons() & Qt.MouseButton.LeftButton:
            # Set playhead position based on mouse position
            self.playhead_position = max(0.0, min(1.0, event.position().x() / self.width()))
            self.update()
