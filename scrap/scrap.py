from requests import Session
import configparser
from bs4 import BeautifulSoup
import os


def scraping():
    # --------database or ini------------------------
    path = os.path.dirname(os.path.abspath(__file__))
    conf = configparser.ConfigParser()
    conf.read(path + r"/config/config.ini")
    # conf.read(path+"\\config\\config.ini")
    url1 = conf.get('DB', 'URL1')
    url2 = conf.get('DB', 'URL2')
    url3 = conf.get('DB', 'URL3')
    url4 = conf.get('DB', 'URL4')
    url5 = conf.get('DB', 'URL5')
    url6 = conf.get('DB', 'URL6')
    url7 = conf.get('DB', 'URL7')
    url8 = conf.get('DB', 'URL8')
    url9 = conf.get('DB', 'URL9')
    url10 = conf.get('DB', 'URL10')
    url11 = conf.get('DB', 'URL11')

    valute = {}
    news = {}
    sport = {}
    weather = {}

    # фейковый заголовок, чтобы не раскрываться что мы - бот
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    # используем сессию, чтобы автоматически работать с куками
    work = Session()

    def get_data_web1(url):
        pass
        response = work.get(url, headers=headers)
        # print("Status: Privatbank", response.status_code)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            data = soup.find_all('div', class_="currency-pairs")
            name = data[0].find('div', class_="names").text.strip()[:3]
            sold = data[0].find('div', class_="purchase").text.replace('\n', '')
            sale = data[0].find('div', class_="sale").text.replace('\n', '')
            valute['bank1_eur'] = 'Privatbank ' + name + ' ' + sold + ' ' + sale
            name = data[1].find('div', class_="names").text.strip()[:3]
            sold = data[1].find('div', class_="purchase").text.replace('\n', '')
            sale = data[1].find('div', class_="sale").text.replace('\n', '')
            valute['bank1_usd'] = 'Privatbank ' + name + ' ' + sold + ' ' + sale

    def get_data_web2(url):
        pass
        response = work.get(url, headers=headers)
        # print("Status: GovermentBank", response.status_code)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            datas = soup.find('tbody')
            datam = datas.find_all('tr')
            data = datam[7].text.replace('\n', '')
            name = data[27:37]
            sold = data[55:63]
            valute['bank2_usd'] = 'NBU ' + name + ' ' + sold
            data = datam[8].text.replace('\n', '')
            name = data[27:37]
            sold = data[51:59]
            valute['bank2_eur'] = 'NBU ' + name + '  ' + sold

    def get_data_web3(url):
        pass
        response = work.get(url, headers=headers)
        # print("Status: UKRSibbank", response.status_code)
        if response.status_code == 200:
            try:
                html = response.text
                soup = BeautifulSoup(html, 'lxml')
                datas = soup.find('tbody')
                data = datas.find_all('td')
                name = data[0].text.replace('\n', '')[:3]
                sold = data[1].text.replace('\n', '')[7:12]
                sale = data[2].text.replace('\n', '')[7:12]
                valute['bank3_usd'] = 'UKRSibbank ' + name + ' ' + sold + ' ' + sale
                name = data[4].text.replace('\n', '')[:3]
                sold = data[5].text.replace('\n', '')[7:12]
                sale = data[6].text.replace('\n', '')[7:12]
                valute['bank3_eur'] = 'UKRSibbank ' + name + ' ' + sold + ' ' + sale
            except:
                pass

    def get_data_web4(url):
        pass
        response = work.get(url, headers=headers)
        # print("Status: Obozrevatel", response.status_code)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            datas = soup.find('aside', class_="page_rightCol")
            data = datas.find_all('article', class_="newsImgRowTime")
            news['oboz1'] = data[0].text
            news['oboz1_href'] = data[0].find('a').get("href")
            news['oboz2'] = data[1].text
            news['oboz2_href'] = data[1].find('a').get("href")

    def get_data_web5(url):
        pass
        response = work.get(url, headers=headers)
        # print("Status: Korrespondent", response.status_code)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            datas = soup.find('div', class_="col__sidebar")
            datam = datas.find('div', class_="unit-rubric")
            data = datam.find_all('div', class_="article article_expert")
            news['korr1'] = data[0].text.strip()
            news['korr1_href'] = data[0].find('a').get("href")
            news['korr2'] = data[1].text.strip()
            news['korr2_href'] = data[1].find('a').get("href")

    def get_data_web6(url):
        pass
        response = work.get(url, headers=headers)
        # print("Status: BBC Ukraine", response.status_code)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            datas = soup.find('div', class_="bbc-1dblbh1 efnv93c1")
            datam = datas.find('p', class_="bbc-dvyt8e ea6by781")
            news['bbc1'] = datam.text
            datam = datas.find('h3', class_="bbc-dvfk01 ea6by782")
            item_s = 'https://www.bbc.com/' + datam.find('a').get("href")
            news['bbc1_href'] = item_s
            datam = datas.find('p', class_="bbc-1messjj ea6by781")
            news['bbc2'] = datam.text
            datam = datas.find('h3', class_="bbc-z3myq8 ea6by782")
            item_s = 'https://www.bbc.com/' + datam.find('a').get("href")
            news['bbc2_href'] = item_s

    def get_data_web7(url):
        pass
        response = work.get(url, headers=headers)
        # print("Status: Sport Football", response.status_code)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            datas = soup.find('div', class_="news-items")
            data = datas.find_all('div', class_="item")
            sport['foot1'] = data[0].find('div', class_="item-title").text.strip()
            sport['foot1_href'] = data[0].find('a').get("href")
            sport['foot2'] = data[1].find('div', class_="item-title").text.strip()
            sport['foot2_href'] = data[1].find('a').get("href")
            sport['foot3'] = data[2].find('div', class_="item-title").text.strip()
            sport['foot3_href'] = data[2].find('a').get("href")

    def get_data_web8(url):
        pass
        response = work.get(url, headers=headers)
        # print("Status: Sport Box", response.status_code)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            datas = soup.find('div', class_="news-items")
            data = datas.find_all('div', class_="item")
            sport['box1'] = data[0].find('div', class_="item-title").text.strip()
            sport['box1_href'] = data[0].find('a').get("href")
            sport['box2'] = data[1].find('div', class_="item-title").text.strip()
            sport['box2_href'] = data[1].find('a').get("href")
            sport['box3'] = data[2].find('div', class_="item-title").text.strip()
            sport['box3_href'] = data[2].find('a').get("href")

    def get_data_web9(url):
        pass
        response = work.get(url, headers=headers)
        # print("Status: Gismeteo Kyiv", response.status_code)
        if response.status_code == 200:
            response.encoding = 'utf8'
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            datas = soup.find('div', class_="weathertabs day-0")
            status = datas.find('a', class_="weathertab weathertab-block tooltip").get("data-text")
            temp = datas.find('span', class_="unit unit_temperature_c").text
            weather['gis1'] = 'Погода у Києві сьогодні - ' + status + ' ' + temp
        else:
            weather['gis1'] = 'Погода у Києві сьогодні - сервер временно не отвечает'

    def get_data_web10(url):
        pass
        response = work.get(url, headers=headers)
        # print("Status: Gismeteo Washington", response.status_code)
        if response.status_code == 200:
            response.encoding = 'utf8'
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            datas = soup.find('div', class_="weathertabs day-0")
            status = datas.find('a', class_="weathertab weathertab-block tooltip").get("data-text")
            temp = datas.find('span', class_="unit unit_temperature_c").text
            weather['gis2'] = 'Погода у Вашингтоні сьогодні - ' + status + ' ' + temp
        else:
            weather['gis2'] = 'Погода у Вашингтоні сьогодні - сервер временно не отвечает'

    def get_data_web11(url):
        pass
        response = work.get(url, headers=headers)
        # print("Status: Gismeteo London", response.status_code)
        if response.status_code == 200:
            response.encoding = 'utf8'
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            datas = soup.find('div', class_="weathertabs day-0")
            status = datas.find('a', class_="weathertab weathertab-block tooltip").get("data-text")
            temp = datas.find('span', class_="unit unit_temperature_c").text
            weather['gis3'] = 'Погода у Лондоні сьогодні - ' + status + ' ' + temp
        else:
            weather['gis3'] = 'Погода у Лондоні сьогодні - сервер временно не отвечает'

    get_data_web1(url1)
    get_data_web2(url2)
    get_data_web3(url3)
    get_data_web4(url4)
    get_data_web5(url5)
    get_data_web6(url6)
    get_data_web7(url7)
    get_data_web8(url8)
    get_data_web9(url9)
    get_data_web10(url10)
    get_data_web11(url11)
    # print(valute['bank1_usd'])
    # print(valute['bank1_eur'])
    # print(valute['bank2_usd'])
    # print(valute['bank2_eur'])
    # print(valute['bank3_usd'])
    # print(valute['bank3_eur'])
    # print(news['oboz1'])
    # print(news['oboz2'])
    # print(news['korr1'])
    # print(news['korr2'])
    # print(news['bbc1'])
    # print(news['bbc2'])
    # print(sport['foot1'])
    # print(sport['foot2'])
    # print(sport['foot3'])
    # print(sport['box1'])
    # print(sport['box2'])
    # print(sport['box3'])
    # print(weather['gis1'])
    # print(weather['gis2'])
    # print(weather['gis3'])
    return valute, news, sport, weather


if __name__ == "__main__":
    v, n, s, w = scraping()
    print(v)
    print(n)
    print(s)
    print(w)
