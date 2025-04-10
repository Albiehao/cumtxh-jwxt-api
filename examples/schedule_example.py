import sys
import os
import json
from collections import Counter
from datetime import datetime, timedelta
from icalendar import Calendar, Event
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.school_api.client import JwxtClient
from src.school_api.models.student import Student

def parse_weeks(weeks_str):
    """解析周次字符串"""
    weeks = set()
    parts = weeks_str.split(',')
    for part in parts:
        if '-' in part:
            # 修复周次解析
            start_week = part.split('-')[0].strip('周')
            end_week = part.split('-')[1].strip('周')
            start = int(''.join(filter(str.isdigit, start_week)))
            end = int(''.join(filter(str.isdigit, end_week)))
            
            if '单' in part:
                weeks.update(range(start, end + 1, 2))
            elif '双' in part:
                weeks.update(range(start + 1, end + 1, 2))
            else:
                weeks.update(range(start, end + 1))
        else:
            # 处理单周情况
            week = int(''.join(filter(str.isdigit, part.strip('周'))))
            weeks.add(week)
    return sorted(list(weeks))

def analyze_schedule(courses):
    """分析课程表数据"""
    total_courses = len(courses)
    teachers = Counter(course.teacher for course in courses)
    locations = Counter(course.location for course in courses)
    
    print("\n=== 课程表分析 ===")
    print(f"总课程数：{total_courses}")
    print(f"\n教师分布：")
    for teacher, count in teachers.items():
        print(f"  {teacher}: {count}门课")
    print(f"\n教室分布：")
    for location, count in locations.items():
        print(f"  {location}: {count}节课")

def generate_ics(courses, semester_start_date):
    """生成 ICS 日历文件"""
    # 创建日历
    cal = Calendar()
    cal.add('prodid', '-//School Schedule//CN')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('method', 'PUBLISH')
    cal.add('x-wr-calname', '课程表')
    
    # 时间段映射（24小时制）
    time_slots = {
        '1-2': ('08:00', '09:35'),
        '3-4': ('10:05', '11:40'),
        '5-6': ('14:00', '15:35'),
        '7-8': ('16:05', '17:40'),
        '9-10': ('18:30', '20:05'),
        '5-8': ('14:00', '17:40')  # 特殊时间段
    }
    
    # 处理每个课程
    for course in courses:
        # 解析上课时间
        day = int(course.time.split('星期')[1].split()[0])
        time_slot = course.time.split('第')[1].split('节')[0]
        weeks = parse_weeks(course.weeks)  # 使用已有的 parse_weeks 函数
        
        start_time, end_time = time_slots[time_slot]
        
        # 为每周的课程创建事件
        for week in weeks:
            # 计算具体日期
            course_date = semester_start_date + timedelta(days=(week-1)*7 + day-1)
            
            # 创建事件
            event = Event()
            event.add('summary', course.name)
            
            # 设置开始和结束时间
            start_dt = datetime.strptime(f"{course_date.date()} {start_time}", "%Y-%m-%d %H:%M")
            end_dt = datetime.strptime(f"{course_date.date()} {end_time}", "%Y-%m-%d %H:%M")
            event.add('dtstart', start_dt)
            event.add('dtend', end_dt)
            
            # 添加地点和描述
            event.add('location', course.location)
            event.add('description', f"教师：{course.teacher}\n地点：{course.location}")
            
            cal.add_component(event)
    
    return cal

def main():
    # 创建客户端
    client = JwxtClient()
    
    # 登录
    student = Student("2223041646", "zjh20041014")
    login_result = client.login(student)
    
    # 如果登录成功，获取课程表
    if login_result["status"] == "success":
        print("登录成功，开始获取课程表...")
        
        # 获取2024-2025学年第2学期的课程表
        schedule = client.get_schedule(year="2024-2025", term=2)
        
        # 保存课程数据为 JSON
        schedule_data = [{
            "name": course.name,
            "teacher": course.teacher,
            "location": course.location,
            "time": course.time,
            "weeks": course.weeks
        } for course in schedule.courses]
        
        json_path = "d:\\PcStudy\\school-api-master\\out\\schedule_2025_2.json"
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(schedule_data, f, ensure_ascii=False, indent=2)
        print(f"\n课程表数据已保存到：{json_path}")
        
        # 生成 ICS 文件
        semester_start = datetime(2025, 2, 24)  # 2024-2025学年第二学期开学日期
        calendar = generate_ics(schedule.courses, semester_start)
        ics_path = "d:\\PcStudy\\school-api-master\\out\\schedule_2025_2.ics"
        with open(ics_path, 'wb') as f:
            f.write(calendar.to_ical())
        print(f"课程表已保存为iCalendar格式：{ics_path}")
        
        # 打印课程信息
        print("\n=== 课程表 ===")
        for course in schedule.courses:
            print(f"""
课程：{course.name}
教师：{course.teacher}
地点：{course.location}
时间：{course.time}
周次：{course.weeks}
            """)
        
        # 分析课程数据
        analyze_schedule(schedule.courses)
        
    else:
        print("登录失败，无法获取课程表")

if __name__ == "__main__":
    main()