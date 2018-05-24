connect c##tushare/didierg160@myoracle ;
drop table tb_stock_forecast_data ;
create table tb_stock_forecast_data
(
"index"        NUMBER ,
CODE           varchar2(16) not null  ,       
NAME           varchar2(16) not null  ,       
TYPE           varchar2(16)           ,       
REPORT_DATE    varchar2(16)           ,       
PRE_EPS        number                 ,
RANGE          varchar2(256)          ,
YEAR           NUMBER                 ,
QUARTER        NUMBER 
);

drop index idx_stock_forecast_data ;                                  
create index idx_stock_forecast_data on tb_stock_forecast_data( CODE ); 

drop table tb_stock_report_data ;
create table tb_stock_report_data
(
  "index"     number not null ,
  CODE        varchar2(16) not null  ,
  NAME        varchar2(16) not null  ,
  EPS         number ,                        --每股收益          
  EPS_YOY     number ,                        --每股收益同比(%)   
  BVPS        number ,                        --每股净资产        
  ROE         number ,                        --净资产收益率(%)   
  EPCF        number ,                        --每股现金流量(元)  
  NET_PROFITS number ,                        --净利润(万元)      
  PROFITS_YOY number ,                        --净利润同比(%)     
  DISTRIB     number ,                        --分配方案          
  REPORT_DATE varchar2(32) not null ,
  YEAR        number not null ,
  QUARTER     number not null 
);
drop index idx_stock_report_data ;                                  
create index idx_stock_report_data on tb_stock_report_data( CODE ); 

drop table tb_stock_profit_data ;
create table tb_stock_profit_data 
(
 "index"             number not null ,                       
 CODE                varchar2(16) not null  ,                
 NAME                varchar2(16) not null  ,                
 ROE                 number                 ,      --净资产收益率(%)                 
 NET_PROFIT_RATIO    number                 ,      --净利率(%)                      
 GROSS_PROFIT_RATE   number                 ,      --毛利率(%)                      
 NET_PROFITS         number                 ,      --净利润(万元)                   
 EPS                 number                 ,      --每股收益                       
 BUSINESS_INCOME     number                 ,      --营业收入(百万元)               
 BIPS                number                 ,      --每股主营业务收入(元)           
 YEAR                number not null        ,                 
 QUARTER             number not null
);                                                   
drop index idx_stock_profit_data ;                                  
create index idx_stock_profit_data on tb_stock_profit_data( CODE ); 

drop table tb_stock_operation_data ;
create table tb_stock_operation_data 
(
  "index"                number not null ,                       
  CODE                   varchar2(16) not null  ,                
  NAME                   varchar2(16) not null  ,
  ARTURNOVER             number ,                    --应收账款周转率(次)  
  ARTURNDAYS             number ,                    --应收账款周转天数(天)
  INVENTORY_TURNOVER     number ,                    --存货周转率(次)      
  INVENTORY_DAYS         number ,                    --存货周转天数(天)    
  CURRENTASSET_TURNOVER  number ,                    --流动资产周转率(次)  
  CURRENTASSET_DAYS      number ,                    --流动资产周转天数(天)
  YEAR                   number not null ,                 
  QUARTER                number not null
) ;
drop index idx_stock_operation_data ;                                  
create index idx_stock_operation_data on tb_stock_operation_data( CODE );
 
drop table tb_stock_growth_data ;
create table tb_stock_growth_data 
(
   "index"                number not null ,                       
   CODE                   varchar2(16) not null  ,                
   NAME                   varchar2(16) not null  ,
   MBRG                   number  ,                 --主营业务收入增长率(%)
   NPRG                   number  ,                 --净利润增长率(%)      
   NAV                    number  ,                 --净资产增长率         
   TARG                   number  ,                 --总资产增长率         
   EPSG                   number  ,                 --每股收益增长率       
   SEG                    number  ,                 --股东权益增长率       
   YEAR                   number not null ,                 
   QUARTER                number not null           
) ;
drop index idx_stock_growth_data ;                                  
create index idx_stock_growth_data on tb_stock_growth_data( CODE );

drop table tb_stock_debtpaying_data ;                                                            
create table tb_stock_debtpaying_data                                                             
(                                                            
   "index"                number not null ,                                                                   
   CODE                   varchar2(16) not null  ,                                                            
   NAME                   varchar2(16) not null  ,                                                            
   CURRENTRATIO           number ,                  --流动比率                                               
   QUICKRATIO             number ,                  --速动比率                                               
   CASHRATIO              number ,                  --现金比率                                               
   ICRATIO                number ,                  --利息支付倍数                                           
   SHEQRATIO              number ,                  --股东权益比率                                           
   ADRATIO                number ,                  --股东权益增长率                                           
   YEAR                   number not null ,                                                                             
   QUARTER                number not null                                                            
) ;                                                            
drop index idx_stock_debtpaying_data ;                                                                                              
create index idx_stock_debtpaying_data on tb_stock_debtpaying_data( CODE );                                                            

drop table tb_stock_cashflow_data ;
create table tb_stock_cashflow_data 
(
   "index"                number not null ,       
   CODE                   varchar2(16) not null  ,
   NAME                   varchar2(16) not null  ,
   CF_SALES               number ,                   --经营现金净流量对销售收入比率     
   RATEOFRETURN           number ,                   --资产的经营现金流量回报率       
   CF_NM                  number ,                   --经营现金净流量与净利润的比率   
   CF_LIABILITIES         number ,                   --经营现金净流量对负债比率       
   CASHFLOWRATIO          number ,                   --现金流量比率                   
   YEAR                   number not null ,                 
   QUARTER                number not null
) ;                                                                        
drop index idx_stock_cashflow_data ;                                     
create index idx_stock_cashflow_data on tb_stock_cashflow_data( CODE );


--股票分类
drop table tb_stock_classified ;
create table tb_stock_classified 
(
  code           varchar2(32) not null,
  name           varchar2(32) not null,
  c_name         varchar2(32)         ,
  shi_jian       varchar2(32)  ,
  weight         number 
);

drop index idx_stock_classified ;
create index idx_stock_classified on tb_stock_classified(c_name );

--股票列表
drop table tb_stock_list ;
create table tb_stock_list
(
    CODE                 varchar2(16)  not null ,
    NAME                 varchar2(16)  not null ,
    INDUSTRY             varchar2(64)  ,
    AREA                 varchar2(16)  ,
    PE                   number        ,
    OUTSTANDING          number        ,
    TOTALS               number        ,
    totalAssets          number        ,
    liquidAssets         number        ,
    fixedAssets          number        ,
    RESERVED             number        ,
    reservedPerShare     number        ,
    ESP                  number  ,
    BVPS                 number        ,
    PB                   number        ,
    timeToMarket         varchar2(16)  ,
    UNDP                 number        ,
    PERUNDP              number        ,
    REV                  number        ,
    PROFIT               number        ,
    GPR                  number        ,
    NPR                  number        ,
    HOLDERS              number        ,
    time_stamp           date default sysdate not null 
);

alter table tb_stock_list add constraint
pk_stock_list
primary key(code) 
/


--股票日数据
drop table tb_stock_data_daily ;

create table tb_stock_data_daily
(
    name               varchar2(64)   not null ,      --名字                     
    code               varchar2(32)   not null ,      --代码                     
    price              number                  ,      --当前价格                 
    price_last_day     number                  ,      --昨收                     
    price_today_open   number                  ,      --今开                                             
    shi_jian           date                    ,      --时间                     
    zhang_die          number                  ,      --涨跌                     
    zhang_die_rate     number                  ,      --涨跌%                    
    max_price          number                  ,      --最高                     
    min_price          number                  ,      --最低                     
    p_v_a              varchar2(256)           ,      --价格/成交量（手）/成交额 
    vol                number                  ,      --成交量（手）             
    amount             number                  ,      --成交额（万）             
    huan_sou_lv        number                  ,      --换手率                   
    pe                 number                  ,      --市盈率                   
    zhenfu             number                  ,      --振幅                     
    liutongshizhi      number                  ,      --流通市值                 
    zhongshizhi        number                  ,      --总市值                   
    shijinglv          number                  ,      --市净率                   
    zhangtingjia       number                  ,      --涨停价                   
    dietingjia         number                  ,      --跌停价
    MA6                number                  , 
    MA12               number                  , 
    MA20               number                  , 
    MA30               number                  , 
    MA45               number                  , 
    MA60               number                  , 
    MA125              number                  , 
    MA250              number                  , 
    KDJ_K              number                  , 
    KDJ_D              number                  , 
    KDJ_J              number                  , 
    xstd_SLONG         number                  , 
    xstd_SSHORT        number                  , 
    xstd_LLONG         number                  , 
    xstd_LSHORT        number                  , 
    BOLL_uBOLL         number                  , 
    BOLL_dBOLL         number                  , 
    BOLL_BOLL          number                  , 
    MACD_DIF           number                  , 
    MACD_MACD          number                  , 
    MACD_DIF_MACD      number                  ,      
    DPO_DPO            number                  ,
    DPO_6MA	           number 
);

--变为内存表后还是要用索引
drop index idx_stock_data_Daily ;
create index idx_stock_data_Daily on tb_stock_data_Daily(code);


connect sys/t2h4o6m8@myoracle as sysdba ;
alter system set inmemory_size=3000M scope=spfile; 

alter table c##tushare.tb_stock_report_data     inmemory ;  
alter table c##tushare.tb_stock_profit_data     inmemory ;
alter table c##tushare.tb_stock_operation_data  inmemory ;
alter table c##tushare.tb_stock_growth_data     inmemory ;
alter table c##tushare.tb_stock_debtpaying_data inmemory ;
alter table c##tushare.tb_stock_cashflow_data   inmemory ;
alter table c##tushare.tb_stock_classified      inmemory ;
