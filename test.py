import urllib.request
import re
import json
import csv
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


class JDitem:
    def __init__(self, url):
        self.url = url
        self.values = {}

        tpR = urllib.request.Request(url)
        tpR.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36")
        self.html = urllib.request.urlopen(tpR).read().decode('GBK')

    def findName(self):
        n = re.search(r"商品名称：.*<", self.html).group(0)
        n = n[5:-1]
        self.values["name"] = {n}

    def findMemo(self):
        memo = re.search(r"运行内存：.*<", self.html).group(0)
        memo = memo[5:-1]
        self.values["memo"] = {memo}

    def findBattery(self):
        battery = re.search(r"电池容量（mAh）：.*<", self.html).group(0)
        battery = battery[10:-1]
        self.values["battery"] = battery
    
    def findColor(self):
        color = re.search(r"机身颜色：.*<", self.html).group(0)
        color = color[5:-1]
        self.values["color"] = color

    def findFront(self):
        front = re.search(r"前摄主摄像素：.*<", self.html).group(0)
        front = front[7:-1]
        self.values["front"] = front

    def findBack(self):
        back = re.search(r"后摄主摄像素：.*<", self.html).group(0)
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
        
# def firstHtml():


# def lastHtml():
#     a = time.time()
#     b = '%.5f'%a
#     url = 'https://search.jd.com/s_new.php?keyword=%E4%B8%89%E6%98%9F%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&suggest=1.his.0.0&cid2=653&cid3=655&ev=exbrand_%E4%B8%89%E6%98%9F%EF%BC%88SAMSUNG%EF%BC%89%5E&page={}&s={}&scrolling=y&log_id='+b



def craw():
    i = 1

    a = time.time()
    b = '%.5f'%a
    url1 = "https://search.jd.com/search?keyword=%E4%B8%89%E6%98%9F%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&suggest=1.his.0.0&cid2=653&cid3=655&ev=exbrand_%E4%B8%89%E6%98%9F%EF%BC%88SAMSUNG%EF%BC%89%5E&page={}&s=1&click=0".format(i)
    url2 = 'https://search.jd.com/s_new.php?keyword=%E4%B8%89%E6%98%9F%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&suggest=1.his.0.0&cid2=653&cid3=655&ev=exbrand_%E4%B8%89%E6%98%9F%EF%BC%88SAMSUNG%EF%BC%89%5E&page={}&s={}&scrolling=y&log_id='+b
    result = []

    try:
        while i == 1:
            req = urllib.request.Request(url1)
            req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36")
            html1 = urllib.request.urlopen(req).read().decode('utf-8')

            result1 = re.compile(r'//item.*html').findall(html1)
            result1 = list(set(result1))

            print(result1)
            for ele in result1:
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
    print("!!")
    return result

def creatCSV(ls):
    fileHeader = ["name", "price", "memo", "battery", "color", "back", "front"]
    f = open("test.csv", "w", encoding='utf-8-sig')
    writer = csv.DictWriter(f, fileHeader)
    writer.writeheader()
    for ele in ls:
        print(ele)
        writer.writerow(ele)

if __name__ == "__main__":
    creatCSV(craw())

