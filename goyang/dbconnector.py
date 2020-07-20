import pymysql
from bs4 import BeautifulSoup
from selenium import webdriver


class Model:
    def __init__(self):
        self._url =''
        self._parser =''

    @property
    def url(self)-> str: return self._url
    @url.setter
    def url(self,url): self._url = url
    @property
    def parser(self)-> str: return self._parser
    @parser.setter
    def parser(self,parser): self._parser = parser


class Service:
    def __init__(self):
        pass
    def getResult(self,payload):
        browser = webdriver.Chrome('./chromedriver')
        browser.get(url=payload.url)
        soup = BeautifulSoup(browser.page_source, payload.parser)
        searchNum=''
        for i in soup.select('div#result-stats'):
                searchNum=i.text


        return  searchNum
    def getData(self):
        conn = pymysql.connect(host='localhost', user='mariadb', password='mariadb',
                               db='mariadb', charset='utf8')
        curs = conn.cursor()
        curs.execute("select * from table_store  where state like '%의정부%' Limit 0,100 ")
        rows = curs.fetchall()
        storeNames = []
        for row in rows:
            storeNames.append(row[2])
        conn.close()
        return storeNames

class Controller:
    def __init__(self):
        self.service = Service()
        self.model = Model()

    def search(self):
        seq=0
        for i in self.service.getData():
            searchWord = '의정부'+'+'+i.replace(" ", "")
            self.model.url = "https://www.google.com/search?q={}&oq={}&aqs=chrome..69i57.4714j0j9&sourceid=chrome&ie=UTF-8".format(searchWord, searchWord)
            self.model.parser = 'html.parser'
            num = self.service.getResult(self.model)
            print("seq:{}, 검색어:{}, 검색갯수:{}".format(seq,searchWord,num))
            seq+=1

def print_menu():
    print('0. Exit\n'
          '1.  크롤\n')
    return input('Menu\n')

app = Controller()

while 1:
    menu = print_menu()
    if menu == '0':
        break
    if menu == '1':
        app.search()
