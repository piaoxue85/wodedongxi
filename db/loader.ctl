load data
infile 'total_cap.TXT'
truncate
into table tb_stock_data_market_cap
fields terminated by ','
(
  code       char,
  shi_jian   char,
  amount     number,
  market_cap number 
)
