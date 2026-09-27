# 报价业务数据分析项目
> 报价数据分析项目｜Power BI + SQL + Python

## 📌 项目背景
模拟企业报价业务场景，对报价转化、订单流失、客户与产品表现进行数据分析，搭建交互式可视化看板，定位业务痛点，输出可落地的业务优化建议。
**技术栈：Python(Pandas、Faker)、MySQL、Power BI Desktop、DAX**

## 📊 数据源说明
使用Python生成模拟业务数据，共3张业务表 + PowerBI内创建日期维度表
1. **quote_main 报价主表**
报价编号、报价日期、客户编号、产品编号、报价金额、成本、报价周期、报价结果、未成交原因、报价员
2. **customer 客户维度表**
客户编号、客户名称、客户类型（大客户/中小客户/零散散户）、所属地区
3. **product 产品维度表**
产品编号、产品名称、物料成本、产品分类（标准产品/定制产品）
4. **DateTable 日期维度表（DAX生成）**
用于时间智能计算：本年累计、同期对比等

## ⚙️ 数据建模与处理
1. Python生成模拟数据，导出CSV文件；
2. CSV导入Power BI，构建**星型模型**：
    - customer表 一对多 → quote_main
    - product表 一对多 → quote_main
    - DateTable日期表 一对多 → quote_main
3. 编写DAX度量值，计算核心业务指标。

### DAX核心度量值
```dax
-- 报价总金额
报价总金额 = SUM(quote_main[quote_amount])

-- 总成本
总成本 = SUM(quote_main[cost_total])

-- 毛利
毛利 = [报价总金额] - [总成本]

-- 毛利率
毛利率 = DIVIDE([毛利],[报价总金额],0)

-- 报价单总数
报价单数量 = COUNTROWS(quote_main)

-- 成交报价单数
成交报价单数 = CALCULATE([报价单数量], quote_main[quote_result] = "成交")

-- 报价成功率
报价成功率 = DIVIDE([成交报价单数], [报价单数量],0)

-- 平均报价周期(天)
平均报价周期 = AVERAGE(quote_main[quote_cycle_day])

-- 未成交单数
未成交单数 = CALCULATE(COUNTROWS(quote_main), quote_main[quote_result]="未成交")

-- YTD本年累计报价金额
YTD报价金额 = TOTALYTD([报价总金额],DateTable[Date])

-- 去年同期报价金额
去年同期报价金额 = CALCULATE([报价总金额], DATEADD(DateTable[Date],-1,YEAR))

-- 报价金额同比
报价金额同比 = DIVIDE([报价总金额] - [去年同期报价金额], [去年同期报价金额], BLANK())
```

## 📈 PowerBI 看板设计

> 
> 一共 3 个页面，支持切片器交互式筛选

1. **报价总览页（首页）**
卡片图：报价总金额、毛利、报价成功率、平均报价周期
折线图：按月报价金额趋势
环形图：成交 / 未成交订单数量分布
饼图：各产品分类报价单数量
2. **流失原因分析页**
横向条形图：未成交原因统计
切片器：客户类型、产品分类、地区，动态筛选查看流失情况
3. **客户分析页**
表格：客户名称、报价次数、成交次数、报价成功率
柱状图：不同客户类型报价成功率对比

## 🗄️ SQL 分析代码（MySQL）

```
-- 1. 按产品统计报价次数、成交单数、平均毛利率
SELECT 
product.product_name,
COUNT(quote_main.quote_id) AS `报价总次数`,
SUM(
    CASE
        WHEN quote_main.quote_result='成交' THEN 1
        ELSE 0
    END
) AS `成交单数`,
ROUND(AVG((quote_main.quote_amount - quote_main.cost_total)/quote_main.quote_amount),3) AS `平均毛利率`
FROM quote_main
LEFT JOIN product ON product.product_id=quote_main.product_id
GROUP BY product.product_name
ORDER BY `报价总次数` DESC;
```

```
-- 2. 统计未成交原因分布
SELECT
    fail_reason,
    COUNT(quote_id) AS 数量
FROM quote_main
WHERE quote_result = '未成交'
GROUP BY fail_reason;
```

```
--3. 按客户类型统计报价数量、成交情况与成功率
SELECT
    c.cust_type,
    COUNT(q.quote_id) AS `报价总数`,
    SUM(CASE WHEN q.quote_result='成交' THEN 1 ELSE 0 END) AS `成交单数`,
    ROUND(AVG(CASE WHEN q.quote_result='成交' THEN 1 ELSE 0 END),3) AS `报价成功率`
FROM quote_main q
LEFT JOIN customer c ON q.cust_id = c.cust_id
GROUP BY c.cust_type;
```

## 🔍 业务洞察

1. 整体报价转化率约 45%，超五成报价单最终流失。
2. 产品差异：定制产品报价周期更长，成交率低于标准产品；标准产品转化更好。
3. 流失首要因素：**价格过高**，零散散户对价格敏感度最高。
4. 客户分层：大客户、中小客户报价成功率更高；散户报价量大，但流失严重。
5. 时间趋势：下半年报价单量上涨，但报价成功率下滑，业务增长伴随转化下降。
6. 风险点：存在部分低毛利报价单，存在亏本接单风险。

## 💡 业务优化建议

1. **散户客户**：制作标准化阶梯报价模板，缩短报价耗时，设置价格红线，减少无效报价。
2. **定制产品**：提前向客户同步交付周期；长周期、低毛利定制订单增加审批流程。
3. **流失复盘**：定期复盘因价格流失订单，收集竞品价格，优化内部报价基准。
4. **风控预警**：报表增加毛利率预警，毛利率低于 5% 需要主管审批。
5. **人力分配**：报价人力向高转化的标准产品、大客户倾斜，减少低效散户报价工作。

## ⚠️ 项目局限

1. 数据为 Python 生成的模拟数据，非企业真实业务数据。
2. 缺少客户复购、竞品报价等维度，无法做更深层次归因。
