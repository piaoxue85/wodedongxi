connect c##stock/didierg160@myoracle ;
--��Ȩ��Ѻ��ϸ����
drop table tb_stock_pledged_detail;
create table tb_stock_pledged_detail
(
   code           varchar2(16)  not null ,
   name           varchar2(16)  not null ,
   ann_date       varchar2(16)           ,          --��������
   pledgor        varchar2(256)          ,          --������
   pledgee        varchar2(256)          ,          --��Ȩ��
   volume         number                 ,          --��Ѻ����
   from_date      varchar2(16)           ,          --��Ѻ����
   end_date       varchar2(16)           ,          --�������
   time_stamp     date not null  
);

--��Ȩ��Ѻͳ������
drop table tb_stock_pledged ;
create table tb_stock_pledged
(
  code             varchar2(16) not null ,   
  name             varchar2(16) not null ,
  deals            number                ,    --��Ѻ����
  unrest_pledged   number                ,    --�����۹���Ѻ��������
  rest_pledged     number                ,    --  ���۹���Ѻ��������
  totals           number                ,    --�ܹɱ�
  p_ratio          number                ,    --��Ѻ����
  time_stamp       date not null 
);


drop table tb_stock_data_daily_taobao ;
create table tb_stock_data_daily_taobao
(
  code                     varchar2(16) not null ,      --��Ʊ����     
  name                     varchar2(16) not null ,      --��Ʊ����     
  shi_jian                 varchar2(16) not null ,      --��������     
  Sina_industry            varchar2(64)          ,      --������ҵ     
  Sina_concept             varchar2(512)         ,      --���˸���     
  Sina_area                varchar2(64)          ,      --���˵���     
  open                     number                ,      --���̼�       
  max                      number                ,      --��߼�       
  min                      number                ,      --��ͼ�       
  close                    number                ,      --���̼�       
  adj_after                number                ,      --��Ȩ��     
  adj_before               number                ,      --ǰ��Ȩ��     
  Change                   number                ,      --�ǵ���       
  vol                      number                ,      --�ɽ���       
  amout                    number                ,      --�ɽ���       
  turnover_rate            number                ,      --������       
  tradable_market_cap      number                ,      --��ͨ��ֵ     
  market_cap               number                ,      --����ֵ       
  is_up_Limit              number                ,      --�Ƿ���ͣ     
  is_down_Limit            number                ,      --�Ƿ��ͣ     
  pe_ttm                   number                ,      --��ӯ��TTM    
  PS_ttm                   number                ,      --������TTM    
  PCF_ttm                  number                ,      --������TTM    
  pb                       number                ,      --�о���       
  MA_5                     number                ,      --MA_5         
  MA_10                    number                ,      --MA_10        
  MA_20                    number                ,      --MA_20        
  MA_30                    number                ,      --MA_30        
  MA_60                    number                ,      --MA_60        
  MA_up_down_corss         varchar2(512)         ,      --MA�������   
  MACD_DIF                 number                ,      --MACD_DIF     
  MACD_DEA                 number                ,      --MACD_DEA     
  MACD_MACD                number                ,      --MACD_MACD    
  MACD_up_down_corss       varchar2(512)         ,      --MACD_�������
  KDJ_K                    number                ,      --KDJ_K        
  KDJ_D                    number                ,      --KDJ_D        
  KDJ_J                    number                ,      --KDJ_J        
  KDJ_up_down_corss        varchar2(512)         ,      --KDJ_������� 
  boll_mid                 number                ,      --�������й�   
  boll_up                  number                ,      --�������Ϲ�   
  boll_low                 number                ,      --�������¹�   
  psy                      number                ,      --psy          
  psyma                    number                ,      --psyma        
  rsi1                     number                ,      --rsi1         
  rsi2                     number                ,      --rsi2         
  rsi3                     number                ,      --rsi3         
  Amplitude                number                ,      --���         
  Volume_Ratio             number                       --����         
);

--��Ϊ�ڴ�����Ҫ������
drop index idx_stock_data_daily_taobao ;
create index idx_stock_data_daily_taobao on tb_stock_data_daily_taobao(code);
--��Ϊ�ڴ�����Ҫ������
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
   pre_close                   number                  ,--ǰ���̼�
   open                        number                  ,--
   high                        number                  ,--
   low                         number                  ,--
   close                       number                  ,--
   volume                      number                  ,--
   amt                         number                  ,--�ɽ���
   dealnum                     number                  ,--�ɽ�����
   chg                         number                  ,--�ǵ�
   pct_chg                     number                  ,--�ǵ���
   swing                       number                  ,--���
   vwap                        number                  ,--����
   --adjfactor                   number                  ,--��Ȩ����
   rel_ipo_chg                 number                  ,--��Է��м��ǵ�
   rel_ipo_pct_chg             number                  ,--��Է��м��ǵ���
   total_shares                number                  ,--�ܹɱ�
   free_float_shares           number                  ,--������ͨ�ɱ�
   mf_amt                      number                  ,--�������ʽ�
   mf_vol                      number                  ,--��������
   mf_amt_ratio                number                  ,--���������
   mf_vol_ratio                number                  ,--�ʽ�����ռ��
   mf_amt_close                number                  ,--β�̾������ʽ�
   mf_amt_open                 number                  ,--���̾������ʽ�
   pe_ttm                      number                  ,--��ӯ�� ttm
   val_pe_deducted_ttm         number                  ,--��ӯ�� ttm���۳��Ǿ���������
   pe_lyr                      number                  ,--��ӯ�� lyr
   pb_lf                       number                  ,--�о��� pb lf
   pb_mrq                      number                  ,--�о��� pb mrq
   ps_ttm                      number                  ,--������ ps ttm
   ps_lyr                      number                  ,--������ ps lyr
   pcf_ocf_ttm                 number                  ,--������pcf ��Ӫ�ֽ���ttm
   pcf_ncf_ttm                 number                  ,--������pcf �ֽ�����ttm
   pcf_ocflyr                  number                  ,--������pcf ��Ӫ�ֽ���lyr
   pcf_nflyr                   number                  ,--������pcf �ֽ�����lyr
   pe_est                      number                  ,--Ԥ��pe 
   estpe_FY1                   number                  ,--Ԥ��pe fy1
   estpe_FY2                   number                  ,--Ԥ��pe fy2
   estpe_FY3                   number                  ,--Ԥ��pe fy3
   pe_est_last                 number                  ,--Ԥ��pe ����Ԥ��
   pe_est_ftm                  number                  ,--Ԥ��pe δ��12����
   est_peg                     number                  ,--Ԥ��peg 
   estpeg_FY1                  number                  ,--Ԥ��peg fy1       
   estpeg_FY2                  number                  ,--Ԥ��peg fy2       
   estpeg_FTM                  number                  ,--Ԥ��peg δ��12����
   estpb                       number                  ,--Ԥ��pb
   estpb_FY1                   number                  ,--Ԥ��pb FY1
   estpb_FY2                   number                  ,--Ԥ��pb FY2
   estpb_FY3                   number                  ,--Ԥ��pb FY3
   ev1                         number                  ,--��ҵ��ֵ �������ʽ�
   ev2                         number                  ,--��ҵ��ֵ �޳������ʽ�
   ev2_to_ebitda               number                  ,--��ҵ���� ev2/ebitda
   history_low                 number                  ,--���ڴ���ʷ�µ�
   stage_high                  number                  ,--���ڴ��׶��¸�
   history_high                number                  ,--���ڴ���ʷ�¸�
   stage_low                   number                  ,--���ڴ���ʷ�µ�
   up_days                     number                  ,--��������
   down_days                   number                  ,--��������
   breakout_ma                 number                  ,--������Чͻ�ƾ���
   breakdown_ma                number                  ,--������Чͻ�ƾ���
   bull_bear_ma                number                  ,--���߶�ͷ���п��ǿ���
   holder_num                  number                  ,--�ɶ�����
   holder_avgnum               number                  ,--�����ֹ�����
   holder_totalbyinst          number                  ,--�����ֹ������ϼ�
   holder_pctbyinst            number                  ,--�����ֹɱ����ϼ�
   mkt_cap_ashare2             number                  ,--����ֵ   �����۹�
   mkt_cap_ashare              number                   --��ͨ��ֵ �������۹�
) ;
--��Ϊ�ڴ�����Ҫ������
drop index idx_stock_data_daily_wind ;
create index idx_stock_data_daily_wind on tb_stock_data_daily_wind(code);
--��Ϊ�ڴ�����Ҫ������
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

insert into tb_stock_bigquant_dict values ('ׯ��cash_balance','400000');
insert into tb_stock_bigquant_dict values ('����cash_balance','0');
update tb_stock_bigquant_dict set cash_balance = 159632.98 + 179299.95 where key = 'ׯ��cash_balance';

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

--��Ʊ�б�
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

--��Ʊ�б�
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



--��Ʊʵʱ����
drop table tb_stock_data_realtime ;
create table tb_stock_data_realtime
(
    name               varchar2(64)   not null ,      --����                     
    code               varchar2(32)   not null ,      --����                     
    price              number                  ,      --��ǰ�۸�                 
    price_last_day     number                  ,      --����                     
    price_today_open   number                  ,      --��                                  
    wai_pan            number                  ,      --����                     
    nei_pan            number                  ,      --����                     
    buy1_price         number                  ,      --��1                      
    buy1_vol           number                  ,      --��1�����֣�              
    buy2_price         number                  ,      --��2                      
    buy2_vol           number                  ,      --��2��                    
    buy3_price         number                  ,      --��3                      
    buy3_vol           number                  ,      --��3��                    
    buy4_price         number                  ,      --��4                      
    buy4_vol           number                  ,      --��4��                    
    buy5_price         number                  ,      --��5                      
    buy5_vol           number                  ,      --��5��                    
    sell1_price        number                  ,      --��1                      
    sell1_vol          number                  ,      --��1��                    
    sell2_price        number                  ,      --��2                      
    sell2_vol          number                  ,      --��2��                    
    sell3_price        number                  ,      --��3                      
    sell3_vol          number                  ,      --��3��                    
    sell4_price        number                  ,      --��4                      
    sell4_vol          number                  ,      --��4��                    
    sell5_price        number                  ,      --��5                      
    sell5_vol          number                  ,      --��5��                    
    zjzbcj             varchar2(512)           ,      --�����ʳɽ�             
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
    dietingjia         number                         --��ͣ��                   
);

--��Ʊ������
drop table tb_stock_data_daily ;

create table tb_stock_data_daily
(
    name               varchar2(64)   not null ,      --����                     
    code               varchar2(32)   not null ,      --����                     
    price              number                  ,      --��ǰ�۸�                 
    price_last_day     number                  ,      --����                     
    price_today_open   number                  ,      --��                                  
    wai_pan            number                  ,      --����                     
    nei_pan            number                  ,      --����                     
    buy1_price         number                  ,      --��1                      
    buy1_vol           number                  ,      --��1�����֣�              
    buy2_price         number                  ,      --��2                      
    buy2_vol           number                  ,      --��2��                    
    buy3_price         number                  ,      --��3                      
    buy3_vol           number                  ,      --��3��                    
    buy4_price         number                  ,      --��4                      
    buy4_vol           number                  ,      --��4��                    
    buy5_price         number                  ,      --��5                      
    buy5_vol           number                  ,      --��5��                    
    sell1_price        number                  ,      --��1                      
    sell1_vol          number                  ,      --��1��                    
    sell2_price        number                  ,      --��2                      
    sell2_vol          number                  ,      --��2��                    
    sell3_price        number                  ,      --��3                      
    sell3_vol          number                  ,      --��3��                    
    sell4_price        number                  ,      --��4                      
    sell4_vol          number                  ,      --��4��                    
    sell5_price        number                  ,      --��5                      
    sell5_vol          number                  ,      --��5��                    
    zjzbcj             varchar2(512)           ,      --�����ʳɽ�             
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

--��Ϊ�ڴ�����Ҫ������
drop index idx_stock_data_Daily ;
create index idx_stock_data_Daily on tb_stock_data_Daily(code);



ALTER TABLE TB_STOCK_DATA_DAILY ADD (DPO_DPO NUMBER) ;
ALTER TABLE TB_STOCK_DATA_DAILY ADD (DPO_6MA NUMBER) ;




--��Ʊ������
drop table tb_stock_data_weekly ;


create table tb_stock_data_weekly
(
    name               varchar2(64)   not null ,      --����                     
    code               varchar2(32)   not null ,      --����                     
    price              number                  ,      --��ǰ�۸�                 
    price_last_day     number                  ,      --����                     
    price_today_open   number                  ,      --��                                  
    wai_pan            number                  ,      --����                     
    nei_pan            number                  ,      --����                     
    buy1_price         number                  ,      --��1                      
    buy1_vol           number                  ,      --��1�����֣�              
    buy2_price         number                  ,      --��2                      
    buy2_vol           number                  ,      --��2��                    
    buy3_price         number                  ,      --��3                      
    buy3_vol           number                  ,      --��3��                    
    buy4_price         number                  ,      --��4                      
    buy4_vol           number                  ,      --��4��                    
    buy5_price         number                  ,      --��5                      
    buy5_vol           number                  ,      --��5��                    
    sell1_price        number                  ,      --��1                      
    sell1_vol          number                  ,      --��1��                    
    sell2_price        number                  ,      --��2                      
    sell2_vol          number                  ,      --��2��                    
    sell3_price        number                  ,      --��3                      
    sell3_vol          number                  ,      --��3��                    
    sell4_price        number                  ,      --��4                      
    sell4_vol          number                  ,      --��4��                    
    sell5_price        number                  ,      --��5                      
    sell5_vol          number                  ,      --��5��                    
    zjzbcj             varchar2(512)           ,      --�����ʳɽ�             
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
    EmaVal1_SLONG      number                  ,
    EmaVal1_SSHORT     number                  ,
    EmaVal1_LLONG      number                  ,
    EmaVal1_LSHORT     number                  ,
    EmaVal2_SLONG      number                  ,
    EmaVal2_SSHORT     number                  ,
    EmaVal2_LLONG      number                  ,
    EmaVal2_LSHORT     number                               
);

--��Ϊ�ڴ�����Ҫ������
drop index idx_stock_data_weekly;
create index idx_stock_data_weekly on tb_stock_data_weekly(code);


--��Ʊ������
drop table tb_stock_data_monthly ;

create table tb_stock_data_monthly
(
    name               varchar2(64)   not null ,      --����                     
    code               varchar2(32)   not null ,      --����                     
    price              number                  ,      --��ǰ�۸�                 
    price_last_day     number                  ,      --����                     
    price_today_open   number                  ,      --��                                  
    wai_pan            number                  ,      --����                     
    nei_pan            number                  ,      --����                     
    buy1_price         number                  ,      --��1                      
    buy1_vol           number                  ,      --��1�����֣�              
    buy2_price         number                  ,      --��2                      
    buy2_vol           number                  ,      --��2��                    
    buy3_price         number                  ,      --��3                      
    buy3_vol           number                  ,      --��3��                    
    buy4_price         number                  ,      --��4                      
    buy4_vol           number                  ,      --��4��                    
    buy5_price         number                  ,      --��5                      
    buy5_vol           number                  ,      --��5��                    
    sell1_price        number                  ,      --��1                      
    sell1_vol          number                  ,      --��1��                    
    sell2_price        number                  ,      --��2                      
    sell2_vol          number                  ,      --��2��                    
    sell3_price        number                  ,      --��3                      
    sell3_vol          number                  ,      --��3��                    
    sell4_price        number                  ,      --��4                      
    sell4_vol          number                  ,      --��4��                    
    sell5_price        number                  ,      --��5                      
    sell5_vol          number                  ,      --��5��                    
    zjzbcj             varchar2(512)           ,      --�����ʳɽ�             
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
    EmaVal1_SLONG      number                  ,
    EmaVal1_SSHORT     number                  ,
    EmaVal1_LLONG      number                  ,
    EmaVal1_LSHORT     number                  ,
    EmaVal2_SLONG      number                  ,
    EmaVal2_SSHORT     number                  ,
    EmaVal2_LLONG      number                  ,
    EmaVal2_LSHORT     number                   
);

--��Ϊ�ڴ�����Ҫ������
drop index idx_stock_data_monthly;
create index idx_stock_data_monthly on tb_stock_data_monthly(code);


--��Ʊ��������
drop table tb_stock_data_Quarterly ;

create table tb_stock_data_Quarterly
(
    name               varchar2(64)   not null ,      --����                     
    code               varchar2(32)   not null ,      --����                     
    price              number                  ,      --��ǰ�۸�                 
    price_last_day     number                  ,      --����                     
    price_today_open   number                  ,      --��                                  
    wai_pan            number                  ,      --����                     
    nei_pan            number                  ,      --����                     
    buy1_price         number                  ,      --��1                      
    buy1_vol           number                  ,      --��1�����֣�              
    buy2_price         number                  ,      --��2                      
    buy2_vol           number                  ,      --��2��                    
    buy3_price         number                  ,      --��3                      
    buy3_vol           number                  ,      --��3��                    
    buy4_price         number                  ,      --��4                      
    buy4_vol           number                  ,      --��4��                    
    buy5_price         number                  ,      --��5                      
    buy5_vol           number                  ,      --��5��                    
    sell1_price        number                  ,      --��1                      
    sell1_vol          number                  ,      --��1��                    
    sell2_price        number                  ,      --��2                      
    sell2_vol          number                  ,      --��2��                    
    sell3_price        number                  ,      --��3                      
    sell3_vol          number                  ,      --��3��                    
    sell4_price        number                  ,      --��4                      
    sell4_vol          number                  ,      --��4��                    
    sell5_price        number                  ,      --��5                      
    sell5_vol          number                  ,      --��5��                    
    zjzbcj             varchar2(512)           ,      --�����ʳɽ�             
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
    EmaVal1_SLONG      number                  ,
    EmaVal1_SSHORT     number                  ,
    EmaVal1_LLONG      number                  ,
    EmaVal1_LSHORT     number                  ,
    EmaVal2_SLONG      number                  ,
    EmaVal2_SSHORT     number                  ,
    EmaVal2_LLONG      number                  ,
    EmaVal2_LSHORT     number                            
);

--��Ϊ�ڴ�����Ҫ������
drop index idx_stock_data_Quarterly;
create index idx_stock_data_Quarterly on tb_stock_data_Quarterly(code);


--��Ʊ��������
drop table tb_stock_data_halfYearly ;

create table tb_stock_data_halfYearly
(
    name               varchar2(64)   not null ,      --����                     
    code               varchar2(32)   not null ,      --����                     
    price              number                  ,      --��ǰ�۸�                 
    price_last_day     number                  ,      --����                     
    price_today_open   number                  ,      --��                                  
    wai_pan            number                  ,      --����                     
    nei_pan            number                  ,      --����                     
    buy1_price         number                  ,      --��1                      
    buy1_vol           number                  ,      --��1�����֣�              
    buy2_price         number                  ,      --��2                      
    buy2_vol           number                  ,      --��2��                    
    buy3_price         number                  ,      --��3                      
    buy3_vol           number                  ,      --��3��                    
    buy4_price         number                  ,      --��4                      
    buy4_vol           number                  ,      --��4��                    
    buy5_price         number                  ,      --��5                      
    buy5_vol           number                  ,      --��5��                    
    sell1_price        number                  ,      --��1                      
    sell1_vol          number                  ,      --��1��                    
    sell2_price        number                  ,      --��2                      
    sell2_vol          number                  ,      --��2��                    
    sell3_price        number                  ,      --��3                      
    sell3_vol          number                  ,      --��3��                    
    sell4_price        number                  ,      --��4                      
    sell4_vol          number                  ,      --��4��                    
    sell5_price        number                  ,      --��5                      
    sell5_vol          number                  ,      --��5��                    
    zjzbcj             varchar2(512)           ,      --�����ʳɽ�             
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
    EmaVal1_SLONG      number                  ,
    EmaVal1_SSHORT     number                  ,
    EmaVal1_LLONG      number                  ,
    EmaVal1_LSHORT     number                  ,
    EmaVal2_SLONG      number                  ,
    EmaVal2_SSHORT     number                  ,
    EmaVal2_LLONG      number                  ,
    EmaVal2_LSHORT     number                      
);

--��Ϊ�ڴ�����Ҫ������
drop index idx_stock_data_halfYearly;
create index idx_stock_data_halfYearly on tb_stock_data_halfYearly(code);


--��Ʊ������
drop table tb_stock_data_Yearly ;

create table tb_stock_data_Yearly
(
    name               varchar2(64)   not null ,      --����                     
    code               varchar2(32)   not null ,      --����                     
    price              number                  ,      --��ǰ�۸�                 
    price_last_day     number                  ,      --����                     
    price_today_open   number                  ,      --��                                  
    wai_pan            number                  ,      --����                     
    nei_pan            number                  ,      --����                     
    buy1_price         number                  ,      --��1                      
    buy1_vol           number                  ,      --��1�����֣�              
    buy2_price         number                  ,      --��2                      
    buy2_vol           number                  ,      --��2��                    
    buy3_price         number                  ,      --��3                      
    buy3_vol           number                  ,      --��3��                    
    buy4_price         number                  ,      --��4                      
    buy4_vol           number                  ,      --��4��                    
    buy5_price         number                  ,      --��5                      
    buy5_vol           number                  ,      --��5��                    
    sell1_price        number                  ,      --��1                      
    sell1_vol          number                  ,      --��1��                    
    sell2_price        number                  ,      --��2                      
    sell2_vol          number                  ,      --��2��                    
    sell3_price        number                  ,      --��3                      
    sell3_vol          number                  ,      --��3��                    
    sell4_price        number                  ,      --��4                      
    sell4_vol          number                  ,      --��4��                    
    sell5_price        number                  ,      --��5                      
    sell5_vol          number                  ,      --��5��                    
    zjzbcj             varchar2(512)           ,      --�����ʳɽ�             
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
    EmaVal1_SLONG      number                  ,
    EmaVal1_SSHORT     number                  ,
    EmaVal1_LLONG      number                  ,
    EmaVal1_LSHORT     number                  ,
    EmaVal2_SLONG      number                  ,
    EmaVal2_SSHORT     number                  ,
    EmaVal2_LLONG      number                  ,
    EmaVal2_LSHORT     number                         
);

--��Ϊ�ڴ�����Ҫ������
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

--��3�������Ƿ����ư���¹ɵĽ����ÿ������9����һ�Σ���֮ǰ���
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
