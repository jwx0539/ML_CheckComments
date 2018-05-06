import requests
import config
import os
from bs4 import BeautifulSoup as bs
import pandas as pd

def get_douban():
    cookies = {
        "ll": "\"108288\"",
        "bid": "jYqmrCi5w_I",
        "__utmt": "1",
        "_ga": "GA1.2.377497527.1525484477",
        "_gid": "GA1.2.1419264461.1525484490",
        "ps": "y",
        "ue": "\"44093818@qq.com\"",
        "dbcl2": "\"178218572:cMggnvWoLo0\"",
        "ck": "70lT",
        "_pk_id.100001.8cb4": "6037a47590a7834f.1525484476.1.1525484505.1525484476.",
        "_pk_ses.100001.8cb4": "*",
        "__ads_session": "7hjirGK0Fwl4Ovc8kQA",
        "push_noty_num": "0",
        "push_doumail_num": "0",
        "__utma": "30149280.377497527.1525484477.1525484477.1525484477.1",
        "__utmb": "30149280.3.10.1525484477",
        "__utmc": "30149280",
        "__utmz": "30149280.1525484477.1.1.utmcsr",
        "__utmv": "30149280.17821",
        "__yadk_uid": "AYZ6syCooOFMBnMOLX1E4LE62q6U2rqc"
    }

    headers = {
        "Host": "www.douban.com",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.90 Safari/537.36 2345Explorer/9.2.1.17116",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Referer": "https://accounts.douban.com/login?alias=jwx0539&redir=https%3A%2F%2Fwww.douban.com%2F&source=index_nav&error=1012",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8",
        'Cookie':'ll="108288"; bid=kEKVyH46TUY; ps=y; dbcl2="178218572:cMggnvWoLo0"; push_noty_num=0; push_doumail_num=0; __utma=30149280.949893437.1525404276.1525488294.1525493742.4; __utmz=30149280.1525484192.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.17821; ck=70lT; __ads_session=ZZ9zdwC4FwmJxPM+kQA=; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1525493740%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DwD3M_Nu5wmnAbUQ5DWV9kIQbtF2uQ20hlba9heDBtqllcdEbw1JOmTzaXFJC40we%26wd%3D%26eqid%3Ded937fd300029d56000000025aed0a9a%22%5D; _pk_id.100001.4cf6=4d5d0bf30700ab2c.1525484189.3.1525493765.1525489524.; __yadk_uid=YST6B01fJyrexSy8PMI8T3Sdm8N86srX; __utmc=30149280; __utma=223695111.1750441595.1525484192.1525488294.1525493742.3; __utmc=223695111; __utmz=223695111.1525484192.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _vwo_uuid_v2=D33AFEB3ED91C9762F07D82BFF1781060|97baa224c332286b02d735f101c5e431; ap=1; _pk_ses.100001.4cf6=*; __utmb=30149280.4.10.1525493742; __utmb=223695111.0.10.1525493742; __utmt=1'
    }
    i= 0
    nums = [0]
    while i < 3700:
        i+=20
        nums.append(i)
    print(nums)
    content = []
    rank = []
    for num in nums:
        url = 'https://movie.douban.com/subject/26683723/reviews?start=' + str(num)
        res = requests.get(url=url,headers=headers)
        #print(res.text)
        soup = bs(res.text,'html.parser')
        divs = soup.find_all('div',{'class':'short-content'})
        spans = soup.find_all('div',{'class':'main review-item'})
        #print(divs)
        for div in divs:
            comment = div.text.strip()
            #print(comment)
            content.append(comment)
        for span in spans:
            try:
                score = span.find('header').find_all('span')[0]['title']
                #print(score)
                rank.append(score)
            except:
                mark = '还行'
                rank.append(mark)
    #print(rank)
    #print(content)
    dataframe = pd.DataFrame({'分数':rank,'影评':content})
    dataframe.to_csv(os.path.join(config.output_path,'影评-后来的我们.csv'),encoding="GB18030")




if __name__ == '__main__':
    get_douban()