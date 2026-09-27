# 报价业务数据分析项目
> 数据分析作品集项目｜Power BI + SQL + Python

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
