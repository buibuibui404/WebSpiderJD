import urllib.request
import re
import json
import csv
import time

class JDitem:
    def __init__(self, url):
        self.url = url
        self.values = {}

        tpR = urllib.request.Request(url)
        tpR.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36")
        self.html = urllib.request.urlopen(tpR).read().decode('GBK')

    def findName(self):
        n = re.search(r"商品名称：.*<", self.html).group(0) # get the product name
        n = n[5:-1]
        self.values["name"] = {n}

    def findMemo(self):
        memo = re.search(r"运行内存：.*<", self.html).group(0) # get the phone memory information
        memo = memo[5:-1]
        self.values["memo"] = {memo}

    def findBattery(self):
        battery = re.search(r"电池容量（mAh）：.*<", self.html).group(0) # get the phone battery information
        battery = battery[10:-1]
        self.values["battery"] = battery
    
    def findColor(self):
        color = re.search(r"机身颜色：.*<", self.html).group(0) # get the phone colour information
        color = color[5:-1]
        self.values["color"] = color

    def findFront(self):
        front = re.search(r"前摄主摄像素：.*<", self.html).group(0) # get the front camera information
        front = front[7:-1]
        self.values["front"] = front

    def findBack(self):
        back = re.search(r"后摄主摄像素：.*<", self.html).group(0) # get the back camera information
        back = back[7:-1]
        self.values["back"] = back

    def getValue(self):
        return self.values
    
    def findPrice(self):
        price = None
        id = self.findID()
        url = 'http://p.3.cn/prices/mgets?skuIds=J_' + id + '&type=1'
        price_json = json.load(urllib.request.urlopen(url))[0]
        if price_json['p']:
            price = price_json['p']
        self.values["price"] = price

    def findID(self):
        id = re.search(r"商品编号：.*<", self.html).group(0)
        id = id[5:-1]
        return id
        
def craw():
    i = 1

    a = time.time()
    b = '%.5f'%a
    result = []

    try:
        while True:
            url1 = "https://search.jd.com/search?keyword=%E4%B8%89%E6%98%9F%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&suggest=1.his.0.0&cid2=653&cid3=655&ev=exbrand_%E4%B8%89%E6%98%9F%EF%BC%88SAMSUNG%EF%BC%89%5E&page={}&s=1&click=0".format(i)
            url2 = 'https://search.jd.com/s_new.php?keyword=%E4%B8%89%E6%98%9F%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&suggest=1.his.0.0&cid2=653&cid3=655&ev=exbrand_%E4%B8%89%E6%98%9F%EF%BC%88SAMSUNG%EF%BC%89%5E&page={}&s={}&scrolling=y&log_id='.format(i+1,48*i - 20)+b

            #Get the first 30 items
            req1 = urllib.request.Request(url1) 
            req1.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36")
            html1 = urllib.request.urlopen(req1).read().decode('utf-8')
            result1 = re.compile(r'//item.*html').findall(html1)
            
            #Get the next 30 items
            req = urllib.request.Request(url2, headers= {
    'method': 'GET',
    'path': '/s_new.php?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA',
    'scheme':'https',
    'referer': 'https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&page=3&s=58&click=0',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'}
            )
            html2 = urllib.request.urlopen(req).read().decode('utf-8')
            result2 = re.compile(r'//item.*html').findall(html2)

            result3 = list(set(result1 + result2))
            print(result3)

            if len(result3) == 0:
                break

            for ele in result3:
                try:
                    ls = ["https:",ele]
                    dict1 = {}
                    tempURL = "".join(ls)

                    item = JDitem(tempURL)
                    item.findBack()
                    item.findBattery()
                    item.findColor()
                    item.findFront()
                    item.findMemo()
                    item.findName()
                    item.findPrice()
                    result.append(item.getValue())
                    print(item.getValue())
                except:
                    pass
            i += 2
    except:
        pass
    return result

def creatCSV(ls):
    fileHeader = ["name", "price", "memo", "battery", "color", "back", "front"]
    f = open("test.csv", "w", encoding='utf-8-sig')
    writer = csv.DictWriter(f, fileHeader)
    writer.writeheader()
    print("Start writing")
    for ele in ls:
        writer.writerow(ele)
    print("finish writing")

if __name__ == "__main__":
    creatCSV(craw())

