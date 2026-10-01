import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker('zh_CN')
np.random.seed(42)
random.seed(42)

row_count = 1200
start_date = datetime(2023,1,1)
end_date = datetime(2024,12,31)

# 客户表
customers = []
for i in range(1, 301):
    customers.append({
        "customer_id":i,
        "customer_name":fake.name(),
        "region":random.choice(["华东","华南","华北","西南","西北"]),
        "industry":random.choice(["制造业","商贸零售","服务业","建筑业","互联网"]),
        "register_date":fake.date_between(start_date, end_date)
    })
df_customer = pd.DataFrame(customers)

#产品表
products = []
for i in range(1,61):
    products.append({
        "product_id":i,
        "product_name":f"产品{i}",
        "category":random.choice(["A类主材","B类辅材","C类配件"]),
        "unit_price":round(random.uniform(100,8000),2)
    })
df_product = pd.DataFrame(products)

#订单表
orders = []
for i in range(1, row_count+1):
    cid = random.randint(1,300)
    pid = random.randint(1,60)
    order_date = fake.date_between(start_date, end_date)
    qty = random.randint(1,12)
    orders.append({
        "order_id":i,
        "customer_id":cid,
        "product_id":pid,
        "order_date":order_date,
        "quantity":qty
    })
df_order = pd.DataFrame(orders)

#退货表
return_list = []
return_cnt = int(row_count*0.08)
for i in range(return_cnt):
    oid = random.randint(1,row_count)
    return_list.append({
        "return_id":i+1,
        "order_id":oid,
        "return_reason":random.choice(["质量问题","客户取消","发货错误"])
    })
df_return = pd.DataFrame(return_list)

#保存
df_customer.to_csv("customer.csv",index=False,encoding="utf-8-sig")
df_product.to_csv("product.csv",index=False,encoding="utf-8-sig")
df_order.to_csv("order.csv",index=False,encoding="utf-8-sig")
df_return.to_csv("return.csv",index=False,encoding="utf-8-sig")

print("数据集生成完成！")
