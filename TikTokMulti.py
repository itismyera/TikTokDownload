#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Description:TikTokMulti.py
@Date       :2021/05/25 00:14:28
@Author     :JohnserfSeed
@version    :1.2
@License    :(C)Copyright 2019-2021, Liugroup-NLPR-CASIA
@Mail       :johnserfseed@gmail.com
'''

import requests,json,os,time,configparser,re,sys,glob
import TikTokDownload

class TikTok():
    #初始化
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.66'
            }

        #绘制布局
        print("#" * 120)
        print( 
    """
                                                TikTokDownload V1.2.2
    使用说明：
            1、运行软件前先打开目录下 conf.ini 文件按照要求进行配置
            2、批量下载可直接修改配置文件，单一视频下载请直接打开粘贴视频链接即可
            3、如有您有任何bug或者意见反馈请在 https://github.com/Johnserf-Seed/TikTokDownload/issues 发起
            4、后续可能会更新GUI界面，操作更简单

    注意：  单个视频链接与用户主页链接要分清，软件闪退可以通过终端运行查看报错信息（一般是链接弄错的问题）
    """
        )
        print("#" * 120)
        print('\r')

        if os.path.isfile("conf.ini") == True:
            pass
        else:
            print('----没有检测到配置文件，生成中----\r')
            try:
                self.cf = configparser.ConfigParser()
                # 往配置文件写入内容
                self.cf.add_section("url")
                self.cf.set("url", "uid", "https://v.douyin.com/JcjJ5Tq/")
                self.cf.add_section("music")
                self.cf.set("music", "musicarg", "yes")
                self.cf.add_section("count")
                self.cf.set("count", "count", "35")
                self.cf.add_section("save")
                self.cf.set("save", "url", "/Download/")
                self.cf.add_section("mode")
                self.cf.set("mode", "mode", "post")
                self.cf.add_section("stopVid")
                self.cf.set("stopVid", "stopVid", "")
                self.cf.add_section("max_download")
                self.cf.set("max_download", "max_download", "0")
                self.cf.add_section("max_cursor")
                self.cf.set("max_cursor", "max_cursor", "0")
                with open("conf.ini","a+") as f:
                    self.cf.write(f)
                print('----生成成功----')
            except:
                input('----生成失败,正在为您下载配置文件----')
                r =requests.get('https://gitee.com/johnserfseed/TikTokDownload/raw/main/conf.ini')
                with open("conf.ini", "a+") as conf:
                    conf.write(r.content)
                sys.exit()

        #实例化读取配置文件
        self.cf = configparser.ConfigParser()

        #用utf-8防止出错
        self.cf.read("conf.ini", encoding="utf-8")

        #读取保存路径
        self.save = os.getcwd() + self.cf.get("save","url")

        #读取下载视频个数
        self.count = int(self.cf.get("count","count"))
    
        #读取下载是否下载音频
        self.musicarg = self.cf.get("music","musicarg")

        #读取用户主页地址
        self.uid = input('批量下载直接回车，单一视频下载直接粘贴视频链接：')
        if self.uid == '':
            self.uid = self.cf.get("url","uid")
        else:
            pass

        #读取下载模式
        self.mode = self.cf.get("mode","mode")

        #保存用户名
        self.nickname = ""

        #读取下载停止标记
        self.stopVid = str(self.cf.get("stopVid","stopVid"))

        #开始解析的页数
        self.max_cursor = self.cf.get("max_cursor","max_cursor")

        #最大下载数量
        self.max_download = int(self.cf.get("max_download","max_download"))

        self.download_num = 0

        print('----读取配置完成----\r')
        self.judge_link()

    #匹配粘贴的url地址
    def Find(self,string): 
        # findall() 查找匹配正则表达式的字符串
        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
        return url

    def fabu_time(self,t,type=0):
        '''
        将时间戳转换成时间格式
        :param t:
        :return:
        '''
        timeArray = time.localtime(t)
        fabu_time = '2021'
        if type == 1:
            fabu_time = '{}'.format(time.strftime("%Y%m%d", timeArray))
        else:
            fabu_time = '({})'.format(time.strftime("%Y-%m-%d %H-%M-%S", timeArray))
        return fabu_time

    def get_follow_url(self, user_id, sec_user_id):
        ts = str(time.time()).split(".")[0]
        _rticket = str(time.time() * 1000).split(".")[0]
        max_time = ts
        url= "https://api.amemv.com/aweme/v1/user/{}/list/?" \
          "user_id={}" \
          "&max_time={}" \
          "&count=20&offset=0&source_type=1&address_book_access=2&gps_access=2" \
          "&ts={}" \
          "&js_sdk_version=1.16.3.5&app_type=normal&manifest_version_code=630" \
          "&_rticket={}" \
          "&ac=wifi&device_id=47xxxx747444&iid=18468xxx477740845" \
          "&os_version=8.0.0&channel=wandoujia_aweme1&version_code=630" \
          "&device_type=HUAWEI%20NXT-AL10&language=zh&resolution=1080*1812&openudid=b202a24ebxxx538a" \
          "&update_version_code=6302&app_name=aweme&version_name=6.3.0&os_api=26&device_brand=HUAWEI&ssmix=a" \
          "&device_platform=android&dpi=480&aid=1128" \
          "&sec_user_id={}".format(self.mode, user_id, max_time, ts, _rticket, sec_user_id)
        return url


    #判断个人主页api链接
    def judge_link(self):
        #获取解码后原地址
        r = requests.get(url = self.Find(self.uid)[0])
        multi_url = 'https://www.douyin.com/user/'
        #multi_url = 'https://www.iesdouyin.com/share/user/'

        # with open(self.save + "aa.txt", 'a+') as f:
        #         f.write(r)

        # return

        #判断输入的是不是用户主页
        #if r.url[:27] == multi_url:
        if r.url[:28] == multi_url:
            print('----为您下载多个视频----\r')
            #获取用户sec_uid
            #key = re.findall('&sec_uid=(.*?)&',str(r.url))[0]
            # key = re.findall('/user/(.*?)?',str(r.url))[0]
            key = re.findall('/user/(.*)\?',str(r.url))[0]
            if not key:
                key  = r.url[28:83]
            print('----'+'用户的sec_id='+key+'----')
        else:
            print('----为您下载单个视频----\r')
            print(r.url)
            urlarg,musicarg = TikTokDownload.main()
            TikTokDownload.video_download(urlarg,musicarg)
            return

        #第一次访问页码
        max_cursor = self.max_cursor

        #构造第一次访问链接
        api_post_url = 'https://www.iesdouyin.com/web/api/v2/aweme/%s/?sec_uid=%s&count=%s&max_cursor=%s&max_cursor=0&aid=1128&_signature=PDHVOQAAXMfFyj02QEpGaDwx1S&dytk=' % (self.mode,key,str(self.count),max_cursor)
        self.get_data(api_post_url,max_cursor)
        return api_post_url,max_cursor,key

    #获取第一次api数据
    def get_data(self,api_post_url,max_cursor):
        #尝试次数
        index = 0

        #存储api数据
        result = []
        while result == []:
            index += 1
            print('----正在进行第 %d 次尝试----\r' % index)
            time.sleep(0.3)
            response = requests.get(url = api_post_url,headers=self.headers)
            print(api_post_url)
            html = json.loads(response.content.decode())
            #print(html)

            # with open(self.save + "aa.txt", 'a+') as f:
            #     f.write(response.content.decode())

            # return

            if html['aweme_list'] != []:
                #下一页值
                self.nickname = html['aweme_list'][0]['author']['nickname']
                print('[  用户  ]:'+str(self.nickname)+'\r')
                max_cursor = html['max_cursor']
                result = html['aweme_list']
                print('----抓获数据成功----\r')

                #处理第一页视频信息
                self.video_info(result,max_cursor)
            else:
                print('----抓获数据失败----\r')

        return result,max_cursor

    #下一页
    def next_data(self,max_cursor):

        #获取解码后原地址
        r = requests.get(url = self.Find(self.uid)[0])

        #获取用户sec_uid
        # key = re.findall('/user/(.*?)?',str(r.url))[0]
        key = re.findall('/user/(.*)\?',str(r.url))[0]
        if not key:
            key  = r.url[28:83]

        #构造下一次访问链接
        api_naxt_post_url = 'https://www.iesdouyin.com/web/api/v2/aweme/%s/?sec_uid=%s&count=%s&max_cursor=%s&aid=1128&_signature=RuMN1wAAJu7w0.6HdIeO2EbjDc&dytk=' % (self.mode,key,str(self.count),max_cursor)
        
        # print("下一次的url:"+api_naxt_post_url)

        index = 0
        result = []
        while result == []:
            index += 1
            print('----正在对',max_cursor,'页进行第 %d 次尝试----\r' % index)
            time.sleep(0.3)
            response = requests.get(url = api_naxt_post_url,headers=self.headers)
            html = json.loads(response.content.decode())

            # if html['aweme_list'] != []:
            if html['has_more'] == True:
                #下一页值
                max_cursor = html['max_cursor']
                result = html['aweme_list']
                print('----',max_cursor,'页抓获数据成功----\r')

                #处理下一页视频信息
                if html['aweme_list'] != []:
                    self.video_info(result,max_cursor)
                else:
                    self.next_data(max_cursor)
            else:
                print('----',max_cursor,'页抓获数据失败----\r')
                sys.exit()

    #处理视频信息
    def video_info(self,result,max_cursor):

        #作者信息
        author_list = []

        #无水印视频链接
        video_list = []

        #作品id
        aweme_id = []

        #作者id
        nickname = []

        #封面大图
        dynamic_cover = []
        for i2 in range(self.count):
            try:
                author_list.append(str(result[i2]['desc']))
                video_list.append(str(result[i2]['video']['play_addr']['url_list'][0]))
                aweme_id.append(str(result[i2]['aweme_id']))
                nickname.append(str(result[i2]['author']['nickname']))
                dynamic_cover.append(str(result[i2]['video']['dynamic_cover']['url_list'][0]))
            except Exception as error:
                pass
                #print(error)
                #input('视频信息处理失败...')
                #sys.exit()
        self.videos_download(author_list,video_list,aweme_id,nickname,dynamic_cover,max_cursor)      
        return self,author_list,video_list,aweme_id,nickname,dynamic_cover,max_cursor

    #检测视频是否已经下载过
    def check_info(self,path):
        v_info = os.listdir(path)
        return v_info

    def save_log_text(self,logText,log_file_name):
        with open(log_file_name, 'a+') as f:
            f.write(logText)

    def videos_download(self,author_list,video_list,aweme_id,nickname,dynamic_cover,max_cursor):
        nicknamePath = '/'
        log_file_name = ''
        logText = '\n'
        vid = ''
        hasWriteCursor = False

        for i in range(self.count):
            try:
                #创建并检测下载目录是否存在
                if self.mode == 'post':
                    nicknamePath = '/' + nickname[i] + '/'
                else:
                    nicknamePath = '/' + self.fabu_time(int(time.time()), 1) + '/'

                log_file_name = self.save + self.mode + nicknamePath + self.fabu_time(int(time.time()), 1) + '.txt'

                v_info = []

                if os.path.exists(self.save + self.mode + nicknamePath):
                    v_info = self.check_info(self.save + self.mode + nicknamePath) 
                else:
                    os.makedirs(self.save + self.mode + nicknamePath)

                if hasWriteCursor == False:
                    tmpStr = '\n' + 'max_cursor:' + str(max_cursor)
                    self.save_log_text(tmpStr, log_file_name)
                    hasWriteCursor = True

                    #达到设置的最大数量停止下载
                    if self.max_download != 0 and self.download_num >= self.max_download: #爬取的数量达到了退出
                        print("self.max_download :" + str(self.max_download))
                        print("self.download_num :" + str(self.download_num))
                        return

            except:
                #有目录不再创建
                pass

            #下载音频
            try:
                jx_url  = f'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={aweme_id[i]}'    #官方接口
                js = json.loads(requests.get(url = jx_url,headers=self.headers).text)
                vid = str(js['item_list'][0]['video']['vid'])
                try: 
                    creat_time = self.fabu_time(js['item_list'][0]['create_time'])
                except:
                    creat_time = ''

                music_url = str(js['item_list'][0]['music']['play_url']['url_list'][0])
                music_title = str(js['item_list'][0]['music']['author'])
                if self.musicarg == "yes":
                    #保留音频
                    music=requests.get(music_url)
                    #保存视频
                    start = time.time() #下载开始时间
                    size = 0            #初始化已下载大小
                    chunk_size = 1024   #每次下载的数据大小
                    content_size = int(music.headers['content-length']) # 下载文件总大小
                    try:
                        if music.status_code == 200: #判断是否响应成功
                            logStr = '[  音频  ]'+author_list[i]+'[文件 大小]:{size:.2f} MB'.format(size = content_size / chunk_size /1024)
                            logText = logText + '\n' + logStr
                            print(logStr) #开始下载，显示下载文件大小
                            m_url = self.save + self.mode + nicknamePath + re.sub(r'[\\/:*?"<>|\r\n]+', "_", music_title) + '_' + author_list[i] + creat_time + '.mp3'
                            with open(m_url,'wb') as file: #显示进度条
                                for data in music.iter_content(chunk_size = chunk_size):
                                    file.write(data)
                                    size +=len(data)
                                    print('\r'+'[下载进度]:%s%.2f%%' % ('>'*int(size*50/ content_size), float(size / content_size * 100)) ,end=' ')
                                end = time.time() #下载结束时间
                                print('\n' + '[下载完成]:耗时: %.2f秒\n' % (end - start)) #输出下载用时时间
                    except:
                        input('下载音频出错!')
                    #print('音频 ',music_title,'-',author_list[i],'    下载中\r')
                    #m_url = self.save + self.mode + nicknamePath + re.sub(r'[\\/:*?"<>|\r\n]+', "_", music_title) + '_' + author_list[i] + '.mp3'
                    #print(m_url)
                    #with open(m_url,'wb') as f:
                    #    f.write(music.content)
            except Exception as error:
                #print(error)
                #if music_url == '':
                print('该页视频没有'+str(self.count)+'个,已为您跳过')
                continue
                #print('该音频目前不可用\r')
                #else:
                #    pass

            #下载视频
            try:
                video = requests.get(video_list[i])
                #保存视频
                start = time.time() #下载开始时间
                size = 0            #初始化已下载大小
                chunk_size = 1024   #每次下载的数据大小
                content_size = int(video.headers['content-length']) # 下载文件总大小
                try:
                    if video.status_code == 200:        #判断是否响应成功
                        logStr = '[  视频' + str(self.download_num+1) + '  ]'+author_list[i]+'[文件 大小]:{size:.2f} MB'.format(size = content_size / chunk_size /1024)

                        # 匹配成功中断下载
                        if self.stopVid !='' and self.stopVid == vid and (self.mode == 'like'):
                            print('下载完成')
                            self.save_log_text(logText,log_file_name)
                            sys.exit()
                            
                        logText = logText + '\n' + logStr + ' ' + vid
                        print(logStr + ' ' + vid)
                        v_url = self.save + self.mode + nicknamePath + re.sub(r'[\\/:*?"<>|\r\n]+', "_", author_list[i]) + creat_time + '.mp4'

                        #每次判断视频是否已经下载过
                        if self.mode == 'post':
                            try:
                                file_name = re.sub(r'[\\/:*?"<>|\r\n]+', "_", author_list[i]) + creat_time + '.mp4'
                                if file_name in v_info:
                                    print('[  提示  ]:'+author_list[i]+'[文件已存在，为您跳过]',end = "") #开始下载，显示下载文件大小
                                    for i in range(20):
                                        print(">",end = '',flush = True)
                                        time.sleep(0.01)
                                    print('\r')
                                    continue
                            except:
                                #防止下标越界
                                pass

                        with open(v_url,'wb') as file: #显示进度条
                            self.download_num = self.download_num + 1
                            for data in video.iter_content(chunk_size = chunk_size):
                                file.write(data)
                                size +=len(data)
                                print('\r'+'[下载进度]:%s%.2f%%' % ('>'*int(size*50/ content_size), float(size / content_size * 100)) ,end=' ')
                            end = time.time()           #下载结束时间
                            print('\n' + '[下载完成]:耗时: %.2f秒\n' % (end - start)) #输出下载用时时间
                except:
                    input('下载视频出错!')
                    self.save_log_text(logText,log_file_name)
                #print('视频 ',author_list[i],'    下载中\r')
                #v_url = self.save + self.mode + nicknamePath + re.sub(r'[\\/:*?"<>|\r\n]+', "_", author_list[i]) + creat_time + '.mp4'
                #with open(v_url,'wb') as f:
                #    f.write(video.content)

                #保存视频动态封面
                #dynamic = requests.get(dynamic_cover[i])
                #with open(self.save + self.mode + nicknamePath + re.sub(r'[\\/:*?"<>|\r\n]+', "_", author_list[i]) + creat_time + '.webp','wb') as f:
                #    f.write(dynamic.content)
            except Exception as error:
                #pass
                print(error)
                self.save_log_text(logText,log_file_name)
                input('缓存失败，请检查！')
                #sys.exit()
        self.save_log_text(logText,log_file_name)
        self.next_data(max_cursor)

#主模块执行
if __name__ == "__main__":
    RTK = TikTok()
