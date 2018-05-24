select * from tb_stock_classified where c_name like '%人%';
select * from tb_stock_classified where c_name like '%恒%';
select * from tb_stock_classified where c_name like '%智%';
select * from tb_stock_classified where c_name like '%果%';
select * from tb_stock_classified where c_name like '%游戏%';
select * from tb_stock_classified where c_name like '%环%';
select * from tb_stock_classified where c_name like '%重组%';
select * from tb_stock_classified where c_name like '%社%';
select code,count(1) from tb_stock_classified group by code having count(1)>1 order by count(1) desc ;
select code,count(1) from tb_stock_classified group by code having count(1)>1;

select * from tb_stock_classified where code = '600292';

connect c##stock/didierg160@myoracle ;
select a.code,
       a.name,
       a.price ,
       a.price/a.pe 每股利润 ,
       a.pe,
       a.pb,
       a.LIQUID_ASSETS,
       a.TOTAL_ASSETS ,
       b.c_name ,
       b.weight
from tb_stock_list a ,
     c##tushare.tb_stock_classified b
where
  a.TOTAL_ASSETS <= 100
    and
  a.pe is not null 
    and
  a.price is not null
    and
  a.pe > 0
    and
  a.pe <=50 
    and
  a.code = b.code
order by a.price/a.pe desc;
  
update tb_stock_list a set 
  price = (
             select price from tb_stock_data_daily where 
               code=a.code 
                 and
               shi_jian = 
               (
                 select max(shi_jian) from tb_stock_data_daily where code = a.code
               )
          )
;

--tb_stock_report_data
--tb_stock_profit_data
--tb_stock_operation_data
--tb_stock_growth_data
--tb_stock_debtpaying_data
--tb_stock_cashflow_data

select code,
       name , 
       sum(eps)/count(1)         avg_eps , 
       sum(epcf)/count(1)        avg_epcf, 
       sum(net_profits)/count(1) avg_profits ,
       count(1)
from tb_stock_report_data 
group by code , name 
order by avg_eps desc ;

select code,
       name , 
       stddev(roe)         ,
       stddev(net_profit_ratio)  ,
       stddev(gross_profit_rate)  ,
       stddev(net_profits)  ,
       count(1)
from tb_stock_profit_data where
	NET_PROFIT_RATIO > 0
group by code , name 
order by  stddev(net_profits) desc ;



select a.code                    ,
       a.name                    ,
       a.YEAR                    ,
       a.QUARTER                 ,
       a.REPORT_DATE             ,       
       a.EPS                   每股收益          ,   
       a.EPS_YOY               每股收益同比   ,   
       a.BVPS                  每股净资产        ,   
       a.ROE                   净资产收益率   ,   
       a.EPCF                  每股现金流量_元  ,   
       a.NET_PROFITS           净利润_万元      ,   
       a.PROFITS_YOY           净利润同比     ,   
       a.DISTRIB               分配方案          ,
       b.ROE                   净资产收益率       ,
       b.NET_PROFIT_RATIO      净利率            ,
       b.GROSS_PROFIT_RATE     毛利率             ,
       b.NET_PROFITS           净利润_万元          ,
       b.EPS                   每股收益              ,
       b.BUSINESS_INCOME       营业收入_百万元      ,
       b.BIPS                  每股主营业务收入_元  ,
       c.ARTURNOVER            应收账款周转率_次    ,
       c.ARTURNDAYS            应收账款周转天数_天  ,
       c.INVENTORY_TURNOVER    存货周转率_次       ,
       c.INVENTORY_DAYS        存货周转天数_天      ,
       c.CURRENTASSET_TURNOVER 流动资产周转率_次    ,
       c.CURRENTASSET_DAYS     流动资产周转天数_天  ,
       d.MBRG                  主营业务收入增长率  ,
       d.NPRG                  净利润增长率       ,
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
        shi_jian = to_date('20170510150000','yyyymmddhh24miss')
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
order by a.code , a.year asc , a.QUARTER asc;


select code,year,QUARTER,count(1) from tb_stock_report_data     group by code,year,QUARTER having count(1) > 1;
select code,year,QUARTER,count(1) from tb_stock_profit_data     group by code,year,QUARTER having count(1) > 1;
select code,year,QUARTER,count(1) from tb_stock_operation_data  group by code,year,QUARTER having count(1) > 1;
select code,year,QUARTER,count(1) from tb_stock_growth_data     group by code,year,QUARTER having count(1) > 1;
select code,year,QUARTER,count(1) from tb_stock_debtpaying_data group by code,year,QUARTER having count(1) > 1;
select code,year,QUARTER,count(1) from tb_stock_cashflow_data   group by code,year,QUARTER having count(1) > 1;

select * from tb_stock_report_data     order by code , year asc , QUARTER asc ;
select * from tb_stock_profit_data     order by code , year asc , QUARTER asc ;
select * from tb_stock_operation_data  order by code , year asc , QUARTER asc ;
select * from tb_stock_growth_data     order by code , year asc , QUARTER asc ;
select * from tb_stock_debtpaying_data order by code , year asc , QUARTER asc ;
select * from tb_stock_cashflow_data   order by code , year asc , QUARTER asc ;