class Exam:
    """考试信息类"""
    def __init__(self, **kwargs):
        self.year = kwargs.get('xnm', '')  # 学年
        self.term = kwargs.get('xqm', '')  # 学期
        self.course_name = kwargs.get('kcmc', '')  # 课程名称
        self.exam_date = kwargs.get('kssj', '')  # 考试时间
        self.exam_location = kwargs.get('ksdd', '')  # 考试地点
        self.exam_campus = kwargs.get('ksxq', '')  # 考试校区
        self.course_code = kwargs.get('kcdm', '')  # 课程代码
        self.retake_flag = kwargs.get('cxbs', '')  # 重修标记
        self.exam_name = kwargs.get('ksmc', '')  # 考试名称
        self.note = kwargs.get('bz', '')  # 备注
        self.class_name = kwargs.get('jxbmc', '')  # 教学班名称
        self.department = kwargs.get('kkxy', '')  # 开课学院
        self.class_composition = kwargs.get('jxbzc', '')  # 教学班组成
        self.campus = kwargs.get('xq', '')  # 校区
        self.exam_method = kwargs.get('ksfs', '')  # 考试方式
        self.venue_short_name = kwargs.get('cdjc', '')  # 场地简称

class ExamList:
    """考试列表类"""
    def __init__(self):
        self.exams = []
    
    def add_exam(self, exam):
        """添加考试记录"""
        self.exams.append(exam)