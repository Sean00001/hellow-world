將所有上市公司的數據都下載完畢 


import requests  # 導入requests模組，呼 Http用
import json  # 導入json模組
import pandas as pd  # 引用套件並縮寫為 pd
import csv

# 正式機_帳號設定--------------------------------------------------------------------------------
appid = "20200326174039472"  # 串接帳號
appsecret = "da560b006f4511ea9dc4000c29cc8594"
with open('output.csv', 'a') as csvfile:
  # 建立 CSV 檔寫入器
  writer = csv.writer(csvfile)


# 正式機_取得交易驗證碼網址----------------------------------------------------------------------
token_url = "https://owl.cmoney.com.tw/OwlApi/auth"

# 組連線參數------------------------------------------------------------------------------------
token_params = "appId=" + appid + "&appSecret=" + appsecret
token_headers = {'content-type': "application/x-www-form-urlencoded"}  # POST表單，預設的編碼方式 (enctype)

# 取得token------------------------------------------------------------------------------------
token_res = requests.request("POST", token_url, headers=token_headers, data=token_params)  # 請求回覆的狀態 <Response [200]>
z = 0
if (token_res.status_code == 200):  # 若請求http 200(成功)
    token_data = json.loads(token_res.text)  # 將token_res的內容，用json.loads()解碼成python編碼
    token = token_data.get("token")  # 取token值

    # 呼叫 data API-------------------------------------------------------------------------------
    data_url = "https://owl.cmoney.com.tw/OwlApi/api/v2/json/"
    pid = "FAA-14813a"  # 個股日收盤行情
    for i in range(1101, 9962):
        sid = i  # 輸入股票代號      
 
        num = "500"  # 輸入期數
        data_headers = {'authorization': "Bearer " + token}
        data_res = requests.request("GET", data_url + pid + "/" + str(sid) + "/" + num, headers=data_headers)

        if (data_res.status_code == 200):
            data = json.loads(data_res.text)

            all = pd.DataFrame(data.get("Data"), columns=data.get("Title"))

          
           
            if (all.shape[0] ==0 ):
                continue ;
            else:
             
                print(all)
                with open('output.csv', 'a', newline='') as f:
                    all.to_csv(f, header=True,encoding='utf-8')
                

    else:
        print("取得資料連線錯誤!" + str(data_res.status_code))

else:
    print("取得token連線錯誤!" + str(token_res.status_code))
#
