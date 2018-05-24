drop SEQUENCE SEQ_TEMP ;
create  SEQUENCE SEQ_TEMP ;

truncate  table tb_train        ;
truncate  table tb_train_regen  ;
truncate  table tb_test         ;
truncate  table tb_test_regen   ;


create table tb_train 
(
  a varchar2(16) ,
  b number ,
  c number
);

create table tb_train_regen 
(
  seq number ,
  a varchar2(16) ,
  b number ,
  c number
);

insert into tb_train_regen 
  select seq_temp.nextval ,
         code,
         to_char(shi_jian,'yyyymmdd'),
         3 
  from 
  (
	  select 
	         code,
	         shi_jian	         
	  from tb_stock_data_daily where
	    code in
	    (
	       select distinct(a) from tb_train
	    )
	      and
	    shi_jian >= to_date('20100101000000','yyyymmddhh24miss')
	  order by code asc , shi_jian asc
  );
    
update tb_train_regen a set a.c = 1 where 
  exists 
  (
    select 1 from tb_train b where
      a.a = b.a 
        and
      a.b = b.b
        and
      b.c = 1 
  ) ;
  

update tb_train_regen a set a.c = 0 where 
  exists 
  (
    select 1 from tb_train b where
      a.a = b.a 
        and
      a.b = b.b
        and
      b.c = 0 
  ) ;  
  
  
update tb_train_regen a set c ='1.0' where
  exists
  (
    select 1 from tb_train_regen b where 
      b.c = '1.0'
        and        
      a.seq >= b.seq - 5
        and
      a.seq <= b.seq + 5
  );  
  
update tb_train_regen a set a.c = b.c where 
  exists 
  (
    select 1 from tb_train b where
      a.a = b.a 
        and
      a.b = b.b
  ) ;  
  

select a||','||b||','||c
from tb_train_regen 
order by a,b asc;


create table tb_test 
(
  a varchar2(16) ,
  b number ,
  c number
);

create table tb_test_regen 
(
  seq number ,
  a varchar2(16) ,
  b number ,
  c number
);

    
insert into tb_test_regen 
  select seq_temp.nextval ,
         code,
         to_char(shi_jian,'yyyymmdd'),
         3 
  from 
  (
	  select 
	         code,
	         shi_jian	         
	  from tb_stock_data_daily where
	    code in
	    (
	       select distinct(a) from tb_test
	    )
	      and
	    shi_jian >= to_date('20100101000000','yyyymmddhh24miss')	    
	  order by code asc , shi_jian asc
  );    
    
update tb_test_regen a set a.c = 1 where 
  exists 
  (
    select 1 from tb_test b where
      a.a = b.a 
        and
      a.b = b.b
        and
      b.c = 1 
  ) ;
  
update tb_test_regen a set a.c = 0 where 
  exists 
  (
    select 1 from tb_test b where
      a.a = b.a 
        and
      a.b = b.b
        and
      b.c = 0 
  ) ;  
  
update tb_test_regen a set c ='1.0' where
  exists
  (
    select 1 from tb_test_regen b where 
      b.c = '1.0'
        and        
      a.seq >= b.seq - 5
        and
      a.seq <= b.seq + 5
  );   
  
update tb_test_regen a set a.c = b.c where 
  exists 
  (
    select 1 from tb_test b where
      a.a = b.a 
        and
      a.b = b.b
  ) ;  
  
select a||','||b||','||c
from tb_test_regen 
order by a,b asc;  


delete tb_test_regen  where
  seq in 
  (  
     select * from
     (
       select seq from tb_test_regen_bak where 
         c = 0
       order by dbms_random.value
     )
     where rownum <= 31714 - 891 * 3
  );
  
select distinct(code) from tb_stock_data_daily where 
  shi_jian >= to_date('19990101000000','yyyymmddhh24miss')
    and
  shi_jian <= to_date('19990201000000','yyyymmddhh24miss')
    and
  code in 
  (
		select distinct(code) from tb_stock_data_daily where 
		  shi_jian >= to_date('20170101000000','yyyymmddhh24miss')
		    and
		  shi_jian <= to_date('20170301000000','yyyymmddhh24miss')
  )
order by dbms_random.value;  


select code||','||to_char(shi_jian , 'yyyymmdd')||',0' from tb_stock_data_daily where 
  shi_jian >= to_date('20000101000000','yyyymmddhh24miss')
    and
  code in 
  (
		'000586',
		'000830',
		'000802',
		'000620',
		'000520',
		'600770',
		'600816',
		'600118',
		'600059',
		'600745'  
  );
  
delete tb_train_regen  where
  seq in 
  (  
     select * from
     (
       select seq from tb_train_regen where 
         c = 3
       order by dbms_random.value
     )
     where rownum <= 
     (
       (select count(1) from tb_train_regen where c = 3) -
       round((select count(1) from tb_train_regen where c <> 3) * 0.5 * 1.2)          
     )
  );  
  
delete tb_test_regen  where
  seq in 
  (  
     select * from
     (
       select seq from tb_test_regen where 
         c = 3
       order by dbms_random.value
     )
     where rownum <= 
     (
       (select count(1) from tb_test_regen where c = 3) -
       round((select count(1) from tb_test_regen where c <> 3) * 0.5 * 1.2)          
     )
  );    