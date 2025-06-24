#!/usr/bin/env python3
import os
import sys
from xinnet_dns_api import query_domain, query_records, delete_record
from logger import log_info, log_error

def main():
    certbot_domain = os.environ.get("CERTBOT_DOMAIN")
    certbot_validation = os.environ.get("CERTBOT_VALIDATION")
    acme_record_name = "_acme-challenge"

    if not certbot_domain or not certbot_validation:
        log_error("CERTBOT_DOMAIN 或 CERTBOT_VALIDATION 环境变量未设置。")
        sys.exit(1)

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

    # 查询所有记录
    records_info = query_records(top_domain_name, domain_id)
    if not records_info or not records_info.get("data"):
        log_error(f"无法获取 DNS 记录: {certbot_domain}")
        sys.exit(1)

    # 找出对应的 TXT 记录并删除
    records = records_info["data"].get("list", [])
    for record in records:
        if (record['recordName'] == f"{acme_record_name}.{top_domain_name}" and 
            record["type"] == "TXT" and 
            record["value"] == certbot_validation):
            log_info(f"删除 TXT 记录: ID={record['recordId']}, 值={record['value']}")
            delete_record(record["recordId"], top_domain_name)
            break
    else:
        log_error("未找到需要删除的 TXT 验证记录。")

if __name__ == "__main__":
    main()

