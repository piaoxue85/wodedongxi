connect c##stock/didierg160@myoracle ;
--股权质押明细数据
drop table tb_stock_pledged_detail;
create table tb_stock_pledged_detail
(
   code           varchar2(16)  not null ,
   name           varchar2(16)  not null ,
   ann_date       varchar2(16)           ,          --公告日期
   pledgor        varchar2(256)          ,          --出质人
   pledgee        varchar2(256)          ,          --质权人
   volume         number                 ,          --质押数量
   from_date      varchar2(16)           ,          --质押日期
   end_date       varchar2(16)           ,          --解除日期
   time_stamp     date not null  
);

--股权质押统计数据
drop table tb_stock_pledged ;
create table tb_stock_pledged
(
  code             varchar2(16) not null ,   
  name             varchar2(16) not null ,
  deals            number                ,    --质押次数
  unrest_pledged   number                ,    --无限售股质押数量（万）
  rest_pledged     number                ,    --  限售股质押数量（万）
  totals           number                ,    --总股本
  p_ratio          number                ,    --质押比例
  time_stamp       date not null 
);


drop table tb_stock_data_daily_taobao ;
create table tb_stock_data_daily_taobao
(
  code                     varchar2(16) not null ,      --股票代码     
  name                     varchar2(16) not null ,      --股票名称     
  shi_jian                 varchar2(16) not null ,      --交易日期     
  Sina_industry            varchar2(64)          ,      --新浪行业     
  Sina_concept             varchar2(512)         ,      --新浪概念     
  Sina_area                varchar2(64)          ,      --新浪地域     
  open                     number                ,      --开盘价       
  max                      number                ,      --最高价       
  min                      number                ,      --最低价       
  close                    number                ,      --收盘价       
  adj_after                number                ,      --后复权价     
  adj_before               number                ,      --前复权价     
  Change                   number                ,      --涨跌幅       
  vol                      number                ,      --成交量       
  amout                    number                ,      --成交额       
  turnover_rate            number                ,      --换手率       
  tradable_market_cap      number                ,      --流通市值     
  market_cap               number                ,      --总市值       
  is_up_Limit              number                ,      --是否涨停     
  is_down_Limit            number                ,      --是否跌停     
  pe_ttm                   number                ,      --市盈率TTM    
  PS_ttm                   number                ,      --市销率TTM    
  PCF_ttm                  number                ,      --市现率TTM    
  pb                       number                ,      --市净率       
  MA_5                     number                ,      --MA_5         
  MA_10                    number                ,      --MA_10        
  MA_20                    number                ,      --MA_20        
  MA_30                    number                ,      --MA_30        
  MA_60                    number                ,      --MA_60        
  MA_up_down_corss         varchar2(512)         ,      --MA金叉死叉   
  MACD_DIF                 number                ,      --MACD_DIF     
  MACD_DEA                 number                ,      --MACD_DEA     
  MACD_MACD                number                ,      --MACD_MACD    
  MACD_up_down_corss       varchar2(512)         ,      --MACD_金叉死叉
  KDJ_K                    number                ,      --KDJ_K        
  KDJ_D                    number                ,      --KDJ_D        
  KDJ_J                    number                ,      --KDJ_J        
  KDJ_up_down_corss        varchar2(512)         ,      --KDJ_金叉死叉 
  boll_mid                 number                ,      --布林线中轨   
  boll_up                  number                ,      --布林线上轨   
  boll_low                 number                ,      --布林线下轨   
  psy                      number                ,      --psy          
  psyma                    number                ,      --psyma        
  rsi1                     number                ,      --rsi1         
  rsi2                     number                ,      --rsi2         
  rsi3                     number                ,      --rsi3         
  Amplitude                number                ,      --振幅         
  Volume_Ratio             number                       --量比         
);

--变为内存表后还是要用索引
drop index idx_stock_data_daily_taobao ;
create index idx_stock_data_daily_taobao on tb_stock_data_daily_taobao(code);
--变为内存表后还是要用索引
drop index idx_stock_data_daily_taobao1 ;
create index idx_stock_data_daily_taobao1 on tb_stock_data_daily_taobao(shi_jian);


create table tb_stock_fator_test
(
 SHI_JIAN  VARCHAR2(32)   ,
 FATOR     VARCHAR2(32)   ,
 CODES     VARCHAR2(1024) ,
 AVG_RET   NUMBER
) ;



drop table tb_stock_data_daily_wind ;
create table tb_stock_data_daily_wind
(
   name                        varchar2(64)   not null ,                
   code                        varchar2(32)   not null ,
   shi_jian                    varchar2(10)   not null ,  
   pre_close                   number                  ,--前收盘价
   open                        number                  ,--
   high                        number                  ,--
   low                         number                  ,--
   close                       number                  ,--
   volume                      number                  ,--
   amt                         number                  ,--成交额
   dealnum                     number                  ,--成交笔数
   chg                         number                  ,--涨跌
   pct_chg                     number                  ,--涨跌幅
   swing                       number                  ,--振幅
   vwap                        number                  ,--均价
   --adjfactor                   number                  ,--复权因子
   rel_ipo_chg                 number                  ,--相对发行价涨跌
   rel_ipo_pct_chg             number                  ,--相对发行价涨跌幅
   total_shares                number                  ,--总股本
   free_float_shares           number                  ,--自由流通股本
   mf_amt                      number                  ,--净流入资金
   mf_vol                      number                  ,--净流入量
   mf_amt_ratio                number                  ,--金额流入率
   mf_vol_ratio                number                  ,--资金流向占比
   mf_amt_close                number                  ,--尾盘净流入资金
   mf_amt_open                 number                  ,--开盘净流入资金
   pe_ttm                      number                  ,--市盈率 ttm
   val_pe_deducted_ttm         number                  ,--市盈率 ttm，扣除非经常性损益
   pe_lyr                      number                  ,--市盈率 lyr
   pb_lf                       number                  ,--市净率 pb lf
   pb_mrq                      number                  ,--市净率 pb mrq
   ps_ttm                      number                  ,--市销率 ps ttm
   ps_lyr                      number                  ,--市销率 ps lyr
   pcf_ocf_ttm                 number                  ,--市现率pcf 经营现金流ttm
   pcf_ncf_ttm                 number                  ,--市现率pcf 现金流量ttm
   pcf_ocflyr                  number                  ,--市现率pcf 经营现金流lyr
   pcf_nflyr                   number                  ,--市现率pcf 现金净流量lyr
   pe_est                      number                  ,--预测pe 
   estpe_FY1                   number                  ,--预测pe fy1
   estpe_FY2                   number                  ,--预测pe fy2
   estpe_FY3                   number                  ,--预测pe fy3
   pe_est_last                 number                  ,--预测pe 最新预测
   pe_est_ftm                  number                  ,--预测pe 未来12个月
   est_peg                     number                  ,--预测peg 
   estpeg_FY1                  number                  ,--预测peg fy1       
   estpeg_FY2                  number                  ,--预测peg fy2       
   estpeg_FTM                  number                  ,--预测peg 未来12个月
   estpb                       number                  ,--预测pb
   estpb_FY1                   number                  ,--预测pb FY1
   estpb_FY2                   number                  ,--预测pb FY2
   estpb_FY3                   number                  ,--预测pb FY3
   ev1                         number                  ,--企业价值 含货币资金
   ev2                         number                  ,--企业价值 剔除货币资金
   ev2_to_ebitda               number                  ,--企业倍数 ev2/ebitda
   history_low                 number                  ,--近期创历史新低
   stage_high                  number                  ,--近期创阶段新高
   history_high                number                  ,--近期创历史新高
   stage_low                   number                  ,--近期创历史新低
   up_days                     number                  ,--连涨天数
   down_days                   number                  ,--连跌天数
   breakout_ma                 number                  ,--向上有效突破均线
   breakdown_ma                number                  ,--向下有效突破均线
   bull_bear_ma                number                  ,--均线多头排列看涨看跌
   holder_num                  number                  ,--股东户数
   holder_avgnum               number                  ,--户均持股数量
   holder_totalbyinst          number                  ,--机构持股数量合计
   holder_pctbyinst            number                  ,--机构持股比例合计
   mkt_cap_ashare2             number                  ,--总市值   含限售股
   mkt_cap_ashare              number                   --流通市值 不含限售股
) ;
--变为内存表后还是要用索引
drop index idx_stock_data_daily_wind ;
create index idx_stock_data_daily_wind on tb_stock_data_daily_wind(code);
--变为内存表后还是要用索引
drop index idx_stock_data_daily_wind1 ;
create index idx_stock_data_daily_wind1 on tb_stock_data_daily_wind(shi_jian);



create table tb_stock_important_day
(
	shi_jian  varchar2(10)  not null ,
	name      varchar2(128) not null 
);

create table tb_stock_my_f
(
	code      varchar2(10) not null ,
	shi_jian  varchar2(16) not null ,
	f1        number , 
	f2        number , 
	f3        number , 
	f4        number , 
	f5        number , 
	f6        number , 
	f7        number , 
	f8        number , 
	f9        number , 
	f10       number , 
	f11       number , 
	f12       number , 
	f13       number , 
	f14       number , 
	f15       number , 
	f16       number  
) ;

create index idx_stock_my_f on tb_stock_my_f(code );
create index idx_stock_my_f1 on tb_stock_my_f(shi_jian );

create table tb_stock_101_selected
(
	code      varchar2(10) not null ,
	shi_jian  varchar2(16) not null ,
	selected  number not null,
);
create index idx_stock_101_selected on tb_stock_101_selected(shi_jian);

create table tb_stock_101_return
(
	code      varchar2(10) not null ,
	shi_jian  varchar2(16) not null ,
	return    number ,
	RET_STD   number ,
	RET_HOT   number 	
);

create index idx_stock_101_return on tb_stock_101_return(shi_jian);

create table tb_stock_101_total_return
(
	shi_jian  varchar2(16) not null primary key ,
	return    number 
);

create index idx_stock_101_total_return on tb_stock_101_total_return(shi_jian);

create table tb_stock_alpha101
(
  code       varchar2(10) not null ,
  shi_Jian   date not null ,
  alpha_001  number ,
  alpha_002  number ,
  alpha_003  number ,
  alpha_004  number ,
  alpha_005  number ,
  alpha_006  number ,
  alpha_007  number ,
  alpha_008  number ,
  alpha_009  number ,
  alpha_010  number ,
  alpha_011  number ,
  alpha_012  number ,
  alpha_013  number ,
  alpha_014  number ,
  alpha_015  number ,
  alpha_016  number ,
  alpha_017  number ,
  alpha_018  number ,
  alpha_019  number ,
  alpha_020  number ,
  alpha_021  number ,
  alpha_022  number ,
  alpha_023  number ,
  alpha_024  number ,
  alpha_025  number ,
  alpha_026  number ,
  alpha_027  number ,
  alpha_028  number ,
  alpha_029  number ,
  alpha_030  number ,
  alpha_031  number ,
  alpha_032  number ,
  alpha_033  number ,
  alpha_034  number ,
  alpha_035  number ,
  alpha_036  number ,
  alpha_037  number ,
  alpha_038  number ,
  alpha_039  number ,
  alpha_040  number ,
  alpha_041  number ,
  alpha_042  number ,
  alpha_043  number ,
  alpha_044  number ,
  alpha_045  number ,
  alpha_046  number ,
  alpha_047  number ,
  alpha_048  number ,
  alpha_049  number ,
  alpha_050  number ,
  alpha_051  number ,
  alpha_052  number ,
  alpha_053  number ,
  alpha_054  number ,
  alpha_055  number ,
  alpha_056  number ,
  alpha_057  number ,
  alpha_058  number ,
  alpha_059  number ,
  alpha_060  number ,
  alpha_061  number ,
  alpha_062  number ,
  alpha_063  number ,
  alpha_064  number ,
  alpha_065  number ,
  alpha_066  number ,
  alpha_067  number ,
  alpha_068  number ,
  alpha_069  number ,
  alpha_070  number ,
  alpha_071  number ,
  alpha_072  number ,
  alpha_073  number ,
  alpha_074  number ,
  alpha_075  number ,
  alpha_076  number ,
  alpha_077  number ,
  alpha_078  number ,
  alpha_079  number ,
  alpha_080  number ,
  alpha_081  number ,
  alpha_082  number ,
  alpha_083  number ,
  alpha_084  number ,
  alpha_085  number ,
  alpha_086  number ,
  alpha_087  number ,
  alpha_088  number ,
  alpha_089  number ,
  alpha_090  number ,
  alpha_091  number ,
  alpha_092  number ,
  alpha_093  number ,
  alpha_094  number ,
  alpha_095  number ,
  alpha_096  number ,
  alpha_097  number ,
  alpha_098  number ,
  alpha_099  number ,
  alpha_100  number ,
  alpha_101  number   
) ;

create index idx_stock_alpha101 on tb_stock_alpha101(shi_jian) ;
create index idx_stock_alpha101_c on tb_stock_alpha101(code) ;

create index idx_stock_alpha101_1 on tb_stock_alpha101_1(shi_jian) ;
create index idx_stock_alpha101_1c on tb_stock_alpha101_1(code) ;

--create table tb_stock_alpha101_tmp as select * from tb_stock_alpha101_1 ;
--create index idx_stock_alpha101_tmp  on tb_stock_alpha101_tmp(shi_jian) ;
--create index idx_stock_alpha101_tmpc on tb_stock_alpha101_tmp(code) ;

drop table tb_stock_data_market_cap;
create table tb_stock_data_market_cap
(
  code       varchar2(6) not null ,
  shi_jian   varchar2(32) not null ,
  amount     number not null ,
  market_cap number not null 
);

drop index idx_stock_data_market_cap ;
create index idx_stock_data_market_cap on tb_stock_data_market_cap(shi_jian);


drop table tb_stock_bigquant_dict ;
create table tb_stock_bigquant_dict
(
  key        varchar2(128) not null primary key,
  value      varchar2(256) not null ,
  time_stamp date default sysdate not null 
);

insert into tb_stock_bigquant_dict values ('庄华cash_balance','400000');
insert into tb_stock_bigquant_dict values ('龚雯cash_balance','0');
update tb_stock_bigquant_dict set cash_balance = 159632.98 + 179299.95 where key = '庄华cash_balance';

drop table tb_stock_bigquant_position ;
create table tb_stock_bigquant_Position
(
  user_name       varchar2(6)  not null ,
  code            varchar2(32) not null ,
  Volume          number not null ,
  last_price      number not null ,
  time_stamp      date   not null 
) ;
delete tb_stock_bigquant_Position ;
insert into tb_stock_bigquant_Position values ('',0,0,sysdate);

drop table tb_stock_bigquant_rank ;
create table tb_stock_bigquant_rank
(
	shi_jian      date  not null ,
	rank          number not null ,
	code          varchar2(16) not null 
);
create index idx_stock_bigquant_rank on tb_stock_bigquant_rank(shi_jian) ;

drop table tb_stock_cursor_rqalpha ;
create table tb_stock_cursor_rqalpha
(
	cur  number not null 
);

drop table tb_stock_list_rqalpha ;
create table tb_stock_list_rqalpha
(
	id     number not null primary key,
	code   varchar2(16) not null 
);

drop sequence seq_stock_list_rqalpha ;
create sequence seq_stock_list_rqalpha ;

insert into tb_stock_cursor_rqalpha values (1) ;

insert into tb_stock_list_rqalpha 
	select seq_stock_list_rqalpha.nextval , code from tb_stock_list where 
		upper(name) not like '%ST%'
		  and
		code not in 
		(
		    select distinct(code) from tb_stock_data_daily where price = 0 and shi_jian >= to_date('20150101150000','yyyymmddhh24miss')
		)
		  and
		code in 
		(
		    select distinct(code) from tb_stock_data_daily where shi_jian <= to_date('20150101150000','yyyymmddhh24miss')
		)	;
		 		
drop table tb_stock_test_res_rqalpha ;
create table tb_stock_test_res_rqalpha
(
	code            varchar2(16) not null  ,
	total_returns   number not null ,
	last_fromtype   number not null ,
	start_time      varchar2(16) ,
	end_time        varchar2(16) 
);		

drop table tb_stock_test_res_rqalpha ;
create table tb_stock_test_res_rqalpha
(
	code            varchar2(16) not null  ,
	total_returns   number not null ,
	last_fromtype   number not null ,
	start_time      varchar2(16) ,
	end_time        varchar2(16) 
);		

ALTER TABLE tb_stock_test_res_rqalpha
    ADD CONSTRAINT uq_stock_test_res_rqalpha
    UNIQUE(code,start_time,end_time) ;

drop table tb_stock_found_rqalpha ;
create table tb_stock_found_rqalpha
(
  code           varchar2(16)  not null ,
  content        varchar2(256) not null ,
  shi_jian       date          not null ,
  time_stamp     date default sysdate not null 
) ;

drop table tb_stock_stop_loss_rqalpha ;
create table tb_stock_stop_loss_rqalpha
(
	code           varchar2(16) not null ,
	stop_count     number       not null ,
	stop_time      date default sysdate not null 
); 

drop table tb_stock_CDL ;
create table tb_stock_CDL
(
  code       varchar2(32) not null,
  shi_jian   date         not null,
  cdl_type   varchar2(128)not null,
  val        number       not null
);

create table tb_stock_week_time 
(
	Monday  date not null ,
	Friday  date not null 
);

drop   sequence seq_stock_predict ;                                     
create sequence seq_stock_predict ;                                     
                                     
drop table tb_stock_predict ;                                     
create table tb_stock_predict                                     
(                                     
	seq         number       not null ,                                     
	code        varchar2(32) not null ,                                     
	end_time    date         not null ,                                     
	predict     number       not null ,                                     
	real_rate   number                ,
	time_stamp  date default sysdate not null 
) ;

alter table tb_stock_predict add (real_val number ) ;
                                   
alter table tb_stock_predict add constraint                                     
pk_stock_predict                                     
primary key(seq)                                      
/                                     
                                     
drop index idx_stock_predict ;                                     
create index idx_stock_predict on tb_stock_predict(code);                                     

drop table tb_stock_list ;
create table tb_stock_list 
(
   code             varchar2(32) not null ,
   name             varchar2(32) not null ,
   pe               number                ,
   pb               number                ,
   LIQUID_ASSETS    number                ,
   TOTAL_ASSETS     number                ,
   price            number                ,   
   time_stamp       date default sysdate not null   
);

alter table tb_stock_list add constraint
pk_stock_list
primary key(code) 
/

--股票列表
drop table tb_stock_list_ts ;
create table tb_stock_list_ts
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

alter table tb_stock_list_ts add constraint
pk_stock_list_ts
primary key(code) 
/

--股票列表
drop table tb_stock_list_tshis ;
create table tb_stock_list_tshis
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
    time_stamp           date default sysdate not null ,
    shi_jian             varchar2(16)  not null 
);
ALTER TABLE tb_stock_list_tshis
    ADD CONSTRAINT uq_stock_list_tshis
    UNIQUE(code,shi_jian) ;



--股票实时数据
drop table tb_stock_data_realtime ;
create table tb_stock_data_realtime
(
    name               varchar2(64)   not null ,      --名字                     
    code               varchar2(32)   not null ,      --代码                     
    price              number                  ,      --当前价格                 
    price_last_day     number                  ,      --昨收                     
    price_today_open   number                  ,      --今开                                  
    wai_pan            number                  ,      --外盘                     
    nei_pan            number                  ,      --内盘                     
    buy1_price         number                  ,      --买1                      
    buy1_vol           number                  ,      --买1量（手）              
    buy2_price         number                  ,      --买2                      
    buy2_vol           number                  ,      --买2量                    
    buy3_price         number                  ,      --买3                      
    buy3_vol           number                  ,      --买3量                    
    buy4_price         number                  ,      --买4                      
    buy4_vol           number                  ,      --买4量                    
    buy5_price         number                  ,      --买5                      
    buy5_vol           number                  ,      --买5量                    
    sell1_price        number                  ,      --卖1                      
    sell1_vol          number                  ,      --卖1量                    
    sell2_price        number                  ,      --卖2                      
    sell2_vol          number                  ,      --卖2量                    
    sell3_price        number                  ,      --卖3                      
    sell3_vol          number                  ,      --卖3量                    
    sell4_price        number                  ,      --卖4                      
    sell4_vol          number                  ,      --卖4量                    
    sell5_price        number                  ,      --卖5                      
    sell5_vol          number                  ,      --卖5量                    
    zjzbcj             varchar2(512)           ,      --最近逐笔成交             
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
    dietingjia         number                         --跌停价                   
);

--股票日数据
drop table tb_stock_data_daily ;

create table tb_stock_data_daily
(
    name               varchar2(64)   not null ,      --名字                     
    code               varchar2(32)   not null ,      --代码                     
    price              number                  ,      --当前价格                 
    price_last_day     number                  ,      --昨收                     
    price_today_open   number                  ,      --今开                                  
    wai_pan            number                  ,      --外盘                     
    nei_pan            number                  ,      --内盘                     
    buy1_price         number                  ,      --买1                      
    buy1_vol           number                  ,      --买1量（手）              
    buy2_price         number                  ,      --买2                      
    buy2_vol           number                  ,      --买2量                    
    buy3_price         number                  ,      --买3                      
    buy3_vol           number                  ,      --买3量                    
    buy4_price         number                  ,      --买4                      
    buy4_vol           number                  ,      --买4量                    
    buy5_price         number                  ,      --买5                      
    buy5_vol           number                  ,      --买5量                    
    sell1_price        number                  ,      --卖1                      
    sell1_vol          number                  ,      --卖1量                    
    sell2_price        number                  ,      --卖2                      
    sell2_vol          number                  ,      --卖2量                    
    sell3_price        number                  ,      --卖3                      
    sell3_vol          number                  ,      --卖3量                    
    sell4_price        number                  ,      --卖4                      
    sell4_vol          number                  ,      --卖4量                    
    sell5_price        number                  ,      --卖5                      
    sell5_vol          number                  ,      --卖5量                    
    zjzbcj             varchar2(512)           ,      --最近逐笔成交             
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
    MA_DISTANCE_AVG_6  number default 99999999 not null ,
    MA_DISTANCE_AVG_7  number default 99999999 not null ,
    MA_DISTANCE_AVG_8  number default 99999999 not null ,  
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



ALTER TABLE TB_STOCK_DATA_DAILY ADD (DPO_DPO NUMBER) ;
ALTER TABLE TB_STOCK_DATA_DAILY ADD (DPO_6MA NUMBER) ;




--股票周数据
drop table tb_stock_data_weekly ;


create table tb_stock_data_weekly
(
    name               varchar2(64)   not null ,      --名字                     
    code               varchar2(32)   not null ,      --代码                     
    price              number                  ,      --当前价格                 
    price_last_day     number                  ,      --昨收                     
    price_today_open   number                  ,      --今开                                  
    wai_pan            number                  ,      --外盘                     
    nei_pan            number                  ,      --内盘                     
    buy1_price         number                  ,      --买1                      
    buy1_vol           number                  ,      --买1量（手）              
    buy2_price         number                  ,      --买2                      
    buy2_vol           number                  ,      --买2量                    
    buy3_price         number                  ,      --买3                      
    buy3_vol           number                  ,      --买3量                    
    buy4_price         number                  ,      --买4                      
    buy4_vol           number                  ,      --买4量                    
    buy5_price         number                  ,      --买5                      
    buy5_vol           number                  ,      --买5量                    
    sell1_price        number                  ,      --卖1                      
    sell1_vol          number                  ,      --卖1量                    
    sell2_price        number                  ,      --卖2                      
    sell2_vol          number                  ,      --卖2量                    
    sell3_price        number                  ,      --卖3                      
    sell3_vol          number                  ,      --卖3量                    
    sell4_price        number                  ,      --卖4                      
    sell4_vol          number                  ,      --卖4量                    
    sell5_price        number                  ,      --卖5                      
    sell5_vol          number                  ,      --卖5量                    
    zjzbcj             varchar2(512)           ,      --最近逐笔成交             
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
    EmaVal1_SLONG      number                  ,
    EmaVal1_SSHORT     number                  ,
    EmaVal1_LLONG      number                  ,
    EmaVal1_LSHORT     number                  ,
    EmaVal2_SLONG      number                  ,
    EmaVal2_SSHORT     number                  ,
    EmaVal2_LLONG      number                  ,
    EmaVal2_LSHORT     number                               
);

--变为内存表后还是要用索引
drop index idx_stock_data_weekly;
create index idx_stock_data_weekly on tb_stock_data_weekly(code);


--股票月数据
drop table tb_stock_data_monthly ;

create table tb_stock_data_monthly
(
    name               varchar2(64)   not null ,      --名字                     
    code               varchar2(32)   not null ,      --代码                     
    price              number                  ,      --当前价格                 
    price_last_day     number                  ,      --昨收                     
    price_today_open   number                  ,      --今开                                  
    wai_pan            number                  ,      --外盘                     
    nei_pan            number                  ,      --内盘                     
    buy1_price         number                  ,      --买1                      
    buy1_vol           number                  ,      --买1量（手）              
    buy2_price         number                  ,      --买2                      
    buy2_vol           number                  ,      --买2量                    
    buy3_price         number                  ,      --买3                      
    buy3_vol           number                  ,      --买3量                    
    buy4_price         number                  ,      --买4                      
    buy4_vol           number                  ,      --买4量                    
    buy5_price         number                  ,      --买5                      
    buy5_vol           number                  ,      --买5量                    
    sell1_price        number                  ,      --卖1                      
    sell1_vol          number                  ,      --卖1量                    
    sell2_price        number                  ,      --卖2                      
    sell2_vol          number                  ,      --卖2量                    
    sell3_price        number                  ,      --卖3                      
    sell3_vol          number                  ,      --卖3量                    
    sell4_price        number                  ,      --卖4                      
    sell4_vol          number                  ,      --卖4量                    
    sell5_price        number                  ,      --卖5                      
    sell5_vol          number                  ,      --卖5量                    
    zjzbcj             varchar2(512)           ,      --最近逐笔成交             
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
    EmaVal1_SLONG      number                  ,
    EmaVal1_SSHORT     number                  ,
    EmaVal1_LLONG      number                  ,
    EmaVal1_LSHORT     number                  ,
    EmaVal2_SLONG      number                  ,
    EmaVal2_SSHORT     number                  ,
    EmaVal2_LLONG      number                  ,
    EmaVal2_LSHORT     number                   
);

--变为内存表后还是要用索引
drop index idx_stock_data_monthly;
create index idx_stock_data_monthly on tb_stock_data_monthly(code);


--股票季度数据
drop table tb_stock_data_Quarterly ;

create table tb_stock_data_Quarterly
(
    name               varchar2(64)   not null ,      --名字                     
    code               varchar2(32)   not null ,      --代码                     
    price              number                  ,      --当前价格                 
    price_last_day     number                  ,      --昨收                     
    price_today_open   number                  ,      --今开                                  
    wai_pan            number                  ,      --外盘                     
    nei_pan            number                  ,      --内盘                     
    buy1_price         number                  ,      --买1                      
    buy1_vol           number                  ,      --买1量（手）              
    buy2_price         number                  ,      --买2                      
    buy2_vol           number                  ,      --买2量                    
    buy3_price         number                  ,      --买3                      
    buy3_vol           number                  ,      --买3量                    
    buy4_price         number                  ,      --买4                      
    buy4_vol           number                  ,      --买4量                    
    buy5_price         number                  ,      --买5                      
    buy5_vol           number                  ,      --买5量                    
    sell1_price        number                  ,      --卖1                      
    sell1_vol          number                  ,      --卖1量                    
    sell2_price        number                  ,      --卖2                      
    sell2_vol          number                  ,      --卖2量                    
    sell3_price        number                  ,      --卖3                      
    sell3_vol          number                  ,      --卖3量                    
    sell4_price        number                  ,      --卖4                      
    sell4_vol          number                  ,      --卖4量                    
    sell5_price        number                  ,      --卖5                      
    sell5_vol          number                  ,      --卖5量                    
    zjzbcj             varchar2(512)           ,      --最近逐笔成交             
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
    EmaVal1_SLONG      number                  ,
    EmaVal1_SSHORT     number                  ,
    EmaVal1_LLONG      number                  ,
    EmaVal1_LSHORT     number                  ,
    EmaVal2_SLONG      number                  ,
    EmaVal2_SSHORT     number                  ,
    EmaVal2_LLONG      number                  ,
    EmaVal2_LSHORT     number                            
);

--变为内存表后还是要用索引
drop index idx_stock_data_Quarterly;
create index idx_stock_data_Quarterly on tb_stock_data_Quarterly(code);


--股票半年数据
drop table tb_stock_data_halfYearly ;

create table tb_stock_data_halfYearly
(
    name               varchar2(64)   not null ,      --名字                     
    code               varchar2(32)   not null ,      --代码                     
    price              number                  ,      --当前价格                 
    price_last_day     number                  ,      --昨收                     
    price_today_open   number                  ,      --今开                                  
    wai_pan            number                  ,      --外盘                     
    nei_pan            number                  ,      --内盘                     
    buy1_price         number                  ,      --买1                      
    buy1_vol           number                  ,      --买1量（手）              
    buy2_price         number                  ,      --买2                      
    buy2_vol           number                  ,      --买2量                    
    buy3_price         number                  ,      --买3                      
    buy3_vol           number                  ,      --买3量                    
    buy4_price         number                  ,      --买4                      
    buy4_vol           number                  ,      --买4量                    
    buy5_price         number                  ,      --买5                      
    buy5_vol           number                  ,      --买5量                    
    sell1_price        number                  ,      --卖1                      
    sell1_vol          number                  ,      --卖1量                    
    sell2_price        number                  ,      --卖2                      
    sell2_vol          number                  ,      --卖2量                    
    sell3_price        number                  ,      --卖3                      
    sell3_vol          number                  ,      --卖3量                    
    sell4_price        number                  ,      --卖4                      
    sell4_vol          number                  ,      --卖4量                    
    sell5_price        number                  ,      --卖5                      
    sell5_vol          number                  ,      --卖5量                    
    zjzbcj             varchar2(512)           ,      --最近逐笔成交             
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
    EmaVal1_SLONG      number                  ,
    EmaVal1_SSHORT     number                  ,
    EmaVal1_LLONG      number                  ,
    EmaVal1_LSHORT     number                  ,
    EmaVal2_SLONG      number                  ,
    EmaVal2_SSHORT     number                  ,
    EmaVal2_LLONG      number                  ,
    EmaVal2_LSHORT     number                      
);

--变为内存表后还是要用索引
drop index idx_stock_data_halfYearly;
create index idx_stock_data_halfYearly on tb_stock_data_halfYearly(code);


--股票年数据
drop table tb_stock_data_Yearly ;

create table tb_stock_data_Yearly
(
    name               varchar2(64)   not null ,      --名字                     
    code               varchar2(32)   not null ,      --代码                     
    price              number                  ,      --当前价格                 
    price_last_day     number                  ,      --昨收                     
    price_today_open   number                  ,      --今开                                  
    wai_pan            number                  ,      --外盘                     
    nei_pan            number                  ,      --内盘                     
    buy1_price         number                  ,      --买1                      
    buy1_vol           number                  ,      --买1量（手）              
    buy2_price         number                  ,      --买2                      
    buy2_vol           number                  ,      --买2量                    
    buy3_price         number                  ,      --买3                      
    buy3_vol           number                  ,      --买3量                    
    buy4_price         number                  ,      --买4                      
    buy4_vol           number                  ,      --买4量                    
    buy5_price         number                  ,      --买5                      
    buy5_vol           number                  ,      --买5量                    
    sell1_price        number                  ,      --卖1                      
    sell1_vol          number                  ,      --卖1量                    
    sell2_price        number                  ,      --卖2                      
    sell2_vol          number                  ,      --卖2量                    
    sell3_price        number                  ,      --卖3                      
    sell3_vol          number                  ,      --卖3量                    
    sell4_price        number                  ,      --卖4                      
    sell4_vol          number                  ,      --卖4量                    
    sell5_price        number                  ,      --卖5                      
    sell5_vol          number                  ,      --卖5量                    
    zjzbcj             varchar2(512)           ,      --最近逐笔成交             
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
    EmaVal1_SLONG      number                  ,
    EmaVal1_SSHORT     number                  ,
    EmaVal1_LLONG      number                  ,
    EmaVal1_LSHORT     number                  ,
    EmaVal2_SLONG      number                  ,
    EmaVal2_SSHORT     number                  ,
    EmaVal2_LLONG      number                  ,
    EmaVal2_LSHORT     number                         
);

--变为内存表后还是要用索引
drop index idx_stock_data_Yearly;
create index idx_stock_data_Yearly on tb_stock_data_Yearly(code);

    
drop table tb_stock_found ;
create table tb_stock_found
(
  seq                  number         not null  primary key,
  type                 varchar2(32)   not null ,
  shi_jian             date           not null ,
  code                 varchar2(32)   not null ,
  name                 varchar2(64)   not null ,
  reason               varchar2(1024) not null ,
  time_stamp           date default sysdate not null 
);

drop   sequence seq_stock_found ;
create sequence seq_stock_found ;

drop table tb_stock_job_done ;
create table tb_stock_job_done
(
  what_done  varchar2(64) not null ,
  time_stamp date default sysdate not null 
);

--找3倍以内涨幅就破板的新股的结果，每天上午9点找一次，找之前清表
create table tb_stock_new_stock
(
    code     varchar2(32) ,
    name     varchar2(32) ,
    shi_jian date 
);




connect sys/t2h4o6m8@myoracle as sysdba ;
alter system set inmemory_size=3000M scope=spfile; 
alter table  c##stock.tb_stock_data_daily_taobao inmemory;
alter table  c##stock.tb_stock_data_daily_wind   inmemory;
alter table  c##stock.tb_stock_data_daily        inmemory;
alter table  c##stock.tb_stock_data_realtime     inmemory;
alter table  c##stock.tb_stock_list              inmemory;
alter table  c##stock.tb_stock_list_ts           inmemory;

alter table  c##stock.tb_stock_data_weekly     inmemory;
alter table  c##stock.tb_stock_data_monthly    inmemory; 
alter table  c##stock.tb_stock_data_Quarterly  inmemory; 
alter table  c##stock.tb_stock_data_halfYearly inmemory; 
alter table  c##stock.tb_stock_data_Yearly     inmemory; 
alter table  c##stock.tb_stock_found           inmemory; 
connect c##stock/didierg160@myoracle ;
                                               
--pk_stock_list
alter index c##stock.idx_stock_data_Daily         inmemory;
alter index c##stock.idx_stock_data_weekly        inmemory;
alter index c##stock.idx_stock_data_monthly       inmemory;      
alter index c##stock.idx_stock_data_Quarterly     inmemory; 
alter index c##stock.idx_stock_data_halfYearly    inmemory; 
alter index c##stock.idx_stock_data_Yearly        inmemory;
