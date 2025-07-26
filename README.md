# xinnet-api

> 新网（Xinnet）API 脚本工具，支持 Certbot DNS 自动化与命令行域名解析管理。

## 功能简介

本工具通过 Xinnet API 实现 Certbot DNS 验证自动化，可用于 Let's Encrypt 证书申请与续期。内置 CLI 支持域名解析记录的增删查改。

## 快速开始

### 1. API 申请与配置

- 在新网后台申请 API 管理权限，开通后添加本机公网 IP 至白名单
- API 有效期为 1 年，需在到期前 1 个月内年审，否则将被限制使用
- 获取 API 账号（如：`agent12345`）与密钥（随机字符串），并填写到 `.env` 文件：

```env
XINNET_ACCESS_ID==你的账号
XINNET_ACCESS_SECRET=你的密钥
```

### 2. 文件结构说明

```
xinnetapi/
├── .env                # API 账号和密钥配置
├── cli.py              # 命令行工具
├── logger.py           # 日志记录器
├── xinnet_auth.py      # Certbot Auth Hook，添加 TXT 记录 （需chmod +x 执行命令权限）
├── xinnet_cleanup.py   # Certbot Cleanup Hook，删除 TXT 记录 （需chmod +x 执行命令权限）
├── xinnet_dns_api.py   # 新网 DNS API 操作类
└── xinnet_dns_log.txt  # 日志文件
```

## CLI 用法

```bash
python cli.py -h
```

**输出：**

```
usage: cli.py [-h] {query-domain,list,create,modify,delete} ...

Xinnet DNS CLI 工具

positional arguments:
  {query-domain,list,create,modify,delete}
                        命令
    query-domain        查询域名信息
    list                查询解析记录
    create              添加解析记录
    modify              修改解析记录
    delete              删除解析记录

optional arguments:
  -h, --help            show this help message and exit
```

## Certbot 集成示例

### 申请证书

```bash
docker run -it --rm --name certbot \
  -v "/root/xinnetapi/:/root/xinnetapi/" \
  -v "/etc/letsencrypt/:/etc/letsencrypt/" \
  certbot/certbot certonly --manual --preferred-challenges dns \
  --manual-auth-hook "/root/xinnetapi/xinnet_auth.py" \
  --manual-cleanup-hook "/root/xinnetapi/xinnet_cleanup.py" \
  -d tmd2.com -d *.tmd2.com
```

### 续期证书

```bash
docker run -it --rm --name certbot \
  -v "/root/xinnetapi/:/root/xinnetapi/" \
  -v "/etc/letsencrypt/:/etc/letsencrypt/" \
  certbot/certbot renew --manual --preferred-challenges dns \
  --manual-auth-hook "/root/xinnetapi/xinnet_auth.py" \
  --manual-cleanup-hook "/root/xinnetapi/xinnet_cleanup.py"
```

## 注意事项

- 确保已正确配置 API 权限和白名单 IP
- 检查 `.env` 文件配置是否正确
- 如遇问题请查看 `xinnet_dns_log.txt` 日志文件
