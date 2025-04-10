import os
import sys
import time
import json
import configparser
from datetime import datetime
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from icalendar import Calendar
from src.school_api.client import JwxtClient
from src.school_api.models.student import Student

# 添加generate_ics导入
from calendar_service.ics_generator import generate_ics
from flask import Flask, send_file
import threading

app = Flask(__name__)
# 确保ICS_PATH使用相对路径
ICS_PATH = os.path.join('..', 'out', 'schedule', 'schedule_2024_2.ics')

# 读取配置文件
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'config.ini'))

def auto_update_schedule(interval_hours=24):
    """自动更新课程表服务"""
    client = JwxtClient()
    try:
        username = config.get('jwxt', 'username')
        password = config.get('jwxt', 'password')
    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        print(f"配置文件错误: {e}")
        return
        
    student = Student(username, password)
    output_dir = os.path.join('..', 'out', 'schedule')
    os.makedirs(output_dir, exist_ok=True)
    
    while True:
        try:
            # 1. 登录并获取最新课表
            login_result = client.login(student)
            if login_result["status"] != "success":
                print(f"{datetime.now()} - 登录失败")
                continue
                
            schedule = client.get_schedule(year="2024-2025", term=2)
            
            # 2. 生成JSON数据
            json_path = os.path.join(output_dir, 'schedule_2024_2.json')
            courses_data = [{
                'name': course.name,
                'teacher': course.teacher,
                'location': course.location,
                'time': course.time,
                'weeks': course.weeks
            } for course in schedule.courses]
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(courses_data, f, ensure_ascii=False, indent=2)
            
            # 3. 生成ICS文件
            semester_start = datetime(2024, 2, 26)
            calendar = generate_ics(json_path, semester_start)
            
            ics_path = os.path.join(output_dir, 'schedule_2024_2.ics')
            with open(ics_path, 'wb') as f:
                f.write(calendar.to_ical())
                
            print(f"{datetime.now()} - 课程表更新成功")
            
        except Exception as e:
            print(f"{datetime.now()} - 更新失败: {str(e)}")
            
        # 4. 等待下次更新
        time.sleep(interval_hours * 3600)