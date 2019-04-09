import pprint
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from IPython.display import display

    
url = pd.read_csv("stock_URL.csv", index_col=0)
dict = {}

# URLの読み込み
for i in url.iloc[[k for k in range(0,3)], 0]: # TODO:rangeの第2引数にはlen(url)を格納
    dfs = pd.read_html(i)
    num = i.split('/')[4]
    len_1 = len(dfs)
    
    df_sub = pd.DataFrame()
    df_Table = pd.DataFrame()
    
    for col in ["日付","始値","高値","安値","終値","出来高","終値調整"]:
        
        for l in range(0, len_1):
            df = pd.DataFrame(dfs)
            
            if l == 0:
                df_sub = dfs[l][col]
            else:
                df_sub = df_sub.append(dfs[l][col])
        df_con = df_sub.reset_index(drop=True)
        
        if col == ["日付"]:
            df_Table = df_con
        else:
            df_Table = pd.concat([df_Table, df_con], axis=1)
            
    # df_Tableを辞書に格納
    p = i.split('/')[3:5]
    a = "".join(p)
    print(a)
    dict[a] = df_Table.values.tolist()
    
    
# stock1301のように欲しい株価のキーを入力する
single_table = pd.DataFrame(dict[input("stock+num:")])
single_table.columns = ["日付","始値","高値","安値","終値","出来高","終値調整"]
display(single_table)
    
    
x = single_table["日付"][-1::-1]
l = single_table["始値"][-1::-1]
z = single_table["高値"][-1::-1]
k = single_table["安値"][-1::-1]
y = single_table["終値"][-1::-1]
d = single_table["出来高"][-1::-1]
s = single_table["終値調整"][-1::-1]
mean75 = pd.DataFrame.rolling(y, window=75, center=True).mean()

plt.figure(figsize=(11,7))
plt.plot(x, y, color='b')
plt.plot(x, z, color='r')
plt.plot(x, l, color='c')
# plt.plot(x, d, color='g')
plt.plot(x, s, color='w')
plt.plot(x, k, color='y')
# plt.plot(x, mean75, color='g', linewidth=1.1, label='std75', marker='o')
ticks = 40
plt.xticks(x[::ticks], rotation=15)
plt.style.use('dark_background')
# plt.legend()
plt.show()
        