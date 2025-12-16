"""Main Window UI for EyeCare AI Agent"""
import logging
import customtkinter as ctk
from datetime import datetime, timedelta
from typing import Optional
from pathlib import Path

# Setup file logging
log_dir = Path(__file__).parent.parent.parent / "logs"
log_dir.mkdir(exist_ok=True)
file_handler = logging.FileHandler(log_dir / "ui.log")
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))


class MainWindow:
    """Main application window with modern UI"""
    
    def __init__(self, root: ctk.CTk, agent, config):
        """
        Initialize main window
        
        Args:
            root: CTk root window
            agent: EyeCareAIAgent instance
            config: ConfigManager instance
        """
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(file_handler)
        self.root = root
        self.agent = agent
        self.config = config

        # Force light theme for a clean white UI
        try:
            ctk.set_appearance_mode("light")
            self.root.configure(fg_color="#f7f7f7")
        except Exception:
            pass
        
        self.logger.info("Setting agent callback...")
        # Set agent callback
        self.agent.set_ui_callback(self._on_agent_update)
        
        self.logger.info("Building UI...")
        # Build UI
        self._build_ui()
        
        self.logger.info("Starting update loop...")
        # DISABLED: Update loop was causing freezing
        # Let the break scheduler and notifier handle everything
        # The break modal will popup via _on_agent_update callback
        
        # Simple timer that updates UI without blocking
        self._update_timer_simple()
        
        self.logger.info("Main window initialized")
    
    def _update_timer_simple(self):
        """Simple non-blocking timer update"""
        try:
            # If light monitor is disabled, update card once
            if not getattr(self.agent, 'light_monitor', None):
                try:
                    self.light_card.value_label.configure(text="DISABLED")
                except:
                    pass
            # Just update the break timer from scheduler
            if self.agent and hasattr(self.agent, 'scheduler') and self.agent.scheduler:
                if self.agent.scheduler.running:
                    remaining = self.agent.scheduler.get_time_until_break()
                    if remaining:
                        if hasattr(remaining, 'total_seconds'):
                            remaining = remaining.total_seconds()
                        # Clamp to a sane range to avoid huge numbers
                        try:
                            max_interval = self.agent.scheduler.work_interval.total_seconds()
                        except Exception:
                            max_interval = 3600
                        remaining = max(0, min(float(remaining), max_interval))
                        minutes = int(remaining // 60)
                        seconds = int(remaining % 60)
                        self.break_card.value_label.configure(text=f"{minutes:02d}:{seconds:02d}")
                        self.status_card.value_label.configure(text="ACTIVE")
                    else:
                        self.status_card.value_label.configure(text="STOPPED")
                else:
                    self.status_card.value_label.configure(text="STOPPED")
        except:
            pass  # Silent fail to not freeze UI
        
        # Schedule next update (super fast, no blocking)
        try:
            self.root.after(500, self._update_timer_simple)  # Update every 500ms
        except:
            pass
    
    def _build_ui(self):
        """Build the user interface"""
        
        # Configure grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Title bar frame
        self._build_title_bar()
        
        # Main content
        self._build_main_content()
        
        # Bottom controls
        self._build_bottom_controls()
    
    def _build_title_bar(self):
        """Build title bar with app name and controls"""
        
        title_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        title_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        # App title
        title_label = ctk.CTkLabel(
            title_frame,
            text="👁️✨ EyeCare AI Pro",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(side="left")
        
        # Theme toggle button
        theme_btn = ctk.CTkButton(
            title_frame,
            text="🌙",
            width=40,
            command=self._toggle_theme
        )
        theme_btn.pack(side="right", padx=5)
        
        # Settings button
        settings_btn = ctk.CTkButton(
            title_frame,
            text="⚙️",
            width=40,
            command=self._show_settings
        )
        settings_btn.pack(side="right")
    
    def _build_main_content(self):
        """Build main content area"""
        
        content_frame = ctk.CTkFrame(self.root)
        content_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        content_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Status cards
        self._build_status_cards(content_frame)
        
        # Monitoring section
        self._build_monitoring_section(content_frame)
        
        # AI Recommendations section
        self._build_ai_section(content_frame)
    
    def _build_status_cards(self, parent):
        """Build status indicator cards"""
        
        cards_frame = ctk.CTkFrame(parent, fg_color="transparent")
        cards_frame.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
        cards_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Status card
        self.status_card = self._create_card(
            cards_frame, "🔵 STATUS", "ACTIVE", 0
        )
        
        # Light card
        self.light_card = self._create_card(
            cards_frame, "💡 LIGHT", "CHECKING...", 1
        )
        
        # Eye strain card
        self.strain_card = self._create_card(
            cards_frame, "👁️ EYE STRAIN", "LOW", 2
        )
        
        # Next break card
        self.break_card = self._create_card(
            cards_frame, "⏱️ NEXT BREAK", "00:00", 3
        )
    
    def _create_card(self, parent, title: str, value: str, column: int):
        """Create a status card"""
        
        card = ctk.CTkFrame(parent)
        card.grid(row=0, column=column, padx=5, pady=5, sticky="ew")
        
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=10, weight="bold")
        )
        title_label.pack(pady=(10, 5))
        
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=16)
        )
        value_label.pack(pady=(0, 10))
        
        # Store reference to value label
        card.value_label = value_label
        
        return card
    
    def _build_monitoring_section(self, parent):
        """Build real-time monitoring section"""
        
        monitor_frame = ctk.CTkFrame(parent)
        monitor_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
        
        title = ctk.CTkLabel(
            monitor_frame,
            text="📊 REAL-TIME MONITORING",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Light level progress
        self._create_progress_bar(
            monitor_frame,
            "Light Level:",
            "light_progress"
        )
        
        # Screen time progress
        self._create_progress_bar(
            monitor_frame,
            "Screen Time Today:",
            "screen_progress"
        )
        
        # Eye strain progress
        self._create_progress_bar(
            monitor_frame,
            "Eye Strain Risk:",
            "strain_progress"
        )
    
    def _create_progress_bar(self, parent, label: str, attr_name: str):
        """Create a labeled progress bar"""
        
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=5)
        
        # Label
        label_widget = ctk.CTkLabel(
            frame,
            text=label,
            font=ctk.CTkFont(size=12)
        )
        label_widget.pack(side="left")
        
        # Value label
        value_label = ctk.CTkLabel(
            frame,
            text="0/100",
            font=ctk.CTkFont(size=10)
        )
        value_label.pack(side="right")
        
        # Progress bar
        progress = ctk.CTkProgressBar(parent)
        progress.pack(fill="x", padx=15, pady=(0, 10))
        progress.set(0)
        
        # Store references
        setattr(self, attr_name, progress)
        setattr(self, f"{attr_name}_label", value_label)
    
    def _build_ai_section(self, parent):
        """Build AI recommendations section"""
        
        ai_frame = ctk.CTkFrame(parent)
        ai_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
        
        title = ctk.CTkLabel(
            ai_frame,
            text="🤖 AI RECOMMENDATIONS",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Recommendation text
        self.recommendation_text = ctk.CTkTextbox(
            ai_frame,
            height=100,
            wrap="word"
        )
        self.recommendation_text.pack(fill="both", padx=15, pady=(0, 15))
        self.recommendation_text.insert("1.0", "💡 Starting AI analysis...\n\nMonitoring your environment for optimal eye care recommendations.")
    
    def _build_bottom_controls(self):
        """Build bottom control buttons"""
        
        controls_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        controls_frame.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="ew")
        
        # Take Break Now button
        break_btn = ctk.CTkButton(
            controls_frame,
            text="🛑 Take Break Now",
            command=self._trigger_break,
            height=40
        )
        break_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        # Pause button
        self.pause_btn = ctk.CTkButton(
            controls_frame,
            text="⏸️ Pause (1 hour)",
            command=self._pause_hour,
            height=40
        )
        self.pause_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        # Analytics button
        analytics_btn = ctk.CTkButton(
            controls_frame,
            text="📊 Analytics",
            command=self._show_analytics,
            height=40
        )
        analytics_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        # Light Check button
        light_btn = ctk.CTkButton(
            controls_frame,
            text="💡 Check Light",
            command=self._check_light,
            height=40
        )
        light_btn.pack(side="left", padx=5, expand=True, fill="x")
    
    def _update_display(self):
        """Update display with current data (lightweight)"""
        
        # Immediately yield to keep UI responsive
        self.root.update_idletasks()
        
        try:
            # Only update if agent is ready
            if not self.agent or not hasattr(self.agent, 'scheduler'):
                return
            
            # Get status quickly (with timeout protection)
            try:
                status = self.agent.get_status()
            except:
                return  # Skip this update if status unavailable
            
            # Update status card
            agent_status = status.get('agent', {})
            if agent_status.get('paused'):
                self.status_card.value_label.configure(text="PAUSED")
            elif agent_status.get('running'):
                self.status_card.value_label.configure(text="ACTIVE")
            else:
                self.status_card.value_label.configure(text="STOPPED")
            
            # Update light card
            light_status = status.get('light', {})
            lux = light_status.get('lux', 0)
            light_state = light_status.get('status', 'unknown').upper()
            self.light_card.value_label.configure(text=f"{int(lux)} lux\n{light_state}")
            
            # Update next break timer
            scheduler_status = status.get('scheduler', {})
            time_until = scheduler_status.get('time_until_break_seconds', 0)
            
            # Handle both int and timedelta
            if hasattr(time_until, 'total_seconds'):
                time_until = time_until.total_seconds()
            
            minutes = int(time_until // 60)
            seconds = int(time_until % 60)
            self.break_card.value_label.configure(text=f"{minutes:02d}:{seconds:02d}")
            
            # Update strain (simple calculation)
            self.strain_card.value_label.configure(text="LOW")
            
        except Exception as e:
            self.logger.debug(f"Error updating display: {e}")
    
    def _on_agent_update(self, data: dict):
        """Handle updates from agent (thread-safe)"""
        
        update_type = data.get('type', 'unknown')
        self.logger.info(f"<<< _on_agent_update received: {update_type} >>>")
        
        # Always marshal to main thread for Tk operations
        try:
            if not self.root or not self.root.winfo_exists():
                self.logger.warning("Root window missing; cannot process UI update")
                return

            if update_type == 'break_due':
                self.logger.info("BREAK DUE - scheduling modal on main thread")
                self.root.after(0, lambda: self._show_break_modal(data.get('data', {})))
            else:
                self.root.after(0, self._process_agent_update, data)
            self.logger.info(f"Scheduled UI work for {update_type}")
        except Exception as e:
            self.logger.error(f"Failed to schedule update: {e}", exc_info=True)

    def _process_agent_update(self, data: dict):
        """Process agent updates on main thread"""

        update_type = data.get('type')
        self.logger.info(f"### Processing agent update: {update_type} ###")

        try:
            if update_type == 'light_update':
                light_data = data.get('data', {})
                recommendation = light_data.get('recommendation')

                if recommendation and hasattr(recommendation, 'recommendation'):
                    self._update_recommendation(recommendation.recommendation)
            elif update_type == 'break_due':
                # Fallback in case it ever routes here
                self._show_break_modal(data.get('data', {}))
        except Exception as e:
            self.logger.error(f"!!! ERROR processing agent update: {e} !!!", exc_info=True)
    
    def _update_recommendation(self, text: str):
        """Update AI recommendation text"""
        
        try:
            self.recommendation_text.delete("1.0", "end")
            self.recommendation_text.insert("1.0", text)
        except Exception as e:
            self.logger.error(f"Error updating recommendation: {e}")
    
    def _show_break_modal(self, data: dict):
        """Show break reminder modal with 20-second countdown"""
        try:
            if not self.root or not self.root.winfo_exists():
                self.logger.warning("Root window not available; skipping break modal")
                return

            self.logger.info("Creating break modal...")
            
            # Pause scheduler for the break
            if self.agent and self.agent.scheduler:
                self.agent.scheduler.pause()
                self.logger.info("Scheduler paused for break")
            
            # Create modal window
            modal = ctk.CTkToplevel(self.root)
            modal.title("Break Time!")
            modal.geometry("500x450")
            modal.attributes('-topmost', True)
            modal.grab_set()  # Grab focus
            
            # Center on screen
            modal.update_idletasks()
            
            self.logger.info("Modal window created")
            
            # Title
            title = ctk.CTkLabel(
                modal,
                text="TAKE A BREAK",
                font=ctk.CTkFont(size=48, weight="bold"),
                text_color="#FF6B6B"
            )
            title.pack(pady=20)
            
            # Instructions
            instructions = ctk.CTkLabel(
                modal,
                text="Look away from the screen\nFocus on something 20 feet away\nFor 20 seconds",
                font=ctk.CTkFont(size=13),
                justify="center"
            )
            instructions.pack(pady=15)
            
            # Countdown display
            countdown_label = ctk.CTkLabel(
                modal,
                text="20",
                font=ctk.CTkFont(size=80, weight="bold"),
                text_color="#4CAF50"
            )
            countdown_label.pack(pady=20)
            
            # Status text
            status_text = ctk.CTkLabel(
                modal,
                text="seconds",
                font=ctk.CTkFont(size=14)
            )
            status_text.pack()
            
            # Skip button
            def close_modal():
                try:
                    modal.destroy()
                    if self.agent and self.agent.scheduler:
                        self.agent.scheduler.resume()
                    if self.agent:
                        self.agent.record_break_skipped()
                except:
                    pass
            
            skip_btn = ctk.CTkButton(
                modal,
                text="Skip Break",
                command=close_modal,
                fg_color="#555",
                width=180,
                height=40
            )
            skip_btn.pack(pady=15)
            
            # Window close button handler
            modal.protocol("WM_DELETE_WINDOW", close_modal)
            
            # Store references for countdown
            self.break_modal = modal
            self.break_countdown_label = countdown_label
            self.break_status_label = status_text
            self.break_countdown = 20
            self.break_countdown_active = True
            self.break_end_ts = None

            self.logger.info("Starting break countdown...")
            # Drift-resistant countdown using monotonic clock
            import time
            self.break_end_ts = time.monotonic() + 20
            self._update_break_countdown()
            
        except Exception as e:
            self.logger.error(f"Failed to show break modal: {e}", exc_info=True)
            try:
                if self.agent and self.agent.scheduler:
                    self.agent.scheduler.resume()
            except:
                pass
    
    def _update_break_countdown(self):
        """Update break countdown using Tk after and monotonic clock"""
        try:
            if not hasattr(self, 'break_modal') or not self.break_modal.winfo_exists():
                return

            if not self.break_countdown_active:
                return

            import time
            remaining = int(round(self.break_end_ts - time.monotonic())) if self.break_end_ts else self.break_countdown
            remaining = max(0, min(remaining, 20))

            self.break_countdown = remaining

            if hasattr(self, 'break_countdown_label'):
                self.break_countdown_label.configure(text=str(remaining))

            if remaining > 0:
                self.root.after(250, self._update_break_countdown)
            else:
                # Finished
                if hasattr(self, 'break_countdown_label'):
                    self.break_countdown_label.configure(text="✓")
                if hasattr(self, 'break_status_label'):
                    self.break_status_label.configure(text="Great job!")
                self.root.after(800, self._close_break_modal)

        except Exception as e:
            self.logger.error(f"Error in countdown: {e}", exc_info=True)
            self._close_break_modal()
    
    def _close_break_modal(self):
        """Close break modal and resume scheduler"""
        try:
            if hasattr(self, 'break_modal') and self.break_modal.winfo_exists():
                self.break_modal.destroy()
        except:
            pass
        
        # Resume scheduler
        try:
            if self.agent and self.agent.scheduler:
                self.agent.scheduler.resume()
            if self.agent:
                self.agent.record_break_completed()
            self.logger.info("Break completed and scheduler resumed")
        except Exception as e:
            self.logger.error(f"Error closing break: {e}", exc_info=True)
    
    def _trigger_break(self):
        """Trigger a break immediately"""
        self.agent.trigger_break_now()
    
    def _pause_hour(self):
        """Pause for one hour"""
        self.agent.pause(3600)
        self.pause_btn.configure(text="▶️ Resume")
        
        # Change button to resume after pause
        def resume():
            self.agent.resume()
            self.pause_btn.configure(text="⏸️ Pause (1 hour)", command=self._pause_hour)
        
        self.pause_btn.configure(command=resume)
    
    def _check_light(self):
        """Perform manual light check"""
        
        result = self.agent.manual_light_check()
        
        # Show result in a dialog
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Light Analysis")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        
        lux = result.get('lux', 0)
        status = result.get('status', 'unknown')
        recommended_brightness = result.get('recommended_brightness', 65)
        
        text = f"Light Level: {lux:.0f} lux\n"
        text += f"Status: {status.upper()}\n\n"
        text += f"Recommended Screen Brightness: {recommended_brightness}%"
        
        label = ctk.CTkLabel(dialog, text=text, font=ctk.CTkFont(size=14))
        label.pack(pady=40)
        
        close_btn = ctk.CTkButton(dialog, text="Close", command=dialog.destroy)
        close_btn.pack(pady=20)
    
    def _show_analytics(self):
        """Show analytics window"""
        
        stats = self.agent.get_statistics()
        
        # Create analytics window
        analytics_window = ctk.CTkToplevel(self.root)
        analytics_window.title("Analytics")
        analytics_window.geometry("600x400")
        analytics_window.transient(self.root)
        
        # Display statistics
        text_widget = ctk.CTkTextbox(analytics_window)
        text_widget.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Format statistics
        today = stats.get('today', {})
        text = f"📊 Today's Statistics\n\n"
        text += f"Screen Time: {today.get('screen_time_minutes', 0):.0f} minutes\n"
        text += f"Total Breaks: {today.get('total_breaks', 0)}\n"
        text += f"Compliance Rate: {today.get('compliance_rate', 0):.0f}%\n"
        text += f"Average Light: {today.get('average_light_lux', 0):.0f} lux\n"
        
        text_widget.insert("1.0", text)
    
    def _show_settings(self):
        """Show settings window"""
        
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("500x400")
        settings_window.transient(self.root)
        
        label = ctk.CTkLabel(
            settings_window,
            text="⚙️ Settings",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        label.pack(pady=20)
        
        # Add settings controls here
        info = ctk.CTkLabel(
            settings_window,
            text="Settings panel - Coming soon!\n\n"
                 "Current config can be edited in config.json"
        )
        info.pack(pady=20)
    
    def _toggle_theme(self):
        """Toggle between dark and light themes"""
        
        current = self.config.get('ui_settings.theme', 'dark')
        new_theme = 'light' if current == 'dark' else 'dark'
        
        ctk.set_appearance_mode(new_theme)
        self.config.set('ui_settings.theme', new_theme)
        
        self.logger.info(f"Theme changed to {new_theme}")
    
    def show_panel(self, panel_name: str):
        """Show a specific panel (for system tray integration)"""
        
        if panel_name == "light_analysis":
            self._check_light()
        elif panel_name == "analytics":
            self._show_analytics()
        elif panel_name == "settings":
            self._show_settings()

