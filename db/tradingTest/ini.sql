connect c##stock/didierg160@myoracle ;

drop sequence seq_trading_test_task     ;
drop sequence seq_trading_test_Volume   ;
drop sequence seq_trading_log           ;
drop sequence seq_trading_test_strategy ;

create sequence seq_trading_test_task     ; 
create sequence seq_trading_test_Volume   ;
create sequence seq_trading_log           ;
create sequence seq_trading_test_strategy ;

truncate table  tb_trading_test_task     ;
truncate table  tb_trading_test_strategy ; 
truncate table  tb_temp ; 

truncate table  tb_trading_test_Volume   ; 
truncate table  tb_trading_log           ;
 

insert into tb_trading_test_strategy values
(
  seq_trading_test_strategy.nextval ,
  'dpo+kdj ÂòÂô' ,
  'fun_ts_kdj_dpo'  ,
  sysdate  
);

insert into tb_trading_test_task values
(
	seq_trading_test_task.nextval ,
	'»Ø²âdpo£¬kdj²ßÂÔ' ,
	1000000 ,
	1000000 ,  
	1.01 ,
	1 ,
	sysdate
);
commit;

set serveroutput on;
exec proc_ts_kdj_dpo(1,to_date('20071001150000','yyyymmddhh24miss'),to_date('20140101150000','yyyymmddhh24miss')); 
--exec proc_ts_kdj_dpo(1,to_date('20071016150000','yyyymmddhh24miss'),to_date('20081104150000','yyyymmddhh24miss'));


