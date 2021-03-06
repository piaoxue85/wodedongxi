declare
	cursor cur is 
		select * from tb_stock_predict ;
	
	rt cur%rowtype ;
	
	nprice_begin number ;
	nprice_end   number ;
	nval         number ;
	nrate        number ;
	ncount       number ;
begin	
	for rt in cur loop
		
		select count(1) into ncount from tb_stock_data_daily where 
		  code = rt.code 
		    and
		  shi_jian = rt.end_time;	
		  
		if ncount<>1 then
			continue ;
		end if; 
		
		select price into nprice_begin from tb_stock_data_daily where 
		  code = rt.code 
		    and
		  shi_jian = rt.end_time;
	
		select price into nprice_end from tb_stock_data_daily where 
		  code = rt.code 
		    and
		  shi_jian = (select max(shi_jian) tb_stock_data_daily from tb_stock_data_daily where code = rt.code and shi_jian <= rt.end_time + 8 );
		
		nrate:=round(10000*(nprice_end - nprice_begin)/nprice_begin)/100; 
		
		if nrate >2 then
			nval := 0 ;
		else
			nval := 1 ;
		end if ; 
		  
		update tb_stock_predict set real_rate = nrate , real_val = nval where seq = rt.seq;
	end loop ;
	
	commit;
end;

declare
	dreset  date ;
	dMonday date ;
	dFriday date ;
	dcur    date ;
	sday    varchar2(32);
begin
	dcur   := to_date('20140106000000','yyyymmddhh24miss');
	dreset := to_date('19890101000000','yyyymmddhh24miss');
	
	while dcur < sysdate  loop
	  select to_char(dcur,'day') into sday  from dual;
		 
	  if sday = '����һ' then
			dMonday := dcur ; 		
		end if;
		
	  if sday = '������' then
			dFriday := dcur ; 		
		end if;		
		
		if dMonday <>dreset and dFriday <> dreset then
			insert into tb_stock_week_time values (dMonday,dFriday);
			dMonday := dreset ; 
			dFriday := dreset ;
		end if;
		
		dcur := dcur + 1;
	end loop ;	
	commit;
end;