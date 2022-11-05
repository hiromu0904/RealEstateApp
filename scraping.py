from retry import retry
import requests
from bs4 import BeautifulSoup
import pandas as pd 
import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe

def get_worksheet():
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    credentials = Credentials.from_service_account_file(
        'service_account.json',
        scopes=scopes
    )
    gc = gspread.authorize(credentials)

    SP_SHEET_KEY = '1co7OezxBYraCGdCENmFvH41EG_HvspnUAOOQAGqkcc8'
    sh = gc.open_by_key(SP_SHEET_KEY)


    SP_SHEET = 'DB'
    worksheet = sh.worksheet(SP_SHEET)
    return worksheet
worksheet = get_worksheet()

def main():
    base_url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13112&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&srch_navi=1'

    result = requests.get(base_url)
    c = result.content
    soup = BeautifulSoup(c, "html.parser")
    body = soup.find("body")
    pages = body.find_all("div", {'class':'pagination pagination_set-nav'})
    pages_text = str(pages)
    pages_split = pages_text.split('</a></li>\n</ol>')
    num_pages = int(pages_split[0].split('>')[-1])

    @retry(tries=3, delay=10, backoff=2)
    def get_html(url):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        return soup

    all_data = []
    for page in range(1, 2):
        # url 
        url = base_url.format(page)
        # get html
        soup = get_html(url)
        # extract all items
        items = soup.findAll("div", {"class": "cassetteitem"})
        # process each item
        for item in items:
            base_data = {}
            # 建物の情報を取得    
            base_data["名称"] = item.find("div", {"class": "cassetteitem_content-title"}).getText().strip()
            base_data["カテゴリー"] = item.find("div", {"class": "cassetteitem_content-label"}).getText().strip()
            base_data["アドレス"] = item.find("li", {"class": "cassetteitem_detail-col1"}).getText().strip()
            base_data["最寄り駅"] = item.find("div", {"class": "cassetteitem_detail-text"}).getText().strip().split('歩')[0]
            base_data["徒歩"] = int(item.find("div", {"class": "cassetteitem_detail-text"}).getText().strip().split('歩')[1].split('分')[0])
            if item.find("li", {"class": "cassetteitem_detail-col3"}).findAll("div")[0].getText().strip() == '新築':
                base_data["築年数"] = 0
            else:
                base_data["築年数"] = int(item.find("li", {"class": "cassetteitem_detail-col3"}).findAll("div")[0].getText().strip().split('築')[1].split('年')[0])
            base_data["構造"] = item.find("li", {"class": "cassetteitem_detail-col3"}).findAll("div")[1].getText().strip()

            # 各部屋の情報を取得
            tbodys = item.find("table", {"class": "cassetteitem_other"}).findAll("tbody")

            for tbody in tbodys:
                data = base_data.copy()

                data["階数"] = tbody.findAll("td")[2].getText().strip()

                data["家賃"] = float(tbody.findAll("td")[3].findAll("li")[0].getText().strip().split('万')[0])
                if tbody.findAll("td")[3].findAll("li")[1].getText().strip()== '-':
                    data["管理費"] = 0
                else:
                    data["管理費"] = int(tbody.findAll("td")[3].findAll("li")[1].getText().strip().split('円')[0])
                if tbody.findAll("td")[4].findAll("li")[0].getText().strip()== '-':
                    data["敷金"] = 0
                else:
                    data["敷金"] = float(tbody.findAll("td")[4].findAll("li")[0].getText().strip().split('万')[0])
                if tbody.findAll("td")[4].findAll("li")[1].getText().strip()== '-':
                    data["礼金"] = 0
                else:
                    data["礼金"] = float(tbody.findAll("td")[4].findAll("li")[1].getText().strip().strip().split('万')[0])

                data["間取り"] = tbody.findAll("td")[5].findAll("li")[0].getText().strip()
                data["面積"] = float(tbody.findAll("td")[5].findAll("li")[1].getText().strip().split('m')[0])

                data["URL"] = "https://suumo.jp" + tbody.findAll("td")[8].find("a").get("href")

                all_data.append(data)    
 
    # データフレーム化
    df = pd.DataFrame(all_data)
    
    set_with_dataframe(worksheet, df, row=1, col=1)

if __name__ == '__main__':
    main()