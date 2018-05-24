Connect c##stock/didierg160@myoracle;

create table tb_stock_state_counter
(
  state        number not null primary key ,
  counter      number not null   
);

create table tb_stock_state_change_counter
(
  state_start  number not null ,
  state_end    number not null ,
  counter      number not null 
);