from .config import Config
from .utils.http import HttpSession
from .models.student import Student
from .models.exam import ExamList
import json

class JwxtClient:
    """教务系统客户端主类"""
    
    def __init__(self):
        self.session = HttpSession(base_url="https://jwxt.cumtxh.cn")
        self.config = Config()
    
    def login(self, student: Student):
        """登录教务系统"""
        # ... 原有登录逻辑 ...
    
    def get_schedule(self, year: str, term: int):
        """获取课程表"""
        # ... 原有课程表获取逻辑 ...
    
    def get_exams(self, year: str, term: int) -> ExamList:
        """获取考试信息"""
        # ... 原有考试信息获取逻辑 ...
    
    def save_to_json(self, data, file_path):
        """保存数据到JSON文件"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)