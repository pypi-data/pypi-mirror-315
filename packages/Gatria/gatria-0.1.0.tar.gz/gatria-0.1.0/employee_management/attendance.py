from datetime import datetime
from typing import Dict, List, Optional
from .utils import DataValidator, Logger, ValidationError
from .storage import StorageManager

class AttendanceTracker:
    def __init__(self, config_manager):
        self.attendance_records: Dict[str, List[dict]] = {}
        self.config = config_manager.config
        self.logger = Logger.setup("attendance")
        self.storage = StorageManager()
        self.storage_path = config_manager.get_storage_path('attendance.json')
        self._load_data()

    def log_entry(self, employee_id: str, entry_type: str = "login") -> bool:
        try:
            DataValidator.validate_employee_id(employee_id)
            timestamp = datetime.now()
            
            if employee_id not in self.attendance_records:
                self.attendance_records[employee_id] = []
            
            record = {
                "timestamp": timestamp.isoformat(),
                "type": entry_type,
                "verified": True
            }
            self.attendance_records[employee_id].append(record)
            self._save_data()
            self.logger.info(f"Attendance logged for {employee_id}: {entry_type}")
            return True
            
        except ValidationError as e:
            self.logger.error(f"Validation error for {employee_id}: {str(e)}")
            raise

    def _save_data(self):
        return self.storage.save_data(self.storage_path, self.attendance_records)

    def _load_data(self):
        self.attendance_records = self.storage.load_data(self.storage_path, {})

    def get_employee_attendance(self, employee_id: str) -> List[dict]:
        return self.attendance_records.get(employee_id, [])
