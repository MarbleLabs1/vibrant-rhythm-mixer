
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QSlider, 
                           QLabel, QPushButton, QGridLayout)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QPainter, QLinearGradient, QBrush, QPen, QFont
from styles import Colors

class VUMeter(QWidget):
    """
    Visual volume level meter with customizable colors
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(16, 150)
        self.level = 0.0  # 0.0 to 1.0
        self.peak_level = 0.0
        self.decay_factor = 0.05
        self.color_low = QColor(Colors.ACCENT_2)
        self.color_mid = QColor(Colors.ACCENT_3)
        self.color_high = QColor(Colors.ACCENT)
    
    def set_level(self, level):
        """Set current audio level (0.0 to 1.0)"""
        self.level = max(0.0, min(1.0, level))
        
        # Update peak level
        if self.level > self.peak_level:
            self.peak_level = self.level
        else:
            # Gradual decay of peak level
            self.peak_level = max(self.level, self.peak_level - self.decay_factor)
        
        self.update()
    
    def paintEvent(self, event):
        """Custom paint for the VU meter"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Background
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(Colors.BG_MEDIUM)))
        painter.drawRect(0, 0, self.width(), self.height())
        
        # Calculate level height
        level_height = int(self.height() * self.level)
        peak_height = int(self.height() * self.peak_level)
        
        # Draw level gradient
        if level_height > 0:
            gradient = QLinearGradient(0, self.height(), 0, self.height() - level_height)
            gradient.setColorAt(0.0, self.color_low)
            gradient.setColorAt(0.7, self.color_mid)
            gradient.setColorAt(1.0, self.color_high)
            
            painter.setBrush(QBrush(gradient))
            painter.drawRect(0, self.height() - level_height, self.width(), level_height)
        
        # Draw peak indicator
        if peak_height > 0 and peak_height > level_height:
            painter.setPen(QPen(QColor("#FFFFFF"), 2))
            painter.drawLine(0, self.height() - peak_height, 
                            self.width(), self.height() - peak_height)

class EQKnob(QWidget):
    """
    EQ knob control with label
    """
    def __init__(self, label, color, parent=None):
        super().__init__(parent)
        self.label = label
        self.color = QColor(color)
        self.value = 0.5  # 0.0 to 1.0, center at 0.5
        self.setMinimumSize(60, 80)
        
        # Handle mouse events for interaction
        self.setMouseTracking(True)
        self.mouse_down = False
        self.last_y = 0
    
    def set_value(self, value):
        """Set knob value (0.0 to 1.0)"""
        self.value = max(0.0, min(1.0, value))
        self.update()
    
    def paintEvent(self, event):
        """Custom paint for the EQ knob"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw label
        painter.setPen(QColor(Colors.TEXT_MEDIUM))
        painter.setFont(QFont("Arial", 8))
        painter.drawText(0, 0, self.width(), 20, 
                        Qt.AlignmentFlag.AlignCenter, self.label)
        
        # Draw knob
        center_x = self.width() / 2
        center_y = 45
        radius = 25
        
        # Draw background circle
        painter.setPen(QPen(QColor(Colors.BG_LIGHT), 2))
        painter.setBrush(QBrush(QColor(Colors.BG_MEDIUM)))
        painter.drawEllipse(center_x - radius, center_y - radius, 
                           radius * 2, radius * 2)
        
        # Draw value indicator
        angle = (240 - (self.value * 300)) * (3.14159 / 180.0)
        indicator_x = center_x + int(radius * 0.8 * -1 * (1.0 if angle < 1.57 else -1.0) * (1.0 - abs(1.57 - angle)))
        indicator_y = center_y - int(radius * 0.8 * -1 * (1.0 if angle > 1.57 else -1.0) * (1.0 - abs(1.57 - angle)))
        
        painter.setPen(QPen(self.color, 3))
        painter.drawLine(center_x, center_y, indicator_x, indicator_y)
        
        # Draw center dot
        painter.setBrush(QBrush(self.color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center_x - 5, center_y - 5, 10, 10)
        
        # Draw value text
        if self.value == 0.5:
            value_text = "0"
        elif self.value > 0.5:
            value_text = f"+{int((self.value - 0.5) * 20)}"
        else:
            value_text = f"-{int((0.5 - self.value) * 20)}"
        
        painter.setPen(QColor(Colors.TEXT_BRIGHT))
        painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        painter.drawText(0, center_y + radius, self.width(), 20, 
                        Qt.AlignmentFlag.AlignCenter, value_text)
    
    def mousePressEvent(self, event):
        """Handle mouse press for knob adjustment"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_down = True
            self.last_y = event.position().y()
            self.setCursor(Qt.CursorShape.SizeVerCursor)
            self.update()
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_down = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.update()
    
    def mouseMoveEvent(self, event):
        """Handle mouse movement for knob adjustment"""
        if self.mouse_down:
            # Adjust value based on vertical movement
            delta_y = self.last_y - event.position().y()
            self.last_y = event.position().y()
            
            # Scale movement: 100px = full range
            self.value = max(0.0, min(1.0, self.value + delta_y / 100.0))
            self.update()
            
            # Emit value change signal (would be implemented in a real app)
            # self.value_changed.emit(self.value)
    
    def mouseDoubleClickEvent(self, event):
        """Reset to center value on double click"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.value = 0.5
            self.update()
            # self.value_changed.emit(self.value)

class Mixer(QWidget):
    """
    Mixer panel with crossfader, volume controls, and EQ
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(300)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # Create crossfader section
        crossfader_section = self.create_crossfader_section()
        layout.addLayout(crossfader_section)
        
        # Create EQ section
        eq_section = self.create_eq_section()
        layout.addLayout(eq_section)
        
        # Create volume section
        volume_section = self.create_volume_section()
        layout.addLayout(volume_section)
        
        # Add stretch to push everything up
        layout.addStretch()
    
    def create_crossfader_section(self):
        """Create the crossfader slider and labels"""
        section = QVBoxLayout()
        
        # Section header
        header = QLabel("CROSSFADER")
        header.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        header.setStyleSheet(f"color: {Colors.TEXT_BRIGHT};")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        section.addWidget(header)
        
        # Crossfader control
        crossfader = QSlider(Qt.Orientation.Horizontal)
        crossfader.setMinimum(0)
        crossfader.setMaximum(100)
        crossfader.setValue(50)
        crossfader.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                             stop:0 {Colors.PURPLE_GRADIENT.split("stop:1")[0]}, 
                             stop:1 {Colors.BLUE_GRADIENT.split("stop:1")[1]});
                height: 12px;
                border-radius: 6px;
            }}
            
            QSlider::handle:horizontal {{
                background: {Colors.ACCENT};
                border: none;
                width: 20px;
                height: 20px;
                margin: -4px 0;
                border-radius: 10px;
            }}
        """)
        section.addWidget(crossfader)
        
        # Deck labels
        labels = QHBoxLayout()
        deck_a = QLabel("DECK A")
        deck_a.setStyleSheet(f"color: {Colors.TEXT_MEDIUM};")
        deck_b = QLabel("DECK B")
        deck_b.setStyleSheet(f"color: {Colors.TEXT_MEDIUM};")
        deck_b.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        labels.addWidget(deck_a)
        labels.addWidget(deck_b)
        section.addLayout(labels)
        
        return section
    
    def create_eq_section(self):
        """Create EQ controls for both decks"""
        section = QVBoxLayout()
        
        # Section header
        header = QLabel("EQUALIZER")
        header.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        header.setStyleSheet(f"color: {Colors.TEXT_BRIGHT};")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        section.addWidget(header)
        
        # EQ controls container
        eq_container = QHBoxLayout()
        
        # EQ for Deck A
        deck_a_eq = QVBoxLayout()
        deck_a_label = QLabel("DECK A")
        deck_a_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        deck_a_label.setStyleSheet(f"color: {Colors.TEXT_MEDIUM};")
        deck_a_eq.addWidget(deck_a_label)
        
        # EQ knobs for deck A
        deck_a_knobs = QHBoxLayout()
        low_a = EQKnob("LOW", Colors.PAD_1)
        mid_a = EQKnob("MID", Colors.PAD_3)
        high_a = EQKnob("HIGH", Colors.PAD_4)
        
        deck_a_knobs.addWidget(low_a)
        deck_a_knobs.addWidget(mid_a)
        deck_a_knobs.addWidget(high_a)
        deck_a_eq.addLayout(deck_a_knobs)
        
        # EQ for Deck B
        deck_b_eq = QVBoxLayout()
        deck_b_label = QLabel("DECK B")
        deck_b_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        deck_b_label.setStyleSheet(f"color: {Colors.TEXT_MEDIUM};")
        deck_b_eq.addWidget(deck_b_label)
        
        # EQ knobs for deck B
        deck_b_knobs = QHBoxLayout()
        low_b = EQKnob("LOW", Colors.PAD_6)
        mid_b = EQKnob("MID", Colors.PAD_7)
        high_b = EQKnob("HIGH", Colors.PAD_8)
        
        deck_b_knobs.addWidget(low_b)
        deck_b_knobs.addWidget(mid_b)
        deck_b_knobs.addWidget(high_b)
        deck_b_eq.addLayout(deck_b_knobs)
        
        # Add both decks to container
        eq_container.addLayout(deck_a_eq)
        eq_container.addLayout(deck_b_eq)
        section.addLayout(eq_container)
        
        return section
    
    def create_volume_section(self):
        """Create volume controls and VU meters"""
        section = QVBoxLayout()
        
        # Section header
        header = QLabel("VOLUME")
        header.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        header.setStyleSheet(f"color: {Colors.TEXT_BRIGHT};")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        section.addWidget(header)
        
        # Volume controls container
        volume_container = QHBoxLayout()
        
        # Volume for Deck A
        deck_a_vol = QVBoxLayout()
        deck_a_label = QLabel("DECK A")
        deck_a_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        deck_a_label.setStyleSheet(f"color: {Colors.TEXT_MEDIUM};")
        deck_a_vol.addWidget(deck_a_label)
        
        # Volume slider and VU meter for deck A
        deck_a_controls = QHBoxLayout()
        vol_a = QSlider(Qt.Orientation.Vertical)
        vol_a.setMinimum(0)
        vol_a.setMaximum(100)
        vol_a.setValue(80)
        vol_a.setStyleSheet(f"""
            QSlider::groove:vertical {{
                background: {Colors.BG_MEDIUM};
                width: 10px;
                border-radius: 5px;
            }}
            
            QSlider::handle:vertical {{
                background: {Colors.ACCENT_3};
                height: 20px;
                width: 20px;
                margin: 0 -5px;
                border-radius: 10px;
            }}
        """)
        
        vu_a = VUMeter()
        vu_a.set_level(0.7)  # Set to some initial level
        
        deck_a_controls.addWidget(vol_a)
        deck_a_controls.addWidget(vu_a)
        deck_a_vol.addLayout(deck_a_controls)
        
        # Volume for Deck B
        deck_b_vol = QVBoxLayout()
        deck_b_label = QLabel("DECK B")
        deck_b_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        deck_b_label.setStyleSheet(f"color: {Colors.TEXT_MEDIUM};")
        deck_b_vol.addWidget(deck_b_label)
        
        # Volume slider and VU meter for deck B
        deck_b_controls = QHBoxLayout()
        vol_b = QSlider(Qt.Orientation.Vertical)
        vol_b.setMinimum(0)
        vol_b.setMaximum(100)
        vol_b.setValue(80)
        vol_b.setStyleSheet(f"""
            QSlider::groove:vertical {{
                background: {Colors.BG_MEDIUM};
                width: 10px;
                border-radius: 5px;
            }}
            
            QSlider::handle:vertical {{
                background: {Colors.ACCENT_3};
                height: 20px;
                width: 20px;
                margin: 0 -5px;
                border-radius: 10px;
            }}
        """)
        
        vu_b = VUMeter()
        vu_b.set_level(0.5)  # Set to some initial level
        
        deck_b_controls.addWidget(vol_b)
        deck_b_controls.addWidget(vu_b)
        deck_b_vol.addLayout(deck_b_controls)
        
        # Master volume
        master_vol = QVBoxLayout()
        master_label = QLabel("MASTER")
        master_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        master_label.setStyleSheet(f"color: {Colors.TEXT_BRIGHT}; font-weight: bold;")
        master_vol.addWidget(master_label)
        
        # Master volume slider and VU meters
        master_controls = QHBoxLayout()
        vol_master = QSlider(Qt.Orientation.Vertical)
        vol_master.setMinimum(0)
        vol_master.setMaximum(100)
        vol_master.setValue(90)
        vol_master.setStyleSheet(f"""
            QSlider::groove:vertical {{
                background: {Colors.BG_MEDIUM};
                width: 10px;
                border-radius: 5px;
            }}
            
            QSlider::handle:vertical {{
                background: {Colors.ACCENT};
                height: 20px;
                width: 20px;
                margin: 0 -5px;
                border-radius: 10px;
            }}
        """)
        
        vu_master_l = VUMeter()
        vu_master_l.set_level(0.8)
        
        vu_master_r = VUMeter()
        vu_master_r.set_level(0.8)
        
        master_controls.addWidget(vol_master)
        master_controls.addWidget(vu_master_l)
        master_controls.addWidget(vu_master_r)
        master_vol.addLayout(master_controls)
        
        # Add all volume controls to container
        volume_container.addLayout(deck_a_vol)
        volume_container.addLayout(master_vol)
        volume_container.addLayout(deck_b_vol)
        section.addLayout(volume_container)
        
        return section
