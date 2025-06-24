#!/usr/bin/env python3
import os
import sys
from xinnet_dns_api import query_domain, create_record
from logger import log_info, log_error

def main():
    certbot_domain = os.environ.get("CERTBOT_DOMAIN")
    certbot_validation = os.environ.get("CERTBOT_VALIDATION")
    
    if not certbot_domain or not certbot_validation:
        log_error("CERTBOT_DOMAIN 或 CERTBOT_VALIDATION 环境变量未设置。")
        sys.exit(1)

    # 提取主域名
    log_info(f"认证域名: {certbot_domain}, 验证值: {certbot_validation}")
    acme_record_name = "_acme-challenge"

    # 获取域名信息
    domain_info = query_domain(certbot_domain)
    if not domain_info or not domain_info.get("data"):
        log_error(f"无法查询域名信息: {certbot_domain}")
        sys.exit(1)

    response = query_domain(certbot_domain)

    if not response or "data" not in response:
        log_error(f"查询域名失败：{response}")
        exit(1)

    domain_data = response["data"]
    top_domain_name = domain_data.get("name")

    domain_id = domain_data["id"]

    # 创建 TXT 记录
    result = create_record(
        domain_name=top_domain_name,
        record_name=f"{acme_record_name}.{top_domain_name}",
        rtype="TXT",
        value=certbot_validation,
        ttl=600
    )

    if result and result.get("code") == "0":
        log_info(f"成功添加 TXT 记录: _acme-challenge.{certbot_domain}")
    else:
        log_error(f"添加 TXT 记录失败: {result}")
        sys.exit(1)

    # 等待解析生效
    import time
    time.sleep(25)

if __name__ == "__main__":
    main()

