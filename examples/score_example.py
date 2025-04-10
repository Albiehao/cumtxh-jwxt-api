import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.school_api.client import JwxtClient
from src.school_api.models.student import Student
import json

def main():
    # 创建客户端
    client = JwxtClient()
    
    # 登录 - 建议从环境变量或配置文件读取
    student = Student(os.getenv("JWXT_USERNAME"), os.getenv("JWXT_PASSWORD"))
    login_result = client.login(student)
    
    if login_result["status"] == "success":
        print("登录成功，开始获取成绩...")
        
        # 获取2024-2025学年第2学期的成绩
        scores = client.get_scores(year="2024-2025", term=1)
        
        # 打印成绩信息
        print("\n=== 成绩信息 ===")
        for score in scores.scores:
            print(f"""
课程：{score.course_name}
学分：{score.credit}
成绩：{score.grade}
课程性质：{score.course_type}
考试性质：{score.exam_type}
教师：{score.teacher}
            """)
        
        # 计算平均学分绩点
        print(f"\n平均学分绩点：{scores.get_gpa()}")
        
        # 保存为JSON文件
        os.makedirs("out/score", exist_ok=True)
        with open("out/score/scores.json", "w", encoding="utf-8") as f:
            json.dump([score.__dict__ for score in scores.scores], f, ensure_ascii=False, indent=4)
        print("成绩已保存到 out/score/scores.json")
        
    else:
        print("登录失败，无法获取成绩")

if __name__ == "__main__":
    main()