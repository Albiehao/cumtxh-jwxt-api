import json
from icalendar import Calendar, Event
from datetime import datetime, timedelta

def generate_ics(json_path, semester_start_date):
    """生成 ICS 日历文件"""
    with open(json_path, 'r', encoding='utf-8') as f:
        courses = json.load(f)
    
    # 创建日历对象
    cal = Calendar()  # 添加这行定义cal变量
    cal.add('prodid', '-//School Schedule//CN')
    cal.add('version', '2.0')
    
    # ... 函数其余实现保持不变 ...
    
    return cal  # 确保最后返回cal对象