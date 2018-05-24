select * from tb_stock_classified where c_name like '%��%';
select * from tb_stock_classified where c_name like '%��%';
select * from tb_stock_classified where c_name like '%��%';
select * from tb_stock_classified where c_name like '%��%';
select * from tb_stock_classified where c_name like '%��Ϸ%';
select * from tb_stock_classified where c_name like '%��%';
select * from tb_stock_classified where c_name like '%����%';
select * from tb_stock_classified where c_name like '%��%';
select code,count(1) from tb_stock_classified group by code having count(1)>1 order by count(1) desc ;
select code,count(1) from tb_stock_classified group by code having count(1)>1;

select * from tb_stock_classified where code = '600292';

connect c##stock/didierg160@myoracle ;
select a.code,
       a.name,
       a.price ,
       a.price/a.pe ÿ������ ,
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
       a.EPS                   ÿ������          ,   
       a.EPS_YOY               ÿ������ͬ��   ,   
       a.BVPS                  ÿ�ɾ��ʲ�        ,   
       a.ROE                   ���ʲ�������   ,   
       a.EPCF                  ÿ���ֽ�����_Ԫ  ,   
       a.NET_PROFITS           ������_��Ԫ      ,   
       a.PROFITS_YOY           ������ͬ��     ,   
       a.DISTRIB               ���䷽��          ,
       b.ROE                   ���ʲ�������       ,
       b.NET_PROFIT_RATIO      ������            ,
       b.GROSS_PROFIT_RATE     ë����             ,
       b.NET_PROFITS           ������_��Ԫ          ,
       b.EPS                   ÿ������              ,
       b.BUSINESS_INCOME       Ӫҵ����_����Ԫ      ,
       b.BIPS                  ÿ����Ӫҵ������_Ԫ  ,
       c.ARTURNOVER            Ӧ���˿���ת��_��    ,
       c.ARTURNDAYS            Ӧ���˿���ת����_��  ,
       c.INVENTORY_TURNOVER    �����ת��_��       ,
       c.INVENTORY_DAYS        �����ת����_��      ,
       c.CURRENTASSET_TURNOVER �����ʲ���ת��_��    ,
       c.CURRENTASSET_DAYS     �����ʲ���ת����_��  ,
       d.MBRG                  ��Ӫҵ������������  ,
       d.NPRG                  ������������       ,
       d.NAV                   ���ʲ�������           ,
       d.TARG                  ���ʲ�������           ,
       d.EPSG                  ÿ������������         ,
       d.SEG                   �ɶ�Ȩ��������         ,
       e.CURRENTRATIO          ��������        ,
       e.QUICKRATIO            �ٶ�����        ,
       e.CASHRATIO             �ֽ����        ,
       e.ICRATIO               ��Ϣ֧������    ,
       e.SHEQRATIO             �ɶ�Ȩ�����    ,
       e.ADRATIO               �ɶ�Ȩ��������  ,
       f.CF_SALES              ��Ӫ�ֽ������������������  ,
       f.RATEOFRETURN          �ʲ��ľ�Ӫ�ֽ������ر���      ,
       f.CF_NM                 ��Ӫ�ֽ������뾻����ı���  ,
       f.CF_LIABILITIES        ��Ӫ�ֽ������Ը�ծ����      ,
       f.CASHFLOWRATIO         �ֽ���������                       
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
      select code from  tb_stock_classified where c_name like '%��%'
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