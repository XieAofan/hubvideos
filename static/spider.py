# 这是一个示例 Python 脚本。
import requests
import parsel
import json
# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。


def main(h):
    url = "https://www.jdlingyu.com/tag/jk%e5%88%b6%e6%9c%8d"+str(h)
    header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/92.0.4515.107 Safari/537.36"}
    response = requests.get(url=url, headers=header)
    print(response)
    html_data = response.text
    selects = parsel.Selector(html_data)
    print(selects)
    lists = selects.xpath('//div[@id="post-list"]/ul/li')
    pic_lists = []
    for li in lists:
        pic_title = li.xpath('.//h2/a/text()').get()
        pic_url = li.xpath('.//h2/a/@href').get()
        response_pic = requests.get(url=pic_url, headers=header)
        pic_data = response_pic.text
        pic_selects = parsel.Selector(pic_data)
        pic_list = pic_selects.xpath('//div[@class="entry-content"]/img/@src').getall()
        pic_dic = {'title': pic_title, 'url': pic_list}
        pic_lists.append(pic_dic)
    return pic_lists

def spider():
    lists = []
    for i in range(16):
        i=i+1
        h="/page/"+str(i)
        lis=main(h)
        print(h)
        for li in lis:
            lists.append(li)
    nr=json.dumps(lists)
    f=open("lists.txt","w")
    f.write(nr)
    f.close()

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    spider()