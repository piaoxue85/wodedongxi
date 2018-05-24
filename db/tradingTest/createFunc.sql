connect c##stock/didierg160@myoracle ;

create or replace function func_trading_test_buy
(
  ptaskid in number ,
  pcode   in varchar2 ,
  pprice  in number ,
  pshi_jian in date
)
return number
is
  cursor cur_task(lptaskid number) is
    select * from tb_trading_test_task where task_id = lptaskid ;
  rt_task           cur_task%rowtype ;

  nres number ;
  nvol number ;
  ncount number ;
  nAmount number ;
begin
  nvol := 0 ;
  nres := 999 ;

  open cur_task(ptaskid) ;
  fetch cur_task into rt_task ;
  close cur_task ;

  if pprice * rt_task.cost_rate * 100 > rt_task.balance then
    nres := 1 ;  --余额不足
  else
    
    if pprice=0 then
	    insert into tb_temp values
	    (
	      ptaskid ,
	      pcode,
	      pprice,
	      pshi_jian
	    );
	    
	    commit;
    end if;
    
    if rt_task.balance < rt_task.init_amount/4 then
      nvol := floor(rt_task.balance/(pprice*100*rt_task.cost_rate)) * 100 ;
    else
      nvol := floor((rt_task.init_amount/4)/(pprice*100*rt_task.cost_rate)) * 100 ;
    end if;
    
    namount := nvol* pprice*rt_task.cost_rate ;

    dbms_output.put_line('code ='||pcode || ',  price = ' ||pprice || ',   shi_jian='||pshi_jian  ); 
    
    insert into tb_trading_log values
    (
      seq_trading_log.nextval ,          --trading_id
      ptaskid                ,           --task_id
      1                       ,          --trading_type  buy
      pcode                   ,          --code
      nvol                    ,          --trading_vol
      pprice                  ,          --trading_amount
      pshi_jian               ,
      rt_task.balance - namount ,
      sysdate
    );

	  select count(1) into ncount from tb_trading_test_Volume where
	    task_id = ptaskid
	      and
	    code = pcode ;

	  if ncount >= 1 then
	    update tb_trading_test_Volume set
	      Volume = Volume + nvol
	    where
	      task_id = ptaskid
	        and
	      code = pcode  ;
	  else
	    insert into tb_trading_test_Volume values
	    (
	      seq_trading_test_Volume.nextval  ,
	      ptaskid ,
	      pcode ,
	      nvol ,
	      sysdate
	    );
	  end if;

    update tb_trading_test_task set balance = rt_task.balance - namount where task_id = ptaskid ;
    commit;
    nres := 0;
  end if ;

  return nres ;
end;
/
create or replace function func_trading_test_sel
(   
  ptaskid in number ,
  pcode   in varchar2 ,
  pprice  in number ,
  pshijian in date
)
return number
is 
  cursor cur_task(lptaskid number) is
    select * from tb_trading_test_task where task_id = lptaskid ;  
  rt_task           cur_task%rowtype ;    
  
  ncount number ;
  nvol number ;
  nres number ;
begin
  open cur_task(ptaskid) ;  
  fetch cur_task into rt_task ;  
  close cur_task ;
  
  select count(1) into ncount from tb_trading_test_Volume where
    task_id = ptaskid 
      and
    code = pcode ;
    
  if ncount < 1 then 
    nres := 1  ;--没有购买过对应股票
  else
    select Volume into nvol from tb_trading_test_Volume where
      task_id = ptaskid 
        and
      code = pcode ;
    
    if nvol <1 then
      nres := 2 ;  --股票余额为0 
    else
    
      update tb_trading_test_Volume set
        volume = volume - nvol       
      where
	      task_id = ptaskid 
	        and
	      code = pcode ;
	      
	    insert into tb_trading_log values
	    (
	      seq_trading_log.nextval ,          --trading_id     
	      ptaskid                ,          --task_id        
	      0                       ,          --trading_type  sel
	      pcode                   ,          --code           
	      nvol                    ,          --trading_vol  
	      pprice                  ,          --trading_amount 
	      pshijian                ,    
	      rt_task.balance + nvol* pprice ,      
	      sysdate     
	    );
	          	    
	    update tb_trading_test_task set balance = rt_task.balance + nvol* pprice where task_id = ptaskid ;
	    commit;

      nres := 0 ;
    end if ;
    
  end if; 
  
  return nres ;
end;
/

create or replace procedure proc_ts_kdj_dpo
(
  ptaskid in number ,
  pbegin  in date   ,
  pend    in date
)
as
  cursor cur_trad_date(lpbegin date, lpend date) is
    select distinct(shi_jian) from tb_stock_data_daily where
      code = 'sh000001'
        and
      shi_jian >= lpbegin
        and
      shi_jian <= lpend
    order by shi_jian asc;

  cursor cur_stock_list_buy(lpshi_jian date, lpbegin date , lpend date) is
    select code from
    (
      select code,
             dpo_6ma
      from tb_stock_data_daily where
        shi_jian=lpshi_jian
          and
        kdj_k < -10
          and
        kdj_d < -10
          and
        kdj_k > kdj_d
          and
        dpo_dpo > dpo_6ma
          and
        kdj_k   is not null
          and
        kdj_d   is not null
          and
        kdj_j   is not null
          and
        dpo_dpo is not null
    )
    where 
      code not in
      (
        select code from
        (
	        select code,count(1) from tb_stock_data_daily where
	          shi_jian >= lpbegin
	            and
	          shi_jian <= lpend
	            and
	          price_today_open=0 
	        group by code 
	        having count(1) > 0 
	      )
      )
    order by dpo_6ma asc;

  cursor cur_stock_list_sel(lpshi_jian date,lptaskid number) is
    select code from
    (
      select code ,
             dpo_6ma
      from tb_stock_data_daily where
        code in
        (
           select code from tb_trading_test_Volume where
             task_id = lptaskid
               and
             Volume > 0
        )
          and
        shi_jian=lpshi_jian
          and
        
        (
          kdj_k >= 70 
            or
          kdj_d >= 70
        )
          and
        (
          kdj_k < kdj_d
            or
          dpo_dpo < dpo_6ma
        )
    )
    --where
    --  dpo_dpo <= last_dpo_dpo
    --    and
    --  dpo_6ma <= last_dpo_6ma
    order by dpo_6ma desc;

  cursor cur_stock_data(lpcode varchar2,lpshi_jian date) is
    select * from
    (
      select kdj_j    ,
             kdj_d    ,
             kdj_k    ,
             dpo_dpo  ,
             dpo_6ma  ,
             price_today_open ,
             price            ,
             price_last_day   ,
             shi_jian         ,
             MA12 ,
             lag(kdj_j  ,1,null)           over(order by shi_jian asc) last_kdj_j            ,
             lag(kdj_d  ,1,null)           over(order by shi_jian asc) last_kdj_d            ,
             lag(kdj_k  ,1,null)           over(order by shi_jian asc) last_kdj_k            ,
             lag(dpo_dpo,1,null)           over(order by shi_jian asc) last_dpo_dpo          ,
             lag(dpo_6ma,1,null)           over(order by shi_jian asc) last_dpo_6ma          ,
             lag(price_today_open,1,null)  over(order by shi_jian asc) last_price_today_open ,
             lag(shi_jian,1,null)          over(order by shi_jian asc) last_shi_jian         ,
             lag(MA12,1,null)              over(order by shi_jian asc) last_MA12             ,
             Lead(price_today_open,1,null) over(order by shi_jian asc) next_price_today_open ,
             Lead(shi_jian,1,null)         over(order by shi_jian asc) next_shi_jian
      from tb_stock_data_daily where
        code = lpcode
    )
    where
      shi_jian = lpshi_jian ;

  rt_trad_date      cur_trad_date%rowtype ;
  rt_stock_list_buy cur_stock_list_buy%rowtype ;
  rt_stock_list_sel cur_stock_list_sel%rowtype ;
  rt_stock_data     cur_stock_data%rowtype ;

  nKDJ_K number ;
  nKDJ_D number ;
  nKDJ_J number ;
  nDPO_DPO number;
  nDPO_6MA number;

  ncount number ;
  ntmp   number ;

  nres   number ;
  
  dtemp date ;
  stemp varchar2(1024);
  ntemp number ;
  btemp boolean;
begin
  nRes := 999 ;

  for rt_trad_date in cur_trad_date(pbegin,pend) loop
    dtemp := rt_trad_date.shi_jian ;
    ncount := 0 ;

    for rt_stock_list_buy in cur_stock_list_buy(rt_trad_date.shi_jian,pbegin,pend) loop
      stemp := rt_stock_list_buy.code ;
      select count(1) into ntmp from tb_trading_test_Volume where
        task_id = ptaskid
          and
        code = rt_stock_list_buy.code ;

      if ntmp > 0 then
        continue ;
      end if ;

      open cur_stock_data(rt_stock_list_buy.code , rt_trad_date.shi_jian) ;
      --open cur_stock_data(stemp , dtemp) ;
      ntemp := cur_stock_data%ROWCOUNT ;
      btemp := cur_stock_data%found ;
      btemp := cur_stock_data%notfound ;
      fetch cur_stock_data into rt_stock_data ;
      close cur_stock_data ;

      --if rt_stock_data.dpo_dpo >= rt_stock_data.last_dpo_dpo and rt_stock_data.dpo_6ma >= rt_stock_data.last_dpo_6ma /*and rt_stock_data.MA12 > rt_stock_data.last_MA12*/ then

        stemp := rt_stock_list_buy.code ;
        ntemp := rt_stock_data.next_price_today_open ;
        dtemp := rt_stock_data.next_shi_jian ;

        if  rt_stock_data.next_price_today_open is not null then
	        nres := func_trading_test_buy( ptaskid ,
	                                       rt_stock_list_buy.code ,
	                                       rt_stock_data.next_price_today_open ,
	                                       rt_stock_data.next_shi_jian
	                                     );
	        ncount := ncount + 1 ;
	      end if ;
      --end if ; 
      exit when ncount>=4;
    end loop;

    select count(1) into ntmp from tb_trading_test_Volume where
      task_id = ptaskid
        and
      Volume > 0;

    if ntmp < 1 then
      continue ;
    end if ;

    for rt_stock_list_sel in cur_stock_list_sel(rt_trad_date.shi_jian,ptaskid) loop

      open cur_stock_data(rt_stock_list_sel.code , rt_trad_date.shi_jian) ;
      fetch cur_stock_data into rt_stock_data ;
      close cur_stock_data ;
      
      --if rt_stock_data.dpo_dpo < rt_stock_data.last_dpo_dpo and rt_stock_data.dpo_6ma < rt_stock_data.last_dpo_6ma then
        nres := func_trading_test_sel( ptaskid ,
                                       rt_stock_list_sel.code ,
                                       rt_stock_data.next_price_today_open ,
                                       rt_stock_data.next_shi_jian
                                     );
      --end if ;
      
    end loop ;
  end loop;
  commit;
  --return nRes ;
end;
/