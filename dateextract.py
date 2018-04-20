
from yahoo_fin.stock_info import *
from datetime import timedelta, date


def dateRange(sdate, edate):
    sdate = sdate
    edate = edate


sdate = date(2016,1,1)
mdate = sdate
edate = date(2018,4,10)

l_data = []
while (sdate != edate):
    mdate = sdate + timedelta(days=59)
    print(get_data("FB", start_date=str(sdate.month)+"/"+str(sdate.day)+"/"+str(sdate.year), end_date=str(mdate.month)
                                                                                                      +"/"+str(mdate.day)+"/"+str(mdate.year))["close"].round(2))
    sdate = mdate + timedelta(days=1)
print(l_data)