from datetime import datetime
from typing import Dict, List
from .utils import DataValidator, Logger, ValidationError
import json
from .storage import StorageManager

class PerformanceTracker:
    def __init__(self, config_manager):
        self.performance_records: Dict[str, List[dict]] = {}
        self.config = config_manager.config
        self.logger = Logger.setup("performance")
        self.storage = StorageManager()
        self.storage_path = config_manager.get_storage_path('performance.json')
        self._load_data()

        # Set default values if min_performance_rating or max_performance_rating are None
        if self.config.min_performance_rating is None:
            self.config.min_performance_rating = 1.0  # default minimum rating
        if self.config.max_performance_rating is None:
            self.config.max_performance_rating = 5.0  # default maximum rating

    def add_review(self, employee_id: str, rating: float, 
                   feedback: str, reviewer_id: str) -> bool:
        try:
            DataValidator.validate_employee_id(employee_id)
            DataValidator.validate_rating(
                rating, 
                self.config.min_performance_rating,
                self.config.max_performance_rating
            )

            if employee_id not in self.performance_records:
                self.performance_records[employee_id] = []
            
            review = {
                "date": datetime.now().isoformat(),
                "rating": rating,
                "feedback": feedback,
                "reviewer_id": reviewer_id
            }
            self.performance_records[employee_id].append(review)
            self._save_data()
            self.logger.info(f"Performance review added for {employee_id}")
            return True

        except ValidationError as e:
            self.logger.error(f"Performance review error for {employee_id}: {str(e)}")
            raise

    def get_employee_reviews(self, employee_id: str) -> List[dict]:
        return self.performance_records.get(employee_id, [])

    def _save_data(self):
        return self.storage.save_data(self.storage_path, self.performance_records)

    def _load_data(self):
        self.performance_records = self.storage.load_data(self.storage_path, {})

    def record_performance(self, employee_id: str, performance_data: dict) -> bool:
        rating = performance_data.get('rating')
        feedback = performance_data.get('feedback')
        reviewer_id = performance_data.get('reviewer_id')

        missing_fields = []
        if rating is None:
            missing_fields.append('rating')
        if feedback is None:
            missing_fields.append('feedback')
        if reviewer_id is None:
            missing_fields.append('reviewer_id')

        if missing_fields:
            raise ValidationError(f"Missing performance data fields: {', '.join(missing_fields)}")

        return self.add_review(employee_id, rating, feedback, reviewer_id)
