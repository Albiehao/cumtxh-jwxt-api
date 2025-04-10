import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calendar_service.auto_update import auto_update_schedule

if __name__ == '__main__':
    print("日历服务已启动，访问地址: http://0.0.0.0:5000/calendar.ics")
    auto_update_schedule()