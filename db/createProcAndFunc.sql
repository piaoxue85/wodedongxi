connect c##stock/didierg160@myoracle ;

create or replace procedure proc_clear_all
as
begin
  delete tb_stock_data_Daily      ;                    
  delete tb_stock_data_weekly     ;
  delete tb_stock_data_monthly    ;
  delete tb_stock_data_Quarterly  ;
  delete tb_stock_data_halfYearly ;
  delete tb_stock_data_Yearly     ;		
  commit;
end; 
/

create or replace procedure proc_get_all
as
begin
  proc_stock_get_week_all     ;
  proc_stock_get_month_all    ;
  proc_stock_get_Quarter_all  ;
  proc_stock_get_HalfYear_all ;
  proc_stock_get_Year_all     ;
  commit;
end; 
/
create or replace function fun_stock_ema
(
  pValue     in number ,
  pLastValue in number ,
  pN         in number 
)
return number 
is 
begin  
  return (2*pValue+(pN-1)*pLastValue)/(pN+1) ;  
end;
/

create or replace function f_getHalfYear
(
  pTime in date
)
return varchar2
is
  vRes varchar2(6) ;
begin
  select to_char(pTime , 'yyyy' ) || decode( to_char(pTime,'mm') ,
                                             01 , 01 ,
                                             02 , 01 ,
                                             03 , 01 ,
                                             04 , 01 ,
                                             05 , 01 ,
                                             06 , 01 ,
                                             07 , 02 ,
                                             08 , 02 ,
                                             09 , 02 ,
                                             10 , 02 ,
                                             11 , 02 ,
                                             12 , 02 
                                           ) into vRes 
  from dual; 
                                           
  return vRes;                                            
end; 
/

create or replace function f_truncHalfYear
(
  pTime in date
)
return date
is
 dRes date ;
 vRes varchar2(6);
begin
  vRes := f_getHalfYear(pTime);
  
  if substr(vRes,5)='1' then
    dRes := to_date(substr(vRes,1,4)||'0101000000','yyyymmddhh24miss');
  else
    dRes := to_date(substr(vRes,1,4)||'0701000000','yyyymmddhh24miss');
  end if ;
                              
  return dRes; 
end; 
/

create or replace procedure proc_stock_get_week_kdj
(
  pcode     in   varchar2 ,
  pprice    in   number   ,
  pk        out  number   ,
  pd        out  number   ,
  pj        out  number     
)
as
  type array_number is varray(4) of number;     
  setting array_number:=array_number(9,3,3,2);    
  
  nmax_price number ;
  nmin_price number ;
  
  nrsv number ;
  nLn  number ;
  nHn  number ;
  nK   number ;
  nd   number ;
  nJ   number ;
  
  ncounter number ;
begin
  --KDJSetting.Add(9);   //kdj天参数
  --KDJSetting.Add(2);   //k
  --KDJSetting.Add(3);   //d
  --KDJSetting.Add(2);   //j形态参数

  select max(max_price) ,
         min(min_price) ,
         count(1)
          into
         nHn ,
         nLn ,
         ncounter
  from
  (
    select * from
    (
      select max_price , min_price from tb_stock_data_weekly where code = pcode order by shi_jian desc
    )
    WHERE ROWNUM <=setting(1)
  );

  if ncounter < setting(1) - 1 then
    return;
  end if;

  if (nHn - nLn) <>0 then

    nrsv :=((pprice - nLn )/(nHn - nLn))*100 ;
  
    nk := null ;
    nd := null ;
    nj := null ;

    select KDJ_K,KDJ_d,KDJ_j into nk,nd,nj from
    (
      select * from
      (
        select KDJ_K,KDJ_d,KDJ_j,shi_jian from tb_stock_data_weekly where code = pcode order by shi_jian desc
      )
      where
        rownum<3
      order by shi_jian asc
    )
    where
      rownum<2;

    if nk is null then
      pk:=50.0 ;
      pd:=50.0 ;
      pj:=null ;
    else
      if nk is null then
        pk := 2/3*50  + (1/3)*nrsv ;
        pd := 2/3*50  + (1/3)*pk    ;
      else
        pk := ( 2/3* nk )+ (1/3)*nrsv ;
        pd := ( 2/3* nd )+ (1/3)*pk  ;
      end if;

      if  setting(4) = 1   then
        pj := 3*pd - 2*pk ;
      else
        pj := 3*pk - 2*pd ;
      end if;
    end if;


  else
    pk:=50.0 ;
    pd:=50.0 ;
    pj:=null ;
  end if ;

end;
/


create or replace procedure proc_stock_get_week_ma
(
  pcode    in  varchar2 ,
  pMA6      out number ,
  pMA12     out number ,
  pMA20     out number ,
  pMA30     out number ,
  pMA45     out number ,
  pMA60     out number ,
  pMA125    out number ,
  pMA250    out number 
)
as
  type array_number is varray(8) of number;     
  setting array_number:=array_number
  (
   6   ,
   12  ,
   20  ,
   30  ,
   45  ,
   60  ,
   125 ,
   250
  );  
  
  nLoop number ;
  
  nMa       number;
  nCounter  number; 
begin

  pMA6   := null ;
  pMA12  := null ;
  pMA20  := null ;
  pMA30  := null ;
  pMA45  := null ;
  pMA60  := null ;
  pMA125 := null ;
  pMA250 := null ;
  
  nloop := 1 ;
  
  for nLoop in 1..setting.count loop
    select sum(price)/count(1) ,
           count(1) 
             into
           nMa ,
           nCounter 
    from 
    (
      select price from tb_stock_data_weekly where 
        code = pcode 
        order by shi_jian desc         
    )
    where
    rownum<= setting(nLoop) ;
           
    if nCounter < setting(nLoop) then
      continue ;
    end if; 
    
    CASE setting(nLoop)  
      WHEN 6   THEN pMA6   := nMa ;   
      WHEN 12  THEN pMA12  := nMa ;  
      WHEN 20  THEN pMA20  := nMa ;        
      WHEN 30  THEN pMA30  := nMa ;   
      WHEN 45  THEN pMA45  := nMa ; 
      WHEN 60  THEN pMA60  := nMa ; 
      WHEN 125 THEN pMA125 := nMa ; 
      WHEN 250 THEN pMA250 := nMa ; 
    end case ;      
  end loop ;

end;
/

create or replace procedure proc_stock_get_week_XSTD
(
  pCode   in  varchar2 ,
  pEmaVal1_SLONG  in out number,
  pEmaVal1_SSHORT in out number,
  pEmaVal1_LLONG  in out number,
  pEmaVal1_LSHORT in out number,
  pEmaVal2_SLONG  in out number,
  pEmaVal2_SSHORT in out number,
  pEmaVal2_LLONG  in out number,
  pEmaVal2_LSHORT in out number,
  pSLONG  out number , 
  pSSHORT out number , 
  pLLONG  out number , 
  pLSHORT out number  
)
as
--[0]-SLONG , [1]-SSHORT , [2]-LLONG , [3]-LSHORT
  --nEmaVal1_SLONG   number ;
  --nEmaVal1_SSHORT  number ;
  --nEmaVal1_LLONG   number ;
  --nEmaVal1_LSHORT  number ;
  nEmaVal2_SLONG   number ;
  nEmaVal2_SSHORT  number ;
  nEmaVal2_LLONG   number ;
  nEmaVal2_LSHORT  number ;
  
  ncounter  number ;
  nmax_price number ;
  nmin_price number ;
begin 
  select count(1) into ncounter from tb_stock_data_weekly where code = pcode ;
  
  if  ncounter <1  then
    return ;
  end if; 
  
  select max_price,min_price into nmax_price,nmin_price from tb_stock_data_weekly where 
    code = pcode 
      and
    shi_jian = (select max(shi_jian) from tb_stock_data_weekly  where code = pcode ) ;
  
  if ncounter = 1 then 
    pEmaVal1_SLONG  :=  fun_stock_ema(nmax_price      , 0 , 1);
    pEmaVal2_SLONG  :=  fun_stock_ema(pEmaVal1_SLONG  , 0 , 1);
                                                      
    pEmaVal1_SSHORT :=  fun_stock_ema(nmin_price      , 0 , 1);  
    pEmaVal2_SSHORT :=  fun_stock_ema(pEmaVal1_SSHORT , 0 , 1);
                                                      
    pEmaVal1_LLONG  :=  fun_stock_ema(nmax_price      , 0 , 1);
    pEmaVal2_LLONG  :=  fun_stock_ema(pEmaVal1_LLONG  , 0 , 1);  
                  
    pEmaVal1_LSHORT :=  fun_stock_ema(nmin_price      , 0 , 1);
    pEmaVal2_LSHORT :=  fun_stock_ema(pEmaVal1_LSHORT , 0 , 1); 
       
  else    
    pEmaVal1_SLONG  :=  fun_stock_ema(nmax_price       , pEmaVal1_SLONG , 5 ); 
    pEmaVal2_SLONG  :=  fun_stock_ema(pEmaVal1_SLONG   , pEmaVal2_SLONG , 10); 
                                                                
    pEmaVal1_SSHORT :=  fun_stock_ema(nmin_price      , pEmaVal1_SSHORT , 5 ); 
    pEmaVal2_SSHORT :=  fun_stock_ema(pEmaVal1_SSHORT , pEmaVal2_SSHORT , 10); 
                                                                
    pEmaVal1_LLONG  :=  fun_stock_ema(nmax_price      , pEmaVal1_LLONG , 5 ); 
    pEmaVal2_LLONG  :=  fun_stock_ema(pEmaVal1_LLONG  , pEmaVal2_LLONG , 5); 
                                                                
    pEmaVal1_LSHORT :=  fun_stock_ema(nmin_price      , pEmaVal1_LSHORT , 5 ); 
    pEmaVal2_LSHORT :=  fun_stock_ema(pEmaVal1_LSHORT , pEmaVal2_LSHORT , 5); 
  
  end if;
  
  pSLONG  := pEmaVal2_SLONG  * 1.12 ; 
  pSSHORT := pEmaVal2_SSHORT * 0.86 ;
  pLLONG  := pEmaVal2_LLONG  * 1.04 ;
  pLSHORT := pEmaVal2_LSHORT * 0.94 ;

end ;
/

create or replace procedure proc_stock_get_week 
(
  pCode in varchar2 ,
  pName in varchar2
)
as
  dmax_Week       date ;
  dmin_Week       date ;
  dcursor         date ;
  nlast_price     number ; 
  nzhang_die_rate number ;  
  
  nTmp            number ;
  dTmp            date ;
  sTmp            varchar2(1) ;
  
  ncounter        number ;
  
  nK    number ;
  nd    number ;
  nJ    number ;  
  
  nMA6   number ;
  nMA12  number ;
  nMA20  number ;
  nMA30  number ;
  nMA45  number ;
  nMA60  number ;
  nMA125 number ;
  nMA250 number ; 
  
  nEmaVal1_SLONG  number ;
  nEmaVal1_SSHORT number ;
  nEmaVal1_LLONG  number ;
  nEmaVal1_LSHORT number ;

  nEmaVal2_SLONG  number ;
  nEmaVal2_SSHORT number ;
  nEmaVal2_LLONG  number ;
  nEmaVal2_LSHORT number ;     
  
  nSLONG  number ; 
  nSSHORT number ; 
  nLLONG  number ; 
  nLSHORT number ; 
 
  cursor curWeekData(stockcode varchar2 , weekCursor date) is
    select * from
    (             
       select 
              max(shi_jian)  shi_jian  ,
              sum(vol)       vol       ,
              sum(amount)    amount    ,
              max(max_price) max_price ,
              min(min_price) min_price  
       from tb_stock_data_Daily where                                
         code = stockcode
           and  
         trunc(shi_jian,'d') = weekCursor
    )a, 
    (   
      select price_today_open from tb_stock_data_Daily where 
        code = stockcode
          and 
        shi_jian = (select min(shi_jian) from tb_stock_data_Daily where 
                      code = stockcode
                        and 
                      trunc(shi_jian,'d') = weekCursor
                    ) 
    )b,
    (  
      select price from tb_stock_data_Daily where 
        code = stockcode
          and 
        shi_jian = ( 
                      select max(shi_jian) from tb_stock_data_Daily where 
                        code = stockcode
                          and 
                        trunc(shi_jian,'d') = weekCursor
                    ) 
    )c ;  
    
  rtWeekData curWeekData%rowtype ;
  
begin
  select trunc(max(shi_jian),'d') max_Week , 
         trunc(min(shi_jian),'d') min_Week 
           into 
         dmax_Week , 
         dmin_Week                    
  from tb_stock_data_Daily where code = pCode ;                   
                   
  if dmax_Week is null or dmin_Week is null then  
    return;        
  end if ;         
  
  select count(1) into ncounter from tb_stock_data_weekly where code = pcode ;
  
  if ncounter>0 then   
    --找出走表里上个周的收盘价和日表里的上周收盘价进行比较
    --如果不一致可能除权，就删掉该股票的周数据重新生成  
    select EmaVal1_SLONG  , 
           EmaVal1_SSHORT ,
           EmaVal1_LLONG  ,
           EmaVal1_LSHORT ,
           EmaVal2_SLONG  ,
           EmaVal2_SSHORT ,
           EmaVal2_LLONG  ,
           EmaVal2_LSHORT ,
           price          ,
           shi_jian 
             into 
           nEmaVal1_SLONG  ,
           nEmaVal1_SSHORT ,
           nEmaVal1_LLONG  ,
           nEmaVal1_LSHORT ,
           nEmaVal2_SLONG  ,
           nEmaVal2_SSHORT ,
           nEmaVal2_LLONG  ,
           nEmaVal2_LSHORT ,             
           nlast_price    ,
           dtmp 
    from tb_stock_data_weekly where 
      code = pcode 
        and
      shi_jian = (select max(shi_Jian) from tb_stock_data_weekly where code=pcode);
    
    /*
    select count(1) into ncounter from tb_stock_data_Daily where                                
      code = pcode                     
        and                       
      trunc(shi_jian,'d') = dtmp ;          
                         
    if ncounter >0 then                     
      open curWeekData(pcode,trunc(dtmp,'d')) ;    
      fetch curWeekData into rtWeekData ;
      close curWeekData ;      
    end if ;
    */
    open curWeekData(pcode,trunc(dtmp,'d')) ;    
    fetch curWeekData into rtWeekData ;
    close curWeekData ;        
    
    if nlast_price <> rtWeekData.price  then    
      nlast_price     := null ;
      nEmaVal1_SLONG  := null ; 
      nEmaVal1_SSHORT := null ;
      nEmaVal1_LLONG  := null ;
      nEmaVal1_LSHORT := null ;
      nEmaVal2_SLONG  := null ;
      nEmaVal2_SSHORT := null ;
      nEmaVal2_LLONG  := null ;
      nEmaVal2_LSHORT := null ;
      delete tb_stock_data_weekly where code = pcode ;
    else             
      --select trunc(max(shi_jian),'d')+7 into dmin_Week from tb_stock_data_weekly where code = pcode ; 
      dmin_Week := trunc(dtmp,'d')+7 ;
    end if ;          
  end if ;           
                     
  dcursor := dmin_Week; 
  
  while dcursor <= dmax_Week loop

    select count(1) into ncounter from tb_stock_data_Daily where                                
      code = pcode
        and  
      trunc(shi_jian,'d') = dcursor ;
    
    if ncounter < 1 then  
      dcursor := dcursor + 7 ;       
      continue ;
    end if;     
    
    open curWeekData(pCode , dcursor) ;            
    fetch curWeekData into rtWeekData;    
    close curWeekData ;      
    
    dcursor := dcursor + 7 ;
        
    if rtWeekData.max_price is null or
       rtWeekData.min_price is null or
       rtWeekData.vol       is null or
       rtWeekData.amount    is null
    then         
      continue ;    
    end if ;
    
    --if rtweekdata.shi_jian = to_date('1994-02-04 15:00:00','yyyy-mm-dd hh24:mi:ss') then
    --  sTmp := '' ;
    --end if ;        
    
		if nlast_price is null then
			nzhang_die_rate := null ;
		else
			nzhang_die_rate := rtweekdata.price/nlast_price - 1 ;
		end if ;    

    insert into tb_stock_data_weekly 
    (
      name             ,
      code             , 
      max_price        ,
      min_price        ,
      vol              ,
      amount           ,
      shi_jian         , 
      price_today_open ,
      price            ,
      zhang_die_rate         
    )
    values
    (
      pname                       ,
      pcode                       ,
      rtweekdata.max_price        ,
      rtweekdata.min_price        ,
      rtweekdata.vol              ,
      rtweekdata.amount           ,
      rtweekdata.shi_jian         ,
      rtweekdata.price_today_open ,
      rtweekdata.price            ,
      nzhang_die_rate                    
    ) ;    
    
    proc_stock_get_week_kdj( pcode    , 
                        rtweekdata.price ,
                        nk ,
                        nd ,
                        nj 
                       );
                       
    proc_stock_get_week_ma(
                       pcode ,
                       nMA6  ,
                       nMA12 ,
                       nMA20 ,
                       nMA30 ,
                       nMA45 ,
                       nMA60 ,
                       nMA125,
                       nMA250
                     ); 
                     
    proc_stock_get_week_XSTD(
                         pcode   ,
                         nEmaVal1_SLONG  , 
                         nEmaVal1_SSHORT ,
                         nEmaVal1_LLONG  ,
                         nEmaVal1_LSHORT ,
                         nEmaVal2_SLONG  ,
                         nEmaVal2_SSHORT ,
                         nEmaVal2_LLONG  ,
                         nEmaVal2_LSHORT ,                                                
                         nSLONG  , 
                         nSSHORT , 
                         nLLONG  , 
                         nLSHORT 
                       ) ;

    update tb_stock_data_weekly 
      set kdj_k          = nk             ,
          kdj_d          = nd             ,
          kdj_j          = nj             ,
          MA6            = nMA6           ,
          MA12           = nMA12          ,
          MA20           = nMA20          ,
          MA30           = nMA30          ,
          MA45           = nMA45          ,
          MA60           = nMA60          ,
          MA125          = nMA125         ,
          MA250          = nMA250         ,
          xstd_SLONG     = nSLONG         , 
          xstd_SSHORT    = nSSHORT        ,
          xstd_LLONG     = nLLONG         ,
          xstd_LSHORT    = nLSHORT        ,
          EmaVal1_SLONG  = nEmaVal1_SLONG  ,
          EmaVal1_SSHORT = nEmaVal1_SSHORT ,
          EmaVal1_LLONG  = nEmaVal1_LLONG  ,
          EmaVal1_LSHORT = nEmaVal1_LSHORT ,
          EmaVal2_SLONG  = nEmaVal2_SLONG  ,
          EmaVal2_SSHORT = nEmaVal2_SSHORT ,
          EmaVal2_LLONG  = nEmaVal2_LLONG  ,
          EmaVal2_LSHORT = nEmaVal2_LSHORT       
    where 
      code = pcode 
        and
      shi_jian = rtweekdata.shi_jian ;
    
    nlast_price := rtweekdata.price ;  

  end loop ;

  delete tb_stock_data_weekly where trunc(shi_jian,'d') = trunc(sysdate+1,'d');
  
  commit;
  
  

end;
/


create or replace procedure proc_stock_get_week_all
as
  cursor cur is 
    select code , name from tb_stock_list where 
      code in 
      (
      	select distinct(code) from tb_stock_data_daily 
      ) ;
  
  rtcur cur%rowtype ;  
  ncounter number ;
  nval number;
begin
  delete tb_stock_data_Daily where amount = 0; 
  
  delete tb_stock_data_weekly where 
    code in 
    (
      select distinct(code) from  tb_stock_data_weekly     where amount = 0 
    );  
  
  commit;
  
  for rt in cur loop
    proc_stock_get_week(rt.code,rt.name);
        
    select sum(c)-1 into ncounter from
    (
	    select count(1) c from dual 
	      union
	    select count(1) c  from 
	    (
	        select code,name from tb_stock_data_weekly where code = rt.code group by code,name
	    )
	    group by code 
    );    
    
    if ncounter > 1 then
      update tb_stock_data_weekly set name = rt.name  where code = rt.code ;
    end if ;
  end loop ;
  
  insert into tb_stock_job_done values ('week',sysdate);
  commit;
end ;
/




create or replace procedure proc_stock_get_month_kdj
(
  pcode     in   varchar2 ,
  pprice    in   number   ,
  pk        out  number   ,
  pd        out  number   ,
  pj        out  number     
)
as
  type array_number is varray(4) of number;     
  setting array_number:=array_number(9,3,3,2);    
  
  nmax_price number ;
  nmin_price number ;
  
  nrsv number ;
  nLn  number ;
  nHn  number ;
  nK   number ;
  nd   number ;
  nJ   number ;
  
  ncounter number ;
begin
  --KDJSetting.Add(9);   //kdj天参数
  --KDJSetting.Add(2);   //k
  --KDJSetting.Add(3);   //d
  --KDJSetting.Add(2);   //j形态参数

  select max(max_price) ,
         min(min_price) ,
         count(1)
          into
         nHn ,
         nLn ,
         ncounter
  from
  (
    select * from
    (
      select max_price , min_price from tb_stock_data_monthly where code = pcode order by shi_jian desc
    )
    WHERE ROWNUM <=setting(1)
  );

  if ncounter < setting(1) - 1 then
    return;
  end if;

  if (nHn - nLn) <>0 then

    nrsv :=((pprice - nLn )/(nHn - nLn))*100 ;
  
    nk := null ;
    nd := null ;
    nj := null ;

    select KDJ_K,KDJ_d,KDJ_j into nk,nd,nj from
    (
      select * from
      (
        select KDJ_K,KDJ_d,KDJ_j,shi_jian from tb_stock_data_monthly where code = pcode order by shi_jian desc
      )
      where
        rownum<3
      order by shi_jian asc
    )
    where
      rownum<2;

    if nk is null then
      pk:=50.0 ;
      pd:=50.0 ;
      pj:=null ;
    else
      if nk is null then
        pk := 2/3*50  + (1/3)*nrsv ;
        pd := 2/3*50  + (1/3)*pk    ;
      else
        pk := ( 2/3* nk )+ (1/3)*nrsv ;
        pd := ( 2/3* nd )+ (1/3)*pk  ;
      end if;

      if  setting(4) = 1   then
        pj := 3*pd - 2*pk ;
      else
        pj := 3*pk - 2*pd ;
      end if;
    end if;


  else
    pk:=50.0 ;
    pd:=50.0 ;
    pj:=null ;
  end if ;

end;
/


create or replace procedure proc_stock_get_month_ma
(
  pcode    in  varchar2 ,
  pMA6      out number ,
  pMA12     out number ,
  pMA20     out number ,
  pMA30     out number ,
  pMA45     out number ,
  pMA60     out number ,
  pMA125    out number ,
  pMA250    out number 
)
as
  type array_number is varray(8) of number;     
  setting array_number:=array_number
  (
   6   ,
   12  ,
   20  ,
   30  ,
   45  ,
   60  ,
   125 ,
   250
  );  
  
  nLoop number ;
  
  nMa       number;
  nCounter  number; 
begin

  pMA6   := null ;
  pMA12  := null ;
  pMA20  := null ;
  pMA30  := null ;
  pMA45  := null ;
  pMA60  := null ;
  pMA125 := null ;
  pMA250 := null ;
  
  nloop := 1 ;
  
  for nLoop in 1..setting.count loop
    select sum(price)/count(1) ,
           count(1) 
             into
           nMa ,
           nCounter 
    from 
    (
      select price from tb_stock_data_monthly where 
        code = pcode 
        order by shi_jian desc         
    )
    where
    rownum<= setting(nLoop) ;
           
    if nCounter < setting(nLoop) then
      continue ;
    end if; 
    
    CASE setting(nLoop)  
      WHEN 6   THEN pMA6   := nMa ;   
      WHEN 12  THEN pMA12  := nMa ;  
      WHEN 20  THEN pMA20  := nMa ;        
      WHEN 30  THEN pMA30  := nMa ;   
      WHEN 45  THEN pMA45  := nMa ; 
      WHEN 60  THEN pMA60  := nMa ; 
      WHEN 125 THEN pMA125 := nMa ; 
      WHEN 250 THEN pMA250 := nMa ; 
    end case ;      
  end loop ;

end;
/

create or replace procedure proc_stock_get_month_XSTD
(
  pCode   in  varchar2 ,
  pEmaVal1_SLONG  in out number,
  pEmaVal1_SSHORT in out number,
  pEmaVal1_LLONG  in out number,
  pEmaVal1_LSHORT in out number,
  pEmaVal2_SLONG  in out number,
  pEmaVal2_SSHORT in out number,
  pEmaVal2_LLONG  in out number,
  pEmaVal2_LSHORT in out number,
  pSLONG  out number , 
  pSSHORT out number , 
  pLLONG  out number , 
  pLSHORT out number  
)
as
--[0]-SLONG , [1]-SSHORT , [2]-LLONG , [3]-LSHORT
  --nEmaVal1_SLONG   number ;
  --nEmaVal1_SSHORT  number ;
  --nEmaVal1_LLONG   number ;
  --nEmaVal1_LSHORT  number ;
  nEmaVal2_SLONG   number ;
  nEmaVal2_SSHORT  number ;
  nEmaVal2_LLONG   number ;
  nEmaVal2_LSHORT  number ;
  
  ncounter  number ;
  nmax_price number ;
  nmin_price number ;
begin 
  select count(1) into ncounter from tb_stock_data_monthly where code = pcode ;
  
  if  ncounter <1  then
    return ;
  end if; 
  
  select max_price,min_price into nmax_price,nmin_price from tb_stock_data_monthly where 
    code = pcode 
      and
    shi_jian = (select max(shi_jian) from tb_stock_data_monthly  where code = pcode ) ;
  
  if ncounter = 1 then 
    pEmaVal1_SLONG  :=  fun_stock_ema(nmax_price      , 0 , 1);
    pEmaVal2_SLONG  :=  fun_stock_ema(pEmaVal1_SLONG  , 0 , 1);
                                                      
    pEmaVal1_SSHORT :=  fun_stock_ema(nmin_price      , 0 , 1);  
    pEmaVal2_SSHORT :=  fun_stock_ema(pEmaVal1_SSHORT , 0 , 1);
                                                      
    pEmaVal1_LLONG  :=  fun_stock_ema(nmax_price      , 0 , 1);
    pEmaVal2_LLONG  :=  fun_stock_ema(pEmaVal1_LLONG  , 0 , 1);  
                  
    pEmaVal1_LSHORT :=  fun_stock_ema(nmin_price      , 0 , 1);
    pEmaVal2_LSHORT :=  fun_stock_ema(pEmaVal1_LSHORT , 0 , 1); 
       
  else    
    pEmaVal1_SLONG  :=  fun_stock_ema(nmax_price       , pEmaVal1_SLONG , 5 ); 
    pEmaVal2_SLONG  :=  fun_stock_ema(pEmaVal1_SLONG   , pEmaVal2_SLONG , 10); 
                                                                
    pEmaVal1_SSHORT :=  fun_stock_ema(nmin_price      , pEmaVal1_SSHORT , 5 ); 
    pEmaVal2_SSHORT :=  fun_stock_ema(pEmaVal1_SSHORT , pEmaVal2_SSHORT , 10); 
                                                                
    pEmaVal1_LLONG  :=  fun_stock_ema(nmax_price      , pEmaVal1_LLONG , 5 ); 
    pEmaVal2_LLONG  :=  fun_stock_ema(pEmaVal1_LLONG  , pEmaVal2_LLONG , 5); 
                                                                
    pEmaVal1_LSHORT :=  fun_stock_ema(nmin_price      , pEmaVal1_LSHORT , 5 ); 
    pEmaVal2_LSHORT :=  fun_stock_ema(pEmaVal1_LSHORT , pEmaVal2_LSHORT , 5); 
  
  end if;
  
  pSLONG  := pEmaVal2_SLONG  * 1.12 ; 
  pSSHORT := pEmaVal2_SSHORT * 0.86 ;
  pLLONG  := pEmaVal2_LLONG  * 1.04 ;
  pLSHORT := pEmaVal2_LSHORT * 0.94 ;

end ;
/



create or replace procedure proc_stock_get_month
(
  pCode in varchar2 ,
  pName in varchar2
)
as
  dmax_month  date ;
  dmin_month  date ;
  dcursor     date ;
  nlast_price     number ; 
  nzhang_die_rate number ;
              
  nTmp        number ;
  dTmp        date ;
  sTmp        varchar2(1) ;
              
  ncounter    number ;
  
  nK    number ;
  nd    number ;
  nJ    number ;  
  
  nMA6   number ;
  nMA12  number ;
  nMA20  number ;
  nMA30  number ;
  nMA45  number ;
  nMA60  number ;
  nMA125 number ;
  nMA250 number ; 
  
  nEmaVal1_SLONG  number ;
  nEmaVal1_SSHORT number ;
  nEmaVal1_LLONG  number ;
  nEmaVal1_LSHORT number ;

  nEmaVal2_SLONG  number ;
  nEmaVal2_SSHORT number ;
  nEmaVal2_LLONG  number ;
  nEmaVal2_LSHORT number ;     
  
  nSLONG  number ; 
  nSSHORT number ; 
  nLLONG  number ; 
  nLSHORT number ; 
 
  cursor curmonthData(stockcode varchar2 , monthCursor date) is
    select * from
    (             
       select 
              max(shi_jian)  shi_jian  ,
              sum(vol)       vol       ,
              sum(amount)    amount    ,
              max(max_price) max_price ,
              min(min_price) min_price  
       from tb_stock_data_Daily where                                
         code = stockcode
           and  
         trunc(shi_jian,'month') = monthCursor
    )a, 
    (   
      select price_today_open from tb_stock_data_Daily where 
        code = stockcode
          and 
        shi_jian = (select min(shi_jian) from tb_stock_data_Daily where 
                      code = stockcode
                        and 
                      trunc(shi_jian,'month') = monthCursor
                    ) 
    )b,
    (  
      select price from tb_stock_data_Daily where 
        code = stockcode
          and 
        shi_jian = ( 
                      select max(shi_jian) from tb_stock_data_Daily where 
                        code = stockcode
                          and 
                        trunc(shi_jian,'month') = monthCursor
                    ) 
    )c ;  
    
  rtmonthData curmonthData%rowtype ;
  
begin
  select trunc(max(shi_jian),'month') max_month , 
         trunc(min(shi_jian),'month') min_month 
           into 
         dmax_month , 
         dmin_month
  from tb_stock_data_Daily where code = pCode ;                   
                   
  if dmax_month is null or dmin_month is null then  
    return;        
  end if ;         
  
  select count(1) into ncounter from tb_stock_data_monthly where code = pcode ;
  
  if ncounter>0 then   
    --找出走表里上个周的收盘价和日表里的上周收盘价进行比较
    --如果不一致可能除权，就删掉该股票的周数据重新生成  
    select EmaVal1_SLONG  , 
           EmaVal1_SSHORT ,
           EmaVal1_LLONG  ,
           EmaVal1_LSHORT ,
           EmaVal2_SLONG  ,
           EmaVal2_SSHORT ,
           EmaVal2_LLONG  ,
           EmaVal2_LSHORT ,
           price          ,
           shi_jian 
             into 
           nEmaVal1_SLONG  ,
           nEmaVal1_SSHORT ,
           nEmaVal1_LLONG  ,
           nEmaVal1_LSHORT ,
           nEmaVal2_SLONG  ,
           nEmaVal2_SSHORT ,
           nEmaVal2_LLONG  ,
           nEmaVal2_LSHORT ,             
           nlast_price    ,
           dtmp 
    from tb_stock_data_monthly where 
      code = pcode 
        and
      shi_jian = (select max(shi_Jian) from tb_stock_data_monthly where code=pcode);
    
    open curmonthData(pcode,trunc(dtmp,'month')) ;    
    fetch curmonthData into rtmonthData ;
    close curmonthData ;        
    
    if nlast_price <> rtmonthData.price  then    
      nlast_price     := null ;
      nEmaVal1_SLONG  := null ; 
      nEmaVal1_SSHORT := null ;
      nEmaVal1_LLONG  := null ;
      nEmaVal1_LSHORT := null ;
      nEmaVal2_SLONG  := null ;
      nEmaVal2_SSHORT := null ;
      nEmaVal2_LLONG  := null ;
      nEmaVal2_LSHORT := null ;
      delete tb_stock_data_monthly where code = pcode ;
    else          
      dmin_month := ADD_MONTHs(trunc(dtmp,'month'),1) ;
    end if ;          
  end if ;           
                     
  dcursor := dmin_month; 
  
  while dcursor <= dmax_month loop

    select count(1) into ncounter from tb_stock_data_Daily where                                
      code = pcode
        and  
      trunc(shi_jian,'month') = dcursor ;
    
    if ncounter < 1 then  
      dcursor := ADD_MONTHs( dcursor , 1 ) ;       
      continue ;
    end if;     
    
    open curmonthData(pCode , dcursor) ;            
    fetch curmonthData into rtmonthData;    
    close curmonthData ;      
    
    dcursor := ADD_MONTHs( dcursor , 1 ) ;
        
    if rtmonthData.max_price is null or
       rtmonthData.min_price is null or
       rtmonthData.vol       is null or
       rtmonthData.amount    is null
    then         
      continue ;    
    end if ;
    
    --if rtmonthdata.shi_jian = to_date('1994-02-04 15:00:00','yyyy-mm-dd hh24:mi:ss') then
    --  sTmp := '' ;
    --end if ;        

		if nlast_price is null then
			nzhang_die_rate := null ;
		else
			nzhang_die_rate := rtmonthdata.price/nlast_price - 1 ;
		end if ;

    insert into tb_stock_data_monthly 
    (
      name             ,
      code             , 
      max_price        ,
      min_price        ,
      vol              ,
      amount           ,
      shi_jian         , 
      price_today_open ,
      price            ,
      zhang_die_rate
    )
    values
    (
      pname                        ,
      pcode                        ,
      rtmonthdata.max_price        ,
      rtmonthdata.min_price        ,
      rtmonthdata.vol              ,
      rtmonthdata.amount           ,
      rtmonthdata.shi_jian         ,
      rtmonthdata.price_today_open ,
      rtmonthdata.price            ,
      nzhang_die_rate             
    ) ;    
    
    proc_stock_get_month_kdj( 
                        pcode    , 
                        rtmonthdata.price ,
                        nk ,
                        nd ,
                        nj 
                       );
                       
    proc_stock_get_month_ma(
                       pcode ,
                       nMA6  ,
                       nMA12 ,
                       nMA20 ,
                       nMA30 ,
                       nMA45 ,
                       nMA60 ,
                       nMA125,
                       nMA250
                     ); 
                     
    proc_stock_get_month_XSTD(
                         pcode   ,
                         nEmaVal1_SLONG  , 
                         nEmaVal1_SSHORT ,
                         nEmaVal1_LLONG  ,
                         nEmaVal1_LSHORT ,
                         nEmaVal2_SLONG  ,
                         nEmaVal2_SSHORT ,
                         nEmaVal2_LLONG  ,
                         nEmaVal2_LSHORT ,
                         nSLONG  , 
                         nSSHORT , 
                         nLLONG  , 
                         nLSHORT 
                       ) ;

    update tb_stock_data_monthly 
      set kdj_k          = nk             ,
          kdj_d          = nd             ,
          kdj_j          = nj             ,
          MA6            = nMA6           ,
          MA12           = nMA12          ,
          MA20           = nMA20          ,
          MA30           = nMA30          ,
          MA45           = nMA45          ,
          MA60           = nMA60          ,
          MA125          = nMA125         ,
          MA250          = nMA250         ,
          xstd_SLONG     = nSLONG         , 
          xstd_SSHORT    = nSSHORT        ,
          xstd_LLONG     = nLLONG         ,
          xstd_LSHORT    = nLSHORT        ,
          EmaVal1_SLONG  = nEmaVal1_SLONG  ,
          EmaVal1_SSHORT = nEmaVal1_SSHORT ,
          EmaVal1_LLONG  = nEmaVal1_LLONG  ,
          EmaVal1_LSHORT = nEmaVal1_LSHORT ,
          EmaVal2_SLONG  = nEmaVal2_SLONG  ,
          EmaVal2_SSHORT = nEmaVal2_SSHORT ,
          EmaVal2_LLONG  = nEmaVal2_LLONG  ,
          EmaVal2_LSHORT = nEmaVal2_LSHORT       
    where 
      code = pcode 
        and
      shi_jian = rtmonthdata.shi_jian ;
    
    nlast_price := rtmonthdata.price ;  

  end loop ;
  
  delete tb_stock_data_monthly where trunc(shi_jian,'month') = trunc(sysdate,'month') ;
  commit;

end;
/

create or replace procedure proc_stock_get_month_all
as
  cursor cur is 
    select code , name from tb_stock_list where 
      code in 
      (
      	select distinct(code) from tb_stock_data_daily 
      ) ;
  
  rtcur cur%rowtype ;  
  ncounter number ;
begin
  delete tb_stock_data_monthly    where code in (select distinct(code) from  tb_stock_data_monthly    where amount = 0 );
  commit;
  for rt in cur loop    
    proc_stock_get_month(rt.code,rt.name);
    
    select sum(c)-1 into ncounter from
    (
	    select count(1) c from dual 
	      union
	    select count(1) c  from 
	    (
	        select code,name from tb_stock_data_monthly where code = rt.code group by code,name
	    )
	    group by code 
    );
    
    if ncounter > 1 then
      update tb_stock_data_monthly set name = rt.name where code = rt.code ;  
    end if ;    
  end loop ;
  
  insert into tb_stock_job_done values ('month',sysdate);
  commit;

end ;
/


create or replace procedure proc_stock_get_Quarter_kdj
(
  pcode     in   varchar2 ,
  pprice    in   number   ,
  pk        out  number   ,
  pd        out  number   ,
  pj        out  number     
)
as
  type array_number is varray(4) of number;     
  setting array_number:=array_number(9,3,3,2);    
  
  nmax_price number ;
  nmin_price number ;
  
  nrsv number ;
  nLn  number ;
  nHn  number ;
  nK   number ;
  nd   number ;
  nJ   number ;
  
  ncounter number ;
begin
  --KDJSetting.Add(9);   //kdj天参数
  --KDJSetting.Add(2);   //k
  --KDJSetting.Add(3);   //d
  --KDJSetting.Add(2);   //j形态参数

  select max(max_price) ,
         min(min_price) ,
         count(1)
          into
         nHn ,
         nLn ,
         ncounter
  from
  (
    select * from
    (
      select max_price , min_price from tb_stock_data_Quarterly where code = pcode order by shi_jian desc
    )
    WHERE ROWNUM <=setting(1)
  );

  if ncounter < setting(1) - 1 then
    return;
  end if;

  if (nHn - nLn) <>0 then

    nrsv :=((pprice - nLn )/(nHn - nLn))*100 ;
  
    nk := null ;
    nd := null ;
    nj := null ;

    select KDJ_K,KDJ_d,KDJ_j into nk,nd,nj from
    (
      select * from
      (
        select KDJ_K,KDJ_d,KDJ_j,shi_jian from tb_stock_data_Quarterly where code = pcode order by shi_jian desc
      )
      where
        rownum<3
      order by shi_jian asc
    )
    where
      rownum<2;

    if nk is null then
      pk:=50.0 ;
      pd:=50.0 ;
      pj:=null ;
    else
      if nk is null then
        pk := 2/3*50  + (1/3)*nrsv ;
        pd := 2/3*50  + (1/3)*pk    ;
      else
        pk := ( 2/3* nk )+ (1/3)*nrsv ;
        pd := ( 2/3* nd )+ (1/3)*pk  ;
      end if;

      if  setting(4) = 1   then
        pj := 3*pd - 2*pk ;
      else
        pj := 3*pk - 2*pd ;
      end if;
    end if;


  else
    pk:=50.0 ;
    pd:=50.0 ;
    pj:=null ;
  end if ;

end;
/


create or replace procedure proc_stock_get_Quarter_ma
(
  pcode    in  varchar2 ,
  pMA6      out number ,
  pMA12     out number ,
  pMA20     out number ,
  pMA30     out number ,
  pMA45     out number ,
  pMA60     out number ,
  pMA125    out number ,
  pMA250    out number 
)
as
  type array_number is varray(8) of number;     
  setting array_number:=array_number
  (
   6   ,
   12  ,
   20  ,
   30  ,
   45  ,
   60  ,
   125 ,
   250
  );  
  
  nLoop number ;
  
  nMa       number;
  nCounter  number; 
begin

  pMA6   := null ;
  pMA12  := null ;
  pMA20  := null ;
  pMA30  := null ;
  pMA45  := null ;
  pMA60  := null ;
  pMA125 := null ;
  pMA250 := null ;
  
  nloop := 1 ;
  
  for nLoop in 1..setting.count loop
    select sum(price)/count(1) ,
           count(1) 
             into
           nMa ,
           nCounter 
    from 
    (
      select price from tb_stock_data_Quarterly where 
        code = pcode 
        order by shi_jian desc         
    )
    where
    rownum<= setting(nLoop) ;
           
    if nCounter < setting(nLoop) then
      continue ;
    end if; 
    
    CASE setting(nLoop)  
      WHEN 6   THEN pMA6   := nMa ;   
      WHEN 12  THEN pMA12  := nMa ;  
      WHEN 20  THEN pMA20  := nMa ;        
      WHEN 30  THEN pMA30  := nMa ;   
      WHEN 45  THEN pMA45  := nMa ; 
      WHEN 60  THEN pMA60  := nMa ; 
      WHEN 125 THEN pMA125 := nMa ; 
      WHEN 250 THEN pMA250 := nMa ; 
    end case ;      
  end loop ;

end;
/

create or replace procedure proc_stock_get_Quarter_XSTD
(
  pCode   in  varchar2 ,
  pEmaVal1_SLONG  in out number,
  pEmaVal1_SSHORT in out number,
  pEmaVal1_LLONG  in out number,
  pEmaVal1_LSHORT in out number,
  pEmaVal2_SLONG  in out number,
  pEmaVal2_SSHORT in out number,
  pEmaVal2_LLONG  in out number,
  pEmaVal2_LSHORT in out number,
  pSLONG  out number , 
  pSSHORT out number , 
  pLLONG  out number , 
  pLSHORT out number  
)
as
--[0]-SLONG , [1]-SSHORT , [2]-LLONG , [3]-LSHORT
  --nEmaVal1_SLONG   number ;
  --nEmaVal1_SSHORT  number ;
  --nEmaVal1_LLONG   number ;
  --nEmaVal1_LSHORT  number ;
  nEmaVal2_SLONG   number ;
  nEmaVal2_SSHORT  number ;
  nEmaVal2_LLONG   number ;
  nEmaVal2_LSHORT  number ;
  
  ncounter  number ;
  nmax_price number ;
  nmin_price number ;
begin 
  select count(1) into ncounter from tb_stock_data_Quarterly where code = pcode ;
  
  if  ncounter <1  then
    return ;
  end if; 
  
  select max_price,min_price into nmax_price,nmin_price from tb_stock_data_Quarterly where 
    code = pcode 
      and
    shi_jian = (select max(shi_jian) from tb_stock_data_Quarterly  where code = pcode ) ;
  
  if ncounter = 1 then 
    pEmaVal1_SLONG  :=  fun_stock_ema(nmax_price      , 0 , 1);
    pEmaVal2_SLONG  :=  fun_stock_ema(pEmaVal1_SLONG  , 0 , 1);
                                                      
    pEmaVal1_SSHORT :=  fun_stock_ema(nmin_price      , 0 , 1);  
    pEmaVal2_SSHORT :=  fun_stock_ema(pEmaVal1_SSHORT , 0 , 1);
                                                      
    pEmaVal1_LLONG  :=  fun_stock_ema(nmax_price      , 0 , 1);
    pEmaVal2_LLONG  :=  fun_stock_ema(pEmaVal1_LLONG  , 0 , 1);  
                  
    pEmaVal1_LSHORT :=  fun_stock_ema(nmin_price      , 0 , 1);
    pEmaVal2_LSHORT :=  fun_stock_ema(pEmaVal1_LSHORT , 0 , 1); 
       
  else    
    pEmaVal1_SLONG  :=  fun_stock_ema(nmax_price       , pEmaVal1_SLONG , 5 ); 
    pEmaVal2_SLONG  :=  fun_stock_ema(pEmaVal1_SLONG   , pEmaVal2_SLONG , 10); 
                                                                
    pEmaVal1_SSHORT :=  fun_stock_ema(nmin_price      , pEmaVal1_SSHORT , 5 ); 
    pEmaVal2_SSHORT :=  fun_stock_ema(pEmaVal1_SSHORT , pEmaVal2_SSHORT , 10); 
                                                                
    pEmaVal1_LLONG  :=  fun_stock_ema(nmax_price      , pEmaVal1_LLONG , 5 ); 
    pEmaVal2_LLONG  :=  fun_stock_ema(pEmaVal1_LLONG  , pEmaVal2_LLONG , 5); 
                                                                
    pEmaVal1_LSHORT :=  fun_stock_ema(nmin_price      , pEmaVal1_LSHORT , 5 ); 
    pEmaVal2_LSHORT :=  fun_stock_ema(pEmaVal1_LSHORT , pEmaVal2_LSHORT , 5); 
  
  end if;
  
  pSLONG  := pEmaVal2_SLONG  * 1.12 ; 
  pSSHORT := pEmaVal2_SSHORT * 0.86 ;
  pLLONG  := pEmaVal2_LLONG  * 1.04 ;
  pLSHORT := pEmaVal2_LSHORT * 0.94 ;

end ;
/

create or replace procedure proc_stock_get_Quarter
(
  pCode in varchar2 ,
  pName in varchar2
)
as
  dmax_Quarter  date ;
  dmin_Quarter  date ;
  dcursor       date ;
  nlast_price     number ; 
  nzhang_die_rate number ;
              
  nTmp        number ;
  dTmp        date ;
  sTmp        varchar2(1) ;
              
  ncounter    number ;
  
  nK    number ;
  nd    number ;
  nJ    number ;  
  
  nMA6   number ;
  nMA12  number ;
  nMA20  number ;
  nMA30  number ;
  nMA45  number ;
  nMA60  number ;
  nMA125 number ;
  nMA250 number ; 
  
  nEmaVal1_SLONG  number ;
  nEmaVal1_SSHORT number ;
  nEmaVal1_LLONG  number ;
  nEmaVal1_LSHORT number ;

  nEmaVal2_SLONG  number ;
  nEmaVal2_SSHORT number ;
  nEmaVal2_LLONG  number ;
  nEmaVal2_LSHORT number ;     
  
  nSLONG  number ; 
  nSSHORT number ; 
  nLLONG  number ; 
  nLSHORT number ; 
 
  cursor curQuarterData(stockcode varchar2 , QuarterCursor date) is
    select * from
    (             
       select 
              max(shi_jian)  shi_jian  ,
              sum(vol)       vol       ,
              sum(amount)    amount    ,
              max(max_price) max_price ,
              min(min_price) min_price  
       from tb_stock_data_Daily where                                
         code = stockcode
           and  
         trunc(shi_jian,'q') = QuarterCursor
    )a, 
    (   
      select price_today_open from tb_stock_data_Daily where 
        code = stockcode
          and 
        shi_jian = (select min(shi_jian) from tb_stock_data_Daily where 
                      code = stockcode
                        and 
                      trunc(shi_jian,'q') = QuarterCursor
                    ) 
    )b,
    (  
      select price from tb_stock_data_Daily where 
        code = stockcode
          and 
        shi_jian = ( 
                      select max(shi_jian) from tb_stock_data_Daily where 
                        code = stockcode
                          and 
                        trunc(shi_jian,'q') = QuarterCursor
                    ) 
    )c ;  
    
  rtQuarterData curQuarterData%rowtype ;
  
begin
  
  select trunc(max(shi_jian),'q') max_Quarter , 
         trunc(min(shi_jian),'q') min_Quarter 
           into 
         dmax_Quarter , 
         dmin_Quarter
  from tb_stock_data_Daily where code = pCode ;                   
                   
  if dmax_Quarter is null or dmin_Quarter is null then  
    return;        
  end if ;         
  
  select count(1) into ncounter from tb_stock_data_Quarterly where code = pcode ;
  
  if ncounter>0 then   
    --找出走表里上个周的收盘价和日表里的上周收盘价进行比较
    --如果不一致可能除权，就删掉该股票的周数据重新生成  
    select EmaVal1_SLONG  , 
           EmaVal1_SSHORT ,
           EmaVal1_LLONG  ,
           EmaVal1_LSHORT ,
           EmaVal2_SLONG  ,
           EmaVal2_SSHORT ,
           EmaVal2_LLONG  ,
           EmaVal2_LSHORT ,
           price          ,
           shi_jian 
             into 
           nEmaVal1_SLONG  ,
           nEmaVal1_SSHORT ,
           nEmaVal1_LLONG  ,
           nEmaVal1_LSHORT ,
           nEmaVal2_SLONG  ,
           nEmaVal2_SSHORT ,
           nEmaVal2_LLONG  ,
           nEmaVal2_LSHORT ,             
           nlast_price    ,
           dtmp 
    from tb_stock_data_Quarterly where 
      code = pcode 
        and
      shi_jian = (select max(shi_Jian) from tb_stock_data_Quarterly where code=pcode);
    
    open curQuarterData(pcode,trunc(dtmp,'q')) ;    
    fetch curQuarterData into rtQuarterData ;
    close curQuarterData ;        
    
    if nlast_price <> rtQuarterData.price  then    
      nlast_price     := null ;
      nEmaVal1_SLONG  := null ; 
      nEmaVal1_SSHORT := null ;
      nEmaVal1_LLONG  := null ;
      nEmaVal1_LSHORT := null ;
      nEmaVal2_SLONG  := null ;
      nEmaVal2_SSHORT := null ;
      nEmaVal2_LLONG  := null ;
      nEmaVal2_LSHORT := null ;
      delete tb_stock_data_Quarterly where code = pcode ;
    else          
      dmin_Quarter := add_months(trunc(dtmp,'q'),3) ;
    end if ;          
  end if ;           
                     
  dcursor := dmin_Quarter; 
  
  while dcursor <= dmax_Quarter loop

    select count(1) into ncounter from tb_stock_data_Daily where                                
      code = pcode
        and  
      trunc(shi_jian,'q') = dcursor ;
    
    if ncounter < 1 then  
      dcursor := add_months( dcursor , 3 ) ;       
      continue ;
    end if;     
    
    open  curQuarterData(pCode , dcursor) ;            
    fetch curQuarterData into rtQuarterData;    
    close curQuarterData ;      
    
    dcursor := add_months( dcursor , 3 ) ;
        
    if rtQuarterData.max_price is null or
       rtQuarterData.min_price is null or
       rtQuarterData.vol       is null or
       rtQuarterData.amount    is null
    then         
      continue ;    
    end if ;
    
    --if rtQuarterdata.shi_jian = to_date('1994-02-04 15:00:00','yyyy-mm-dd hh24:mi:ss') then
    --  sTmp := '' ;
    --end if ;
    
		if nlast_price is null then
			nzhang_die_rate := null ;
		else
			nzhang_die_rate := rtQuarterdata.price/nlast_price - 1 ;
		end if ;            

    insert into tb_stock_data_Quarterly 
    (
      name             ,
      code             , 
      max_price        ,
      min_price        ,
      vol              ,
      amount           ,
      shi_jian         , 
      price_today_open ,
      price            ,
      zhang_die_rate         
    )
    values
    (
      pname                       ,
      pcode                       ,
      rtQuarterdata.max_price        ,
      rtQuarterdata.min_price        ,
      rtQuarterdata.vol              ,
      rtQuarterdata.amount           ,
      rtQuarterdata.shi_jian         ,
      rtQuarterdata.price_today_open ,
      rtQuarterdata.price            ,
      nzhang_die_rate                     
    ) ;    
    
    proc_stock_get_Quarter_kdj( 
                        pcode    , 
                        rtQuarterdata.price ,
                        nk ,
                        nd ,
                        nj 
                       );
                       
    proc_stock_get_Quarter_ma(
                       pcode ,
                       nMA6  ,
                       nMA12 ,
                       nMA20 ,
                       nMA30 ,
                       nMA45 ,
                       nMA60 ,
                       nMA125,
                       nMA250
                     ); 
                     
    proc_stock_get_Quarter_XSTD(
                         pcode   ,
                         nEmaVal1_SLONG  , 
                         nEmaVal1_SSHORT ,
                         nEmaVal1_LLONG  ,
                         nEmaVal1_LSHORT ,
                         nEmaVal2_SLONG  ,
                         nEmaVal2_SSHORT ,
                         nEmaVal2_LLONG  ,
                         nEmaVal2_LSHORT ,                                                
                         nSLONG  , 
                         nSSHORT , 
                         nLLONG  , 
                         nLSHORT 
                       ) ;

    update tb_stock_data_Quarterly 
      set kdj_k          = nk             ,
          kdj_d          = nd             ,
          kdj_j          = nj             ,
          MA6            = nMA6           ,
          MA12           = nMA12          ,
          MA20           = nMA20          ,
          MA30           = nMA30          ,
          MA45           = nMA45          ,
          MA60           = nMA60          ,
          MA125          = nMA125         ,
          MA250          = nMA250         ,
          xstd_SLONG     = nSLONG         , 
          xstd_SSHORT    = nSSHORT        ,
          xstd_LLONG     = nLLONG         ,
          xstd_LSHORT    = nLSHORT        ,
          EmaVal1_SLONG  = nEmaVal1_SLONG  ,
          EmaVal1_SSHORT = nEmaVal1_SSHORT ,
          EmaVal1_LLONG  = nEmaVal1_LLONG  ,
          EmaVal1_LSHORT = nEmaVal1_LSHORT ,
          EmaVal2_SLONG  = nEmaVal2_SLONG  ,
          EmaVal2_SSHORT = nEmaVal2_SSHORT ,
          EmaVal2_LLONG  = nEmaVal2_LLONG  ,
          EmaVal2_LSHORT = nEmaVal2_LSHORT       
    where 
      code = pcode 
        and
      shi_jian = rtQuarterdata.shi_jian ;
    
    nlast_price := rtQuarterdata.price ;  

  end loop ;
  commit;

end;
/

create or replace procedure proc_stock_get_Quarter_all
as
  cursor cur is 
    select code , name from tb_stock_list where 
      code in 
      (
      	select distinct(code) from tb_stock_data_daily 
      ) ;
  
  rtcur cur%rowtype ;
  ncounter number ;
begin
  delete tb_stock_data_Quarterly where code in (select distinct(code) from  tb_stock_data_Quarterly  where amount = 0 );
  delete tb_stock_data_Quarterly where trunc(shi_jian,'q') = trunc(sysdate,'q');
  commit;
  for rt in cur loop    
    proc_stock_get_Quarter(rt.code,rt.name);
    
    select sum(c)-1 into ncounter from
    (
	    select count(1) c from dual 
	      union
	    select count(1) c  from 
	    (
	        select code,name from tb_stock_data_Quarterly where code = rt.code group by code,name
	    )
	    group by code 
    );    
    
    if ncounter > 1 then
      update tb_stock_data_Quarterly set name = rt.name where code = rt.code ;
    end if ;      

  end loop ;
  
  insert into tb_stock_job_done values ('quarter',sysdate);
  commit;

end ;
/



create or replace procedure proc_stock_get_HalfYear_kdj
(
  pcode     in   varchar2 ,
  pprice    in   number   ,
  pk        out  number   ,
  pd        out  number   ,
  pj        out  number     
)
as
  type array_number is varray(4) of number;     
  setting array_number:=array_number(9,3,3,2);    
  
  nmax_price number ;
  nmin_price number ;
  
  nrsv number ;
  nLn  number ;
  nHn  number ;
  nK   number ;
  nd   number ;
  nJ   number ;
  
  ncounter number ;
begin
  --KDJSetting.Add(9);   //kdj天参数
  --KDJSetting.Add(2);   //k
  --KDJSetting.Add(3);   //d
  --KDJSetting.Add(2);   //j形态参数

  select max(max_price) ,
         min(min_price) ,
         count(1)
          into
         nHn ,
         nLn ,
         ncounter
  from
  (
    select * from
    (
      select max_price , min_price from tb_stock_data_HalfYearly where code = pcode order by shi_jian desc
    )
    WHERE ROWNUM <=setting(1)
  );

  if ncounter < setting(1) - 1 then
    return;
  end if;

  if (nHn - nLn) <>0 then

    nrsv :=((pprice - nLn )/(nHn - nLn))*100 ;
  
    nk := null ;
    nd := null ;
    nj := null ;

    select KDJ_K,KDJ_d,KDJ_j into nk,nd,nj from
    (
      select * from
      (
        select KDJ_K,KDJ_d,KDJ_j,shi_jian from tb_stock_data_HalfYearly where code = pcode order by shi_jian desc
      )
      where
        rownum<3
      order by shi_jian asc
    )
    where
      rownum<2;

    if nk is null then
      pk:=50.0 ;
      pd:=50.0 ;
      pj:=null ;
    else
      if nk is null then
        pk := 2/3*50  + (1/3)*nrsv ;
        pd := 2/3*50  + (1/3)*pk    ;
      else
        pk := ( 2/3* nk )+ (1/3)*nrsv ;
        pd := ( 2/3* nd )+ (1/3)*pk  ;
      end if;

      if  setting(4) = 1   then
        pj := 3*pd - 2*pk ;
      else
        pj := 3*pk - 2*pd ;
      end if;
    end if;


  else
    pk:=50.0 ;
    pd:=50.0 ;
    pj:=null ;
  end if ;

end;
/


create or replace procedure proc_stock_get_HalfYear_ma
(
  pcode    in  varchar2 ,
  pMA6      out number ,
  pMA12     out number ,
  pMA20     out number ,
  pMA30     out number ,
  pMA45     out number ,
  pMA60     out number ,
  pMA125    out number ,
  pMA250    out number 
)
as
  type array_number is varray(8) of number;     
  setting array_number:=array_number
  (
   6   ,
   12  ,
   20  ,
   30  ,
   45  ,
   60  ,
   125 ,
   250
  );  
  
  nLoop number ;
  
  nMa       number;
  nCounter  number; 
begin

  pMA6   := null ;
  pMA12  := null ;
  pMA20  := null ;
  pMA30  := null ;
  pMA45  := null ;
  pMA60  := null ;
  pMA125 := null ;
  pMA250 := null ;
  
  nloop := 1 ;
  
  for nLoop in 1..setting.count loop
    select sum(price)/count(1) ,
           count(1) 
             into
           nMa ,
           nCounter 
    from 
    (
      select price from tb_stock_data_HalfYearly where 
        code = pcode 
        order by shi_jian desc         
    )
    where
    rownum<= setting(nLoop) ;
           
    if nCounter < setting(nLoop) then
      continue ;
    end if; 
    
    CASE setting(nLoop)  
      WHEN 6   THEN pMA6   := nMa ;   
      WHEN 12  THEN pMA12  := nMa ;  
      WHEN 20  THEN pMA20  := nMa ;        
      WHEN 30  THEN pMA30  := nMa ;   
      WHEN 45  THEN pMA45  := nMa ; 
      WHEN 60  THEN pMA60  := nMa ; 
      WHEN 125 THEN pMA125 := nMa ; 
      WHEN 250 THEN pMA250 := nMa ; 
    end case ;      
  end loop ;

end;
/

create or replace procedure proc_stock_get_HalfYear_XSTD
(
  pCode   in  varchar2 ,
  pEmaVal1_SLONG  in out number,
  pEmaVal1_SSHORT in out number,
  pEmaVal1_LLONG  in out number,
  pEmaVal1_LSHORT in out number,
  pEmaVal2_SLONG  in out number,
  pEmaVal2_SSHORT in out number,
  pEmaVal2_LLONG  in out number,
  pEmaVal2_LSHORT in out number,
  pSLONG  out number , 
  pSSHORT out number , 
  pLLONG  out number , 
  pLSHORT out number  
)
as
--[0]-SLONG , [1]-SSHORT , [2]-LLONG , [3]-LSHORT
  --nEmaVal1_SLONG   number ;
  --nEmaVal1_SSHORT  number ;
  --nEmaVal1_LLONG   number ;
  --nEmaVal1_LSHORT  number ;
  nEmaVal2_SLONG   number ;
  nEmaVal2_SSHORT  number ;
  nEmaVal2_LLONG   number ;
  nEmaVal2_LSHORT  number ;
  
  ncounter  number ;
  nmax_price number ;
  nmin_price number ;
begin 
  select count(1) into ncounter from tb_stock_data_HalfYearly where code = pcode ;
  
  if  ncounter <1  then
    return ;
  end if; 
  
  select max_price,min_price into nmax_price,nmin_price from tb_stock_data_HalfYearly where 
    code = pcode 
      and
    shi_jian = (select max(shi_jian) from tb_stock_data_HalfYearly  where code = pcode ) ;
  
  if ncounter = 1 then 
    pEmaVal1_SLONG  :=  fun_stock_ema(nmax_price      , 0 , 1);
    pEmaVal2_SLONG  :=  fun_stock_ema(pEmaVal1_SLONG  , 0 , 1);
                                                      
    pEmaVal1_SSHORT :=  fun_stock_ema(nmin_price      , 0 , 1);  
    pEmaVal2_SSHORT :=  fun_stock_ema(pEmaVal1_SSHORT , 0 , 1);
                                                      
    pEmaVal1_LLONG  :=  fun_stock_ema(nmax_price      , 0 , 1);
    pEmaVal2_LLONG  :=  fun_stock_ema(pEmaVal1_LLONG  , 0 , 1);  
                  
    pEmaVal1_LSHORT :=  fun_stock_ema(nmin_price      , 0 , 1);
    pEmaVal2_LSHORT :=  fun_stock_ema(pEmaVal1_LSHORT , 0 , 1); 
       
  else    
    pEmaVal1_SLONG  :=  fun_stock_ema(nmax_price       , pEmaVal1_SLONG , 5 ); 
    pEmaVal2_SLONG  :=  fun_stock_ema(pEmaVal1_SLONG   , pEmaVal2_SLONG , 10); 
                                                                
    pEmaVal1_SSHORT :=  fun_stock_ema(nmin_price      , pEmaVal1_SSHORT , 5 ); 
    pEmaVal2_SSHORT :=  fun_stock_ema(pEmaVal1_SSHORT , pEmaVal2_SSHORT , 10); 
                                                                
    pEmaVal1_LLONG  :=  fun_stock_ema(nmax_price      , pEmaVal1_LLONG , 5 ); 
    pEmaVal2_LLONG  :=  fun_stock_ema(pEmaVal1_LLONG  , pEmaVal2_LLONG , 5); 
                                                                
    pEmaVal1_LSHORT :=  fun_stock_ema(nmin_price      , pEmaVal1_LSHORT , 5 ); 
    pEmaVal2_LSHORT :=  fun_stock_ema(pEmaVal1_LSHORT , pEmaVal2_LSHORT , 5); 
  
  end if;
  
  pSLONG  := pEmaVal2_SLONG  * 1.12 ; 
  pSSHORT := pEmaVal2_SSHORT * 0.86 ;
  pLLONG  := pEmaVal2_LLONG  * 1.04 ;
  pLSHORT := pEmaVal2_LSHORT * 0.94 ;

end ;
/



create or replace procedure proc_stock_get_HalfYear
(
  pCode in varchar2 ,
  pName in varchar2
)
as
  dmax_HalfYear  date ;
  dmin_HalfYear  date ;
  dcursor        date ;
  nlast_price     number ; 
  nzhang_die_rate number ;  
              
  nTmp        number ;
  dTmp        date ;
  sTmp        varchar2(1) ;
              
  ncounter    number ;
  
  nK    number ;
  nd    number ;
  nJ    number ;  
  
  nMA6   number ;
  nMA12  number ;
  nMA20  number ;
  nMA30  number ;
  nMA45  number ;
  nMA60  number ;
  nMA125 number ;
  nMA250 number ; 
  
  nEmaVal1_SLONG  number ;
  nEmaVal1_SSHORT number ;
  nEmaVal1_LLONG  number ;
  nEmaVal1_LSHORT number ;

  nEmaVal2_SLONG  number ;
  nEmaVal2_SSHORT number ;
  nEmaVal2_LLONG  number ;
  nEmaVal2_LSHORT number ;     
  
  nSLONG  number ; 
  nSSHORT number ; 
  nLLONG  number ; 
  nLSHORT number ; 
 
  cursor curHalfYearData(stockcode varchar2 , HalfYearCursor date) is
    select * from
    (             
       select 
              max(shi_jian)  shi_jian  ,
              sum(vol)       vol       ,
              sum(amount)    amount    ,
              max(max_price) max_price ,
              min(min_price) min_price  
       from tb_stock_data_Daily where                                
         code = stockcode
           and  
         f_getHalfYear(shi_jian) = f_getHalfYear(HalfYearCursor)
    )a, 
    (   
      select price_today_open from tb_stock_data_Daily where 
        code = stockcode
          and 
        shi_jian = (select min(shi_jian) from tb_stock_data_Daily where 
                      code = stockcode
                        and 
                      f_getHalfYear(shi_jian) = f_getHalfYear(HalfYearCursor)
                    ) 
    )b,
    (  
      select price from tb_stock_data_Daily where 
        code = stockcode
          and 
        shi_jian = ( 
                      select max(shi_jian) from tb_stock_data_Daily where 
                        code = stockcode
                          and 
                        f_getHalfYear(shi_jian) = f_getHalfYear(HalfYearCursor)
                    ) 
    )c ;  
    
  rtHalfYearData curHalfYearData%rowtype ;
  
begin
  select trunc(max(shi_jian),'q') max_HalfYear , 
         trunc(min(shi_jian),'q') min_HalfYear 
           into 
         dmax_HalfYear , 
         dmin_HalfYear
  from tb_stock_data_Daily where code = pCode ;                   
                   
  if dmax_HalfYear is null or dmin_HalfYear is null then  
    return;        
  end if ;         
  
  select count(1) into ncounter from tb_stock_data_HalfYearly where code = pcode ;
  
  if ncounter>0 then   
    --找出走表里上个周的收盘价和日表里的上周收盘价进行比较
    --如果不一致可能除权，就删掉该股票的周数据重新生成  
    select EmaVal1_SLONG  , 
           EmaVal1_SSHORT ,
           EmaVal1_LLONG  ,
           EmaVal1_LSHORT ,
           EmaVal2_SLONG  ,
           EmaVal2_SSHORT ,
           EmaVal2_LLONG  ,
           EmaVal2_LSHORT ,
           price          ,
           shi_jian 
             into 
           nEmaVal1_SLONG  ,
           nEmaVal1_SSHORT ,
           nEmaVal1_LLONG  ,
           nEmaVal1_LSHORT ,
           nEmaVal2_SLONG  ,
           nEmaVal2_SSHORT ,
           nEmaVal2_LLONG  ,
           nEmaVal2_LSHORT ,             
           nlast_price    ,
           dtmp 
    from tb_stock_data_HalfYearly where 
      code = pcode 
        and
      shi_jian = (select max(shi_Jian) from tb_stock_data_HalfYearly where code=pcode);
    
    open curHalfYearData(pcode,trunc(dtmp,'q')) ;    
    fetch curHalfYearData into rtHalfYearData ;
    close curHalfYearData ;        
    
    if nlast_price <> rtHalfYearData.price  then    
      nlast_price     := null ;
      nEmaVal1_SLONG  := null ; 
      nEmaVal1_SSHORT := null ;
      nEmaVal1_LLONG  := null ;
      nEmaVal1_LSHORT := null ;
      nEmaVal2_SLONG  := null ;
      nEmaVal2_SSHORT := null ;
      nEmaVal2_LLONG  := null ;
      nEmaVal2_LSHORT := null ;
      delete tb_stock_data_HalfYearly where code = pcode ;
    else          
      dmin_HalfYear := add_months(trunc(dtmp,'q'),6) ;
    end if ;          
  end if ;           
                     
  dcursor := dmin_HalfYear; 
  
  while dcursor <= dmax_HalfYear loop

    select count(1) into ncounter from tb_stock_data_Daily where                                
      code = pcode
        and  
      trunc(shi_jian,'q') = dcursor ;
    
    if ncounter < 1 then  
      dcursor := add_months( dcursor , 6 ) ;       
      continue ;
    end if;     
    
    open curHalfYearData(pCode , dcursor) ;            
    fetch curHalfYearData into rtHalfYearData;    
    close curHalfYearData ;      
    
    dcursor := add_months( dcursor , 6 ) ;
        
    if rtHalfYearData.max_price is null or
       rtHalfYearData.min_price is null or
       rtHalfYearData.vol       is null or
       rtHalfYearData.amount    is null
    then         
      continue ;    
    end if ;
    
    --if rtHalfYeardata.shi_jian = to_date('1994-02-04 15:00:00','yyyy-mm-dd hh24:mi:ss') then
    --  sTmp := '' ;
    --end if ;     

		if nlast_price is null then
			nzhang_die_rate := null ;
		else
			nzhang_die_rate := rtHalfYeardata.price/nlast_price - 1 ;
		end if ;       

    insert into tb_stock_data_HalfYearly 
    (
      name             ,
      code             , 
      max_price        ,
      min_price        ,
      vol              ,
      amount           ,
      shi_jian         , 
      price_today_open ,
      price            ,
      zhang_die_rate         
    )
    values
    (
      pname                       ,
      pcode                       ,
      rtHalfYeardata.max_price        ,
      rtHalfYeardata.min_price        ,
      rtHalfYeardata.vol              ,
      rtHalfYeardata.amount           ,
      rtHalfYeardata.shi_jian         ,
      rtHalfYeardata.price_today_open ,
      rtHalfYeardata.price            ,
      nzhang_die_rate                  
    ) ;    
    
    proc_stock_get_HalfYear_kdj( 
                        pcode    , 
                        rtHalfYeardata.price ,
                        nk ,
                        nd ,
                        nj 
                       );
                       
    proc_stock_get_HalfYear_ma(
                       pcode ,
                       nMA6  ,
                       nMA12 ,
                       nMA20 ,
                       nMA30 ,
                       nMA45 ,
                       nMA60 ,
                       nMA125,
                       nMA250
                     ); 
                     
    proc_stock_get_HalfYear_XSTD(
                         pcode   ,
                         nEmaVal1_SLONG  , 
                         nEmaVal1_SSHORT ,
                         nEmaVal1_LLONG  ,
                         nEmaVal1_LSHORT ,
                         nEmaVal2_SLONG  ,
                         nEmaVal2_SSHORT ,
                         nEmaVal2_LLONG  ,
                         nEmaVal2_LSHORT ,                                                
                         nSLONG  , 
                         nSSHORT , 
                         nLLONG  , 
                         nLSHORT 
                       ) ;

    update tb_stock_data_HalfYearly 
      set kdj_k          = nk             ,
          kdj_d          = nd             ,
          kdj_j          = nj             ,
          MA6            = nMA6           ,
          MA12           = nMA12          ,
          MA20           = nMA20          ,
          MA30           = nMA30          ,
          MA45           = nMA45          ,
          MA60           = nMA60          ,
          MA125          = nMA125         ,
          MA250          = nMA250         ,
          xstd_SLONG     = nSLONG         , 
          xstd_SSHORT    = nSSHORT        ,
          xstd_LLONG     = nLLONG         ,
          xstd_LSHORT    = nLSHORT        ,
          EmaVal1_SLONG  = nEmaVal1_SLONG  ,
          EmaVal1_SSHORT = nEmaVal1_SSHORT ,
          EmaVal1_LLONG  = nEmaVal1_LLONG  ,
          EmaVal1_LSHORT = nEmaVal1_LSHORT ,
          EmaVal2_SLONG  = nEmaVal2_SLONG  ,
          EmaVal2_SSHORT = nEmaVal2_SSHORT ,
          EmaVal2_LLONG  = nEmaVal2_LLONG  ,
          EmaVal2_LSHORT = nEmaVal2_LSHORT       
    where 
      code = pcode 
        and
      shi_jian = rtHalfYeardata.shi_jian ;
    
    nlast_price := rtHalfYeardata.price ;  

  end loop ;
  
  delete tb_stock_data_HalfYearly where f_getHalfYear(shi_jian) = f_getHalfYear(sysdate);
  commit;

end;
/

create or replace procedure proc_stock_get_HalfYear_all
as
  cursor cur is 
    select code , name from tb_stock_list where 
      code in 
      (
      	select distinct(code) from tb_stock_data_daily 
      ) ;
  
  rtcur cur%rowtype ;
  ncounter number ;
begin
  delete tb_stock_data_halfYearly where code in (select distinct(code) from  tb_stock_data_halfYearly where amount = 0 );
  commit; 
  
  for rt in cur loop    
    proc_stock_get_HalfYear(rt.code,rt.name);
        
    select sum(c)-1 into ncounter from
    (
	    select count(1) c from dual 
	      union
	    select count(1) c  from 
	    (
	        select code,name from tb_stock_data_halfYearly where code = rt.code group by code,name
	    )
	    group by code 
    );    
    
    if ncounter > 1 then
      update tb_stock_data_halfYearly set name = rt.name where code = rt.code ;
    end if ;      
    
  end loop ;
  
  insert into tb_stock_job_done values ('halfyear',sysdate);
  commit;  

end ;
/



create or replace procedure proc_stock_get_Year_kdj
(
  pcode     in   varchar2 ,
  pprice    in   number   ,
  pk        out  number   ,
  pd        out  number   ,
  pj        out  number     
)
as
  type array_number is varray(4) of number;     
  setting array_number:=array_number(9,3,3,2);    
  
  nmax_price number ;
  nmin_price number ;
  
  nrsv number ;
  nLn  number ;
  nHn  number ;
  nK   number ;
  nd   number ;
  nJ   number ;
  
  ncounter number ;
begin
  --KDJSetting.Add(9);   //kdj天参数
  --KDJSetting.Add(2);   //k
  --KDJSetting.Add(3);   //d
  --KDJSetting.Add(2);   //j形态参数

  select max(max_price) ,
         min(min_price) ,
         count(1)
          into
         nHn ,
         nLn ,
         ncounter
  from
  (
    select * from
    (
      select max_price , min_price from tb_stock_data_Yearly where code = pcode order by shi_jian desc
    )
    WHERE ROWNUM <=setting(1)
  );

  if ncounter < setting(1) - 1 then
    return;
  end if;

  if (nHn - nLn) <>0 then

    nrsv :=((pprice - nLn )/(nHn - nLn))*100 ;
  
    nk := null ;
    nd := null ;
    nj := null ;

    select KDJ_K,KDJ_d,KDJ_j into nk,nd,nj from
    (
      select * from
      (
        select KDJ_K,KDJ_d,KDJ_j,shi_jian from tb_stock_data_Yearly where code = pcode order by shi_jian desc
      )
      where
        rownum<3
      order by shi_jian asc
    )
    where
      rownum<2;

    if nk is null then
      pk:=50.0 ;
      pd:=50.0 ;
      pj:=null ;
    else
      if nk is null then
        pk := 2/3*50  + (1/3)*nrsv ;
        pd := 2/3*50  + (1/3)*pk    ;
      else
        pk := ( 2/3* nk )+ (1/3)*nrsv ;
        pd := ( 2/3* nd )+ (1/3)*pk  ;
      end if;

      if  setting(4) = 1   then
        pj := 3*pd - 2*pk ;
      else
        pj := 3*pk - 2*pd ;
      end if;
    end if;


  else
    pk:=50.0 ;
    pd:=50.0 ;
    pj:=null ;
  end if ;

end;
/


create or replace procedure proc_stock_get_Year_ma
(
  pcode    in  varchar2 ,
  pMA6      out number ,
  pMA12     out number ,
  pMA20     out number ,
  pMA30     out number ,
  pMA45     out number ,
  pMA60     out number ,
  pMA125    out number ,
  pMA250    out number 
)
as
  type array_number is varray(8) of number;     
  setting array_number:=array_number
  (
   6   ,
   12  ,
   20  ,
   30  ,
   45  ,
   60  ,
   125 ,
   250
  );  
  
  nLoop number ;
  
  nMa       number;
  nCounter  number; 
begin

  pMA6   := null ;
  pMA12  := null ;
  pMA20  := null ;
  pMA30  := null ;
  pMA45  := null ;
  pMA60  := null ;
  pMA125 := null ;
  pMA250 := null ;
  
  nloop := 1 ;
  
  for nLoop in 1..setting.count loop
    select sum(price)/count(1) ,
           count(1) 
             into
           nMa ,
           nCounter 
    from 
    (
      select price from tb_stock_data_Yearly where 
        code = pcode 
        order by shi_jian desc         
    )
    where
    rownum<= setting(nLoop) ;
           
    if nCounter < setting(nLoop) then
      continue ;
    end if; 
    
    CASE setting(nLoop)  
      WHEN 6   THEN pMA6   := nMa ;   
      WHEN 12  THEN pMA12  := nMa ;  
      WHEN 20  THEN pMA20  := nMa ;        
      WHEN 30  THEN pMA30  := nMa ;   
      WHEN 45  THEN pMA45  := nMa ; 
      WHEN 60  THEN pMA60  := nMa ; 
      WHEN 125 THEN pMA125 := nMa ; 
      WHEN 250 THEN pMA250 := nMa ; 
    end case ;      
  end loop ;

end;
/

create or replace procedure proc_stock_get_Year_XSTD
(
  pCode   in  varchar2 ,
  pEmaVal1_SLONG  in out number,
  pEmaVal1_SSHORT in out number,
  pEmaVal1_LLONG  in out number,
  pEmaVal1_LSHORT in out number,
  pEmaVal2_SLONG  in out number,
  pEmaVal2_SSHORT in out number,
  pEmaVal2_LLONG  in out number,
  pEmaVal2_LSHORT in out number,
  pSLONG  out number , 
  pSSHORT out number , 
  pLLONG  out number , 
  pLSHORT out number  
)
as
--[0]-SLONG , [1]-SSHORT , [2]-LLONG , [3]-LSHORT
  --nEmaVal1_SLONG   number ;
  --nEmaVal1_SSHORT  number ;
  --nEmaVal1_LLONG   number ;
  --nEmaVal1_LSHORT  number ;
  nEmaVal2_SLONG   number ;
  nEmaVal2_SSHORT  number ;
  nEmaVal2_LLONG   number ;
  nEmaVal2_LSHORT  number ;
  
  ncounter  number ;
  nmax_price number ;
  nmin_price number ;
begin 
  select count(1) into ncounter from tb_stock_data_Yearly where code = pcode ;
  
  if  ncounter <1  then
    return ;
  end if; 
  
  select max_price,min_price into nmax_price,nmin_price from tb_stock_data_Yearly where 
    code = pcode 
      and
    shi_jian = (select max(shi_jian) from tb_stock_data_Yearly  where code = pcode ) ;
  
  if ncounter = 1 then 
    pEmaVal1_SLONG  :=  fun_stock_ema(nmax_price      , 0 , 1);
    pEmaVal2_SLONG  :=  fun_stock_ema(pEmaVal1_SLONG  , 0 , 1);
                                                      
    pEmaVal1_SSHORT :=  fun_stock_ema(nmin_price      , 0 , 1);  
    pEmaVal2_SSHORT :=  fun_stock_ema(pEmaVal1_SSHORT , 0 , 1);
                                                      
    pEmaVal1_LLONG  :=  fun_stock_ema(nmax_price      , 0 , 1);
    pEmaVal2_LLONG  :=  fun_stock_ema(pEmaVal1_LLONG  , 0 , 1);  
                  
    pEmaVal1_LSHORT :=  fun_stock_ema(nmin_price      , 0 , 1);
    pEmaVal2_LSHORT :=  fun_stock_ema(pEmaVal1_LSHORT , 0 , 1); 
       
  else    
    pEmaVal1_SLONG  :=  fun_stock_ema(nmax_price       , pEmaVal1_SLONG , 5 ); 
    pEmaVal2_SLONG  :=  fun_stock_ema(pEmaVal1_SLONG   , pEmaVal2_SLONG , 10); 
                                                                
    pEmaVal1_SSHORT :=  fun_stock_ema(nmin_price      , pEmaVal1_SSHORT , 5 ); 
    pEmaVal2_SSHORT :=  fun_stock_ema(pEmaVal1_SSHORT , pEmaVal2_SSHORT , 10); 
                                                                
    pEmaVal1_LLONG  :=  fun_stock_ema(nmax_price      , pEmaVal1_LLONG , 5 ); 
    pEmaVal2_LLONG  :=  fun_stock_ema(pEmaVal1_LLONG  , pEmaVal2_LLONG , 5); 
                                                                
    pEmaVal1_LSHORT :=  fun_stock_ema(nmin_price      , pEmaVal1_LSHORT , 5 ); 
    pEmaVal2_LSHORT :=  fun_stock_ema(pEmaVal1_LSHORT , pEmaVal2_LSHORT , 5); 
  
  end if;
  
  pSLONG  := pEmaVal2_SLONG  * 1.12 ; 
  pSSHORT := pEmaVal2_SSHORT * 0.86 ;
  pLLONG  := pEmaVal2_LLONG  * 1.04 ;
  pLSHORT := pEmaVal2_LSHORT * 0.94 ;

end ;
/


create or replace procedure proc_stock_get_Year
(
  pCode in varchar2 ,
  pName in varchar2
)
as
  dmax_Year  date ;
  dmin_Year  date ;
  dcursor    date ;
  nlast_price     number ; 
  nzhang_die_rate number ;
              
  nTmp        number ;
  dTmp        date ;
  sTmp        varchar2(1) ;
              
  ncounter    number ;
  
  nK    number ;
  nd    number ;
  nJ    number ;  
  
  nMA6   number ;
  nMA12  number ;
  nMA20  number ;
  nMA30  number ;
  nMA45  number ;
  nMA60  number ;
  nMA125 number ;
  nMA250 number ; 
  
  nEmaVal1_SLONG  number ;
  nEmaVal1_SSHORT number ;
  nEmaVal1_LLONG  number ;
  nEmaVal1_LSHORT number ;

  nEmaVal2_SLONG  number ;
  nEmaVal2_SSHORT number ;
  nEmaVal2_LLONG  number ;
  nEmaVal2_LSHORT number ;     
  
  nSLONG  number ; 
  nSSHORT number ; 
  nLLONG  number ; 
  nLSHORT number ; 
 
  cursor curYearData(stockcode varchar2 , YearCursor date) is
    select * from
    (             
       select 
              max(shi_jian)  shi_jian  ,
              sum(vol)       vol       ,
              sum(amount)    amount    ,
              max(max_price) max_price ,
              min(min_price) min_price  
       from tb_stock_data_Daily where                                
         code = stockcode
           and  
         trunc(shi_jian,'year') = YearCursor
    )a, 
    (   
      select price_today_open from tb_stock_data_Daily where 
        code = stockcode
          and 
        shi_jian = (select min(shi_jian) from tb_stock_data_Daily where 
                      code = stockcode
                        and 
                      trunc(shi_jian,'year') = YearCursor
                    ) 
    )b,
    (  
      select price from tb_stock_data_Daily where 
        code = stockcode
          and 
        shi_jian = ( 
                      select max(shi_jian) from tb_stock_data_Daily where 
                        code = stockcode
                          and 
                        trunc(shi_jian,'year') = YearCursor
                    ) 
    )c ;  
    
  rtYearData curYearData%rowtype ;
  
begin
  select trunc(max(shi_jian),'year') max_Year , 
         trunc(min(shi_jian),'year') min_Year 
           into 
         dmax_Year , 
         dmin_Year
  from tb_stock_data_Daily where code = pCode ;                   
                   
  if dmax_Year is null or dmin_Year is null then  
    return;        
  end if ;         
  
  select count(1) into ncounter from tb_stock_data_Yearly where code = pcode ;
  
  if ncounter>0 then   
    --找出走表里上个周的收盘价和日表里的上周收盘价进行比较
    --如果不一致可能除权，就删掉该股票的周数据重新生成  
    select EmaVal1_SLONG  , 
           EmaVal1_SSHORT ,
           EmaVal1_LLONG  ,
           EmaVal1_LSHORT ,
           EmaVal2_SLONG  ,
           EmaVal2_SSHORT ,
           EmaVal2_LLONG  ,
           EmaVal2_LSHORT ,
           price          ,
           shi_jian 
             into 
           nEmaVal1_SLONG  ,
           nEmaVal1_SSHORT ,
           nEmaVal1_LLONG  ,
           nEmaVal1_LSHORT ,
           nEmaVal2_SLONG  ,
           nEmaVal2_SSHORT ,
           nEmaVal2_LLONG  ,
           nEmaVal2_LSHORT ,             
           nlast_price    ,
           dtmp 
    from tb_stock_data_Yearly where 
      code = pcode 
        and
      shi_jian = (select max(shi_Jian) from tb_stock_data_Yearly where code=pcode);
    
    open curYearData(pcode,trunc(dtmp,'year')) ;    
    fetch curYearData into rtYearData ;
    close curYearData ;        
    
    if nlast_price <> rtYearData.price  then    
      nlast_price     := null ;
      nEmaVal1_SLONG  := null ; 
      nEmaVal1_SSHORT := null ;
      nEmaVal1_LLONG  := null ;
      nEmaVal1_LSHORT := null ;
      nEmaVal2_SLONG  := null ;
      nEmaVal2_SSHORT := null ;
      nEmaVal2_LLONG  := null ;
      nEmaVal2_LSHORT := null ;
      delete tb_stock_data_Yearly where code = pcode ;
    else          
      dmin_Year := add_months(trunc(dtmp,'year'),12) ;
    end if ;          
  end if ;           
                     
  dcursor := dmin_Year; 
  
  while dcursor <= dmax_Year loop

    select count(1) into ncounter from tb_stock_data_Daily where                                
      code = pcode
        and  
      trunc(shi_jian,'year') = dcursor ;
    
    if ncounter < 1 then  
      dcursor := add_months( dcursor , 12 ) ;       
      continue ;
    end if;     
    
    open curYearData(pCode , dcursor) ;            
    fetch curYearData into rtYearData;    
    close curYearData ;      
    
    dcursor := add_months( dcursor , 12 ) ;
        
    if rtYearData.max_price is null or
       rtYearData.min_price is null or
       rtYearData.vol       is null or
       rtYearData.amount    is null
    then         
      continue ;    
    end if ;
    
    --if rtYeardata.shi_jian = to_date('1994-02-04 15:00:00','yyyy-mm-dd hh24:mi:ss') then
    --  sTmp := '' ;
    --end if ;      

		if nlast_price is null then
			nzhang_die_rate := null ;
		else
			nzhang_die_rate := rtYeardata.price/nlast_price - 1 ;
		end if ;      

    insert into tb_stock_data_Yearly 
    (
      name             ,
      code             , 
      max_price        ,
      min_price        ,
      vol              ,
      amount           ,
      shi_jian         , 
      price_today_open ,
      price            ,
      zhang_die_rate          
    )
    values
    (
      pname                       ,
      pcode                       ,
      rtYeardata.max_price        ,
      rtYeardata.min_price        ,
      rtYeardata.vol              ,
      rtYeardata.amount           ,
      rtYeardata.shi_jian         ,
      rtYeardata.price_today_open ,
      rtYeardata.price            ,
      nzhang_die_rate               
    ) ;    
    
    proc_stock_get_Year_kdj( 
                        pcode    , 
                        rtYeardata.price ,
                        nk ,
                        nd ,
                        nj 
                       );
                       
    proc_stock_get_Year_ma(
                       pcode ,
                       nMA6  ,
                       nMA12 ,
                       nMA20 ,
                       nMA30 ,
                       nMA45 ,
                       nMA60 ,
                       nMA125,
                       nMA250
                     ); 
                     
    proc_stock_get_Year_XSTD(
                         pcode   ,
                         nEmaVal1_SLONG  , 
                         nEmaVal1_SSHORT ,
                         nEmaVal1_LLONG  ,
                         nEmaVal1_LSHORT ,
                         nEmaVal2_SLONG  ,
                         nEmaVal2_SSHORT ,
                         nEmaVal2_LLONG  ,
                         nEmaVal2_LSHORT ,                                                
                         nSLONG  , 
                         nSSHORT , 
                         nLLONG  , 
                         nLSHORT 
                       ) ;

    update tb_stock_data_Yearly 
      set kdj_k          = nk             ,
          kdj_d          = nd             ,
          kdj_j          = nj             ,
          MA6            = nMA6           ,
          MA12           = nMA12          ,
          MA20           = nMA20          ,
          MA30           = nMA30          ,
          MA45           = nMA45          ,
          MA60           = nMA60          ,
          MA125          = nMA125         ,
          MA250          = nMA250         ,
          xstd_SLONG     = nSLONG         , 
          xstd_SSHORT    = nSSHORT        ,
          xstd_LLONG     = nLLONG         ,
          xstd_LSHORT    = nLSHORT        ,
          EmaVal1_SLONG  = nEmaVal1_SLONG  ,
          EmaVal1_SSHORT = nEmaVal1_SSHORT ,
          EmaVal1_LLONG  = nEmaVal1_LLONG  ,
          EmaVal1_LSHORT = nEmaVal1_LSHORT ,
          EmaVal2_SLONG  = nEmaVal2_SLONG  ,
          EmaVal2_SSHORT = nEmaVal2_SSHORT ,
          EmaVal2_LLONG  = nEmaVal2_LLONG  ,
          EmaVal2_LSHORT = nEmaVal2_LSHORT       
    where 
      code = pcode 
        and
      shi_jian = rtYeardata.shi_jian ;
    
    nlast_price := rtYeardata.price ;  

  end loop ;
  delete tb_stock_data_Yearly where  trunc(shi_jian,'year') = trunc(sysdate,'year') ;
  commit;

end;
/

create or replace procedure proc_stock_get_Year_all
as
  cursor cur is 
    select code , name from tb_stock_list where 
      code in 
      (
      	select distinct(code) from tb_stock_data_daily 
      ) ;
  
  rtcur cur%rowtype ;
  ncounter number ;
begin
  delete tb_stock_data_Yearly     where code in (select distinct(code) from  tb_stock_data_Yearly     where amount = 0 );
  commit;
  for rt in cur loop    
    proc_stock_get_Year(rt.code,rt.name);
    
    select sum(c)-1 into ncounter from
    (
	    select count(1) c from dual 
	      union
	    select count(1) c  from 
	    (
	        select code,name from tb_stock_data_Yearly where code = rt.code group by code,name
	    )
	    group by code 
    );    
    
    if ncounter > 1 then
      update tb_stock_data_Yearly set name = rt.name where code = rt.code ;
    end if ;          
  end loop ;
  
  insert into tb_stock_job_done values ('year',sysdate);
  commit;    

end ;
/


create or replace function fun_zhang_ting
(
  pLastZhangTing in number 
)
return number 
is 
begin
	return round(pLastZhangTing*1.1*100)/100 ;
end; 


--新股6日内破板
create or replace procedure proc_stock_new_stock
as
  --取出只有6天数据的新股股票，非银行股
  cursor cur is 
    select code ,
           min(shi_jian) min_shi_jian ,
           count(1) c 
    from tb_stock_data_daily where 
      name not like '%银行%' 
    group by code 
    having count(1) <= 6 ;	
   
	rt cur%rowtype ;	
	fprice number ;	
	counter number ;
	bfound boolean ;
	vname varchar2(32) ;
begin
	bfound := false ;
  delete tb_stock_new_stock ;

  --第一天收盘价的2.1倍
  --第6个交易日内  
  for rt in cur loop    
  	
    select count(1) into counter  from
    (
       --排除上市第一天数据
       select * from tb_stock_data_daily where 
         code = rt.code  
           and
         shi_jian > rt.min_shi_jian
       order by shi_jian  asc
    )
    where 
      min_price <> max_price ;   --代表破板
    
    if counter >0 then
    	select name into vname from tb_stock_list where code = rt.code ;
      insert into tb_stock_new_stock values ( rt.code, vname,rt.min_shi_jian);
      bfound := true ;
    end if;
  end loop ;
  
  if bfound then 
  	insert into tb_stock_job_done values ('new_stock',sysdate);
  end if ;
  
  delete tb_stock_data_daily      where code in (select code from tb_stock_new_stock ) ;
  delete tb_stock_data_weekly     where code in (select code from tb_stock_new_stock ) ;
  delete tb_stock_data_monthly    where code in (select code from tb_stock_new_stock ) ;
  delete tb_stock_data_Quarterly  where code in (select code from tb_stock_new_stock ) ;
  delete tb_stock_data_halfYearly where code in (select code from tb_stock_new_stock ) ;
  delete tb_stock_data_Yearly     where code in (select code from tb_stock_new_stock ) ;  
  commit;
end;     