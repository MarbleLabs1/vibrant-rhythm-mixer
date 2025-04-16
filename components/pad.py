
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QPainter, QColor, QBrush, QLinearGradient
from styles import Colors

class DJPad(QPushButton):
    """
    Custom button for DJ pads with vibrant colors and animation effects.
    """
    def __init__(self, text, color, parent=None):
        super().__init__(text, parent)
        self.setMinimumSize(100, 100)
        self.setMaximumSize(200, 200)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        
        # Set properties
        self.color = color
        self.is_pressed = False
        self.hover_strength = 0
        
        # Enable animation
        self.setAutoFillBackground(False)
        self.animation = QPropertyAnimation(self, b"hover_strength")
        self.animation.setDuration(150)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Setup style
        self.update_style()
    
    def update_style(self):
        """Update the button styling"""
        # Default style with gradient background
        base_color = QColor(self.color)
        lighter_color = QColor(self.color)
        lighter_color.setAlpha(200)
        
        # Keep text white for readability
        text_color = "#FFFFFF"
        
        # Different style when pressed
        if self.is_pressed:
            # Invert gradient when pressed
            self.setStyleSheet(f"""
                QPushButton {{
                    color: {text_color};
                    border: none;
                    border-radius: 8px;
                    font-weight: bold;
                    padding-bottom: 4px;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    color: {text_color};
                    border: none;
                    border-radius: 8px;
                    font-weight: bold;
                }}
            """)
    
    def paintEvent(self, event):
        """Custom paint event for gradients and effects"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Create gradient based on state
        gradient = QLinearGradient(0, 0, 0, self.height())
        
        color = QColor(self.color)
        lighter = QColor(self.color)
        lighter.setHsv(
            lighter.hue(),
            max(0, lighter.saturation() - 30),
            min(255, lighter.value() + 30)
        )
        darker = QColor(self.color)
        darker.setHsv(
            darker.hue(),
            min(255, darker.saturation() + 20),
            max(0, darker.value() - 40)
        )
        
        if self.is_pressed:
            # Pressed gradient (reversed)
            gradient.setColorAt(0.0, darker)
            gradient.setColorAt(1.0, color)
        else:
            # Normal gradient with hover effect
            hover_effect = min(100, self.hover_strength)
            
            # Adjust brightness based on hover
            hover_lighter = QColor(lighter)
            hover_lighter.setHsv(
                hover_lighter.hue(),
                hover_lighter.saturation(),
                min(255, hover_lighter.value() + hover_effect)
            )
            
            gradient.setColorAt(0.0, hover_lighter)
            gradient.setColorAt(1.0, color)
        
        # Draw rounded rectangle with gradient
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(gradient))
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 8, 8)
        
        # Draw text
        painter.setPen(QColor("#FFFFFF"))
        painter.setFont(self.font())
        painter.drawText(
            0, 0, self.width(), self.height(),
            Qt.AlignmentFlag.AlignCenter, self.text()
        )
    
    def mousePressEvent(self, event):
        """Handle mouse press with visual feedback"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_pressed = True
            self.update_style()
            self.update()
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release with animation"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_pressed = False
            self.update_style()
            self.update()
        super().mouseReleaseEvent(event)
    
    def enterEvent(self, event):
        """Handle mouse enter with hover animation"""
        self.animation.setStartValue(0)
        self.animation.setEndValue(100)
        self.animation.start()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Handle mouse leave with hover animation"""
        self.animation.setStartValue(self.hover_strength)
        self.animation.setEndValue(0)
        self.animation.start()
        super().leaveEvent(event)
    
    # Property for animation
    @property
    def hover_strength(self):
        return self._hover_strength
    
    @hover_strength.setter
    def hover_strength(self, value):
        self._hover_strength = value
        self.update()
