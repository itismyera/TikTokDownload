import logging
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from typing import List
import requests
from rich.console import Console

from constant import Constant
from untils import mkdir
from save_excel import SaveExecl


console = Console()
const = Constant()

logging.basicConfig(level=logging.INFO,
                    filename='log.txt',
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filemode='a')


class Kuaishou:

    def __init__(self) -> None:
        self.nickname = "" # 主播名字存放点
        self.datas = []
    def get_json(self) ->List:
        '''
        获取json数据
        '''
        response = requests.post(
            url=const.base_url, headers=const.headers, json=const.data)
        json_data = response.json()
        feeds = json_data['data']['visionProfilePhotoList']['feeds']
        # 下一页 链接pcursor导入data
        const.pcursor = json_data['data']['visionProfilePhotoList']['pcursor']
        return feeds

    def get_caption_photoUrl(self, feed):
        '''
        获取视频地址和标题
        feed: 单个视频数据
        '''
        try:
            filepath = os.getcwd() + '/' + 'kuaishou_downloads' + '/' + feed['author']['name'] if feed['author']['name'] else os.getcwd() + '/' + 'kuaishou_downloads' + '/' + '未知用户'
            self.nickname = feed['author']['name'] if feed['author']['name'] else "未知"
            caption = feed['photo']['caption']  # title
            photoUrl = feed['photo']['photoUrl']  # video link
            caption = re.sub('[ \\/:*?"<>|\n\t]', '', caption)
            caption = caption[:128] if len(caption)>128 else caption
            video_data = requests.get(photoUrl).content
            if caption:
                # time_ns = time.time()
                # self.save_video(os.path.normpath(filepath), caption + '_' + str(time_ns) + '.mp4', video_data,photoUrl)
                self.save_video(os.path.normpath(filepath), caption + '.mp4', video_data,photoUrl)
        except Exception as e:
            logging.error(f'错误:{e},获取数据失败,请检查网址是否正确,也可能cookies已过期!')
            console.print('[blue]获取数据失败,请检查网址是否正确,也可能cookies已过期!')

    def save_video(self, path: Path, filename: str, video_data,url):
        '''
        保存视频文件
        '''
        mkdir(path)
        filepath = os.path.normpath(os.path.join(path, filename))
        if os.path.exists(filepath):
            print(f'{filename} >>> 已存在!!!')
            # time.sleep(1)
            return
        with open(filepath, 'wb') as f:
            f.write(video_data)
            now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            console.print(
                f'创建时间:{now_time}\n文件:[yellow]{filename}\n状态:[green]下载完成！')
            console.print('[blue]-'*20)
            self.datas.append([now_time,filename,path,url])

    def save_excel(self, nickname):
        '''
        保存excel数据
        '''
        print('请输入保存的excel文件名称(例如:快手.xlsx):')
        # ex_file_name = input()
        ex_file_name = nickname
        se = SaveExecl(ex_file_name, sheet_name = '快手下载数据')
        num = 1 # 序号 
        one_row = ['序号', '创建时间', '文件名', '路径','网址']
        # 注:添加第一行,map是生成器函数，需用list执行生成器
        list(map(lambda x:se.save_to_excel(1,x+1,one_row[x]), range(len(one_row))))
        for row,data in enumerate(self.datas):
            se.save_to_excel(row+2,1,num)
            num += 1
            for col,d in enumerate(data):
                se.save_to_excel(row+2,col+2,d)
        se.sucess_sing(True)
        console.print('[red]保存成功！')

    def main(self):
        '''
        主函数
        '''
        page_num = 1
        start_time = time.time()

        while True:
            if const.pcursor != 'no_more':
                feeds = self.get_json()
                with ThreadPoolExecutor(max_workers=5) as executor:
                    executor.map(self.get_caption_photoUrl, feeds)
                logging.info(f'正在下载第{page_num}页数据...')
                page_num += 1
            else:
                console.print(f'[red]已全部完成下载！')
                logging.info(f'{self.nickname}已全部完成下载！')
                break
        logging.info(f'主播:{self.nickname}的视频下载总耗时:{time.time()-start_time}秒')
        time.sleep(2)
        console.print(f'[red]总耗时:{time.time()-start_time-2}秒')
        self.save_excel(self.nickname)


if __name__ == '__main__':
    kuaishou = Kuaishou()
    kuaishou.main()
