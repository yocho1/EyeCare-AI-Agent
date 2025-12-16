"""Intelligent Break Scheduler"""
import logging
from datetime import datetime, timedelta
from typing import Optional, Callable
from threading import Thread, Event, Lock
import time


class BreakScheduler:
    """Manages intelligent break scheduling with 20-20-20 rule"""
    
    def __init__(self, config: dict, callback: Optional[Callable] = None):
        """
        Initialize break scheduler
        
        Args:
            config: Configuration dictionary
            callback: Callback function when break is due
        """
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.callback = callback
        
        # Settings
        self.work_interval = timedelta(minutes=config.get('work_interval_minutes', 20))
        self.break_duration = config.get('break_duration_seconds', 20)
        self.enabled = config.get('enable_breaks', True)
        self.auto_pause_on_idle = config.get('auto_pause_on_idle', True)
        self.idle_threshold = timedelta(minutes=config.get('idle_threshold_minutes', 5))
        
        # State
        self.running = False
        self.paused = False
        self.thread: Optional[Thread] = None
        self.stop_event = Event()
        self.pause_event = Event()
        self.state_lock = Lock()
        
        # Timing
        self.last_break_time = datetime.now()
        self.next_break_time = self.last_break_time + self.work_interval
        self.last_activity_time = datetime.now()
        self.pause_until: Optional[datetime] = None
        
        # Statistics
        self.breaks_today = 0
        self.breaks_completed = 0
        self.breaks_skipped = 0
        self.total_work_time = timedelta()
        self.session_start = datetime.now()
    
    def start(self):
        """Start the break scheduler"""
        
        if self.running:
            self.logger.warning("Break scheduler already running")
            return
        
        self.logger.info("Starting break scheduler")
        self.running = True
        self.session_start = datetime.now()
        self.last_break_time = datetime.now()
        self.next_break_time = self.last_break_time + self.work_interval
        self.stop_event.clear()
        
        # Start scheduler thread
        self.thread = Thread(target=self._scheduler_loop, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop the break scheduler"""
        
        if not self.running:
            return
        
        self.logger.info("Stopping break scheduler")
        self.running = False
        self.stop_event.set()
        
        if self.thread:
            self.thread.join(timeout=2)
        
        # Update statistics
        session_duration = datetime.now() - self.session_start
        self.total_work_time += session_duration
        
        self.logger.info(f"Break scheduler stopped. Session duration: {session_duration}")
    
    def _scheduler_loop(self):
        """Main scheduler loop"""
        
        while self.running and not self.stop_event.is_set():
            try:
                with self.state_lock:
                    # Check if paused
                    if self.paused or (self.pause_until and datetime.now() < self.pause_until):
                        time.sleep(1)
                        continue
                    
                    # Check if temporarily paused
                    if self.pause_until and datetime.now() >= self.pause_until:
                        self.pause_until = None
                        self.logger.info("Temporary pause ended, resuming break schedule")
                    
                    # Check for idle (if enabled)
                    if self.auto_pause_on_idle:
                        idle_time = datetime.now() - self.last_activity_time
                        if idle_time > self.idle_threshold:
                            # User is idle, pause the timer
                            time.sleep(5)
                            continue
                    
                    # Check if break is due
                    now = datetime.now()
                    if now >= self.next_break_time and self.enabled:
                        self._trigger_break()
                
                time.sleep(1)  # Check every second
                
            except Exception as e:
                self.logger.error(f"Error in scheduler loop: {e}")
                time.sleep(1)
    
    def _trigger_break(self):
        """Trigger a break notification"""
        
        self.logger.info("Break time! 20-20-20 rule reminder")
        self.breaks_today += 1
        
        # Calculate next break time
        self.last_break_time = datetime.now()
        self.next_break_time = self.last_break_time + self.work_interval
        
        # Call callback if provided
        if self.callback:
            try:
                self.callback({
                    'type': 'break_reminder',
                    'duration': self.break_duration,
                    'breaks_today': self.breaks_today,
                    'next_break': self.next_break_time
                })
            except Exception as e:
                self.logger.error(f"Error in break callback: {e}")
    
    def pause(self, duration_seconds: Optional[int] = None):
        """
        Pause the scheduler
        
        Args:
            duration_seconds: If provided, pause for this many seconds. Otherwise pause indefinitely.
        """
        
        with self.state_lock:
            if duration_seconds:
                self.pause_until = datetime.now() + timedelta(seconds=duration_seconds)
                self.logger.info(f"Pausing scheduler for {duration_seconds} seconds")
            else:
                self.paused = True
                self.logger.info("Pausing scheduler indefinitely")
    
    def resume(self):
        """Resume the scheduler"""
        
        with self.state_lock:
            self.paused = False
            self.pause_until = None
            
            # Reset next break time to give user a fresh interval
            self.last_break_time = datetime.now()
            self.next_break_time = self.last_break_time + self.work_interval
            
            self.logger.info("Scheduler resumed")
    
    def record_activity(self):
        """Record user activity (resets idle timer)"""
        
        with self.state_lock:
            self.last_activity_time = datetime.now()
    
    def break_completed(self):
        """Record that a break was completed"""
        
        with self.state_lock:
            self.breaks_completed += 1
            self.logger.debug(f"Break completed. Total: {self.breaks_completed}")
    
    def break_skipped(self):
        """Record that a break was skipped"""
        
        with self.state_lock:
            self.breaks_skipped += 1
            self.logger.debug(f"Break skipped. Total: {self.breaks_skipped}")
    
    def trigger_break_now(self):
        """Manually trigger a break immediately"""
        
        with self.state_lock:
            self._trigger_break()
    
    def reset_timer(self):
        """Reset the break timer"""
        
        with self.state_lock:
            self.last_break_time = datetime.now()
            self.next_break_time = self.last_break_time + self.work_interval
            self.logger.info("Break timer reset")
    
    def get_time_until_break(self) -> timedelta:
        """Get time remaining until next break"""
        
        with self.state_lock:
            if self.paused or self.pause_until:
                return timedelta(hours=99)  # Effectively paused
            
            remaining = self.next_break_time - datetime.now()
            return remaining if remaining.total_seconds() > 0 else timedelta(0)
    
    def get_status(self) -> dict:
        """Get current scheduler status"""
        
        with self.state_lock:
            time_until_break = self.get_time_until_break()
            
            return {
                'running': self.running,
                'paused': self.paused or (self.pause_until and datetime.now() < self.pause_until),
                'enabled': self.enabled,
                'time_until_break_seconds': int(time_until_break.total_seconds()),
                'next_break_time': self.next_break_time.isoformat(),
                'breaks_today': self.breaks_today,
                'breaks_completed': self.breaks_completed,
                'breaks_skipped': self.breaks_skipped,
                'compliance_rate': self._calculate_compliance_rate(),
                'work_interval_minutes': self.work_interval.total_seconds() / 60,
                'break_duration_seconds': self.break_duration
            }
    
    def _calculate_compliance_rate(self) -> float:
        """Calculate break compliance rate"""
        
        total_breaks = self.breaks_today
        if total_breaks == 0:
            return 100.0
        
        return (self.breaks_completed / total_breaks) * 100
    
    def get_statistics(self) -> dict:
        """Get detailed statistics"""
        
        with self.state_lock:
            session_duration = datetime.now() - self.session_start
            
            return {
                'session_start': self.session_start.isoformat(),
                'session_duration_minutes': session_duration.total_seconds() / 60,
                'total_breaks_offered': self.breaks_today,
                'breaks_completed': self.breaks_completed,
                'breaks_skipped': self.breaks_skipped,
                'compliance_rate': self._calculate_compliance_rate(),
                'average_break_interval_minutes': self.work_interval.total_seconds() / 60,
                'total_break_time_minutes': (self.breaks_completed * self.break_duration) / 60
            }
    
    def update_settings(self, **kwargs):
        """Update scheduler settings"""
        
        with self.state_lock:
            if 'work_interval_minutes' in kwargs:
                self.work_interval = timedelta(minutes=kwargs['work_interval_minutes'])
                self.logger.info(f"Work interval updated to {kwargs['work_interval_minutes']} minutes")
            
            if 'break_duration_seconds' in kwargs:
                self.break_duration = kwargs['break_duration_seconds']
                self.logger.info(f"Break duration updated to {kwargs['break_duration_seconds']} seconds")
            
            if 'enable_breaks' in kwargs:
                self.enabled = kwargs['enable_breaks']
                self.logger.info(f"Breaks {'enabled' if self.enabled else 'disabled'}")
            
            # Reset timer with new settings
            self.next_break_time = datetime.now() + self.work_interval
