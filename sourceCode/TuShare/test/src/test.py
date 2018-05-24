import jqdatasdk as jq

jq.auth('13600069823','didierg160')

# res = jq.get_all_securities()
# print(res)

res = jq.get_price('000002.XSHE',start_date="1995-01-01",end_date="2018-12-31")
res = res.dropna()
print(res)