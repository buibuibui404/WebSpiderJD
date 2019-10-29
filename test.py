import urllib.request
import re
# import string
# from urllib.parse import quote

# url = quote(url, safe = string.printable)
# response = urllib.request.urlopen(url)
# result = response.read().decode('utf-8')
# print(result)

    # f = open("test.txt","w") # create a new file
    # f.write(str(html1, 'utf-8')) # put html to the new file
    # f = open("test.txt", "w")
    # html2 = urllib.request.urlopen(req2).read()
    # f.write(str( html2, 'utf-8' ))

header1 = "User-Agent","Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"

class item:
    def __init__(self, url):
        self.url = url
        self.values = {}

        tpR = urllib.request.Request(url)
        tpR.add_header(header1)
        self.html = urllib.request.urlopen(tpR).reead().decode('GBK')
    def findName(self):


def craw():
    i = 1
    url = "https://search.jd.com/search?keyword=%E4%B8%89%E6%98%9F%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&suggest=1.his.0.0&cid2=653&cid3=655&ev=exbrand_%E4%B8%89%E6%98%9F%EF%BC%88SAMSUNG%EF%BC%89%5E&page={}&s=1&click=0".format(i)
    
    while True:
        req = urllib.request.Request(url)
        req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36")
        html1 = urllib.request.urlopen(req).read().decode('utf-8')

        result1 = re.compile(r'//item.*html').findall(html1)
        result1 = list(set(result1))

        result = []
        for ele in result1:
            try:
                ls = ["https:",ele]
                dict1 = {}
                tempURL = "".join(ls)
                tpR2 = urllib.request.Request(tempURL)
                tpR2.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36")
                html2 = urllib.request.urlopen(tpR2).read().decode('GBK')

                n = re.search(r"商品名称：.*<", html2).group(0)
                n = n[5:-1]

                memo = re.search(r"运行内存：.*<", html2).group(0)
                memo = memo[5:-1]

                battery = re.search(r"电池容量（mAh）：.*<", html2).group(0)
                battery = battery[10:-1]

                color = re.search(r"机身颜色：.*<", html2).group(0)
                color = color[5:-1]

                front = re.search(r"前摄主摄像素：.*<", html2).group(0)
                front = front[7:-1]

                back = re.search(r"后摄主摄像素：.*<", html2).group(0)
                back = back[7:-1]

                dict1["name"] = {n}
                dict1["memo"] = {memo}
                dict1["battery"] = {battery}
                dict1["color"] = {color}
                dict1["front"] = {front}
                dict1["back"] = {back}
                result.append(dict1)
                print(dict1)
            except:
                pass
        i += 2


craw()