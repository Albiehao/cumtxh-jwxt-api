import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.school_api.client import JwxtClient
from src.school_api.models.student import Student

def main():
    # 使用示例
    student = Student("yourid", "yourpsg")
    client = JwxtClient()
    login_result = client.login(student)
    print(login_result["message"])

if __name__ == "__main__":
    main()