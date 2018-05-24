from WindPy import *
import pandas as pd

w.start();

# data = w.wsd("000001.SZ", "close,last_trade_day,lastradeday_s,sec_name,trade_code", "1990-01-01", "2017-12-20", "Fill=Previous;PriceAdj=F")
# print(data)

req1 = "trade_code,sec_name,pre_close,open,high,low,close,volume,amt,dealnum,chg,pct_chg,swing,vwap,adjfactor,rel_ipo_chg,rel_ipo_pct_chg,total_shares,free_float_shares,mf_amt,mf_vol,mf_amt_ratio,mf_vol_ratio,mf_amt_close,mf_amt_open,pe_ttm,val_pe_deducted_ttm,pe_lyr,pb_lf,pb_mrq,ps_ttm,ps_lyr,pcf_ocf_ttm,pcf_ncf_ttm,pcf_ocflyr,pcf_nflyr,pe_est,estpe_FY1,estpe_FY2,estpe_FY3,pe_est_last,pe_est_ftm,est_peg,estpeg_FY1,estpeg_FY2,estpeg_FTM"
req2 = "estpb,estpb_FY1,estpb_FY2,estpb_FY3,ev1,ev2,ev2_to_ebitda,history_low,stage_high,history_high,stage_low,up_days,down_days,breakout_ma,breakdown_ma,bull_bear_ma,holder_num,holder_avgnum,holder_totalbyinst,holder_pctbyinst" 
 
res = w.wsd("000001.SZ", req1+","+req2 , "1990-12-19", "", "year=2018;rptYear=2018;n=3;m=60;meanLine=60;N1=5;N2=10;N3=20;N4=30;upOrLow=1;shareType=1;Fill=Previous;PriceAdj=F")

shi_jian = res.Times
Fields   = res.Fields
data     = res.Data

Data = pd.DataFrame()

for field , d in zip(Fields,data) :
    Data[field] = d
    
Data["shi_jian"] = shi_jian

print(Data)

a = ""

# data = w.wsd("000004.SZ", "trade_code,sec_name,pre_close,open,high,low,close,volume,amt,dealnum,chg,pct_chg,swing,vwap,adjfactor,rel_ipo_chg,rel_ipo_pct_chg,total_shares,free_float_shares,mf_amt,mf_vol,mf_amt_ratio,mf_vol_ratio,mf_amt_close,mf_amt_open,pe_ttm,val_pe_deducted_ttm,pe_lyr,pb_lf,pb_mrq,ps_ttm,ps_lyr,pcf_ocf_ttm,pcf_ncf_ttm,pcf_ocflyr,pcf_nflyr,pe_est,estpe_FY1,estpe_FY2,estpe_FY3,pe_est_last,pe_est_ftm,est_peg,estpeg_FY1,estpeg_FY2,estpeg_FTM", "2017-11-20", "2017-12-20", "year=2015;rptYear=2015;Fill=Previous;PriceAdj=F")
# print(data)
# data = w.wsd("000004.SZ", "estpb,estpb_FY1,estpb_FY2,estpb_FY3,ev1,ev2,ev2_to_ebitda,history_low,stage_high,history_high,stage_low,up_days,down_days,breakout_ma,breakdown_ma,bull_bear_ma,holder_num,holder_avgnum,holder_totalbyinst,holder_pctbyinst", "2017-11-20", "2017-12-20", "year=2018;n=3;m=60;meanLine=60;N1=5;N2=10;N3=20;N4=30;upOrLow=1;shareType=1;Fill=Previous;PriceAdj=F")
# print(data)