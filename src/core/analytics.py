"""Analytics and Data Tracking"""
import logging
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import sqlite3
from dataclasses import dataclass, asdict


@dataclass
class SessionData:
    """Data for a work session"""
    session_id: str
    start_time: datetime
    end_time: Optional[datetime]
    breaks_offered: int
    breaks_completed: int
    breaks_skipped: int
    average_light_lux: float
    screen_time_minutes: float
    eye_strain_level: str


class Analytics:
    """Analytics and data tracking system"""
    
    def __init__(self, config: dict):
        """Initialize analytics system"""
        
        self.logger = logging.getLogger(__name__)
        self.config = config
        
        # Settings
        self.enabled = config.get('enabled', True)
        self.track_screen_time = config.get('track_screen_time', True)
        self.track_breaks = config.get('track_break_compliance', True)
        self.track_light = config.get('track_light_conditions', True)
        
        # Data directory
        self.data_dir = Path.home() / '.eyecare_agent' / 'data'
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Database
        self.db_path = self.data_dir / 'analytics.db'
        self._init_database()
        
        # Current session
        self.current_session_id = self._generate_session_id()
        self.session_start = datetime.now()
        self.session_data = {
            'breaks_offered': 0,
            'breaks_completed': 0,
            'breaks_skipped': 0,
            'light_readings': [],
            'screen_time_seconds': 0
        }
        
        self.logger.info(f"Analytics initialized (Session: {self.current_session_id})")
    
    def _init_database(self):
        """Initialize SQLite database"""
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    date TEXT,
                    start_time TEXT,
                    end_time TEXT,
                    duration_minutes REAL,
                    breaks_offered INTEGER,
                    breaks_completed INTEGER,
                    breaks_skipped INTEGER,
                    compliance_rate REAL,
                    average_light_lux REAL,
                    eye_strain_level TEXT
                )
            ''')
            
            # Light readings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS light_readings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    timestamp TEXT,
                    lux REAL,
                    status TEXT,
                    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
                )
            ''')
            
            # Break events table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS break_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    timestamp TEXT,
                    event_type TEXT,
                    duration_seconds INTEGER,
                    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
                )
            ''')
            
            # Daily summaries table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS daily_summaries (
                    date TEXT PRIMARY KEY,
                    total_screen_time_minutes REAL,
                    total_breaks INTEGER,
                    compliance_rate REAL,
                    average_light_lux REAL,
                    sessions_count INTEGER
                )
            ''')
            
            conn.commit()
            conn.close()
            
            self.logger.info("Analytics database initialized")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize database: {e}")
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        return f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def record_break_offered(self):
        """Record that a break was offered"""
        if not self.enabled or not self.track_breaks:
            return
        
        self.session_data['breaks_offered'] += 1
        self._save_break_event('offered')
    
    def record_break_completed(self, duration_seconds: int = 20):
        """Record that a break was completed"""
        if not self.enabled or not self.track_breaks:
            return
        
        self.session_data['breaks_completed'] += 1
        self._save_break_event('completed', duration_seconds)
    
    def record_break_skipped(self):
        """Record that a break was skipped"""
        if not self.enabled or not self.track_breaks:
            return
        
        self.session_data['breaks_skipped'] += 1
        self._save_break_event('skipped')
    
    def record_light_reading(self, lux: float, status: str):
        """Record ambient light reading"""
        if not self.enabled or not self.track_light:
            return
        
        self.session_data['light_readings'].append({
            'timestamp': datetime.now(),
            'lux': lux,
            'status': status
        })
        
        # Save to database
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO light_readings (session_id, timestamp, lux, status)
                VALUES (?, ?, ?, ?)
            ''', (
                self.current_session_id,
                datetime.now().isoformat(),
                lux,
                status
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Failed to record light reading: {e}")
    
    def _save_break_event(self, event_type: str, duration: int = 0):
        """Save break event to database"""
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO break_events (session_id, timestamp, event_type, duration_seconds)
                VALUES (?, ?, ?, ?)
            ''', (
                self.current_session_id,
                datetime.now().isoformat(),
                event_type,
                duration
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Failed to save break event: {e}")
    
    def end_session(self):
        """End current session and save data"""
        
        if not self.enabled:
            return
        
        session_end = datetime.now()
        duration = session_end - self.session_start
        
        # Calculate statistics
        breaks_offered = self.session_data['breaks_offered']
        breaks_completed = self.session_data['breaks_completed']
        
        compliance_rate = 0.0
        if breaks_offered > 0:
            compliance_rate = (breaks_completed / breaks_offered) * 100
        
        # Calculate average light
        light_readings = self.session_data['light_readings']
        avg_light = 0.0
        if light_readings:
            avg_light = sum(r['lux'] for r in light_readings) / len(light_readings)
        
        # Save session to database
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO sessions (
                    session_id, date, start_time, end_time, duration_minutes,
                    breaks_offered, breaks_completed, breaks_skipped,
                    compliance_rate, average_light_lux, eye_strain_level
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.current_session_id,
                self.session_start.date().isoformat(),
                self.session_start.isoformat(),
                session_end.isoformat(),
                duration.total_seconds() / 60,
                breaks_offered,
                breaks_completed,
                self.session_data['breaks_skipped'],
                compliance_rate,
                avg_light,
                'unknown'  # TODO: Calculate eye strain level
            ))
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Session ended: {self.current_session_id}")
            
            # Update daily summary
            self._update_daily_summary()
            
        except Exception as e:
            self.logger.error(f"Failed to save session: {e}")
    
    def _update_daily_summary(self):
        """Update or create daily summary"""
        
        try:
            today = datetime.now().date().isoformat()
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get today's data
            cursor.execute('''
                SELECT 
                    SUM(duration_minutes),
                    SUM(breaks_offered),
                    AVG(compliance_rate),
                    AVG(average_light_lux),
                    COUNT(*)
                FROM sessions
                WHERE date = ?
            ''', (today,))
            
            row = cursor.fetchone()
            
            if row:
                total_minutes, total_breaks, avg_compliance, avg_light, session_count = row
                
                # Insert or replace daily summary
                cursor.execute('''
                    INSERT OR REPLACE INTO daily_summaries (
                        date, total_screen_time_minutes, total_breaks,
                        compliance_rate, average_light_lux, sessions_count
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    today,
                    total_minutes or 0,
                    total_breaks or 0,
                    avg_compliance or 0,
                    avg_light or 0,
                    session_count or 0
                ))
                
                conn.commit()
            
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Failed to update daily summary: {e}")
    
    def get_today_statistics(self) -> Dict:
        """Get statistics for today"""
        
        try:
            today = datetime.now().date().isoformat()
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    total_screen_time_minutes,
                    total_breaks,
                    compliance_rate,
                    average_light_lux,
                    sessions_count
                FROM daily_summaries
                WHERE date = ?
            ''', (today,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return {
                    'screen_time_minutes': row[0] or 0,
                    'total_breaks': row[1] or 0,
                    'compliance_rate': row[2] or 0,
                    'average_light_lux': row[3] or 0,
                    'sessions': row[4] or 0
                }
            
        except Exception as e:
            self.logger.error(f"Failed to get today's statistics: {e}")
        
        return {
            'screen_time_minutes': 0,
            'total_breaks': 0,
            'compliance_rate': 0,
            'average_light_lux': 0,
            'sessions': 0
        }
    
    def get_weekly_summary(self) -> List[Dict]:
        """Get summary for the past 7 days"""
        
        try:
            week_ago = (datetime.now() - timedelta(days=7)).date().isoformat()
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT *
                FROM daily_summaries
                WHERE date >= ?
                ORDER BY date DESC
            ''', (week_ago,))
            
            rows = cursor.fetchall()
            conn.close()
            
            summaries = []
            for row in rows:
                summaries.append({
                    'date': row[0],
                    'screen_time_minutes': row[1],
                    'total_breaks': row[2],
                    'compliance_rate': row[3],
                    'average_light_lux': row[4],
                    'sessions': row[5]
                })
            
            return summaries
            
        except Exception as e:
            self.logger.error(f"Failed to get weekly summary: {e}")
            return []
    
    def export_data(self, output_path: Optional[str] = None) -> str:
        """Export all data to JSON"""
        
        if output_path is None:
            output_path = self.data_dir / f'export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get all data
            cursor.execute('SELECT * FROM sessions')
            sessions = cursor.fetchall()
            
            cursor.execute('SELECT * FROM daily_summaries')
            daily = cursor.fetchall()
            
            conn.close()
            
            data = {
                'export_date': datetime.now().isoformat(),
                'sessions': [dict(zip(['session_id', 'date', 'start_time', 'end_time', 
                                      'duration_minutes', 'breaks_offered', 'breaks_completed',
                                      'breaks_skipped', 'compliance_rate', 'average_light_lux',
                                      'eye_strain_level'], row)) for row in sessions],
                'daily_summaries': [dict(zip(['date', 'total_screen_time_minutes', 'total_breaks',
                                            'compliance_rate', 'average_light_lux', 'sessions_count'], 
                                            row)) for row in daily]
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Data exported to {output_path}")
            return str(output_path)
            
        except Exception as e:
            self.logger.error(f"Failed to export data: {e}")
            return ""
