import json
import os
from datetime import datetime, timedelta
from icalendar import Calendar, Event
from prettytable import PrettyTable

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

def format_schedule(json_path, week_number=None):
    """格式化课程表"""
    with open(json_path, 'r', encoding='utf-8') as f:
        courses = json.load(f)

    # 创建周一到周五的时间段表格
    time_slots = {
        '1-2': 0, '3-4': 1, '5-6': 2, '7-8': 3, '9-10': 4,
        # 添加特殊时间段
        '5-8': 2  # 5-8节占用5-6节的位置
    }
    weekdays = ['周一', '周二', '周三', '周四', '周五']
    
    # 创建表格
    table = PrettyTable()
    table.field_names = ['时间'] + weekdays
    table.align = 'c'  # 居中对齐
    
    # 初始化课程矩阵
    schedule_matrix = [['' for _ in range(6)] for _ in range(5)]
    
    # 填充时间段
    schedule_matrix[0][0] = '1-2节\n08:00-09:35'
    schedule_matrix[1][0] = '3-4节\n10:05-11:40'
    schedule_matrix[2][0] = '5-6节\n14:00-15:35'
    schedule_matrix[3][0] = '7-8节\n16:05-17:40'
    schedule_matrix[4][0] = '9-10节\n18:30-20:05'

    # 处理每个课程
    for course in courses:
        day = int(course['time'].split('星期')[1].split()[0])
        time = course['time'].split('第')[1].split('节')[0]
        weeks = parse_weeks(course['weeks'])
        
        # 如果指定了周数，只显示该周的课程
        if week_number and week_number not in weeks:
            continue
            
        time_slot = time_slots[time]
        course_info = f"{course['name']}\n{course['teacher']}\n{course['location']}"
        if not week_number:
            course_info += f"\n{course['weeks']}"
        
        # 处理跨时段的课程
        if time == '5-8':
            # 同时占用5-6和7-8节
            schedule_matrix[2][day] = course_info
            schedule_matrix[3][day] = '（续）' + course_info
            
        else:
            schedule_matrix[time_slot][day] = course_info

    # 添加到表格
    for row in schedule_matrix:
        table.add_row(row)

    return table

def format_schedule_text(json_path, week_number=None):
    """生成文本格式的课程表"""
    with open(json_path, 'r', encoding='utf-8') as f:
        courses = json.load(f)
    
    # 按周次整理课程
    week_courses = {}
    for course in courses:
        weeks = parse_weeks(course['weeks'])
        for week in weeks:
            if week not in week_courses:
                week_courses[week] = []
            week_courses[week].append(course)
    
    # 生成输出文本
    output = []
    weeks = sorted(week_courses.keys())
    for week in weeks:
        if week_number and week != week_number:
            continue
            
        output.append(f"\n第{week}周课程安排")
        output.append("=" * 50)
        
        # 按星期和时间排序
        sorted_courses = sorted(week_courses[week], 
                              key=lambda x: (int(x['time'].split('星期')[1].split()[0]), 
                                           x['time'].split('第')[1].split('节')[0]))
        
        for course in sorted_courses:
            output.append(f"""
{course['time']}
课程：{course['name']}
教师：{course['teacher']}
地点：{course['location']}
""")
        
        output.append("=" * 50)
    
    return "\n".join(output)

def generate_ics(json_path, semester_start_date):
    """生成 ICS 日历文件"""
    with open(json_path, 'r', encoding='utf-8') as f:
        courses = json.load(f)
    
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
        day = int(course['time'].split('星期')[1].split()[0])
        time_slot = course['time'].split('第')[1].split('节')[0]
        weeks = parse_weeks(course['weeks'])
        
        start_time, end_time = time_slots[time_slot]
        
        # 为每周的课程创建事件
        for week in weeks:
            # 计算具体日期
            course_date = semester_start_date + timedelta(days=(week-1)*7 + day-1)
            
            # 创建事件
            event = Event()
            event.add('summary', course['name'])
            
            # 设置开始和结束时间
            start_dt = datetime.strptime(f"{course_date.date()} {start_time}", "%Y-%m-%d %H:%M")
            end_dt = datetime.strptime(f"{course_date.date()} {end_time}", "%Y-%m-%d %H:%M")
            event.add('dtstart', start_dt)
            event.add('dtend', end_dt)
            
            # 添加地点和描述
            event.add('location', course['location'])
            event.add('description', f"教师：{course['teacher']}\n地点：{course['location']}")
            
            cal.add_component(event)
    
    return cal

def main():
    import sys
    import os
    # 添加项目根目录到 Python 路径
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from src.school_api.client import JwxtClient
    from src.school_api.models.student import Student
    
    json_path = 'd:\\PcStudy\\school-api-master\\out\\schedule_2024_2.json'
    output_dir = 'd:\\PcStudy\\school-api-master\\out'
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取课程表数据
    client = JwxtClient()
    student = Student("2223041646", "zjh20041014")
    login_result = client.login(student)
    
    if login_result["status"] == "success":
        print("登录成功，开始获取课程表...")
        schedule = client.get_schedule(year="2024-2025", term=2)
        
        # 将课程对象转换为字典列表
        courses_data = []
        for course in schedule.courses:
            courses_data.append({
                'name': course.name,
                'teacher': course.teacher,
                'location': course.location,
                'time': course.time,
                'weeks': course.weeks
            })
        
        # 保存为 JSON
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(courses_data, f, ensure_ascii=False, indent=2)
        print(f"课程表数据已保存到：{json_path}")
        
        # 设置学期开始日期（2024年春季学期）
        semester_start = datetime(2024, 2, 26)
        
        # 生成 ICS 文件
        calendar = generate_ics(json_path, semester_start)
        
        # 保存 ICS 文件
        ics_path = os.path.join(output_dir, 'schedule_2024_2.ics')
        with open(ics_path, 'wb') as f:
            f.write(calendar.to_ical())
        print(f"课程表已保存为iCalendar格式：{ics_path}")
    else:
        print("登录失败，无法获取课程表")

if __name__ == '__main__':
    main()