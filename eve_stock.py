from urllib import request
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
from tqdm import tqdm
from IPython.display import display
import matplotlib
import matplotlib.pyplot as plt

# stock_URL.csvの読み込み
url_list = pd.read_csv("page_URL.csv", index_col=0)
url_df = pd.DataFrame(url_list)
pages = {}

# ページを選択してそのページ内の企業urlを取得する

for page in tqdm(list(url_df.iloc[:,0]),desc='first'):
    u_page = page.split('=')[1]
    
    # pageを辞書に格納
    pages[u_page] = [page]
    
page_num = input("ページ数を入力:")   
page_s = pages[page_num]


# 入力したページのhtmlを取得
base_page = "".join(page_s)
html = request.urlopen(base_page)
soup = BeautifulSoup(html,"html.parser")
url = []

for t in tqdm(soup.find_all("a"),desc='second'):
    url.append(''.join(list(urljoin(base_page, t.get('href')))))
    
Table = pd.DataFrame(url)
# display(Table)

# 入力したページの企業urlテーブルを取得
Table = Table.iloc[range(8,128),0]

Table.reset_index(inplace=True, drop=True)
Table.to_csv('page_' + page_num + '.csv', header=True)


    
# データの欲しい企業番号を入力
C_num = input("企業番号:")
s_t_url = "https://kabuoji3.com/stock/" + C_num + "/"
print(s_t_url)

# 企業の株価テーブルを取得
stock_table = pd.read_html(s_t_url)
# print(stock_table)

len_t_list = len(stock_table)
# print(len_t_list)

df_sub = pd.DataFrame()
df_Table = pd.DataFrame()

for col in ["日付","始値","高値","安値","終値","出来高","終値調整"]:
    
    for l in range(0, len_t_list):
        
        df = pd.DataFrame(stock_table)
        
        if l == 0:
            df_sub = stock_table[l][col]
        else:
            df_sub = df_sub.append(stock_table[l][col])
            
    df_con = df_sub.reset_index(drop=True)
    
    if col == ["日付"]:
        df_Table = df_con
    else:
        df_Table = pd.concat([df_Table, df_con], axis=1)
        
# display(df_Table)
    
# 取得した株価テーブルを図にプロット
x = df_Table["日付"][-1::-1]
y = df_Table["終値"][-1::-1]
ma75 = pd.DataFrame.rolling(y, window=75, center=True).mean()
ma25 = pd.DataFrame.rolling(y, window=25, center=True).mean()

plt.figure(figsize=(15,5))
plt.plot(x, y, color='b')
plt.plot(x, ma75, color='g', linewidth=1.7, label='ma75')
plt.plot(x, ma25, color='tomato', linewidth=1.7, label='ma25')
ticks = 40
plt.xticks(x[::ticks], rotation=15)
plt.grid()
plt.show()
    