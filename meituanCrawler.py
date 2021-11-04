from collections import namedtuple
import uiautomator2 as u2
import time
import pandas as pd

d = u2.connect()

d.jsonrpc.setConfigurator({"waitForIdleTimeout": 50})

# d.swipe(0.251, 0.763, 0.251, 0.259)
price = ""
normalPrice = ""
monthSales = ""
drugName = ""

info = d(resourceId="com.sankuai.meituan.takeoutnew:id/detail_content_layout")
df = pd.DataFrame(columns=['品名', '月销售', '折扣价', '正价'])


def retriveProductInfo(info, num):
    price = ""
    normalPrice = ""
    monthSales = ""
    drugName = ""
    # print(time.strftime("%H:%M:%S", time.localtime()))
    drugName = info[num].child(
        resourceId="com.sankuai.meituan.takeoutnew:id/txt_stickyfoodList_adapter_food_name").info['text']
    # print(time.strftime("%H:%M:%S", time.localtime()))
    monthSales = info[num].child(
        resourceId='com.sankuai.meituan.takeoutnew:id/tv_stickyfood_sold_count').info['text']
    monthSales = monthSales.lstrip('月售')
    # print(time.strftime("%H:%M:%S", time.localtime()))
    price = info[num].child(
        resourceId='com.sankuai.meituan.takeoutnew:id/txt_stickyfoodList_adapter_food_price_fix').info['text']
    # print(time.strftime("%H:%M:%S", time.localtime()))
    normalPriceInfo = info[num].child(
        resourceId='com.sankuai.meituan.takeoutnew:id/txt_stickyfoodList_adapter_food_original_price_fix')
    # print(time.strftime("%H:%M:%S", time.localtime()))
    if len(normalPriceInfo) > 0:
        normalPrice = normalPriceInfo.info['text']
        normalPrice = normalPrice.lstrip('¥')
    return(drugName, monthSales, normalPrice, price)


info = d(resourceId="com.sankuai.meituan.takeoutnew:id/detail_content_layout")
while True:

    for j in range(2):
        drugName, monthSales, normalPrice, price = retriveProductInfo(info, j)
        if df.shape[0] > 0 and drugName != df.iloc[-1, :]['品名']:
            # infoArray.append({'drugName': drugName, 'monthSales': monthSales,
            #                   'normalPrice': normalPrice, 'price': price})
            df = df.append({'品名': drugName, '月销售': monthSales,
                           '折扣价': normalPrice, '正价': price}, ignore_index=True)
            print(time.strftime("%H:%M:%S", time.localtime()),
                  drugName, price, '采集')

        else:
            df = df.append({'品名': drugName, '月销售': monthSales,
                           '折扣价': normalPrice, '正价': price}, ignore_index=True)
            print(time.strftime("%H:%M:%S", time.localtime()),
                  drugName, price, '采集')

    d.swipe(0.251, 0.763, 0.251, 0.259)
    info = d(resourceId="com.sankuai.meituan.takeoutnew:id/detail_content_layout")
    drugName, monthSales, normalPrice, price = retriveProductInfo(info, 3)
    if drugName == df.iloc[-1, :]['品名']:
        break
df.to_excel("线上价格爬取", index=False)
