#股灾后反弹不多
#股价5元以下
#股东人数少
#社保持仓
#盈利稳定
import numpy as np
import pandas as pd
import cx_oracle 


select a.code                    ,
       a.name                    ,
       a.YEAR                    ,
       a.QUARTER                 ,
       a.REPORT_DATE             ,       
       a.EPS                   每股收益          ,   
       a.EPS_YOY               每股收益同比(%)   ,   
       a.BVPS                  每股净资产        ,   
       a.ROE                   净资产收益率(%)   ,   
       a.EPCF                  每股现金流量(元)  ,   
       a.NET_PROFITS           净利润(万元)      ,   
       a.PROFITS_YOY           净利润同比(%)     ,   
       a.DISTRIB               分配方案          ,
       b.ROE                   净资产收益率(%)       ,
       b.NET_PROFIT_RATIO      净利率(%)             ,
       b.GROSS_PROFIT_RATE     毛利率(%)             ,
       b.NET_PROFITS           净利润(万元)          ,
       b.EPS                   每股收益              ,
       b.BUSINESS_INCOME       营业收入(百万元)      ,
       b.BIPS                  每股主营业务收入(元)  ,
       c.ARTURNOVER            应收账款周转率(次)    ,
       c.ARTURNDAYS            应收账款周转天数(天)  ,
       c.INVENTORY_TURNOVER    存货周转率(次)        ,
       c.INVENTORY_DAYS        存货周转天数(天)      ,
       c.CURRENTASSET_TURNOVER 流动资产周转率(次)    ,
       c.CURRENTASSET_DAYS     流动资产周转天数(天)  ,
       d.MBRG                  主营业务收入增长率(%)  ,
       d.NPRG                  净利润增长率(%)        ,
       d.NAV                   净资产增长率           ,
       d.TARG                  总资产增长率           ,
       d.EPSG                  每股收益增长率         ,
       d.SEG                   股东权益增长率         ,
       e.CURRENTRATIO          流动比率        ,
       e.QUICKRATIO            速动比率        ,
       e.CASHRATIO             现金比率        ,
       e.ICRATIO               利息支付倍数    ,
       e.SHEQRATIO             股东权益比率    ,
       e.ADRATIO               股东权益增长率  ,
       f.CF_SALES              经营现金净流量对销售收入比率  ,
       f.RATEOFRETURN          资产的经营现金流量回报率      ,
       f.CF_NM                 经营现金净流量与净利润的比率  ,
       f.CF_LIABILITIES        经营现金净流量对负债比率      ,
       f.CASHFLOWRATIO         现金流量比率                       
from tb_stock_report_data         a,
     tb_stock_profit_data         b,
     tb_stock_operation_data      c,
     tb_stock_growth_data         d,
     tb_stock_debtpaying_data     e,
     tb_stock_cashflow_data       f
where
  a.code in      
  (
      select code from c##stock.tb_stock_data_daily where 
        price <= 5
         and
        shi_jian = (select max(shi_jian) from c##stock.tb_stock_data_daily )
  )
    and
  a.code in 
  (
      select code from  tb_stock_classified where c_name like '%社%'
  )
    and
    a.code = b.code
      and
    a.code = c.code
      and
    a.code = d.code
      and            
    a.code = e.code
      and
    a.code = f.code
      and
    a.year = b.year
      and
    a.year = c.year
      and
    a.year = d.year
      and
    a.year = e.year
      and
    a.year = f.year
      and                    
    a.QUARTER = b.QUARTER
      and      
    a.QUARTER = c.QUARTER
      and      
    a.QUARTER = d.QUARTER
      and      
    a.QUARTER = e.QUARTER
      and      
    a.QUARTER = f.QUARTER 
order by code , year asc , QUARTER asc;