class Course:
    """课程模型"""
    def __init__(self, name=None, teacher=None, location=None, time=None, weeks=None):
        self.name = name          # 课程名称
        self.teacher = teacher    # 教师
        self.location = location  # 上课地点
        self.time = time          # 上课时间
        self.weeks = weeks        # 上课周次