import os

from rich.console import Console

console = Console()


def your_cookies() -> str:
    print('请将COOKIES复制到此处，按enter继续.')
    # cookies = input()
    cookies = "did=web_c6c0b3351566fd0c8c4aa693c2bb4b36; didv=1649765402460; kpf=PC_WEB; kpn=KUAISHOU_VISION; clientid=3; client_key=65890b29; userId=1688968822; kuaishou.server.web_st=ChZrdWFpc2hvdS5zZXJ2ZXIud2ViLnN0EqABLQMvy57-lMK9fFxeDVtAdm4-foTUXidiubuWxPzAHEHW4Opkyz8qQA_1lgi7avgI6NB-XHihS3Uv0-lc5RZctqZDk47xvqAARscYaovYoxhrJ26GfrrChwDFij6mFNe5WnT8XWZD60xVkrx5B-O_oWK55du7ffZAjC92SK7XBXno5v6H4rD26LRSyFrhpwh6hVgOMREN5b3Or-Ie88k0-BoSPic3ODA5dC1PisVLgMefbzz0IiB0tXQ2H4E4qlHBQ_7m6I-nnrXL_POmnWhORQLLHUhLTigFMAE; kuaishou.server.web_ph=d877fea6303c41bf384a3a1cbc313a530d58"
    return cookies


def target_your_urls() -> str:
    print('请将目标用户的url复制到此处，按enter继续.')
    # url = input()
    # url = "https://www.kuaishou.com/profile/3x3iabhcnyqpjry" #小蓝蓝plus
    # url = "https://www.kuaishou.com/profile/3xmxtgjhi9x6xg2" #猫女骑
    # url = "https://www.kuaishou.com/profile/3xk3j8k7hj4n992" #婷婷与直男
    url = "https://www.kuaishou.com/profile/3xi2ppw4g866pyk" #刘二萌🐰
    
    return url


def mkdir(path):
    """
    创建文件夹
    """
    if not os.path.exists(path):
        os.makedirs(path)
