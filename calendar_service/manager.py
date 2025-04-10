import os
from .service import start_calendar_service

def main():
    ics_path = os.path.join('..', 'out', 'schedule', 'schedule_2024_2.ics')
    start_calendar_service(ics_path)
    
    # 保持主线程运行
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n服务已停止")

if __name__ == '__main__':
    main()