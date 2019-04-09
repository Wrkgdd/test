
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def Make_Stock_Table():
    u = pd.read_csv("stock_URL.csv", index_col=0)
    for i in u.iloc[[k for k in range(0,120)],0]:
        print(i)
        url = i
        dfs = pd.read_html(url)

        data = pd.DataFrame()
        data4 = pd.DataFrame()
        for j in ["日付","始値","高値","安値","終値","出来高","終値調整"]:
            df = pd.DataFrame()
            for i in range(0,2):
                k = pd.DataFrame(dfs)
    #             print(k)
                x = 0
                if len(k.index)==1 and i==1:
                    x = 2
                    continue
                    df = df.append(dfs[i][j])  
                else:
                    df = df.append(dfs[i][j])
            df = df.T
    #         print(df)
            data1 = df.iloc[:,[0]]
            if x == 2:
                data1 = data1.dropna()
            else:
                data2 = df.iloc[:,[1]]
                data3 = pd.concat([data1, data2])
                data3 = data3.reset_index(drop=True)
                data1 = data3.dropna()
        #     print(data3.head())
            if j == ["日付"]:
                data4 = data1
            else:
                data4 = pd.concat([data4, data1], axis=1)
        # print(data4)

        data4.to_csv("Stock_Data_" + str(url.split('/')[4]) + ".csv")
        
# TODO: グラフ作成
def Make_Stock_Chart():
    u = pd.read_csv("stock_URL.csv", index_col=0)
    for i in u.iloc[[k for k in range(0,120)],0]:
        x = []
        y = []
        num = i.split('/')[4]

        url_name = pd.read_csv("Stock_Data_" + str(num) + ".csv", index_col=0)
        d = pd.DataFrame(url_name.loc[:,["日付","終値"]])
        x = d["日付"]
        x = list(x[-1::-1])
    #     print(x)
        y = d["終値"]
        y = y[-1::-1]
    #     print(y)
        sma75 = pd.DataFrame.rolling(y, window=75, center=True).mean()
        sma25 = pd.DataFrame.rolling(y, window=20, center=True).mean()

        plt.figure(figsize=(11,7))
        plt.xlabel('Year-Month')
        plt.ylabel('Stock Price')
        plt.title(str(num), fontsize=18)
        plt.plot(x, y, color='blue', linewidth=0.9, linestyle="-", label="Price")
        plt.plot(x, sma75, color='g', linewidth=1, linestyle="-", label="sma75", marker="o")
        plt.plot(x, sma25, color='r', linewidth=1, linestyle="-", label="sma20", marker=".")
        ticks = 40
        plt.xticks(x[::ticks])
        plt.xticks(rotation=15)
        plt.tick_params(labelsize=14)
        plt.legend()
        plt.show()
        plt.savefig(str(num) + '.png') 
    
    
if __name__ == '__main__':
    Make_Stock_Table()
    Make_Stock_Chart()
    
