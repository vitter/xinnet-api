
import requests
import json
import hmac
import hashlib
from datetime import datetime, timezone
from urllib.parse import urlparse
from dotenv import load_dotenv
import os

from logger import log_info, log_error
load_dotenv()

BASE_URL = "https://apiv2.xinnet.com"
ACCESS_ID = os.getenv("XINNET_ACCESS_ID")
ACCESS_SECRET = os.getenv("XINNET_ACCESS_SECRET")

assert ACCESS_ID and ACCESS_SECRET, "请在.env文件中设置 XINNET_ACCESS_ID 和 XINNET_ACCESS_SECRET"

def _get_utc_timestamp():
    return datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")


def _sign_request(method, url_path, body, timestamp):
    algorithm = "HMAC-SHA256"
    string_to_sign = f"{algorithm}\n{timestamp}\n{method}\n{url_path}\n{body}"
    signature = hmac.new(
        ACCESS_SECRET.encode("utf-8"),
        string_to_sign.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    auth = f"{algorithm} Access={ACCESS_ID}, Signature={signature}"
    return auth


def _post(endpoint, payload, use_cache=False, cache_expire=300):
    url = BASE_URL + endpoint
    url_path = urlparse(url).path + "/"  # 注意尾部的 /
    body_str = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
    timestamp = _get_utc_timestamp()
    headers = {
        "timestamp": timestamp,
        "authorization": _sign_request("POST", url_path, body_str, timestamp),
        "Content-Type": "application/json"
    }


    try:
        log_info(f"[POST] {url_path} -> {body_str}")
        response = requests.post(url, headers=headers, data=body_str.encode('utf-8'), timeout=10)
        response.raise_for_status()
        result = response.json()
        log_info(f"[RESPONSE] {result}")

        return result
    except Exception as e:
        log_error(f"[ERROR] {e}")
        return None


# --------------------------------------------
# 🧩 API 功能封装函数
def query_domain(domain_name, use_cache=True):
    return _post("/api/dns/queryDomain", {"domainName": domain_name})


def query_records(domain_name, domain_id, page_no=1, page_size=20):
    return _post("/api/dns/queryRecordsPage", {
        "domainName": domain_name,
        "domainId": str(domain_id),
        "pageNo": page_no,
        "pageSize": page_size
    })


def query_record_unique(domain_name, record_name, rtype, value, line="默认"):
    return _post("/api/dns/queryRecordsUnique", {
        "domainName": domain_name,
        "recordName": record_name,
        "type": rtype,
        "value": value,
        "line": line
    })


def create_record(domain_name, record_name, rtype, value, line="默认", ttl=600, mx=0, status=0):
    return _post("/api/dns/create", {
        "domainName": domain_name,
        "recordName": record_name,
        "type": rtype,
        "value": value,
        "line": line,
        "ttl": ttl,
        "mx": mx,
        "status": status
    })


def modify_record(record_id, domain_name, value=None, ttl=600, mx=0, status=0):
    data = {
        "recordId": record_id,
        "domainName": domain_name,
        "ttl": ttl,
        "mx": mx,
        "status": status
    }
    if value:
        data["value"] = value
    return _post("/api/dns/modify", data)


def delete_record(record_id, domain_name):
    return _post("/api/dns/delete", {
        "recordId": record_id,
        "domainName": domain_name
    })

