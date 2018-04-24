
from yahoo_fin.stock_info import *
from datetime import timedelta, date
from pandas import *
from rpy2.robjects.packages import importr
import rpy2.robjects as ro
import pandas.rpy.common as com

def val_opt_acc(t_rate, t_grow, costs):
    ro.r('x <- ')
    ro.r('x[1]=22')
    ro.r('x[2]=44')


def dateRange(sdate, edate):
    sdate = sdate
    edate = edate


costs = []
data = get_data('FB', start_date='01/02/2018', end_date='01/10/2018')["close"].round(2)
for y in data:
    costs.append(y)

#val_opt_acc(0.13, 2, costs)

''' 
sdate = date(2016,1,1)
mdate = sdate
edate = date(2018,4,10)

l_data = []
while (sdate != edate):
    mdate = sdate + timedelta(days=59)
    print(get_data("FB", start_date=str(sdate.month)+"/"+str(sdate.day)+"/"+str(sdate.year), end_date=str(mdate.month)+"/"+str(mdate.day)+"/"+str(mdate.year))["close"].round(2))
    sdate = mdate + timedelta(days=1)
print(l_data)

'''