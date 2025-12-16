"""Theme Manager for CustomTkinter"""
import customtkinter as ctk
from typing import Dict, Literal
import logging


class ThemeManager:
    """Manages application themes and colors"""
    
    THEMES = {
        "dark": {
            "mode": "dark",
            "colors": {
                "primary": "#1f6feb",
                "secondary": "#238636",
                "background": "#0d1117",
                "surface": "#161b22",
                "surface_variant": "#21262d",
                "text": "#c9d1d9",
                "text_secondary": "#8b949e",
                "error": "#f85149",
                "warning": "#d29922",
                "success": "#3fb950",
                "border": "#30363d"
            }
        },
        "light": {
            "mode": "light",
            "colors": {
                "primary": "#0969da",
                "secondary": "#1a7f37",
                "background": "#ffffff",
                "surface": "#f6f8fa",
                "surface_variant": "#eaeef2",
                "text": "#24292f",
                "text_secondary": "#57606a",
                "error": "#cf222e",
                "warning": "#9a6700",
                "success": "#1a7f37",
                "border": "#d0d7de"
            }
        }
    }
    
    # Light status colors (consistent across themes)
    LIGHT_STATUS_COLORS = {
        'optimal': '#10b981',      # Green
        'low': '#f59e0b',          # Amber
        'very_low': '#ef4444',     # Red
        'high': '#8b5cf6',         # Purple
        'changing': '#3b82f6'      # Blue
    }
    
    def __init__(self, theme: Literal["dark", "light"] = "dark"):
        self.logger = logging.getLogger(__name__)
        self.current_theme = theme
        self._apply_theme(theme)
    
    def _apply_theme(self, theme: str):
        """Apply theme to application"""
        if theme not in self.THEMES:
            self.logger.warning(f"Unknown theme: {theme}, using dark")
            theme = "dark"
        
        ctk.set_appearance_mode(self.THEMES[theme]["mode"])
        self.current_theme = theme
        self.logger.info(f"Applied theme: {theme}")
    
    def get_color(self, color_name: str) -> str:
        """Get color value from current theme"""
        return self.THEMES[self.current_theme]["colors"].get(color_name, "#ffffff")
    
    def get_light_status_color(self, status: str) -> str:
        """Get color for light status"""
        return self.LIGHT_STATUS_COLORS.get(status, "#6b7280")
    
    def toggle_theme(self):
        """Toggle between dark and light themes"""
        new_theme = "light" if self.current_theme == "dark" else "dark"
        self._apply_theme(new_theme)
        return new_theme
    
    def set_theme(self, theme: str):
        """Set specific theme"""
        self._apply_theme(theme)
    
    @staticmethod
    def get_icon_for_status(status: str) -> str:
        """Get emoji icon for light status"""
        icons = {
            'optimal': '🟢',
            'low': '🟡',
            'very_low': '🔴',
            'high': '🟣',
            'changing': '🔵'
        }
        return icons.get(status, '⚪')
