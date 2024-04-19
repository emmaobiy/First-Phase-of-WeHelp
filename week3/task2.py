
import urllib.request as req
import bs4
import csv

def getData(url):
    request=req.Request(url, headers={
        "cookie":"over18=1",  
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    })

    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")

    root = bs4.BeautifulSoup(data, "html.parser")

    titles = root.find_all("div", class_="title")
    for title in titles:
        if title.a != None:
            # 取得標題
            ArticleTitle = title.a.string
            ArticlLink = "https://www.ptt.cc" + title.a["href"]

            # 取得讚數
            LikeDislike= title.parent.find("div", class_="nrec").string 
            if LikeDislike == None:
                LikeDislike=0
 

            # 進入文章連結頁面
            article_request=req.Request(ArticlLink, headers={
                "cookie": "over18=1",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
            })
            with req.urlopen(article_request) as response:
                article_data = response.read().decode("utf-8")
            article_root = bs4.BeautifulSoup(article_data, "html.parser")


            PublishTime = ""
            # 找main-content
            maincontent = article_root.find("div", id="main-content")
            if maincontent != None:

                # 找所有class為article-metaline的標籤
                metalines = maincontent.find_all("div", class_="article-metaline")

                # 找時間
                for metaline in metalines:
                    if metaline.find("span", class_="article-meta-tag").string == "時間":
                        # 找到對應的值
                        PublishTime = metaline.find("span", class_="article-meta-value").string
                        break

            # print(f"{ArticleTitle},{LikeDislike},{PublishTime}") 

            writer.writerow([ArticleTitle, LikeDislike, PublishTime])

    nextLink = root.find("a", string="‹ 上頁")
    return nextLink["href"]

pageURL = "https://www.ptt.cc/bbs/Lottery/index.html"

count = 0
with open('article.csv', mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)

    while count < 3:
        pageURL = "https://www.ptt.cc/" + getData(pageURL)
        count += 1
