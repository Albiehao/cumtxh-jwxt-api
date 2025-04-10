import sys
import os
import json
import configparser
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.school_api.client import JwxtClient
from src.school_api.models.student import Student

def main():
    # 读取配置文件 - 使用绝对路径确保能找到文件
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.ini')
    config.read(config_path)
    
    # 创建客户端
    client = JwxtClient()  # 这行被遗漏了，需要添加
    
    # 从配置文件获取登录信息
    try:
        username = config.get('jwxt', 'username')
        password = config.get('jwxt', 'password')
    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        print(f"配置文件错误: {e}")
        return

    student = Student(username, password)
    login_result = client.login(student)
    
    if login_result["status"] == "success":
        print("登录成功，开始获取考试信息...")
        
        # 获取2024-2025学年第2学期的考试信息
        exams = client.get_exams(year="2024-2025", term=1)
        
        # 准备保存的数据
        all_exams_data = []
        
        # 打印考试信息
        print("\n=== 考试信息 ===")
        for exam in exams.exams:
            exam_info = {
                "学年": exam.year,
                "学期": exam.term,
                "课程名称": exam.course_name,
                "考试时间": exam.exam_date,
                "考试地点": exam.exam_location,
                "考试校区": exam.exam_campus,
                "课程代码": exam.course_code,
                "重修标记": exam.retake_flag,
                "考试名称": exam.exam_name,
                "备注": exam.note,
                "教学班名称": exam.class_name,
                "开课学院": exam.department,
                "教学班组成": exam.class_composition,
                "校区": exam.campus
            }
            
            # 过滤掉值为空的字段
            filtered_info = {k: v for k, v in exam_info.items() if v}
            all_exams_data.append(filtered_info)
            
            # 打印过滤后的信息
            for key, value in filtered_info.items():
                print(f"{key}：{value}")
            print()
        
        # 保存为JSON文件
        output_dir = os.path.join('..', 'out', 'exam')
        os.makedirs(output_dir, exist_ok=True)
        json_path = os.path.join(output_dir, 'exams.json')
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(all_exams_data, f, ensure_ascii=False, indent=4)
        print(f"\n考试信息已保存到 {json_path}")

    else:
        print("登录失败，无法获取考试信息")

if __name__ == "__main__":
    main()