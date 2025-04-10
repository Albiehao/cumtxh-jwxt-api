# 中国矿业大学徐海学院教务系统API

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

本项目提供对中国矿业大学徐海学院教务系统的API封装，方便开发者快速接入和使用教务系统功能。

## 功能特性

- ✅ 学生登录认证
- 📅 课程表查询
- 📝 考试成绩查询
- 📆 考试安排查询
- 🔄 数据导出(JSON/iCalendar格式)

## 项目结构

 ```
📦 school-api-master
├── 📂 data                      # 数据文件目录
│   └── 📄 schedule_2024_2.json  # 课程表数据示例
├── 📂 examples                  # 示例代码目录
│   ├── 📄 login_example.py      # 登录示例
│   ├── 📄 schedule_example.py   # 课程表查询示例
│   ├── 📄 exam_example.py       # 考试信息示例
│   ├── 📄 score_example.py      # 成绩查询示例
│   └── 📄 schedule_formatter.py # 课程表格式化工具
├── 📂 src                       # 源代码目录
│   └── 📂 school_api           # API核心模块
│       ├── 📂 models           # 数据模型
│       │   ├── 📄 course.py    # 课程模型
│       │   ├── 📄 schedule.py  # 课程表模型
│       │   └── 📄 student.py   # 学生模型
│       └── 📄 client.py        # API客户端
├── 📂 tests                     # 测试目录
├── 📄 setup.py                  # 项目安装配置
└── 📄 requirements.txt          # 项目依赖
```




## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
 ```


### 配置账号
编辑 config.ini 文件：

```ini
[jwxt]
username = 您的学号
password = 您的密码
 ```

### 使用示例
```python
from src.school_api.client import JwxtClient
from src.school_api.models.student import Student

# 创建客户端
client = JwxtClient()

# 创建学生对象
student = Student("学号", "密码")

# 登录
login_result = client.login(student)

if login_result["status"] == "success":
    # 获取课程表
    schedule = client.get_schedule(year="2024-2025", term=2)
    print(schedule)
else:
    print("登录失败")
 ```


## 示例代码
项目提供了多个使用示例，位于 examples 目录：

```
from src.school_api.client import JwxtClient
from src.school_api.models.student import Student

# 创建客户端
client = JwxtClient()

# 创建学生对象
student = Student("学号", "密码")

# 登录
login_result = client.login(student)

if login_result["status"] == "success":
    # 获取课程表
    schedule = client.get_schedule(year="2024-2025", term=2)
    print(schedule)
else:
    print("登录失败")
```

- login_example.py - 登录示例
- schedule_example.py - 课程表查询示例
- exam_example.py - 考试信息查询示例
- score_example.py - 成绩查询示例
- schedule_formatter.py - 课程表格式化工具
## 数据导出
支持将数据导出为多种格式：

- JSON格式
- iCalendar格式(可导入到日历应用)
- 文本表格格式
## 贡献指南
欢迎提交Pull Request或Issue。提交前请确保：

1. 代码符合PEP8规范
2. 添加适当的单元测试
3. 更新相关文档
## 许可证

本项目采用 [MIT 许可证](LICENSE)。

### 许可证条款摘要

- **允许**：
  - 自由使用、复制、修改、合并、发布、分发
  - 用于商业用途
  - 允许子授权
  
- **要求**：
  - 包含原始许可证和版权声明
  
- **免责声明**：
  - 不提供任何担保
  - 作者不对使用本软件造成的任何损害负责

完整许可证内容请查看项目根目录下的 [LICENSE](LICENSE) 文件。

## 📧 联系方式

如有问题或建议，欢迎通过以下方式联系：

- Issue: [GitHub Issues](https://github.com/Albiehao/cumtxh-jwxt-api/issues)
- Email: 1185902279@qq.com
- GitHub: [@Albiehao](https://github.com/Albiehao)

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Albiehao/cumtxh-jwxt-api&type=Date)](https://star-history.com/#Albiehao/cumtxh-jwxt-api&Date)