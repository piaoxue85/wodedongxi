connect c##stock/didierg160@myoracle ;

drop table tb_trading_test_task      ;
drop table tb_trading_test_Volume    ;
drop table tb_trading_log            ;
drop table tb_trading_test_strategy  ;

create table tb_trading_test_task 
(
   task_id         number        not null ,
   description     varchar2(256) not null ,
   init_amount     number        not null ,
   balance         number        not null ,
   cost_rate       number        not null ,
   strategy_id     number        not null ,
   time_stamp      date default sysdate not null 
);

alter table tb_trading_test_task add constraint
pk_trading_test_task
primary key(task_id) 
/

create table tb_trading_test_Volume   
(
  vol_id          number not null ,
  task_id         number not null ,
  code            varchar2(32) not null ,
  Volume          number not null ,
  time_stamp      date   not null 
);

alter table tb_trading_test_Volume add constraint
pk_trading_test_Volume
primary key(vol_id) 
/


create table tb_trading_log 
(
  trading_id      number not null ,
  task_id         number not null ,
  trading_type    number not null ,
  code            varchar2(32) not null ,
  trading_vol     number not null ,
  trading_price   number not null ,
  trading_date    date   not null ,
  balance         number not null ,
  time_stamp      date default sysdate not null    
);

alter table tb_trading_log add constraint
pk_trading_log
primary key(trading_id) 
/

create table tb_trading_test_strategy
(
  strategy_id     number not null ,
  descrption      varchar2(256) null ,
  fun_name        varchar2(256) not null ,
  time_stamp      date default sysdate not null           
);
  
alter table tb_trading_test_strategy add constraint
pk_trading_test_strategy
primary key(strategy_id) 
/
 
create table tb_temp 
(
	taskid      number ,
	code        varchar2(32),
	price       number ,
	shi_jian    date
);