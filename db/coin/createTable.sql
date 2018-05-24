connect c##coin/didierg160@myoracle ;

drop   sequence seq_act_id ;
create sequence seq_act_id ;

drop table tb_act_log ;
create table tb_act_log
(
	act_id      number       not null ,
	act_type    varchar2(32) not null ,
	market      varchar2(32) not null ,
	price       number       not null ,
	vol         number       not null ,
	act_res     number       not null ,
	act_res_msg varchar2(512)not null ,
  time_stamp  date         not null 
);

