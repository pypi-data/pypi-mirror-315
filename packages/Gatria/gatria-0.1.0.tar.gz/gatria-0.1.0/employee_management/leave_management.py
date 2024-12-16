from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum
from .utils import DataValidator, Logger, ValidationError
import json
from .storage import StorageManager

class LeaveStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

class LeaveManagement:
    def __init__(self, config_manager):
        self.leave_requests: Dict[str, List[dict]] = {}
        self.config = config_manager.config
        self.logger = Logger.setup("leave_management")
        self.storage = StorageManager()
        self.storage_path = config_manager.get_storage_path('leave.json')
        self._load_data()

    def request_leave(self, employee_id: str, start_date: datetime, 
                     end_date: datetime, reason: str) -> bool:
        try:
            DataValidator.validate_employee_id(employee_id)
            DataValidator.validate_date_range(start_date, end_date)
            
            if not reason.strip():
                raise ValidationError("Reason cannot be empty")

            leave_days = (end_date - start_date).days
            if leave_days > self.config.max_leave_days:
                raise ValidationError(f"Leave request exceeds maximum allowed days ({self.config.max_leave_days})")

            if employee_id not in self.leave_requests:
                self.leave_requests[employee_id] = []
            
            request = {
                "start_date": start_date,
                "end_date": end_date,
                "reason": reason,
                "status": LeaveStatus.PENDING.value,  # Store as string
                "request_date": datetime.now()
            }
            self.leave_requests[employee_id].append(request)
            self._save_data()
            self.logger.info(f"Leave requested for {employee_id}")
            return True

        except ValidationError as e:
            self.logger.error(f"Leave request error for {employee_id}: {str(e)}")
            raise

    def process_leave_request(self, employee_id: str, request_index: int, 
                            status: LeaveStatus) -> bool:
        if employee_id in self.leave_requests:
            self.leave_requests[employee_id][request_index]["status"] = status.value  # Store as string
            self._save_data()
            return True
        return False

    def get_leave_status(self, status_value: str) -> LeaveStatus:
        """Convert stored string value back to LeaveStatus enum"""
        return LeaveStatus(status_value)

    def _save_data(self):
        return self.storage.save_data(self.storage_path, self.leave_requests)

    def _load_data(self):
        self.leave_requests = self.storage.load_data(self.storage_path, {})
