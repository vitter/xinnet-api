import argparse
import json
import sys
from xinnet_dns_api import (
    query_domain,
    query_records,
    query_record_unique,
    create_record,
    modify_record,
    delete_record
)


def run():
    parser = argparse.ArgumentParser(description="Xinnet DNS CLI 工具")
    subparsers = parser.add_subparsers(dest="command", help="命令")

    # 查询域名
    domain_parser = subparsers.add_parser("query-domain", help="查询域名信息")
    domain_parser.add_argument("domain", help="域名，例如 tmd2.com")

    # 查询解析记录
    list_parser = subparsers.add_parser("list", help="查询解析记录")
    list_parser.add_argument("domain", help="域名")
    list_parser.add_argument("domain_id", help="域名 ID")

    # 创建解析记录
    create_parser = subparsers.add_parser("create", help="添加解析记录")
    create_parser.add_argument("domain", help="域名")
    create_parser.add_argument("name", help="记录名称")
    create_parser.add_argument("type", help="记录类型，例如 A、CNAME")
    create_parser.add_argument("value", help="记录值")
    create_parser.add_argument("line", default="默认", help="线路类型，默认 默认")
    create_parser.add_argument("ttl", type=int, default=600, help="TTL 值")
    create_parser.add_argument("mx", type=int, default=0, help="MX 优先级")
    create_parser.add_argument("status", type=int, default=0, help="状态，0 表示启用")

    # 修改解析记录
    modify_parser = subparsers.add_parser("modify", help="修改解析记录")
    modify_parser.add_argument("domain", help="域名")
    modify_parser.add_argument("record_id", help="记录 ID")
    modify_parser.add_argument("value", help="新值")
    modify_parser.add_argument("ttl", type=int, default=600, help="TTL 值")
    modify_parser.add_argument("mx", type=int, default=0, help="MX 优先级")
    modify_parser.add_argument("status", type=int, default=0, help="状态")

    # 删除解析记录
    delete_parser = subparsers.add_parser("delete", help="删除解析记录")
    delete_parser.add_argument("domain", help="域名")
    delete_parser.add_argument("record_id", help="记录 ID")

    args = parser.parse_args()

    if args.command == "query-domain":
        res = query_domain(args.domain)
        print(json.dumps(res, indent=2, ensure_ascii=False))

    elif args.command == "list":
        res = query_records(args.domain, args.domain_id)
        print(json.dumps(res, indent=2, ensure_ascii=False))

    elif args.command == "create":
        res = create_record(
            domain_name=args.domain,
            record_name=args.name,
            rtype=args.type,
            value=args.value,
            line=args.line,
            ttl=args.ttl,
            mx=args.mx,
            status=args.status,
        )
        print(json.dumps(res, indent=2, ensure_ascii=False))

    elif args.command == "modify":
        res = modify_record(
            record_id=args.record_id,
            domain_name=args.domain,
            value=args.value,
            ttl=args.ttl,
            mx=args.mx,
            status=args.status
        )
        print(json.dumps(res, indent=2, ensure_ascii=False))

    elif args.command == "delete":
        res = delete_record(record_id=args.record_id, domain_name=args.domain)
        print(json.dumps(res, indent=2, ensure_ascii=False))

    else:
        parser.print_help()


if __name__ == "__main__":
    run()

