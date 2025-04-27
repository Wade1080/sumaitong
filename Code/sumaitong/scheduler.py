import schedule
import time
import subprocess
import logging
import os

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_script(script_path, working_dir=None):
    """运行指定的Python脚本"""
    try:
        logging.info(f"开始执行脚本: {script_path}")
        
        # 如果指定了工作目录，切换到该目录
        original_dir = os.getcwd()
        if working_dir:
            os.chdir(working_dir)
            logging.info(f"切换到工作目录: {working_dir}")
        
        # 执行脚本
        subprocess.run(['python', script_path], check=True)
        
        # 如果切换了目录，切换回原目录
        if working_dir:
            os.chdir(original_dir)
            
        logging.info(f"脚本执行完成: {script_path}")
    except subprocess.CalledProcessError as e:
        logging.error(f"执行脚本时出错 {script_path}: {e}")
    except Exception as e:
        logging.error(f"发生未知错误: {e}")
    finally:
        # 确保总是切换回原目录
        if working_dir:
            os.chdir(original_dir)

def schedule_tasks(script1_path, script2_path, time_to_run, script2_working_dir=None):
    """设置定时任务"""
    # 清除所有现有任务
    schedule.clear()
    
    # 设置定时任务
    schedule.every().day.at(time_to_run).do(run_script, script1_path)
    schedule.every().day.at(time_to_run).do(run_script, script2_path, script2_working_dir)
    
    logging.info(f"已设置定时任务，将在每天 {time_to_run} 执行")
    
    # 持续运行调度器
    while True:
        schedule.run_pending()
        time.sleep(3)  # 每分钟检查一次

if __name__ == "__main__":
    # 这里需要您提供要执行的脚本路径和执行时间
    script1 = "./sumaitong_login.py"  # 请替换为第一个脚本的路径
    script2 = "./run.py"  # 请替换为第二个脚本的路径
    run_time = "09:00"  # 请替换为您想要执行的时间
    script2_working_dir = r"E:\Code\sumaitong"  # Scrapy项目的根目录
    schedule_tasks(script1, script2, run_time, script2_working_dir)
