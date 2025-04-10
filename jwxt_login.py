import requests
from urllib.parse import urlencode
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64
import time

class Student:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class JwxtClient:
    BASE_URL = "http://jwxt.cumtxh.cn"
    LOGIN_URL = f"{BASE_URL}/jwglxt/xtgl/login_slogin.html"
    PUBLIC_KEY_URL = f"{BASE_URL}/jwglxt/xtgl/login_getPublicKey.html"
    
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "Referer": self.LOGIN_URL,  # 修改这里
            "Origin": self.BASE_URL,    # 修改这里
            "Content-Type": "application/x-www-form-urlencoded"
        }
        self.session.headers.update(self.headers)

    def _get_csrf_token(self):
        """获取CSRF Token"""
        response = self.session.get(self.LOGIN_URL)
        csrf_token = response.text.split('name="csrftoken" value="')[1].split('"')[0]
        return csrf_token

    def _get_public_key(self):
        """获取RSA公钥"""
        response = self.session.get(
            self.PUBLIC_KEY_URL, 
            params={"time": int(time.time() * 1000)}
        )
        return response.json()

    def _encrypt_password(self, password, public_key):
        """使用RSA加密密码"""
        modulus = public_key['modulus']
        exponent = public_key['exponent']
        
        n = int.from_bytes(base64.b64decode(modulus), 'big')
        e = int.from_bytes(base64.b64decode(exponent), 'big')
        
        rsa_key = RSA.construct((n, e))
        cipher = PKCS1_v1_5.new(rsa_key)
        encrypted = cipher.encrypt(password.encode())
        
        return base64.b64encode(encrypted).decode()

    def login(self, student, save_response=True):
        """
        登录教务系统
        :param student: Student对象，包含用户名和密码
        :param save_response: 是否保存响应到文件
        :return: 登录结果字典
        """
        csrf_token = self._get_csrf_token()
        public_key = self._get_public_key()
        encrypted_password = self._encrypt_password(student.password, public_key)
        
        data = {
            "csrftoken": csrf_token,
            "language": "zh_CN",
            "ydType": "",
            "yhm": student.username,
            "mm": encrypted_password
        }

        response = self.session.post(
            self.LOGIN_URL, 
            data=urlencode(data), 
            allow_redirects=False
        )

        if response.status_code == 302:
            redirect_url = response.headers["Location"]
            response = self.session.get(redirect_url, allow_redirects=False)
            
            if response.status_code == 302:
                final_url = response.headers["Location"]
                final_response = self.session.get(final_url)
                
                if save_response:
                    log_path = "d:\\PcStudy\\school-api-master\\log\\login_response.log"
                    os.makedirs(os.path.dirname(log_path), exist_ok=True)
                    with open(log_path, "w", encoding="utf-8") as f:
                        f.write(final_response.text)
                
                return {
                    "status": "success",
                    "session": self.session,
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

def main():
    # 使用示例
    student = Student("2223041646", "zjh20041014")
    client = JwxtClient()
    login_result = client.login(student)
    print(login_result["message"])

if __name__ == "__main__":
    main()