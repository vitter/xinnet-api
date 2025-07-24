# xinnet_dns/logger.py

import logging
import os

# 获取当前脚本所在目录，确保日志文件写入到脚本目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, "xinnet_dns_log.txt")

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# 创建logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 清除现有的处理器，避免重复
logger.handlers.clear()

# 创建文件处理器，记录所有级别的日志
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
file_handler.setFormatter(file_formatter)

# 创建控制台处理器，只输出ERROR级别及以上的日志
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
console_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
console_handler.setFormatter(console_formatter)

# 添加处理器到logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def log_info(msg):
    logger.info(msg)
    # 强制刷新到磁盘
    for handler in logger.handlers:
        if hasattr(handler, 'flush'):
            handler.flush()

def log_error(msg):
    logger.error(msg)
    # 强制刷新到磁盘
    for handler in logger.handlers:
        if hasattr(handler, 'flush'):
            handler.flush()

def log_debug(msg):
    logger.debug(msg)
    # 强制刷新到磁盘
    for handler in logger.handlers:
        if hasattr(handler, 'flush'):
            handler.flush()

def get_log_file_path():
    return LOG_FILE

def log_startup_info():
    """记录启动信息，帮助调试"""
    log_info(f"=== 脚本启动 ===")
    log_info(f"当前时间: {__import__('datetime').datetime.now()}")
    log_info(f"环境变量 CERTBOT_DOMAIN: {os.getenv('CERTBOT_DOMAIN', '未设置')}")
    log_info(f"环境变量 CERTBOT_VALIDATION: {os.getenv('CERTBOT_VALIDATION', '未设置')}")
    log_info(f"=================")

