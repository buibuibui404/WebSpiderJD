import urllib.request
import string
from urllib.parse import quote

# url = quote(url, safe = string.printable)
# response = urllib.request.urlopen(url)
# result = response.read().decode('utf-8')
# print(result)


def craw(url):
    req = urllib.request.Request(url)
    req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36")
    html1 = urllib.request.urlopen(req).read()
    f = open("test.txt","w") # create a new file
    f.write(str(html1, 'utf-8')) # put html to the new file

url = r'https://search.jd.com/search?keyword=%E4%B8%89%E6%98%9F%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&wq=%E4%B8%89%E6%98%9F%E6%89%8B%E6%9C%BA&ev=exbrand_%E4%B8%89%E6%98%9F%EF%BC%88SAMSUNG%EF%BC%89%5E&cid3=655#J_searchWrap'
craw(url)