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
  EPS         number ,                        --ÿ������          
  EPS_YOY     number ,                        --ÿ������ͬ��(%)   
  BVPS        number ,                        --ÿ�ɾ��ʲ�        
  ROE         number ,                        --���ʲ�������(%)   
  EPCF        number ,                        --ÿ���ֽ�����(Ԫ)  
  NET_PROFITS number ,                        --������(��Ԫ)      
  PROFITS_YOY number ,                        --������ͬ��(%)     
  DISTRIB     number ,                        --���䷽��          
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
 ROE                 number                 ,      --���ʲ�������(%)                 
 NET_PROFIT_RATIO    number                 ,      --������(%)                      
 GROSS_PROFIT_RATE   number                 ,      --ë����(%)                      
 NET_PROFITS         number                 ,      --������(��Ԫ)                   
 EPS                 number                 ,      --ÿ������                       
 BUSINESS_INCOME     number                 ,      --Ӫҵ����(����Ԫ)               
 BIPS                number                 ,      --ÿ����Ӫҵ������(Ԫ)           
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
  ARTURNOVER             number ,                    --Ӧ���˿���ת��(��)  
  ARTURNDAYS             number ,                    --Ӧ���˿���ת����(��)
  INVENTORY_TURNOVER     number ,                    --�����ת��(��)      
  INVENTORY_DAYS         number ,                    --�����ת����(��)    
  CURRENTASSET_TURNOVER  number ,                    --�����ʲ���ת��(��)  
  CURRENTASSET_DAYS      number ,                    --�����ʲ���ת����(��)
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
   MBRG                   number  ,                 --��Ӫҵ������������(%)
   NPRG                   number  ,                 --������������(%)      
   NAV                    number  ,                 --���ʲ�������         
   TARG                   number  ,                 --���ʲ�������         
   EPSG                   number  ,                 --ÿ������������       
   SEG                    number  ,                 --�ɶ�Ȩ��������       
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
   CURRENTRATIO           number ,                  --��������                                               
   QUICKRATIO             number ,                  --�ٶ�����                                               
   CASHRATIO              number ,                  --�ֽ����                                               
   ICRATIO                number ,                  --��Ϣ֧������                                           
   SHEQRATIO              number ,                  --�ɶ�Ȩ�����                                           
   ADRATIO                number ,                  --�ɶ�Ȩ��������                                           
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
   CF_SALES               number ,                   --��Ӫ�ֽ������������������     
   RATEOFRETURN           number ,                   --�ʲ��ľ�Ӫ�ֽ������ر���       
   CF_NM                  number ,                   --��Ӫ�ֽ������뾻����ı���   
   CF_LIABILITIES         number ,                   --��Ӫ�ֽ������Ը�ծ����       
   CASHFLOWRATIO          number ,                   --�ֽ���������                   
   YEAR                   number not null ,                 
   QUARTER                number not null
) ;                                                                        
drop index idx_stock_cashflow_data ;                                     
create index idx_stock_cashflow_data on tb_stock_cashflow_data( CODE );


--��Ʊ����
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

--��Ʊ�б�
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


--��Ʊ������
drop table tb_stock_data_daily ;

create table tb_stock_data_daily
(
    name               varchar2(64)   not null ,      --����                     
    code               varchar2(32)   not null ,      --����                     
    price              number                  ,      --��ǰ�۸�                 
    price_last_day     number                  ,      --����                     
    price_today_open   number                  ,      --��                                             
    shi_jian           date                    ,      --ʱ��                     
    zhang_die          number                  ,      --�ǵ�                     
    zhang_die_rate     number                  ,      --�ǵ�%                    
    max_price          number                  ,      --���                     
    min_price          number                  ,      --���                     
    p_v_a              varchar2(256)           ,      --�۸�/�ɽ������֣�/�ɽ��� 
    vol                number                  ,      --�ɽ������֣�             
    amount             number                  ,      --�ɽ����             
    huan_sou_lv        number                  ,      --������                   
    pe                 number                  ,      --��ӯ��                   
    zhenfu             number                  ,      --���                     
    liutongshizhi      number                  ,      --��ͨ��ֵ                 
    zhongshizhi        number                  ,      --����ֵ                   
    shijinglv          number                  ,      --�о���                   
    zhangtingjia       number                  ,      --��ͣ��                   
    dietingjia         number                  ,      --��ͣ��
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

--��Ϊ�ڴ�����Ҫ������
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
