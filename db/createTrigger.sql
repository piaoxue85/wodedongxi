connect c##stock/didierg160@myoracle ;

create or replace trigger tri_stock_data_market_cap
/*
这个TRIGGER是在表tb_ivr_bmans进行update,delete这一系列动作前将所有变化保存到对应的
合作网员信息表审计表tb_ivr_bmans_audit
*/
	after update or delete
	on	tb_stock_data_market_cap
	for each row
declare
	vaction varchar2(20);
begin
	
	insert into tb_stock_data_market_cap
	(
		code       ,
		shi_jian   ,
		amount     ,
		market_cap
	)
	values 
	(
	
	);
	
	
	insert into tb_ivr_bmans_audit(
																	bman_id 			,
																	bman_name			,
																	action				,
																	time_stamp		,
																	reserved_char,
																	reserved_number
																)
														values
																 (:old.bman_id 			,
																	:old.bman_name			,
																	vaction				,
																	:old.time_stamp		,
																	:old.reserved_char, 
																	:old.reserved_number
																);

                                     
end;                                 
/                      
     