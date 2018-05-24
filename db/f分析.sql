select max(kdj_k),
       max(kdj_d),
       max(kdj_j),
       min(kdj_k),
       min(kdj_d),
       min(kdj_j)
from tb_stock_data_daily where 
 kdj_k > 1
   and
 kdj_d > 1
 ;
 
 
select * from  tb_stock_data_daily where kdj_j=-32.92 ;


select * from  tb_stock_data_daily where 
	shi_jian > (select max(shi_jian)-5 from tb_stock_data_daily )
	kdj_d <10 
	  and
	kdj_k < 10 
	  and
	kdj_j> kdj_k
	  and
	kdj_k>kdj_d ;
	
	
select * from  tb_stock_data_daily where 
	shi_jian > (select max(shi_jian)-5 from tb_stock_data_daily )
	  and
	kdj_d <10 
	  and
	kdj_k < 10 
	  and
	kdj_j> kdj_k
	  and
	kdj_k>kdj_d 
	  and
	xstd_lshort < xstd_sshort;
	
select name, (max(price)-(select min(price) from tb_stock_data_daily where shi_jian > (select max(shi_jian)-5 from tb_stock_data_daily ) ))/max(price) jumprate from  tb_stock_data_daily where 
	shi_jian > (select max(shi_jian)-5 from tb_stock_data_daily )
	  and
	price < 10
	  and
	kdj_d <15 
	  and
	kdj_k < 15 
	  and
	kdj_j> kdj_k
	  and
	kdj_k>kdj_d 
	  and
	xstd_lshort < xstd_sshort
group by name;	


select (max(price)-(select min(price) from tb_stock_data_daily where shi_jian > (select max(shi_jian)-10 from tb_stock_data_daily ) ))/max(price) jumprate from  tb_stock_data_daily 
where 
  code = '300431' ;



select * from tb_stock_data_weekly where
  shi_jian = (select max(shi_jian) from tb_stock_data_weekly )
    and
  kdj_k <=18
    and
  kdj_j <=18
    and
  kdj_j >kdj_k
    and
  kdj_k >kdj_d 
  	  and
	xstd_lshort < xstd_sshort;
	
	
select * from tb_stock_data_weekly where
  shi_jian = (select max(shi_jian) from tb_stock_data_weekly )
    and
  kdj_k <=18
    and
  kdj_j <=18
    and
	xstd_lshort < xstd_sshort;
	
	
select code,name , 
       (max(price)-min(price))/min(price) percent
from tb_stock_data_daily where 
  shi_jian >= to_date('20150708000000','yyyymmddhh24miss')
group by code,name 
having (max(price)-min(price))/min(price)>0
order by percent asc ;


select * from 
(
	select code,name , 
	       (max(price)-min(price))/min(price) percent ,
	       count(1) c
	from tb_stock_data_daily where 
	  shi_jian >= to_date('20120101000000','yyyymmddhh24miss')
	group by code,name 
	having (max(price)-min(price))/min(price)>0
)
where 
  c > 100
order by percent asc ;


select * from 
(
	select code,name , 
	       (max(price)-min(price))/min(price) percent ,
	       min(shi_jian) shi_jian,
	       sum(kdj_k) kdj_k,
	       count(1) c
	from tb_stock_data_daily where 
	  shi_jian >= to_date('20120101000000','yyyymmddhh24miss')
	group by code,name 
	having (max(price)-min(price))/min(price)>0
)
where 
  c > 200
    and
  shi_jian<=to_date('20120201000000','yyyymmddhh24miss')
order by kdj_k desc ;

   select b.code,b.name,(b.max_price-a.price)/price percent from
	  tb_stock_data_daily a ,
	  (
			select code,name , 
			       max(max_price) max_price ,
			       min(shi_jian) min_shi_jian,
			       max(shi_jian) max_shi_jian,
			       sum(kdj_k) kdj_k,
			       count(1) c
			from tb_stock_data_daily where 
			  shi_jian >= to_date('20150610000000','yyyymmddhh24miss')
			group by code,name 
		) b
  where
    a.code = b.code 
      and
    a.shi_jian = b.max_shi_jian
  order by percent;
	
	select code,name,max(shi_jian) from
	
	
	
select name,
       code,
       (max(max_price)-min(min_price))/max(max_price) discount 
from tb_stock_data_weekly where 
  code in 
  (
    '002577',
    '300316',
    '600880',
    '601618',
    '601718',
    '603600',
    '000958',
    '300134',
    '300030',
    '600072',
    '600643',
    '600193',
    '000782',
    '300216',
    '002313',
    '300135',
    '600707',
    '600750',
    '600839' 
  )
    and
  shi_jian >= to_date('20150601000000','yyyymmddhh24miss')
group by name,code  
order by discount desc ;


NAME                                                             CODE                               DISCOUNT
---------------------------------------------------------------- -------------------------------- ----------
四川长虹                                                         600839                           .775347913
永艺股份                                                         603600                           .752767296
创兴资源                                                         600193                           .749546828
际华集团                                                         601718                             .7433213
钢构工程                                                         600072                           .741266622
东方能源                                                         000958                           .729759786
美达股份                                                         000782                             .7208981
彩虹股份                                                         600707                            .71679933
宝利国际                                                         300135                           .705882353
千山药机                                                         300216                           .700183294
博瑞传播                                                         600880                           .696982055
日海通讯                                                         002313                           .691119691
晶盛机电                                                         300316                           .687956907
大富科技                                                         300134                           .685625846
阳普医疗                                                         300030                           .680526316
雷柏科技                                                         002577                           .677383469
中国中冶                                                         601618                           .643968872
爱建集团                                                         600643                           .643254818
江中药业                                                         600750                           .597532768

已选择19行。



declare 
  cursor cur is 
	  select code ,
	         name ,
	         max(max_price) max_price ,
	         min(min_price) min_price 
	  from tb_stock_data_daily where 
	    shi_jian >= to_date('20150612000000','yyyymmddhh24miss')
	      and
	    code in 
	    (
	      select code from tb_stock_list
	    )
	  group by code, name ;
	
	rt cur%rowtype ;
	
	max_shi_jian date ;
	min_shi_jian date ;
	vpe varchar2(10); 
begin

  delete tb_didier_temp ;
	
	for rt in cur loop
	  select shi_jian into max_shi_jian from
	  (
			select shi_jian  from tb_stock_data_daily where 
			  code = rt.code 
			    and
			  shi_jian >= to_date('20150612000000','yyyymmddhh24miss') 
			    and
			  max_price = rt.max_price 
			    and
			  rownum<2
	  );
		
		select shi_jian into min_shi_jian from
		(  
			select shi_jian  from tb_stock_data_daily where 
			  code = rt.code 
			    and
			  shi_jian >= to_date('20150612000000','yyyymmddhh24miss') 
			    and
			  min_price = rt.min_price
			    and
			  rownum<2
		) ;		
		  
		if  min_shi_jian > max_shi_jian then 
			select pe into vpe from tb_stock_list where code = rt.code ;
			
			if vpe <>'亏损' then
			
				insert into tb_didier_temp values ( rt.code ,
				                                    rt.name , 
				                                    rt.max_price , 
				                                    rt.min_price ,
				                                    (rt.max_price - rt.min_price)/rt.max_price ,
				                                    to_number(vpe ) 
				                                  );
			end if ;
		end if ; 
		
	end loop ;
	
  commit; 

end; 
         
         
select * from tb_didier_temp where 
 pe <= 50 
   and
 code in 
 (
    '000782',  
    '000812',  
    '000837',  
    '000850',  
    '000917',  
    '000922',  
    '000958',  
    '000979',  
    '002002',  
    '002037',  
    '002067',  
    '600633',  
    '600634',  
    '300184',  
    '300094',  
    '300096',  
    '600643',  
    '300112',  
    '000529',  
    '300216',  
    '300131',  
    '300134',  
    '300135',  
    '600705',  
    '600707',  
    '600708',  
    '000566',  
    '002238',  
    '002481',  
    '002268',  
    '600491',  
    '600499',  
    '600818',  
    '000633',  
    '600525',  
    '600839',  
    '300316',  
    '002303',  
    '600545',  
    '600555',  
    '300010',  
    '600737',  
    '000016',  
    '002348',  
    '002577',  
    '300030',  
    '600750',  
    '600751',  
    '002353',  
    '300052',  
    '000062',  
    '300380',  
    '601989',  
    '603568',  
    '600193',  
    '002106',  
    '603600',  
    '603686',  
    '600880',  
    '600026',  
    '002183',  
    '601003',  
    '601016',  
    '600058',  
    '600072',  
    '601106',  
    '601618',  
    '600139',  
    '601718',  
    '603166',  
    '600170',  
    '601866',  
    '601877',  
    '601918',  
    '601919',  
    '600180',  
    '600259',  
    '600277',  
    '600280',  
    '600288',  
    '600428',  
    '600429',  
    '600432'  
 )
order by die_fu desc;



declare 
  cursor cur is 
	  select code ,
	         name ,
	         max(max_price) max_price ,
	         min(min_price) min_price 
	  from tb_stock_data_daily where 
	    shi_jian >= to_date('20100101000000','yyyymmddhh24miss')
	      and
	    code in 
	    (
	      select code from tb_stock_list
	    )
	  group by code, name ;
	
	rt cur%rowtype ;
	
	max_shi_jian date ;
	min_shi_jian date ;
	vpe varchar2(10); 
begin

  delete tb_didier_temp ;
	
	for rt in cur loop
	  select shi_jian into max_shi_jian from
	  (
			select shi_jian  from tb_stock_data_daily where 
			  code = rt.code 
			    and
			  shi_jian >= to_date('20100101000000','yyyymmddhh24miss') 
			    and
			  max_price = rt.max_price 
			    and
			  rownum<2
	  );
		
		select shi_jian into min_shi_jian from
		(  
			select shi_jian  from tb_stock_data_daily where 
			  code = rt.code 
			    and
			  shi_jian >= to_date('20100101000000','yyyymmddhh24miss') 
			    and
			  min_price = rt.min_price
			    and
			  rownum<2
		) ;		
		  
		if  min_shi_jian < max_shi_jian and min_shi_jian < to_date('20150101000000','yyyymmddhh24miss') then 
			select pe into vpe from tb_stock_list where code = rt.code ;
			
			if vpe <>'亏损' then
			
				insert into tb_didier_temp values ( rt.code ,
				                                    rt.name , 
				                                    rt.max_price , 
				                                    rt.min_price ,
				                                    rt.max_price - rt.min_price/rt.min_price ,
				                                    vpe 
				                                  );
			end if ;
		end if ; 
		
	end loop ;
	
  commit; 

end; 
         
         
         
declare 
  cursor cur is 
    select code ,
           shi_jian                                                       
     from tb_stock_data_Quarterly where                                                                                      
       kdj_j>=kdj_k                                                  
         and                                                         
       kdj_k>=kdj_d ;
    
  cursor cur1(pcode varchar2,pshi_jian date) is   
    select code ,    
           name ,    
           shi_jian ,
           to_char(kdj_k) k,  
           to_char(kdj_d) d,  
           to_char(kdj_j) j   
    from                                            
    (                                               
      select code ,                                 
             name ,                                 
             shi_jian,
             kdj_k,                                 
             kdj_d,                                 
             kdj_j                                  
      from tb_stock_data_Quarterly where   
        code = pcode
          and
        shi_jian <= pshi_jian
      order by shi_jian desc                        
    )                                               
    where   
      rownum<3;                                        
  
  rt cur%rowtype;
  rt1 cur1%rowtype ;
  
  ncount number ;
begin
  delete tb_didier_temp1 ;
  commit;
	for rt in cur loop
	
	  ncount := 0 ;
	  for rt1 in cur1(rt.code , rt.shi_jian) loop
	  
	    ncount := ncount + 1 ;
	      
	    if ncount = 2 then
	    
	      if rt1.k is not null or 
	         rt1.d is not null or
	         rt1.j is not null
	      then
	    
	        if (rt1.k<=20) and 
	           (rt1.d<=20) and 
	           (rt1.j<=20) --and
	           --(rt1.d>=rt1.k) and
	           --(rt1.k>=rt1.j) 
	        then
	          insert into tb_didier_temp1 values ( rt1.code , rt1.name , rt1.shi_jian ); 	          
	        end if ;	        
	    
	      end if ;	      
	    
	    end if ;	    
	  
	  end loop ;
		
	end loop ;
  commit;
end; 


--新股8日内破板

declare
  cursor cur is 
    select code ,name , min(shi_jian) shi_jian from tb_stock_data_daily group by code , name having min(shi_jian) >= to_date('20160101150000','yyyymmddhh24miss') ;	
	rt cur%rowtype ;	
	fprice number ;	
	counter number ;
begin
  delete tb_stock_new_stock ;

  --第一天收盘价的2.1倍
  --第9个交易日内
  
  for rt in cur loop    
    select count(1) into counter  from
    (
      select * from 
      (
        select * from tb_stock_data_daily where 
          code = rt.code  
            and
          shi_jian > rt.shi_jian
        order by shi_jian  asc
      )
      where rownum <= 8
    )
    where 
      min_price <> max_price ;
    
    if counter >0 and instr(rt.name,'银行') < 1 then
      insert into tb_stock_new_stock values ( rt.code, rt.name,rt.shi_jian);
    end if;
  end loop ;
  
  commit;
end; 



