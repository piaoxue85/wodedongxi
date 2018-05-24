'''
Created on 2017年10月11日

@author: moonlit

python Z:\StockAnalysis\sourceCode\TuShare\test\src\importAlpha101_process_data.py

'''
import numpy as np
import pandas as pd
import cx_Oracle
import getStockData as gsd 

def getCodeReturns(code = ""):
#     data = gsd.get_stock_data_daily_101_price(code)
    data = gsd.get_stock_data_daily_wind_price(code)
    #计算未来N日收益率（未来第N日的收盘价/今天的收盘价）
    N = 5
    data['return'] = data['price'].shift(-N) / data['price'] - 1 
    return data 

def getTotalReturns():
    pass

def updateData():
    codes = gsd.get_code_list()
    codes = codes["code"].values
        
    db=cx_Oracle.connect('c##stock','didierg160','myoracle')  #创建连接  
    cr=db.cursor()
    
    sql = "truncate table tb_stock_101_return"
    cr.execute(sql) 
        
    for code in codes :
        data      = getCodeReturns(code)
        rets      = data["return"].values
        shi_jians = data["shi_jian"].values
       
        for ret,shi_jian in zip(rets,shi_jians) :
            sql = "insert into tb_stock_101_return (CODE,SHI_JIAN,RETURN) values ('" + code + "','" + shi_jian + "'," + str(ret) +")"
            try :
                cr.execute(sql)
            except :
#                 print(sql)  
                pass
        
        db.commit()
        print("code:",code , " 5day return done")
    
    sql = "update tb_stock_101_return set ret_std=return"
    cr.execute(sql)
    
    sql = "update tb_stock_101_return set RET_HOT=1 where return>0 "
    cr.execute(sql) 
    
    sql = "update tb_stock_101_return set RET_HOT=0 where return<=0"
    cr.execute(sql)          
    
    db.commit()
    print(" 5day return all done")
        
updateData()        

'''
declare 
    cursor cur is 
      select distinct(to_char(shi_jian,'yyyy-mm-dd')) shi_jian from tb_stock_data_daily order by shi_jian asc ;
    
    total_return number ;
begin
  delete tb_stock_101_total_return ;
  
    for rt in cur loop 
        
      select sum( return ) into total_return from 
      (
          select * from tb_stock_101_return where 
            shi_jian = rt.shi_jian
          order by return desc 
        ) 
        where 
          rownum <=20;
          
      insert into tb_stock_101_total_return values (rt.shi_jian , total_return );
        
    end loop;
  
  commit;
end; 

declare 
    cursor cur is 
      select distinct(to_char(shi_jian,'yyyy-mm-dd')) shi_jian from tb_stock_data_daily order by shi_jian asc ;
    
begin
  update tb_stock_101_selected set selected = 0;
  
  for rt in cur loop 
        
    update tb_stock_101_selected set selected = 1 where 
      shi_jian = rt.shi_jian 
        and
      code in 
      (
              select code from 
            (
                select * from tb_stock_101_return where 
                  shi_jian = rt.shi_jian
                order by return desc 
            ) 
            where 
              rownum <=20  
      );
      
  end loop;
  
  commit;
end; 


declare 
    cursor cur is 
      select distinct(to_char(shi_jian,'yyyy-mm-dd')) shi_jian from tb_stock_data_daily order by shi_jian asc ;
      
    cursor curCodes(pshi_jian varchar2) is
      select distinct(code) code from tb_stock_101_return where shi_jian = pshi_jian ;
      
    total_return number ;
    nmax number ;
    nmin number ;
begin
  --update tb_stock_101_return set ret_std = null ;
  --commit;
  
  for rt in cur loop 
     
        select max(return) , min(return) into nmax , nmin from tb_stock_101_return where 
            shi_jian = rt.shi_jian ;
            
        for rtcode in curCodes(rt.shi_jian) loop
        
            if nmax <> nmin then
                update tb_stock_101_return set RET_STD = (return - nmin)/(nmax-nmin) where 
                  code     = rtcode.code
                    and
                  shi_jian = rt.shi_jian ;
            end if ;        
            
        end loop ;
        
        commit;  
  end loop;
  
  commit;
end; 


declare 
    cursor cur is 
      select distinct(to_char(shi_jian,'yyyy-mm-dd')) shi_jian from tb_stock_data_daily order by shi_jian asc ;

begin

  for rt in cur loop 
     
      update tb_stock_101_return set ret_hot = 1 where 
        shi_jian = rt.shi_jian
          and
        code in 
        (
          select code from
          (
            select code from tb_stock_101_return where shi_jian =rt.shi_jian  order by return desc 
          )
          where 
            rownum<=20
        );
      commit;
  end loop;
  
  commit;
end; 


declare 
    cursor cur is 
      select distinct(to_char(shi_jian,'yyyy-mm-dd')) shi_jian from tb_stock_data_daily order by shi_jian asc ;
      
    cursor curCodes(pshi_jian varchar2) is
      select code from tb_stock_101_return where shi_jian = pshi_jian order by return asc;
     
    ncounter number ;
    pos number ;
    step number ;
begin
  
  for rt in cur loop 
     
        select count(*) into ncounter from tb_stock_101_return where 
            shi_jian = rt.shi_jian ;
            
        if ncounter = 1 then 
          continue ;
        end if;
            
        pos  := 0 ;
        step := 1/(ncounter -1);
        
        for rtcode in curCodes(rt.shi_jian) loop
        
            update tb_stock_101_return set RET_STD = pos where 
                  code     = rtcode.code
                    and
                  shi_jian = rt.shi_jian ;   
            
            pos := pos + step ;
        end loop ;
        
        commit;  
  end loop;
  
  commit;
end; 


declare 
    cursor cur is 
      select distinct(to_char(shi_jian,'yyyy-mm-dd')) shi_jian from tb_stock_data_daily order by shi_jian asc ;
      
    cursor curCodes(pshi_jian varchar2) is
      select code,return from tb_stock_101_return where shi_jian = pshi_jian order by return asc;
     
    ncounter number ;
    pos number ;
    step number ;
    
    return_tmp number ;
begin
  
  for rt in cur loop 
     
        select count(distinct(return)) into ncounter from tb_stock_101_return where 
            shi_jian = rt.shi_jian ;
            
        if ncounter = 1 then 
          continue ;
        end if;
            
        
        step := 1/(ncounter -1) ;
        pos  := -1/(ncounter -1);
        
        return_tmp := -99999 ;
        
        for rtcode in curCodes(rt.shi_jian) loop
        
                if rtcode.return > return_tmp then
                    pos := pos + step ;
                end if;
        
            update tb_stock_101_return set RET_STD = pos where 
                  code     = rtcode.code
                    and
                  shi_jian = rt.shi_jian ;
                  
            return_tmp := rtcode.return ;

        end loop ;
        
        commit;  
  end loop;
  
  commit;
end; 
'''
    
       

