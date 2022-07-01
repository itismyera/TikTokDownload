# coding:utf-8
import json
import os
import pprint
import re
import string
import sys
import time
import ctypes
import os
import platform
from zhon.hanzi import punctuation
import requests
import urllib3
 
urllib3.disable_warnings()
 
 
# 请求网页
def req_data(url, id, pcursor, ck, ua):
    # 请求头
    headers = {
        'content-type': 'application/json',
        'Cookie': ck,
        'Host': 'www.kuaishou.com',
        'Origin': 'https://www.kuaishou.com',
        'Referer': 'https://www.kuaishou.com/profile/' + id,
        'User-Agent': ua
    }
    # 请求参数
    data = {
        'operationName': 'visionProfilePhotoList',
        'query': "query visionProfilePhotoList($pcursor: String, $userId: String, $page: String, $webPageArea: "
                 "String) {\n  visionProfilePhotoList(pcursor: $pcursor, userId: $userId, page: $page, webPageArea: "
                 "$webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      type\n      author {\n  "
                 "      id\n        name\n        following\n        headerUrl\n        headerUrls {\n          cdn\n "
                 "         url\n          __typename\n        }\n        __typename\n      }\n      tags {\n        "
                 "type\n        name\n        __typename\n      }\n      photo {\n        id\n        duration\n      "
                 "  caption\n        likeCount\n        realLikeCount\n        coverUrl\n        coverUrls {\n        "
                 "  cdn\n          url\n          __typename\n        }\n        photoUrls {\n          cdn\n         "
                 " url\n          __typename\n        }\n        photoUrl\n        liked\n        timestamp\n        "
                 "expTag\n        animatedCoverUrl\n        stereoType\n        videoRatio\n        "
                 "profileUserTopPhoto\n        __typename\n      }\n      canAddComment\n      currentPcursor\n      "
                 "llsid\n      status\n      __typename\n    }\n    hostName\n    pcursor\n    __typename\n  }\n}\n",
        'variables': {'userId': id, 'pcursor': pcursor, 'page': 'profile'}
    }
    data = json.dumps(data)
    # url = 'https://www.kuaishou.com/graphql'
    # https://www.kuaishou.com/profile/3x3iabhcnyqpjry
    # print(id)
    data_json = requests.post(url=url, headers=headers, data=data, timeout=6.05).json()

    response = requests.post(url=url, headers=headers, data=data)
    data_json = response.json()

    # data_json = json.loads(requests.post(url=url, headers=headers, data=data, timeout=6.05).json())
    # pprint.pprint(data_json)
    return data_json
 
 
# 清洗文件名
def rep_char(chars):
    eg_punctuation = string.punctuation
    ch_punctuation = punctuation
    # print("所有标点符号：", eg_punctuation, ch_punctuation)
    for item1 in eg_punctuation:
        chars = chars.replace(item1, '')
    for item2 in ch_punctuation:
        chars = chars.replace(item2, '')
    chars = chars.replace(' ', '').replace('\n', '').replace('\xa0', '').replace('\r', '')
    return chars
 
 
# 磁盘内存检查
def get_free_space():
    folder = os.path.abspath(sys.path[0])
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value / 1024 / 1024 / 1024
    else:
        st = os.statvfs(folder)
        return st.f_bavail * st.f_frsize / 1024 / 1024
 
 
# 保存数据
def save(url, page, ck, ua, selfid, idlist):
    except_lit = []
    count = 0
    if idlist == []:
        idlist = get_all_ids(url, page, ck, ua, selfid)
        return
    for id in idlist:
        count = count + 1
        print(f'第{count}位关注：{id} 全部视频下载中...')
        num = 0
        # 循环下载视频，直到 page == 'no_more'
        while page != 'no_more':
            time.sleep(1)
            data = req_data(url, id, page, ck, ua)
            # 获取翻页的参数
            print(data)
            next_page_Pcursor = data['data']['visionProfilePhotoList']['pcursor']

            page = next_page_Pcursor
            print(next_page_Pcursor)
            data_list = data['data']['visionProfilePhotoList']['feeds']
            for item in data_list:
                num = num + 1
                video_name = item['photo']['caption']
                video_url = item['photo']['photoUrl']
                author = item['author']['name']
                author = rep_char(author)
                video_name = rep_char(video_name)
                path = './video1'
                if not os.path.exists(path + '/' + author + '/'):
                    os.makedirs(path + '/' + author + '/')
                filepath = path + '/' + author + '/' + str(num) + '.' + video_name + '.mp4'
                if os.path.exists(filepath):
                    print(f'{num}、 {video_name} >>> 已存在!!!')
                    # time.sleep(1)
                    continue
                # 请求二进制视频数据
                try:
                    video_content = requests.get(url=video_url, timeout=(3, 7)).content
                except:
                    strss = f'{author}_{num}video_name：{video_url}'
                    except_lit.append(strss)
                    continue
                with open(filepath, mode='wb') as f:
                    f.write(video_content)
                print(f'{num}、 {video_name} >>> 下载完成!!!')
                # 判断剩余容量是否充足
                free_space = get_free_space()
                if free_space <= 1:
                    break
        # pcursor = page 这个变量的值必须为空，不用动他，它是换页的参数
        page = ''
        print(f'第{count}位关注：{id} 全部视频下载完成！！！')
    with open('yc_info.txt', 'a') as f:
        f.write(except_lit)
        print('异常保存成功')
    print(except_lit)
 
 
# 获取全部关注页面数据
def req_follow_data(url, pcursor, ck, ua, selfid):
    # 请求头
    headers = {
        'content-type': 'application/json',
        'Cookie': ck,
        'Host': 'www.kuaishou.com',
        'Origin': 'https://www.kuaishou.com',
        'Referer': 'https://www.kuaishou.com/profile/' + selfid,
        'User-Agent': ua
    }
    # 请求参数
    data = {
        'operationName': 'visionProfileUserList',
        'query': 'query visionProfileUserList($pcursor: String, $ftype: Int) {\n  visionProfileUserList(pcursor: '
                 '$pcursor, ftype: $ftype) {\n    result\n    fols {\n      user_name\n      headurl\n      '
                 'user_text\n      isFollowing\n      user_id\n      __typename\n    }\n    hostName\n    pcursor\n   '
                 ' __typename\n  }\n}\n',
        'variables': {'ftype': 1, 'pcursor': pcursor}
    }
    data = json.dumps(data)
    follow_json = requests.post(url=url, headers=headers, data=data).json()
    # pprint.pprint(follow_json)
    return follow_json
 
 
# 获取全部关注的id
def get_all_ids(url, page, ck, ua, selfid):
    id_list = []
    num = sign = 0
    info_str = ''
    # 循环保存id，直到 Pcursor == 'no_more'
    while page != 'no_more':
        time.sleep(1)
        follow_data = req_follow_data(url, page, ck, ua, selfid)
        # 获取翻页的参数
        next_pcursor = follow_data['data']['visionProfileUserList']['pcursor']
        page = next_pcursor
        sign = sign + 1
        print(f'第{sign}页:{next_pcursor}')
        fols_list = follow_data['data']['visionProfileUserList']['fols']
        for item in fols_list:
            num = num + 1
            user_name = item['user_name']
            user_id = item['user_id']
            id_list.append(user_id)
            logStr = f'{num}、 {user_name}：{user_id} >>> ID获取成功！！！'
            info_str = info_str + '\n' + logStr
            print(logStr)

    with open('info_str.txt', 'a+') as f:
        f.write(info_str)

    # print(id_list)
    # print(id_list)
    return id_list
 
 
if __name__ == '__main__':
    link = 'https://www.kuaishou.com/graphql'
    # pcursor这个变量的值开始必须为空，不用动他，它是换页的参数
    # selfid 是自己账号网址的最后面那一串 例如 https://www.kuaishou.com/profile/3xkfgnn9hkacbwc selfid 就是 3xkfgnn9hkacbwc
    selfid = '3xxi9qk7z3gdtzu'
    pcursor = ''
    # ck =''  引号中间填登录后的 Cookie 值
    ck ='web_c6c0b3351566fd0c8c4aa693c2bb4b36; didv=1649765402460; kpf=PC_WEB; kpn=KUAISHOU_VISION; clientid=3; client_key=65890b29; userId=1688968822; kuaishou.server.web_st=ChZrdWFpc2hvdS5zZXJ2ZXIud2ViLnN0EqABIc20T-3I7MIC5ZjSrnLOjO22PWxCiQo3oiPpNGGHs1afEHsnVaUOgVWoA4S629vWO6djaGdQC4MTawIaOwZAi9C-GNJN7_70zOy0KaOeEaxSq8Pz6Ikk_CShSYQbRvDp38LeYOIX18cF7mMgzT7vE-f5-J6MMGqy0MtxLLsjAlwKxLChvwTs0ylO3ayQ694Hq58RuHezKTmJxf_PpXSiWBoStEyT9S95saEmiR8Dg-bb1DKRIiCPMHrla6rrrq-PqNaagKpzxiyaor2-eHmyhmgfg6_XwSgFMAE; kuaishou.server.web_ph=b9ec858adf19787e4cdad96e163e37222e1b'
    # ua = '' 引号中间填 User-Agent
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    idlist = ['3x3iabhcnyqpjry']
    # idlist = []
    save(link, pcursor, ck, ua, selfid, idlist)