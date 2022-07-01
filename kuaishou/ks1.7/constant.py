from typing import Dict

from pydantic import BaseModel

from untils import target_your_urls, your_cookies


class Constant(BaseModel):
    headers: dict = {'content-type': 'application/json',
                     'Cookie': your_cookies(),
                     'Host': 'www.kuaishou.com',
                     'Origin': 'https://www.kuaishou.com',
                     'Referer': 'https://www.kuaishou.com/profile/3xv78fxycm35nn4',
                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}

    base_url: str = 'https://www.kuaishou.com/graphql'
    your_urls: str = ''
    pcursor: str = ''

    def __init__(self, **kargs):
        super(Constant, self).__init__(**kargs)
        self.your_urls = target_your_urls()
        self.pcursor = ''


    @property
    def data(self)->Dict:
        # self.pcursor = 'no_more' 没有更多视频了
        data_info: dict={'operationName span>':"visionProfilePhotoList",
        'query': """query visionProfilePhotoList($pcursor: String, $userId: String, $page:
        String, $webPageArea: String) {\n visionProfilePhotoList(pcursor: $pcursor, userId:
        $userId, page: $page, webPageArea: $webPageArea) {\n result\n llsid\n
        webPageArea\n feeds {\n type\n author {\n id\n name\n
        following\n headerUrl\n headerUrls {\n cdn\n url\n
        __typename\n }\n __typename\n }\n tags {\n type\n
        name\n __typename \n }\n photo {\n id\n
        duration\n caption\n likeCount\n realLikeCount\n
        coverUrl\n coverUrls {\n cdn\n url\n __typename\n
        }\n photoUrls {\n cdn\n url\n __typename\n
        }\n photoUrl\n liked\n timestamp\n expTag\n
        animatedCoverUrl\n stereoType\n videoRatio\n
        profileUserTopPhoto\n __typename \n }\n canAddComment\n
        currentPcursor\n llsid\n status\n __typename\n }\n hostName\n
        pcursor\n __typename\n }\n}\n""",
        'variables': {'userId':self.your_urls.split('/')[-1] , 'pcursor': self.pcursor, 'page': "profile"}
        }
        return data_info
