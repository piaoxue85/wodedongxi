load data
infile 'total_cap.TXT'
append
into table tb_stock_data_market_cap
fields terminated by ','
(
  code       char,
  shi_jian   char,
  amount     char,
  market_cap char 
)
       