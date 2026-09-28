import pandas as pd
from faker import Faker
import random
from datetime import date

fake = Faker('zh_CN')
Faker.seed(66)
random.seed(66)

# ====================== 1. 产品表 product ======================
product_list = [
    {"product_id": "P001", "product_name": "A基础款", "material_cost": 1200, "product_category": "标准产品"},
    {"product_id": "P002", "product_name": "B升级款", "material_cost": 2200, "product_category": "标准产品"},
    {"product_id": "P003", "product_name": "C定制款A", "material_cost": 3500, "product_category": "定制产品"},
    {"product_id": "P004", "product_name": "C定制款B", "material_cost": 4200, "product_category": "定制产品"},
    {"product_id": "P005", "product_name": "D简易款", "material_cost": 800, "product_category": "标准产品"},
    {"product_id": "P006", "product_name": "E高端定制", "material_cost": 6000, "product_category": "定制产品"},
]
df_product = pd.DataFrame(product_list)

# ====================== 2. 客户表 customer ======================
cust_data = []
cust_type_list = ["大客户", "中小客户", "零散散户"]
region_list = ["华东", "华北", "华南"]
for i in range(1, 31):
    cust_id = f"C{i:03d}"
    cust_name = fake.company()
    cust_type = random.choices(cust_type_list, weights=[0.2, 0.5, 0.3])[0]
    region = random.choice(region_list)
    cust_data.append({"cust_id": cust_id, "cust_name": cust_name, "cust_type": cust_type, "region": region})
df_customer = pd.DataFrame(cust_data)

# ====================== 3. 报价主表 quote_main ======================
quote_data = []
fail_reason_pool = ["价格过高", "客户取消需求", "竞品抢单", "方案不满足需求", ""]
quoter_list = ["张三", "李四", "王五"]

start_dt = date(2025, 1, 1)
end_dt = date(2025, 12, 31)

for quote_no in range(1, 121):
    quote_id = f"Q2026{quote_no:03d}"
    # 改成传入date对象，不再传字符串，解决解析报错
    quote_date = fake.date_between(start_date=start_dt, end_date=end_dt)

    # 随机选客户、产品
    cust_row = df_customer.sample(1).iloc[0]
    product_row = df_product.sample(1).iloc[0]
    cust_id = cust_row["cust_id"]
    product_id = product_row["product_id"]
    mat_cost = product_row["material_cost"]

    # 报价金额：在物料成本基础上浮
    rate = random.uniform(1.1, 2.2)
    quote_amount = round(mat_cost * rate, 2)
    cost_total = mat_cost

    # 报价周期：定制产品周期更长
    if product_row["product_category"] == "定制产品":
        quote_cycle_day = random.randint(5, 18)
    else:
        quote_cycle_day = random.randint(1, 6)

    # 成交逻辑：定制产品失败率更高；散户更容易因为价格丢单
    if product_row["product_category"] == "定制产品":
        is_success = random.choices([1, 0], weights=[0.35, 0.65])[0]
    else:
        is_success = random.choices([1, 0], weights=[0.45, 0.55])[0]

    if is_success == 1:
        quote_result = "成交"
        fail_reason = ""
    else:
        quote_result = "未成交"
        # 散户更容易因为价格过高失败
        if cust_row["cust_type"] == "零散散户":
            fail_reason = random.choices(fail_reason_pool[:-1], weights=[0.5, 0.2, 0.2, 0.1])[0]
        else:
            fail_reason = random.choice(fail_reason_pool[:-1])

    quoter_name = random.choice(quoter_list)
    quote_data.append({
        "quote_id": quote_id,
        "quote_date": quote_date,
        "cust_id": cust_id,
        "product_id": product_id,
        "quote_amount": quote_amount,
        "cost_total": cost_total,
        "quote_cycle_day": quote_cycle_day,
        "quote_result": quote_result,
        "fail_reason": fail_reason,
        "quoter_name": quoter_name
    })

df_quote = pd.DataFrame(quote_data)

# ====================== 导出CSV文件 ======================
df_quote.to_csv("quote_main.csv", index=False, encoding="utf-8-sig")
df_customer.to_csv("customer.csv", index=False, encoding="utf-8-sig")
df_product.to_csv("product.csv", index=False, encoding="utf-8-sig")

print("✅ 文件生成完成！")
print("已生成3个csv文件：quote_main.csv、customer.csv、product.csv")
print(f"报价主表共 {len(df_quote)} 条记录")

