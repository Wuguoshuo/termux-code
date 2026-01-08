"""
Scheduler for Xiaohongshu Daily Autoposter
Manages automated daily execution with configurable timing
"""

import os
import sys
import logging
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path
from enum import Enum


class SchedulerState(Enum):
    """Scheduler state enumeration."""
    STOPPED = "stopped"
    RUNNING = "running"
    PAUSED = "paused"


class ContentCalendar:
    """Manages content scheduling and calendar operations."""
    
    def __init__(self, calendar_file: str = "./content_calendar.json"):
        """
        Initialize content calendar.
        
        Args:
            calendar_file: Path to calendar storage file
        """
        self.calendar_file = Path(calendar_file)
        self.schedule: Dict[str, Dict] = {}
        self._load_calendar()
    
    def _load_calendar(self) -> None:
        """Load calendar from file."""
        if self.calendar_file.exists():
            import json
            try:
                with open(self.calendar_file, 'r', encoding='utf-8') as f:
                    self.schedule = json.load(f)
            except Exception:
                self.schedule = {}
    
    def _save_calendar(self) -> None:
        """Save calendar to file."""
        import json
        os.makedirs(self.calendar_file.parent, exist_ok=True)
        with open(self.calendar_file, 'w', encoding='utf-8') as f:
            json.dump(self.schedule, f, ensure_ascii=False, indent=2)
    
    def add_post(self, date: str, topic: str, metadata: Dict = None) -> bool:
        """
        Add a scheduled post to the calendar.
        
        Args:
            date: Date string (YYYY-MM-DD)
            topic: Content topic
            metadata: Additional metadata
            
        Returns:
            True if successful
        """
        self.schedule[date] = {
            'topic': topic,
            'status': 'scheduled',
            'created_at': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        self._save_calendar()
        return True
    
    def remove_post(self, date: str) -> bool:
        """
        Remove a scheduled post from the calendar.
        
        Args:
            date: Date string (YYYY-MM-DD)
            
        Returns:
            True if post was removed
        """
        if date in self.schedule:
            del self.schedule[date]
            self._save_calendar()
            return True
        return False
    
    def get_post(self, date: str) -> Optional[Dict]:
        """
        Get scheduled post for a specific date.
        
        Args:
            date: Date string (YYYY-MM-DD)
            
        Returns:
            Post dictionary or None
        """
        return self.schedule.get(date)
    
    def get_schedule(self, month: str = None) -> Dict[str, Dict]:
        """
        Get schedule for a specific month.
        
        Args:
            month: Month string (YYYY-MM), or current month if None
            
        Returns:
            Dictionary of scheduled posts
        """
        if month is None:
            month = datetime.now().strftime('%Y-%m')
        
        return {date: post for date, post in self.schedule.items() 
                if date.startswith(month)}
    
    def get_upcoming(self, days: int = 7) -> List[Dict]:
        """
        Get upcoming scheduled posts.
        
        Args:
            days: Number of days to look ahead
            
        Returns:
            List of upcoming posts
        """
        today = datetime.now().date()
        upcoming = []
        
        for i in range(days):
            check_date = today + timedelta(days=i)
            date_str = check_date.strftime('%Y-%m-%d')
            
            if date_str in self.schedule:
                upcoming.append({
                    'date': date_str,
                    **self.schedule[date_str]
                })
        
        return upcoming
    
    def mark_completed(self, date: str) -> bool:
        """
        Mark a post as completed.
        
        Args:
            date: Date string (YYYY-MM-DD)
            
        Returns:
            True if successful
        """
        if date in self.schedule:
            self.schedule[date]['status'] = 'completed'
            self.schedule[date]['completed_at'] = datetime.now().isoformat()
            self._save_calendar()
            return True
        return False
    
    def export_ics(self, output_path: str) -> str:
        """
        Export calendar to iCal format.
        
        Args:
            output_path: Output file path
            
        Returns:
            Path to exported file
        """
        lines = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//Xiaohongshu Autoposter//EN",
            "CALSCALE:GREGORIAN",
            "METHOD:PUBLISH"
        ]
        
        for date, post in self.schedule.items():
            dt_start = date.replace('-', '') + "T080000"
            lines.extend([
                "BEGIN:VEVENT",
                f"DTSTART;VALUE=DATE:{dt_start[:8]}",
                f"SUMMARY:小红书发布 - {post['topic']}",
                f"DESCRIPTION:状态: {post['status']}",
                "END:VEVENT"
            ])
        
        lines.extend(["END:VCALENDAR"])
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        return output_path


class Scheduler:
    """Main scheduler for automated content generation."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize scheduler.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.state = SchedulerState.STOPPED
        self.calendar = ContentCalendar()
        
        # Setup logging
        self.log_file = self.config.get('log_file', './logs/scheduler.log')
        self.log_level = getattr(logging, self.config.get('log_level', 'INFO'))
        self._setup_logging()
        
        # Task tracking
        self.current_task: Optional[threading.Thread] = None
        self.stop_event = threading.Event()
        self.schedule_lock = threading.Lock()
    
    def _setup_logging(self) -> None:
        """Setup logging configuration."""
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
        logging.basicConfig(
            level=self.log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger('XiaohongshuScheduler')
    
    def start(self, time_str: str = "08:00", callback: Callable = None) -> bool:
        """
        Start the scheduler.
        
        Args:
            time_str: Daily execution time (HH:MM)
            callback: Optional callback function for post-generation
            
        Returns:
            True if started successfully
        """
        if self.state == SchedulerState.RUNNING:
            self.logger.warning("Scheduler is already running")
            return False
        
        self.state = SchedulerState.RUNNING
        self.stop_event.clear()
        
        self.logger.info(f"Starting scheduler with daily execution at {time_str}")
        
        # Start scheduler thread
        self.current_task = threading.Thread(
            target=self._run_scheduler,
            args=(time_str, callback),
            daemon=True
        )
        self.current_task.start()
        
        return True
    
    def stop(self) -> bool:
        """
        Stop the scheduler.
        
        Returns:
            True if stopped successfully
        """
        if self.state == SchedulerState.STOPPED:
            return True
        
        self.logger.info("Stopping scheduler...")
        self.stop_event.set()
        
        if self.current_task and self.current_task.is_alive():
            self.current_task.join(timeout=5)
        
        self.state = SchedulerState.STOPPED
        self.logger.info("Scheduler stopped")
        
        return True
    
    def pause(self) -> bool:
        """
        Pause the scheduler.
        
        Returns:
            True if paused successfully
        """
        if self.state != SchedulerState.RUNNING:
            return False
        
        self.state = SchedulerState.PAUSED
        self.logger.info("Scheduler paused")
        return True
    
    def resume(self) -> bool:
        """
        Resume the scheduler.
        
        Returns:
            True if resumed successfully
        """
        if self.state != SchedulerState.PAUSED:
            return False
        
        self.state = SchedulerState.RUNNING
        self.logger.info("Scheduler resumed")
        return True
    
    def _run_scheduler(self, time_str: str, callback: Callable = None) -> None:
        """Main scheduler loop."""
        from autoposter import run_daily_post
        
        self.logger.info(f"Scheduler loop started for time {time_str}")
        
        while not self.stop_event.is_set():
            try:
                now = datetime.now()
                target_time = datetime.strptime(time_str, "%H:%M").time()
                
                # Calculate next run time
                next_run = datetime.combine(now.date(), target_time)
                if now >= next_run:
                    next_run += timedelta(days=1)
                
                # Wait until target time
                wait_seconds = (next_run - now).total_seconds()
                
                self.logger.debug(f"Next run in {wait_seconds} seconds")
                
                # Wait with periodic checks
                while wait_seconds > 0 and not self.stop_event.is_set():
                    time.sleep(min(60, wait_seconds))
                    wait_seconds -= 60
                
                if self.stop_event.is_set():
                    break
                
                # Execute daily post
                self.logger.info("Executing scheduled daily post")
                
                # Check calendar for specific topics
                today_str = datetime.now().strftime('%Y-%m-%d')
                scheduled_post = self.calendar.get_post(today_str)
                topic = scheduled_post['topic'] if scheduled_post else None
                
                # Run post generation
                result = run_daily_post(topic=topic)
                
                if result['success']:
                    self.calendar.mark_completed(today_str)
                    self.logger.info(f"Daily post generated successfully: {result['topic']}")
                else:
                    self.logger.error(f"Daily post generation failed: {result.get('error')}")
                
                # Execute callback if provided
                if callback:
                    try:
                        callback(result)
                    except Exception as e:
                        self.logger.error(f"Callback execution failed: {e}")
                
            except Exception as e:
                self.logger.error(f"Scheduler loop error: {e}")
                time.sleep(60)  # Wait before retrying
        
        self.logger.info("Scheduler loop ended")
    
    def trigger_now(self, topic: str = None) -> Dict[str, Any]:
        """
        Trigger an immediate post generation.
        
        Args:
            topic: Optional topic for the post
            
        Returns:
            Result dictionary
        """
        from autoposter import run_daily_post
        
        self.logger.info(f"Manual trigger invoked with topic: {topic}")
        return run_daily_post(topic=topic)
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current scheduler status.
        
        Returns:
            Status dictionary
        """
        return {
            'state': self.state.value,
            'is_running': self.state == SchedulerState.RUNNING,
            'is_paused': self.state == SchedulerState.PAUSED,
            'upcoming_posts': self.calendar.get_upcoming(7),
            'today_scheduled': self.calendar.get_post(datetime.now().strftime('%Y-%m-%d'))
        }
    
    def schedule_post(self, date: str, topic: str, metadata: Dict = None) -> bool:
        """
        Schedule a specific post.
        
        Args:
            date: Date string (YYYY-MM-DD)
            topic: Content topic
            metadata: Additional metadata
            
        Returns:
            True if scheduled successfully
        """
        with self.schedule_lock:
            return self.calendar.add_post(date, topic, metadata)
    
    def remove_scheduled_post(self, date: str) -> bool:
        """
        Remove a scheduled post.
        
        Args:
            date: Date string (YYYY-MM-DD)
            
        Returns:
            True if removed successfully
        """
        with self.schedule_lock:
            return self.calendar.remove_post(date)


# Convenience functions
def create_scheduler(config: Dict = None) -> Scheduler:
    """Create a new scheduler instance."""
    return Scheduler(config)


def start_daily_scheduler(time_str: str = "08:00", callback: Callable = None) -> Scheduler:
    """Start the daily scheduler."""
    scheduler = create_scheduler()
    scheduler.start(time_str, callback)
    return scheduler


if __name__ == "__main__":
    # Example usage
    scheduler = create_scheduler()
    
    # Schedule a post
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    scheduler.schedule_post(tomorrow, "职场效率")
    
    # Get status
    print(scheduler.get_status())
    
    # Or start the scheduler
    # scheduler.start("08:00")
