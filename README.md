# 方正教务系统 SDK

![GitHub Stars](https://img.shields.io/github/stars/Albiehao/cumtxh-jwxt-api?style=social)
![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 功能特性

- ✅ 教务系统安全登录
- 📅 课程表查询与解析
- 📝 考试信息查询
- 📤 多格式数据导出 (JSON/ICS)
- 🛡️ 基于Session的安全请求

### 基本使用

```python
from school_api import JwxtClient
from school_api.models import Student

# 初始化客户端
client = JwxtClient()

# 学生登录
student = Student("学号", "密码")
result = client.login(student)

if result["status"] == "success":
    # 获取课程表
    schedule = client.get_schedule(year="2024-2025", term=1)
    
    # 获取考试信息
    exams = client.get_exams(year="2024-2025", term=1)
```

### 数据导出示例

```python
# 导出课程表为ICS日历格式
from datetime import datetime
from school_api.utils import export_ics

schedule = client.get_schedule(...)
export_ics(schedule, "schedule.ics", semester_start=datetime(2024, 2, 26))
```

## 文档

### 核心类

#### JwxtClient
| 方法 | 描述 |
|------|------|
| `login(student)` | 学生登录 |
| `get_schedule(year, term)` | 获取课程表 |
| `get_exams(year, term)` | 获取考试信息 |

#### 数据模型
- `Student`: 学号/密码认证模型
- `Schedule`: 课程表数据结构
- `ExamList`: 考试信息集合

## 示例代码

查看 [examples/](d:\PcStudy\fzsdk\examples) 目录获取更多使用示例：

- 课程表导出: `schedule_example.py`
- 考试查询: `exam_example.py`
- 数据格式化: `schedule_formatter.py`

## 贡献

欢迎提交Issue和Pull Request


## 许可证

本项目采用 [MIT License](LICENSE) 开源许可证。

### 主要授权条款
- 允许自由使用、复制、修改、合并、出版发行、散布、再授权及销售软件
- 允许修改源代码，但必须在所有副本中包含原始版权声明和许可声明
- 软件按"原样"提供，不承担任何明示或暗示的担保责任

完整许可条款请查看项目根目录下的 [LICENSE](LICENSE) 文件。

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Albiehao/cumtxh-jwxt-api&type=Date)](https://star-history.com/#Albiehao/cumtxh-jwxt-api&Date)

