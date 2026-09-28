# 项目2：客户流失分析
## 项目简介
背景：模拟企业询价报价业务场景，客户提交报价单之后存在大量客户流失。结合之前的业务经验，通过数据分析定位客户流失根源，找到高风险客户群体，给销售、报价岗位提供可落地的优化策略，提升客户成交转化率。
技术栈：Python（生成模拟数据集）、MySQL（SQL探索性数据分析）、Power BI（数据建模、DAX度量值开发、交互式可视化看板）

## 数据字典
共4张数据表：
1. 客户表：客户ID、企业名称、所属行业、企业规模、注册时间、联系人
2. 报价记录表：报价单号、客户ID、报价日期、产品名称、报价金额、交付周期
3. 客户跟进表：跟进编号、客户ID、跟进日期、销售负责人、沟通内容
4. 客户状态表：客户ID、最终状态（成交/流失）、流失原因

## 数据建模
在Power BI中建立模型关系，使用customer_id作为关联键：
- 客户表（一） ↔ 报价记录表（多）
- 客户表（一） ↔ 客户跟进表（多）
- 客户表（一） ↔ 客户状态表（多）

## SQL探索分析
```sql
-- 1. 整体流失统计
SELECT `客户状态表`.final_status, COUNT(DISTINCT `客户状态表`.customer_id) AS `客户数量`
FROM `客户状态表`
GROUP BY `客户状态表`.final_status;

-- 2. 各行业流失率
SELECT
    c.industry,
    COUNT(DISTINCT CASE WHEN s.final_status='流失' THEN c.customer_id END) AS `流失客户数`,
    COUNT(DISTINCT c.customer_id) AS `总客户数`,
    ROUND(
        COUNT(DISTINCT CASE WHEN s.final_status='流失' THEN c.customer_id END)
        / COUNT(DISTINCT c.customer_id) *100,2
    ) AS `流失率(%)`
FROM `客户表` c
LEFT JOIN `客户状态表` s ON c.customer_id = s.customer_id
GROUP BY c.industry;

-- 3. 流失原因分布（带数量+占比）
SELECT 
    `客户状态表`.lose_reason,
    COUNT(DISTINCT `客户状态表`.customer_id) AS `数量`,
    ROUND(
        COUNT(DISTINCT `客户状态表`.customer_id) 
        / (SELECT COUNT(DISTINCT `客户状态表`.customer_id) FROM `客户状态表` WHERE `客户状态表`.final_status = '流失') 
        * 100,
        2
    ) AS `占比(%)`
FROM `客户状态表`
WHERE `客户状态表`.final_status = '流失'
GROUP BY `客户状态表`.lose_reason;
```

## Power BI 部分

### DAX 度量值

```
总客户数 = DISTINCTCOUNT('客户表'[customer_id])
流失客户数 = CALCULATE([总客户数],'客户状态表'[final_status]="流失")
成交客户数 = CALCULATE([总客户数],'客户状态表'[final_status]="成交")
流失率 = DIVIDE([流失客户数],[总客户数],0)

当月报价客户_流失数量 =
CALCULATE(
    [流失客户数],
    TREATAS(VALUES('报价记录表'[customer_id]),'客户表'[customer_id])
)
当月报价客户_流失率 = DIVIDE([当月报价客户_流失数量], DISTINCTCOUNT('报价记录表'[customer_id]),0)
```

### PowerBI 可视化看板设计

看板页面一共包含 5 个可视化组件：

1. 指标卡片：展示核心 KPI，总客户数、成交客户数量、流失客户数量、整体流失率
2. 饼图：流失原因分布，直观查看各类流失原因的客户占比
3. 簇状柱形图：各行业客户流失率对比，定位高流失行业
4. 折线图：每月报价客户流失趋势，观察不同时间段的转化变化
5. 切片器：企业规模、产品名称，支持交互式筛选，自由查看细分维度数据

> 
> 技术亮点：使用 TREATAS 实现虚拟关系，解决按月统计报价客户流失的上下文计算问题，实现看板动态筛选联动。

## 业务洞察

1. 整体客户流失率 71%，流失占比偏高；**流失首要原因为预算不足**，其次是项目周期无法满足/项目取消，预算限制是客户流失最大痛点。
2. 行业维度：**商贸零售行业客户流失率最高**，制造业流失相对更低，商贸零售客户预算管控严格，对成本更加敏感。
3. 交付周期越长，客户流失概率越高，过长交付周期会降低客户意向。
4. 每月询价客户数量存在波动，部分月份询价客户多，但成交转化没有同步提升。

## 落地优化建议

1. 针对商贸零售这类高流失行业，报价设计双方案：基础精简套餐（控制总价适配有限预算）+ 高配增值套餐，客户按需选择。
2. 遇到预算不足的客户，报价阶段可提供分期、分批次交付方案，降低一次性资金压力，缓解预算短板。
3. 因竞品价格流失的客户，销售增加二次议价沟通，重点展示产品附加价值，减少单纯比价流失。
4. 长交付周期订单，报价前期提前同步交付节点，可提供分段交付选项，减少周期带来的客户流失。
5. 在月度询价高峰期，增加销售跟进人力，提前沟通客户预算预期，抓住询价窗口期，提升成交转化。
