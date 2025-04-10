# 修改相对导入为绝对导入
import time
import os
from src.school_api.utils.http import HttpClient
from src.school_api.utils.crypto import encrypt_password
import requests

class JwxtClient:
    """教务系统客户端"""
    def __init__(self, base_url="http://jwxt.cumtxh.cn"):
        self.base_url = base_url
        self.http_client = HttpClient(base_url)
        self.session = requests.Session()  # 添加session属性
        
    def _get_csrf_token(self):
        """获取CSRF Token"""
        response = self.http_client.get("/jwglxt/xtgl/login_slogin.html")
        return response.text.split('name="csrftoken" value="')[1].split('"')[0]

    def _get_public_key(self):
        """获取RSA公钥"""
        response = self.http_client.get(
            "/jwglxt/xtgl/login_getPublicKey.html",
            params={"time": int(time.time() * 1000)}
        )
        return response.json()

    def login(self, student, save_response=True):
        """
        登录教务系统
        :param student: Student对象，包含用户名和密码
        :param save_response: 是否保存响应到文件
        :return: 登录结果字典
        """
        csrf_token = self._get_csrf_token()
        public_key = self._get_public_key()
        encrypted_password = encrypt_password(student.password, public_key)
        
        data = {
            "csrftoken": csrf_token,
            "language": "zh_CN",
            "ydType": "",
            "yhm": student.username,
            "mm": encrypted_password
        }

        response = self.http_client.post("/jwglxt/xtgl/login_slogin.html", data)

        if response.status_code == 302:
            redirect_url = response.headers["Location"]
            response = self.http_client.session.get(redirect_url, allow_redirects=False)
            
            if response.status_code == 302:
                final_url = response.headers["Location"]
                final_response = self.http_client.session.get(final_url)
                
                if save_response:
                    log_path = "d:\\PcStudy\\school-api-master\\log\\login_response.log"
                    os.makedirs(os.path.dirname(log_path), exist_ok=True)
                    with open(log_path, "w", encoding="utf-8") as f:
                        f.write(final_response.text)
                
                return {
                    "status": "success",
                    "session": self.http_client.session,
                    "response": final_response,
                    "redirect_url": final_url,
                    "message": f"""
=== 登录成功 ===
用户：{student.username}
最终URL：{final_url}
响应已保存到: {log_path}
"""
                }
        
        return {
            "status": "fail",
            "response": response,
            "message": f"""
=== 登录失败 ===
状态码：{response.status_code}
错误信息：{response.text}
"""
        }

    def get_schedule(self, year=None, term=None):
        """
        获取课程表
        :param year: 学年，如 "2024-2025"
        :param term: 学期，如 1, 2, 3
        :return: Schedule对象
        """
        # 处理学年参数
        if "-" in str(year):
            xnm = year.split("-")[0]
        else:
            xnm = str(year)
        
        # 处理学期参数
        term_map = {
            1: "3",    # 第一学期
            2: "12",   # 第二学期
            3: "16"    # 第三学期
        }
        xqm = term_map.get(term, "3")
        
        data = {
            "xnm": xnm,
            "xqm": xqm,
            "kzlx": "ck",
            "xsdm": ""
        }
        
        response = self.http_client.post(
            "/jwglxt/kbcx/xskbcx_cxXsgrkb.html?gnmkdm=N2151",
            data=data
        )
        
        from .models.schedule import Schedule
        from .models.course import Course
        
        schedule = Schedule()
        
        # 解析响应数据
        result = response.json()
        if "kbList" in result:
            for item in result["kbList"]:
                course = Course(
                    name=item.get("kcmc", ""),  # 课程名称
                    teacher=item.get("xm", ""),  # 教师姓名
                    location=item.get("cdmc", ""),  # 上课地点
                    time=f"星期{item.get('xqj', '')} 第{item.get('jc', '')}节",  # 上课时间
                    weeks=item.get("zcd", "")  # 上课周次
                )
                schedule.add_course(course)
        
        return schedule

    def get_scores(self, year=None, term=None, mark_type=None):
        """
        获取成绩信息
        :param year: 学年，如 "2024-2025"
        :param term: 学期，如 1, 2, 3
        :param mark_type: 课程标记，如 "主修"/"辅修"等
        :return: ScoreList对象
        """
        # 处理学年参数
        if "-" in str(year):
            xnm = year.split("-")[0]
        else:
            xnm = str(year)
        
        # 处理学期参数
        term_map = {
            1: "3",    # 第一学期
            2: "12",   # 第二学期
            3: "16"    # 第三学期
        }
        xqm = term_map.get(term, "")
        
        # 处理课程标记
        mark_type_map = {
            "主修": "0",
            "辅修": "1",
            "二专业": "2",
            "二学位": "3",
            "非学位": "4"
        }
        kcbjdm = mark_type_map.get(mark_type, "")
        
        data = {
            "xnm": xnm,
            "xqm": xqm,
            "kcbjdm": kcbjdm,
            "_search": False,
            "nd": int(time.time() * 1000),
            "queryModel.showCount": 100,
            "queryModel.currentPage": 1,
            "queryModel.sortName": "",
            "queryModel.sortOrder": "asc",
            "time": 0
        }
        
        response = self.http_client.post(
            "/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005",
            data=data
        )
        
        from .models.score import Score, ScoreList
        score_list = ScoreList()
        
        result = response.json()
        if "items" in result:
            for item in result["items"]:
                score = Score(**item)
                score_list.add_score(score)
        
        return score_list

    def get_exams(self, year=None, term=None, exam_name=None):
        """
        获取考试信息
        :param year: 学年，如 "2024-2025"
        :param term: 学期，如 1, 2, 3
        :param exam_name: 考试名称，如 "期末考试"
        :return: ExamList对象
        """
        # 处理学年参数
        if "-" in str(year):
            xnm = year.split("-")[0]
        else:
            xnm = str(year)
        
        # 处理学期参数
        term_map = {
            1: "3",    # 第一学期
            2: "12",   # 第二学期
            3: "16"    # 第三学期
        }
        xqm = term_map.get(term, "")
        
        data = {
            "xnm": xnm,
            "xqm": xqm,
            "ksmcdmb_id": exam_name if exam_name else "",
            "_search": False,
            "nd": int(time.time() * 1000),
            "queryModel.showCount": 100,
            "queryModel.currentPage": 1,
            "queryModel.sortName": "",
            "queryModel.sortOrder": "asc",
            "time": 0
        }
        
        response = self.http_client.post(
            "/jwglxt/kwgl/kscx_cxXsksxxIndex.html?doType=query&gnmkdm=N358105",
            data=data
        )
        
        from .models.exam import Exam, ExamList
        exam_list = ExamList()
        
        result = response.json()
        if "items" in result:
            for item in result["items"]:
                exam = Exam(**item)
                exam_list.add_exam(exam)
        
        return exam_list