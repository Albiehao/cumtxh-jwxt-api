from typing import List
from .course import Course

class Schedule:
    """课程表模型"""
    def __init__(self):
        self.courses: List[Course] = []
    
    def add_course(self, course: Course):
        self.courses.append(course)