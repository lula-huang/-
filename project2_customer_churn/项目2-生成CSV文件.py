import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker('zh_CN')
Faker.seed(42)
random.seed(42)

# ========== 1.客户表 ==========
customer_list = []
industry_list = ["制造业", "商贸零售", "建筑工程", "IT互联网", "教育培训"]
scale_list = ["小微企业", "中型企业", "大型企业"]

for cid in range(1, 301):
    customer = {
        "customer_id": cid,
        "company_name": fake.company(),
        "industry": random.choice(industry_list),
        "company_scale": random.choice(scale_list),
        "register_date": fake.date_between(start_date="-2y", end_date="today"),
        "contact_name": fake.name(),
        "phone": fake.phone_number()
    }
    customer_list.append(customer)
df_customer = pd.DataFrame(customer_list)

# ========== 2.报价记录表 ==========
quote_list = []
product_list = ["A产品", "B产品", "C产品", "D产品"]
for qid in range(1, 451):
    cid = random.randint(1, 300)
    quote_date = fake.date_between(start_date="-2y", end_date="today")
    quote = {
        "quote_id": qid,
        "customer_id": cid,
        "quote_date": quote_date,
        "product_name": random.choice(product_list),
        "quote_amount": round(random.uniform(5000, 200000), 2),
        "delivery_days": random.choice([7,15,30,45,60])
    }
    quote_list.append(quote)
df_quote = pd.DataFrame(quote_list)

# ==========3.客户跟进表 ==========
follow_list = []
staff_list = ["销售甲","销售乙","销售丙"]
for fid in range(1, 701):
    cid = random.randint(1,300)
    follow_date = fake.date_between(start_date="-2y", end_date="today")
    follow = {
        "follow_id": fid,
        "customer_id": cid,
        "follow_date": follow_date,
        "sales_staff": random.choice(staff_list),
        "content": random.choice(["电话沟通需求","发送报价单","方案讲解","二次议价","客户回访"])
    }
    follow_list.append(follow)
df_follow = pd.DataFrame(follow_list)

# ==========4.客户状态表（核心：流失/成交+流失原因） ==========
status_list = []
lose_reason = ["报价高于竞品","交付周期无法满足","项目取消","选择其他供应商","预算不足"]
for cid in range(1,301):
    # 70%流失，30%成交
    is_lose = random.choices([1,0], weights=[0.7,0.3])[0]
    if is_lose ==1:
        reason = random.choice(lose_reason)
    else:
        reason = "已成交"
    status = {
        "customer_id": cid,
        "final_status": "流失" if is_lose else "成交",
        "lose_reason": reason
    }
    status_list.append(status)
df_status = pd.DataFrame(status_list)

# 导出csv
df_customer.to_csv("客户表.csv", index=False, encoding="utf-8-sig")
df_quote.to_csv("报价记录表.csv", index=False, encoding="utf-8-sig")
df_follow.to_csv("客户跟进表.csv", index=False, encoding="utf-8-sig")
df_status.to_csv("客户状态表.csv", index=False, encoding="utf-8-sig")

print("✅ 4张CSV文件生成完成！")
print("客户表、报价记录表、客户跟进表、客户状态表")