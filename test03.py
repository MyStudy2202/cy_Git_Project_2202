import urllib.request

from bs4 import BeautifulSoup
import pymysql.cursors

# 连接数据库
connect = pymysql.Connect(host='localhost',
                          user='root',
                          password='123456',
                          db='spider2202_douban',
                          cursorclass=pymysql.cursors.DictCursor,
                          )

# 创建一个request（等于一个url），request需要放headers


# req = urllib.request.Request("https://movie.douban.com/top250", headers=h)

with connect:
    for page in range(0,250,25):
        h = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        }
        web_url = f"https://movie.douban.com/top250?start={page}&filter="

        req = urllib.request.Request(web_url, headers=h)

        # 参数可以是一个url地址，也可以是一个Request

        r = urllib.request.urlopen(req)
        # print(r.status)
        # print(r.read().decode())
        html = r.read().decode()

        #  使用bs4或者正则表达式进行数据提取
        soup = BeautifulSoup(html, "html.parser")
        items = soup.find_all("div", class_="item")

        infos = soup.find_all("div", class_="info")
        # print(items)


        for info in infos:
            title = info.find('span', class_='title').text
            yanYuan = info.find('span'[1].strip(), class_='').text.strip().split("\n")[0]
            foreign_name = info.find('span', class_='other').text.strip()
            other_info = info.find('p',class_="").text.strip()
            score = info.find('span', class_='rating_num').text
            print(title, end='')
            print(score)
            print(yanYuan)
            for item in items:
                # print(item)
                img = item.find("div", class_="pic").a.img
                # 取出img标签 里面的 alt属性

                url = str(img["src"])

            with connect.cursor() as cursor:
                sql = "INSERT INTO  `movie_info`(`movie_name`,`movie_url`,`foreign_name`,`score`,`actor`,other_info) VALUES (%s, %s, %s, %s,%s,%s)"
                cursor.execute(sql, (title, url, foreign_name, score, yanYuan.strip(),other_info))

        connect.commit()

