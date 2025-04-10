import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.school_api.client import JwxtClient
from src.school_api.models.student import Student

def main():
    # 创建客户端
    client = JwxtClient()
    
    # 登录
    student = Student("2223041646", "zjh20041014")
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
        os.makedirs("out/exam", exist_ok=True)
        with open("out/exam/exams.json", "w", encoding="utf-8") as f:
            json.dump(all_exams_data, f, ensure_ascii=False, indent=4)
        print("\n考试信息已保存到 out/exam/exams.json")
        
    else:
        print("登录失败，无法获取考试信息")

if __name__ == "__main__":
    main()