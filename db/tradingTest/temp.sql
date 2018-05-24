select code, price from tb_stock_data_daily where 
  shi_jian = to_date('20160601150000','yyyymmddhh24miss')
    and
  code in
  ( 
    select code from tb_trading_test_Volume where Volume>0 
  )
  order by code asc ;
  
select * from tb_trading_test_task ;
select * from tb_trading_test_Volume where volume >0 order by code asc;
select * from tb_trading_log order by code , trading_date asc;


select code , price from tb_stock_data_daily where 
  code in 
  (
     select code from tb_trading_test_Volume where volume >0 
  )
    and
  shi_jian = to_date('20081104150000','yyyymmddhh24miss')
order by code asc ;  