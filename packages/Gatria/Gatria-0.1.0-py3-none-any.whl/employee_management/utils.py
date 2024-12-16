import re
from datetime import datetime
import logging
from typing import Any, Optional

class ValidationError(Exception):
    pass

class DataValidator:
    @staticmethod
    def validate_employee_id(employee_id: str) -> bool:
        if not re.match(r'^EMP\d{3,6}$', employee_id):
            raise ValidationError("Invalid employee ID format. Must be EMP followed by 3-6 digits")
        return True

    @staticmethod
    def validate_date_range(start_date: datetime, end_date: datetime) -> bool:
        if start_date > end_date:
            raise ValidationError("Start date must be before end date")
        return True

    @staticmethod
    def validate_rating(rating: float, min_rating: float, max_rating: float) -> bool:
        if not min_rating <= rating <= max_rating:
            raise ValidationError(f"Rating must be between {min_rating} and {max_rating}")
        return True

class Logger:
    @staticmethod
    def setup(name: str, log_file: str = "employee_management.log"):
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        return logger
