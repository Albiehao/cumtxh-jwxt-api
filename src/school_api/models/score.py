class Score:
    """成绩信息类"""
    def __init__(self, **kwargs):
        self.course_name = kwargs.get('kcmc', '')  # 课程名称
        self.credit = kwargs.get('xf', '')  # 学分
        self.grade = kwargs.get('cj', '')  # 成绩
        self.course_type = kwargs.get('kcxzmc', '')  # 课程性质
        self.exam_type = kwargs.get('ksxz', '')  # 考试性质
        self.semester = kwargs.get('xqmmc', '')  # 学期
        self.year = kwargs.get('xnmmc', '')  # 学年
        self.course_id = kwargs.get('kch', '')  # 课程号
        self.teacher = kwargs.get('jsxm', '')  # 教师姓名
        self.mark_type = kwargs.get('kcbj', '')  # 课程标记（主修/辅修等）

class ScoreList:
    """成绩列表类"""
    def __init__(self):
        self.scores = []
    
    def add_score(self, score):
        """添加成绩记录"""
        self.scores.append(score)
    
    def get_gpa(self):
        """计算平均学分绩点"""
        total_credit = 0
        total_grade_point = 0
        
        for score in self.scores:
            try:
                credit = float(score.credit)
                grade = float(score.grade)
                if grade >= 60:
                    grade_point = (grade - 50) / 10
                    total_grade_point += grade_point * credit
                    total_credit += credit
            except (ValueError, TypeError):
                continue
        
        return round(total_grade_point / total_credit, 2) if total_credit > 0 else 0