Connect c##stock/didierg160@myoracle;

create or replace procedure proc_stock_get_state_count
(
  pcode in varchar2
)
as
  
  cursor cur(lpcode varchar2) is 
     select f_get_state(zhang_die_rate) state
     from tb_stock_data_daily where 
       code = lpcode 
         and
       shi_jian > (select min(shi_jian) from tb_stock_data_daily where code =lpcode )
         and
       shi_jian <= to_date('20160419153000','yyyymmddhh24miss')
     order by shi_jian ;
  
  rt cur%rowtype ; 
     
  nlast_state number ;
  nthis_state number ;

  ncounter number ;
begin
   delete tb_stock_state_counter ;
   delete tb_stock_state_change_counter ;
   
   insert into tb_stock_state_counter 
     select f_get_state(zhang_die_rate),
            count(1) 
     from tb_stock_data_daily where 
       code = pcode 
         and
       shi_jian > (select min(shi_jian) from tb_stock_data_daily where code =pcode )
         and
       shi_jian <= to_date('20160419153000','yyyymmddhh24miss')       
     group by f_get_state(zhang_die_rate) 
     order by f_get_state(zhang_die_rate) asc ;
   
   nlast_state := 999 ;
     
   for rt in cur(pcode) loop
       nthis_state := rt.state ;
        
       if nlast_state = 999 then
         nlast_state := nthis_state;
         continue ;
       end if;
       
       select count(1) into ncounter from tb_stock_state_change_counter where 
         state_start = nlast_state 
           and
         state_end   = nthis_state ;
         
       if ncounter < 1 then
         insert into tb_stock_state_change_counter values ( nlast_state , nthis_state , 1 ) ;
       else
         update tb_stock_state_change_counter set counter = counter+1 where 
           state_start = nlast_state 
             and
           state_end   = nthis_state ;
       end if ;
       nlast_state := nthis_state;
   end loop ;

   commit;
end;


create or replace function f_get_state
(
  prate in number 
)
return number 
is 
  nRes number ;
begin
  nRes := 0 ;
  nRes := ceil(prate * 100 +  10)  ;
  
  if prate <= -0.1 then 
    nRes := 1 ;
  end if ;
  
  if prate >= 0.1 then 
    nRes := 20 ;
  end if ;
    
  return nRes ;
  
end; 