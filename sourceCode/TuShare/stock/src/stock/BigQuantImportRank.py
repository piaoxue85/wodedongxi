'''
Created on 2017年6月1日

@author: moonlit  
'''
import numpy as np
import cx_Oracle

def importRank(prank = [], shi_jian = ""):
#     print("start")
        
    db=cx_Oracle.connect('c##stock','didierg160','myoracle')  #创建连接  
    cr=db.cursor()
        
    rank = np.array(prank)    
    
    sql = "delete tb_stock_bigquant_rank where shi_jian = to_date('" + shi_jian +" 15:00:00','yyyy-mm-dd hh24:mi:ss') "
    cr.execute(sql) 
    
    seq = 1
    for code in rank :
        sql = "insert into tb_stock_bigquant_rank values (to_date('" + shi_jian +" 15:00:00','yyyy-mm-dd hh24:mi:ss') , " + str(seq)+" , '" + code[0:6] +"' )"  
        cr.execute(sql) 
        seq += 1   
    
    db.commit()        
    cr.close ()  
    db.close () 
    
#     print("end")