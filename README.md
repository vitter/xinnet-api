# xinnet-api
Xinnet API脚本工具

这个脚本程序通过Xinnet的API接口可以实现Cretbot Hook自动化。CLI工具可以增删查改域名。

首先你要在Xinnet后台申请域名API管理：开通成功后，请添加接入IP，添加后方可正常使用API。API开通后有效期为1年，需在到期前一个月内进行在线年审。逾期未年审，将限制API使用。

API 账号：agent12345
API 密钥：是一串随机字符串

记得添加白名单IP，就是你执行接口程序的IP。

文件结构

xinnetapi
├── .env    <--    配置Xinnet的API帐号和密钥
├── cli.py    <--    功能命令行工具
├── logger.py    <--    日志记录器
├── xinnet_auth.py    <--    Certbot Auth Hook：用于certbot在验证前添加TXT记录 ( chmod +x )
├── xinnet_cleanup.py    <--    Certbot Cleanup Hook：用于certbot验证完成后删除TXT记录 ( chmod +x )
├── xinnet_dns_api.py    <--    新网DNS API 执行 增/查/改/删 记录的类# xinnet-api
└── xinnet_dns_log.txt    <--    log记录文件

root@Vfocus:~/xinnetapi# python cli.py
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

  

docker run -it --rm --name certbot -v "/root/xinnetapi/:/root/xinnetapi/" -v "/etc/letsencrypt/:/etc/letsencrypt/"  certbot/certbot  certonly --manual --preferred-challenges dns --manual-auth-hook "/root/xinnetapi/xinnet_auth.py" --manual-cleanup-hook "/root/xinnetapi/xinnet_cleanup.py" -d tmd2.com -d *.tmd2.com

docker run -i --rm --name certbot -v "/root/xinnetapi/:/root/xinnetapi/" -v "/etc/letsencrypt/:/etc/letsencrypt/"  certbot/certbot  renew --manual --preferred-challenges dns --manual-auth-hook "/root/xinnetapi/xinnet_auth.py" --manual-cleanup-hook "/root/xinnetapi/xinnet_cleanup.py"
