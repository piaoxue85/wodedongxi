'''
Created on 2017年5月14日

@author: moonlit
'''
import getStockData as gsd

code ,max_id , cur = gsd.get_stock_code_rqalpha()

print(code ,max_id , cur)
print(gsd.move_to_next_cur_rqalpha(max_id = max_id , cur = cur))
