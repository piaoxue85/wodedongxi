connect c##stock/didierg160@myoracle ;

select to_char(sysdate,'yyyy-mm-dd hh24:mi:ss') from dual;
exec proc_get_all ;
select to_char(sysdate,'yyyy-mm-dd hh24:mi:ss') from dual;

select to_char(sysdate,'hh24:mi:ss') ,count(1) from tb_stock_data_daily ;

select code,name from tb_stock_data_daily where 
  shi_jian = to_date('20150828150000','yyyymmddhh24miss')
    and
  xstd_lshort <= xstd_sshort ;



set autotrace on;
set autotrace off;

truncate table tb_stock_list ;

truncate table tb_stock_data_daily ;

connect sys/t2h4o6m8@myoracle as sysdba ;
alter system set inmemory_size=3000M scope=spfile; 
alter table c##stock.tb_stock_data_daily inmemory;

http://download.oracle.com/otn/java/sqldeveloper/sqldeveloper-4.1.1.19.59-x64.zip?AuthParam=1440486206_d27ab5ebb8c8b4b2d1ac3d1b0c682258


SQL> CREATE PFILE FROM SPFILE;
MANUALLY EDIT PFILE & CORRECT MEMORY_TARGET VALUE
SQL> CREATE SPFILE FROM PFILE;
SQL> STARTUP 

spfileMyOracle.ora

connect c##stock/didierg160@myoracle ;
select (3652262-1659662)/((to_date('2015010113:03:28','yyyymmddhh24:mi:ss')-to_date('2015010111:58:03','yyyymmddhh24:mi:ss'))*3600*24) from dual ;

declare
  cursor cur is
    select code , shi_jian , count(1) c from tb_stock_data_daily 
      group by code , shi_jian 
      having count(1) > 1 ;
  
  rt cur%rowtype ;
  
begin
  open cur ;
  loop 
    fetch cur into rt;  
    exit when cur%NOTFOUND;
    
    delete tb_stock_data_daily where 
      code = rt.code 
        and 
      shi_jian = rt.shi_jian 
        and 
      rownum<rt.c;
  end loop ;
  commit;
end; 

declare
  cursor cur is
    select code , shi_jian , count(1) c from tb_stock_data_HalfYearly 
      group by code , shi_jian 
      having count(1) > 1 ;
  
  rt cur%rowtype ;
  
begin
  open cur ;
  loop 
    fetch cur into rt;  
    exit when cur%NOTFOUND;
    
    delete tb_stock_data_HalfYearly where 
      code = rt.code 
        and 
      shi_jian = rt.shi_jian 
        and 
      rownum<rt.c;
  end loop ;
  commit;
end; 
  



select * from
(
  select to_char(to_date('20080928000000','yyyymmddhh24miss') + 7,'yyyymmddhh24miss') next_cursor,          
         to_char(max(shi_jian),'yyyymmddhh24miss') last_day  ,          
         sum(vol)                                    vol       ,          
         sum(amount)                                 amount    ,          
         max(max_price)                              max_price ,          
         min(min_price)                              min_price     
  from tb_stock_data_Daily where                                     
    code = '002202'       
      and       
    trunc(shi_jian,'d') = to_date('20080928000000','yyyymmddhh24miss')
)a, 
(     
  select price_today_open from tb_stock_data_Daily where     
    code = '002202'      
      and     
    shi_jian = (
                  select min(shi_jian)  from tb_stock_data_Daily where                   
                    code = '002202'                    
                      and                   
                    trunc(shi_jian,'d') = to_date('20080928000000','yyyymmddhh24miss')                
               ) 
)b,
(    
  select price from tb_stock_data_Daily where     
    code = '002202'      
      and     
    shi_jian = (                   
                 select max(shi_jian) from tb_stock_data_Daily where                     
                   code = '002202'                      
                     and                     
                   trunc(shi_jian,'d') = to_date('20080928000000','yyyymmddhh24miss')                
               ) 
)c 



declare
  cursor cur is 
    select code , name from tb_stock_list ;
  
  rtcur cur%rowtype ;
begin
  
  for rt in cur loop        
    update tb_stock_data_Daily      set name = rt.name where code = rt.code ;    
    update tb_stock_data_weekly     set name = rt.name where code = rt.code ;
    update tb_stock_data_monthly    set name = rt.name where code = rt.code ;
    update tb_stock_data_Quarterly  set name = rt.name where code = rt.code ;
    update tb_stock_data_halfYearly set name = rt.name where code = rt.code ;
    update tb_stock_data_Yearly     set name = rt.name where code = rt.code ;
  end loop ;  
  
  commit;
end;     


select code,count(1) from 
(
    select code,name from tb_stock_data_Daily group by code,name
)
group by code 
having count(1)>1 ;

select code,count(1) from 
(
    select code,name from tb_stock_data_weekly group by code,name
)
group by code 
having count(1)>1 ;

select code,count(1) from 
(
    select code,name from tb_stock_data_monthly group by code,name
)
group by code 
having count(1)>1 ;

select code,count(1) from 
(
    select code,name from tb_stock_data_Quarterly group by code,name
)
group by code 
having count(1)>1 ;

select code,count(1) from 
(
    select code,name from tb_stock_data_halfYearly group by code,name
)
group by code 
having count(1)>1 ;

select code,count(1) from 
(
    select code,name from tb_stock_data_Yearly group by code,name
)
group by code 
having count(1)>1 ;



delete tb_stock_data_Daily      where amount = 0; 

delete tb_stock_data_weekly     where code in (select distinct(code) from  tb_stock_data_weekly     where amount = 0 );   
delete tb_stock_data_monthly    where code in (select distinct(code) from  tb_stock_data_monthly    where amount = 0 );
delete tb_stock_data_Quarterly  where code in (select distinct(code) from  tb_stock_data_Quarterly  where amount = 0 );
delete tb_stock_data_halfYearly where code in (select distinct(code) from  tb_stock_data_halfYearly where amount = 0 );
delete tb_stock_data_Yearly     where code in (select distinct(code) from  tb_stock_data_Yearly     where amount = 0 );


exec proc_stock_get_week_all    ;
exec proc_stock_get_month_all   ;
exec proc_stock_get_Quarter_all ;
exec proc_stock_get_HalfYear_all;
exec proc_stock_get_Year_all    ;


delete tb_stock_data_Daily      where code ='002261';                    
delete tb_stock_data_weekly     where code ='002261';
delete tb_stock_data_monthly    where code ='002261';
delete tb_stock_data_Quarterly  where code ='002261';
delete tb_stock_data_halfYearly where code ='002261';
delete tb_stock_data_Yearly     where code ='002261';


delete tb_stock_data_weekly where 
  shi_jian >=to_date('20160222000000','yyyymmddhh24miss');        
  
  
truncate table tb_stock_data_Quarterly  ;
truncate table tb_stock_data_halfYearly ;
truncate table tb_stock_data_Yearly     ;  
exec proc_stock_get_Quarter_all ;
exec proc_stock_get_HalfYear_all;
exec proc_stock_get_Year_all    ;


select code ,                                                 
       name ,                                                 
       to_char(shi_jian,'yyyymmddhh24miss') shi_jian        
 from tb_stock_data_monthly where                                                                                     
  kdj_k <=20                                                  
    and                                                       
  kdj_j <=20                                                  
    and                                                       
  xstd_lshort < xstd_sshort
order by code ,
         shi_jian desc ;                              
         
         
select * from tb_stock_data_monthly where
  code = '000001'
    and
  kdj_k <=20                                                  
    and                                                       
  kdj_j <=20                                                  
    and                                                       
  xstd_lshort < xstd_sshort
order by code ,
         shi_jian desc ;     
         
            
select code ,                                                 
       name ,                                                 
       to_char(shi_jian,'yyyymmddhh24miss') shi_jian   
from tb_stock_data_monthly where
  kdj_d <=20
    and
  kdj_k <=20                                                  
    and                                                       
  kdj_j <=20                                                  
order by code ,
         shi_jian desc ;   
         
         
delete tb_stock_data_weekly     where 
  shi_jian = (select max(shi_jian) from tb_stock_data_weekly);

delete tb_stock_data_weekly     where 
  shi_jian >=to_date('20160408000000','yyyymmddhh24miss');  

delete tb_stock_data_daily where 
  code in 
  (
    '000683',
    '600507',
    '002341'
  );  
  
  
delete tb_stock_data_weekly where 
  code in 
  (
    '000683',
    '600507',
    '002341'
  );
    


declare 
	cursor curcode is 
	  select distinct(code) code from tb_stock_data_daily;
	  
	cursor curdaily( pcode varchar2 ) is
	  select * from tb_stock_data_daily where code = pcode order by shi_jian asc ;
	
 rtcode curcode%rowtype;
 rtdaily curdaily%rowtype ;
 
 nrow number ;
 nlast_price number ;
begin

  for rtcode in curcode loop
  		
    nrow := 1 ;
    nlast_price :=null ;
    for rtdaily in curdaily(rtcode.code) loop 
      if nrow = 1 then
      
      	update tb_stock_data_daily set price_last_day = null,
      	                               zhang_die_rate = null ,
      	                               zhang_die      = null        	
      	where 
      	  code = rtdaily.code 
      	    and
      	  shi_jian = rtdaily.shi_jian ;
      	
      	nlast_price := rtdaily.price ;   
        nrow := nrow + 1 ;
        continue ;
      end if; 
      
      if nlast_price <> 0 then
      
	      update tb_stock_data_daily set price_last_day = nlast_price ,
	                                     zhang_die_rate = (rtdaily.price - nlast_price)/nlast_price,
	                                     zhang_die      = rtdaily.price - nlast_price       	
	      where 
	        code = rtdaily.code 
	          and
	        shi_jian = rtdaily.shi_jian ;   
	    else
	      update tb_stock_data_daily set price_last_day = nlast_price ,
	                                     zhang_die_rate = null,
	                                     zhang_die      = rtdaily.price - nlast_price       	
	      where 
	        code = rtdaily.code 
	          and
	        shi_jian = rtdaily.shi_jian ;  	    	    
	    end if ;   
      nlast_price := rtdaily.price ; 
      nrow := nrow + 1 ;
    end loop ;
    commit;
  end loop;

end; 



truncate table tb_stock_data_weekly ;
--delete tb_stock_data_weekly where   code ='sh000001'  and  shi_jian > to_date('2000-05-24 15:00:00','yyyy-mm-dd hh24:mi:ss');
select to_char(sysdate,'yyyy-mm-dd hh24:mi:ss') from dual; 
exec proc_stock_get_week('sh000001','上证指数');
select to_char(sysdate,'yyyy-mm-dd hh24:mi:ss') from dual; 



truncate table tb_stock_data_monthly ;
--delete tb_stock_data_monthly where   code ='sh000001'  and  shi_jian > to_date('2000-05-24 15:00:00','yyyy-mm-dd hh24:mi:ss');
select to_char(sysdate,'yyyy-mm-dd hh24:mi:ss') from dual; 
exec proc_stock_get_month('sh000001','上证指数');
select to_char(sysdate,'yyyy-mm-dd hh24:mi:ss') from dual; 

truncate table tb_stock_data_daily ;

truncate table tb_stock_data_weekly     ;
truncate table tb_stock_data_monthly    ;
truncate table tb_stock_data_Quarterly  ;
truncate table tb_stock_data_halfYearly ;
truncate table tb_stock_data_Yearly     ;
select to_char(sysdate,'yyyy-mm-dd hh24:mi:ss') from dual;
exec  proc_stock_get_week_all  ;   
select to_char(sysdate,'yyyy-mm-dd hh24:mi:ss') from dual;
exec  proc_stock_get_month_all ;
select to_char(sysdate,'yyyy-mm-dd hh24:mi:ss') from dual; 
exec proc_stock_get_Quarter_all  ; 
select to_char(sysdate,'yyyy-mm-dd hh24:mi:ss') from dual; 
exec proc_stock_get_HalfYear_all ;
select to_char(sysdate,'yyyy-mm-dd hh24:mi:ss') from dual; 
exec proc_stock_get_Year_all     ;
select to_char(sysdate,'yyyy-mm-dd hh24:mi:ss') from dual; 


select to_char(shi_jian,'yyyy-mm-dd hh24:mi:ss') ,price,price_today_open , max_price,min_price,amount from tb_stock_data_weekly order by shi_jian asc;                                                                                                                       

select to_char(trunc(shi_jian,'d'),'yyyy-mm-dd hh24:mi:ss') , count(1) from tb_stock_data_weekly group by shi_jian having count(1)>1 order by shi_jian asc;

select 2003-01-29 15:00:00 

  	select * from
		(
		   select
		          max(shi_jian)  shi_jian  ,
		          sum(vol)       vol       ,
		          sum(amount)    amount    ,
		          max(max_price) max_price ,
		          min(min_price) min_price
		   from tb_stock_data_Daily where
		     code = 'sh000001'
		       and
		     trunc(shi_jian,'d') =  to_date('1994-01-30 00:00:00','yyyy-mm-dd hh24:mi:ss')+7 
		)a,
		(
		  select price_today_open from tb_stock_data_Daily where
		    code = 'sh000001'
		      and
		    shi_jian = (select min(shi_jian) from tb_stock_data_Daily where
		                  code = 'sh000001'
		                    and
		                  trunc(shi_jian,'d') =  to_date('1994-01-30 00:00:00','yyyy-mm-dd hh24:mi:ss')+7 
		                )
		)b,
		(
		  select price from tb_stock_data_Daily where
		    code = 'sh000001'
		      and
		    shi_jian = (
		                  select max(shi_jian) from tb_stock_data_Daily where
		                    code = 'sh000001'
		                      and
		                    trunc(shi_jian,'d') =  to_date('1994-01-30 00:00:00','yyyy-mm-dd hh24:mi:ss')+7 
		                )
		)c ;
		

select to_char(shi_jian,'yyyy-mm-dd hh24:mi:ss') ,
       xstd_SLONG  ,	
       xstd_SSHORT ,
       xstd_LLONG  ,
       xstd_LSHORT
from tb_stock_data_weekly where code = 'sh000001' order by shi_jian asc;       

select to_char(shi_jian,'yyyy-mm-dd hh24:mi:ss') ,
       price,
       price_last_day   ,                
       price_today_open ,
       max_price   ,
       min_price   ,
       MA6         , 
       MA12        , 
       MA20        ,
       MA30        ,
       MA45        ,
       MA60        ,
       MA125       ,
       MA250       ,
       KDJ_K,
       KDJ_D,
       KDJ_J,       
       xstd_SLONG  ,	
       xstd_SSHORT ,
       xstd_LLONG  ,
       xstd_LSHORT
from tb_stock_data_monthly where code = 'sh000001' order by shi_jian asc; 

1258

delete tb_stock_data_weekly where 
  code ='sh000001'
    and
  shi_jian > to_date('1991-05-24 15:00:00','yyyy-mm-dd hh24:mi:ss');
  
  
  
insert into  tb_stock_data_weekly 
(
name                 ,         
code                 ,
price                ,
price_last_day       ,
price_today_open     ,
wai_pan              ,
nei_pan              ,
buy1_price           ,
buy1_vol             ,
buy2_price           ,
buy2_vol             ,
buy3_price           ,
buy3_vol             ,
buy4_price           ,
buy4_vol             ,
buy5_price           ,
buy5_vol             ,
sell1_price          ,
sell1_vol            ,
sell2_price          ,
sell2_vol            ,
sell3_price          ,
sell3_vol            ,
sell4_price          ,
sell4_vol            ,
sell5_price          ,
sell5_vol            ,
zjzbcj               ,
shi_jian             ,
zhang_die            ,
zhang_die_rate       ,
max_price            ,
min_price            ,
p_v_a                ,
vol                  ,
amount               ,
huan_sou_lv          ,
pe                   ,
zhenfu               ,
liutongshizhi        ,
zhongshizhi          ,
shijinglv            ,
zhangtingjia         ,
dietingjia           ,
MA6                  ,
MA12                 ,
MA20                 ,
MA30                 ,
MA45                 ,
MA60                 ,
MA125                ,
MA250                ,
KDJ_K                ,
KDJ_D                ,
KDJ_J                ,
xstd_SLONG           ,
xstd_SSHORT          ,
xstd_LLONG           ,
xstd_LSHORT          ,
BOLL_uBOLL           ,
BOLL_dBOLL           ,
BOLL_BOLL            ,
MACD_DIF             ,
MACD_MACD            ,
MACD_DIF_MACD    
) 
	select * from tb_stock_data_daily where 
	  code = 'sh000001'
	    and
	  shi_jian >=to_date('20151105000000','yyyymmddhh24miss');  
	  
	  
update tb_stock_data_Quarterly 
  set kdj_k = 10      ,
      kdj_d = 10      ,
      kdj_j = 10      ,
      xstd_lshort = 2 ,
      xstd_sshort = 1
where 
  shi_jian = to_date(20151109150000,'yyyymmddhh24miss');
  
  
update tb_stock_data_Quarterly 
  set kdj_k = 19      ,
      kdj_d = 17      ,
      kdj_j = 19      ,
      xstd_lshort = 1 ,
      xstd_sshort = 2
where 
  shi_jian = to_date(20151110150000,'yyyymmddhh24miss');	  
  

insert into tb_stock_data_Yearly 
  select * from tb_stock_data_Quarterly ;
  
  


select count(1) from tb_stock_data_weekly     ;
select count(1) from tb_stock_data_monthly    ;
select count(1) from tb_stock_data_Quarterly  ;
select count(1) from tb_stock_data_halfYearly ;
select count(1) from tb_stock_data_Yearly     ;


select count(distinct(code)) from tb_stock_data_weekly     ;
select count(distinct(code)) from tb_stock_data_monthly    ;
select count(distinct(code)) from tb_stock_data_Quarterly  ;
select count(distinct(code)) from tb_stock_data_halfYearly ;
select count(distinct(code)) from tb_stock_data_Yearly     ;


select * from                                   
(                                                 
   select code ,                                          
          name ,                                          
          to_char(shi_jian ,'yyyymmddhh24miss') shi_jian,         
          kdj_k,                                          
          kdj_d,                                          
          kdj_j                                    
   from tb_stock_data_Quarterly where       
     code = '000027'
   order by shi_jian desc                        
)                                               
where                                             
rownum < 3 ;


delete tb_stock_data_Daily      where code in ('000598','000719','000620');
delete tb_stock_data_weekly     where code in ('000598','000719','000620');
delete tb_stock_data_monthly    where code in ('000598','000719','000620');
delete tb_stock_data_Quarterly  where code in ('000598','000719','000620');
                                                                                                                                                   
                                                                                                                                                   
                                                                                                                                                   
                                                                                                                                                   select * from 
(
select shi_jiana ,zhang/(zhang+die)*100 rate from
(select to_char(shi_jian,'yyyy-mm') shi_jiana,count(*) zhang from tb_stock_data_monthly where zhang_die_rate >0 group by to_char(shi_jian,'yyyy-mm')) a
inner join 
(select to_char(shi_jian,'yyyy-mm') shi_jianb,count(*) die from tb_stock_data_monthly where zhang_die_rate <=0 group by to_char(shi_jian,'yyyy-mm')) b
on a.shi_jiana=b.shi_jianb
)
where 
  rate >=20
order by shi_jiana desc ;

select substr(shi_jiana,1,4) ,count(1) from 
(
select shi_jiana ,zhang/(zhang+die)*100 rate from
(select to_char(shi_jian,'yyyy-mm') shi_jiana,count(*) zhang from tb_stock_data_monthly where zhang_die_rate >0 group by to_char(shi_jian,'yyyy-mm')) a
inner join 
(select to_char(shi_jian,'yyyy-mm') shi_jianb,count(*) die from tb_stock_data_monthly where zhang_die_rate <=0 group by to_char(shi_jian,'yyyy-mm')) b
on a.shi_jiana=b.shi_jianb
)
where 
  rate >=20
group by   substr(shi_jiana,1,4)
order by substr(shi_jiana,1,4) desc ;