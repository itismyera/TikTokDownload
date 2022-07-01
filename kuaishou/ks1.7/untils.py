import os

from rich.console import Console

console = Console()


def your_cookies() -> str:
    print('请将COOKIES复制到此处，按enter继续.')
    # cookies = input()
    cookies = "did=web_c6c0b3351566fd0c8c4aa693c2bb4b36; didv=1649765402460; kpf=PC_WEB; kpn=KUAISHOU_VISION; clientid=3; client_key=65890b29; userId=1688968822; ktrace-context=1|MS43NjQ1ODM2OTgyODY2OTgyLjE3Nzk1OTIxLjE2NTY2NDYzMjgxNjcuNjk3NDg=|MS43NjQ1ODM2OTgyODY2OTgyLjk4MjExNjE4LjE2NTY2NDYzMjgxNjcuNjk3NDk=|0|graphql-server|webservice|false|NA; kuaishou.server.web_st=ChZrdWFpc2hvdS5zZXJ2ZXIud2ViLnN0EqABveHRT5Rg_wGzt9EZeLI_r1uU3k9y2vz9K4BiO0iha_Uzxn2lQ4BrdCBAKqL0_Mg6iRIGb5cPtu05T-cXyv6JMbIoZnjFEtGjXfcWsI6dO1jDnsjRslmo3qGVLWusZtqPSn8LzlaSzYY_VM5adeI8tfvfLpcnBl_M0NPPGt9f47YowXeZ_w5PKCXA1Y4Mb7oWoN42Hzt5e8RxcQmqOUXyYhoS_47WhL3lHryRDUsr7Z0BqLaUIiBNS_9DlPQOSKbliyVYpAF6EOV8_waerfFBEoQewpJ0sygFMAE; kuaishou.server.web_ph=021d5d65206861536fd282ebeaabe99da1ff"
    return cookies


def target_your_urls() -> str:
    print('请将目标用户的url复制到此处，按enter继续.')
    # url = input()
    url = "https://www.kuaishou.com/profile/3x3iabhcnyqpjry" #小蓝蓝plus
    return url


def mkdir(path):
    """
    创建文件夹
    """
    if not os.path.exists(path):
        os.makedirs(path)
