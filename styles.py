
"""
Styles and colors for the DJ Pad application
"""

class Colors:
    # Main theme colors
    PRIMARY = "#6200EA"   # Deep Purple
    SECONDARY = "#03DAC6" # Teal
    ACCENT = "#FF3D00"    # Orange-Red
    ACCENT_2 = "#00E676"  # Green
    ACCENT_3 = "#FFAB00"  # Amber
    
    # Background colors
    BG_DARK = "#121212"
    BG_MEDIUM = "#1E1E1E"
    BG_LIGHT = "#2D2D2D"
    
    # Text colors
    TEXT_BRIGHT = "#FFFFFF"
    TEXT_MEDIUM = "#BBBBBB"
    TEXT_DIM = "#777777"
    
    # Performance pad colors
    PAD_1 = "#FF5252"  # Red
    PAD_2 = "#FF4081"  # Pink
    PAD_3 = "#7C4DFF"  # Deep Purple
    PAD_4 = "#40C4FF"  # Light Blue
    PAD_5 = "#18FFFF"  # Cyan
    PAD_6 = "#69F0AE"  # Green
    PAD_7 = "#FFFF00"  # Yellow
    PAD_8 = "#FFAB40"  # Orange
    
    # Gradients
    BG_GRADIENT = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0D0D2B, stop:1 #1A2A56)"
    PURPLE_GRADIENT = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4A148C, stop:1 #7B1FA2)"
    BLUE_GRADIENT = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1A237E, stop:1 #0D47A1)"
    RED_GRADIENT = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #D50000, stop:1 #C62828)"
    GREEN_GRADIENT = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2E7D32, stop:1 #1B5E20)"
    
    # Highlight effects
    GLOW = "0px 0px 15px"

class DarkStyle:
    """Dark theme stylesheet for the application"""
    
    STYLESHEET = f"""
        QMainWindow, QDialog {{
            background-color: {Colors.BG_DARK};
            color: {Colors.TEXT_BRIGHT};
        }}
        
        QWidget {{
            color: {Colors.TEXT_BRIGHT};
            font-family: 'Segoe UI', Arial, sans-serif;
        }}
        
        QPushButton {{
            background-color: {Colors.BG_MEDIUM};
            color: {Colors.TEXT_BRIGHT};
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }}
        
        QPushButton:hover {{
            background-color: {Colors.BG_LIGHT};
        }}
        
        QPushButton:pressed {{
            background-color: {Colors.PRIMARY};
        }}
        
        QLabel {{
            color: {Colors.TEXT_BRIGHT};
        }}
        
        QSlider::groove:horizontal {{
            border: none;
            height: 8px;
            background: {Colors.BG_MEDIUM};
            border-radius: 4px;
        }}
        
        QSlider::handle:horizontal {{
            background: {Colors.ACCENT};
            border: none;
            width: 18px;
            height: 18px;
            margin: -5px 0;
            border-radius: 9px;
        }}
        
        QSlider::groove:vertical {{
            border: none;
            width: 8px;
            background: {Colors.BG_MEDIUM};
            border-radius: 4px;
        }}
        
        QSlider::handle:vertical {{
            background: {Colors.ACCENT};
            border: none;
            width: 18px;
            height: 18px;
            margin: 0 -5px;
            border-radius: 9px;
        }}
        
        QLineEdit, QTextEdit, QComboBox {{
            background-color: {Colors.BG_MEDIUM};
            color: {Colors.TEXT_BRIGHT};
            border: 1px solid {Colors.BG_LIGHT};
            border-radius: 4px;
            padding: 6px;
        }}
        
        QTabWidget::pane {{
            border: 1px solid {Colors.BG_LIGHT};
            border-radius: 4px;
            background-color: {Colors.BG_DARK};
        }}
        
        QTabBar::tab {{
            background-color: {Colors.BG_MEDIUM};
            color: {Colors.TEXT_MEDIUM};
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            padding: 8px 16px;
            margin-right: 2px;
        }}
        
        QTabBar::tab:selected {{
            background-color: {Colors.PRIMARY};
            color: {Colors.TEXT_BRIGHT};
        }}
        
        QScrollBar:vertical {{
            border: none;
            background: {Colors.BG_DARK};
            width: 12px;
            margin: 0px;
        }}
        
        QScrollBar::handle:vertical {{
            background: {Colors.BG_LIGHT};
            min-height: 30px;
            border-radius: 6px;
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        QScrollBar:horizontal {{
            border: none;
            background: {Colors.BG_DARK};
            height: 12px;
            margin: 0px;
        }}
        
        QScrollBar::handle:horizontal {{
            background: {Colors.BG_LIGHT};
            min-width: 30px;
            border-radius: 6px;
        }}
        
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}
        
        QMenu {{
            background-color: {Colors.BG_MEDIUM};
            color: {Colors.TEXT_BRIGHT};
            border: 1px solid {Colors.BG_LIGHT};
            border-radius: 4px;
        }}
        
        QMenu::item {{
            padding: 6px 20px;
        }}
        
        QMenu::item:selected {{
            background-color: {Colors.PRIMARY};
        }}
        
        QMenuBar {{
            background-color: {Colors.BG_DARK};
            color: {Colors.TEXT_BRIGHT};
        }}
        
        QMenuBar::item:selected {{
            background-color: {Colors.BG_MEDIUM};
        }}
    """
