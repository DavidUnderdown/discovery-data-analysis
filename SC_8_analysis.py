import pandas as pd;
import matplotlib.pyplot as plt;

df1=pd.read_csv(r"..\DiscoveryAPI\myRecords.csv",parse_dates=["numStartDate","numEndDate"],infer_datetime_format=True,dayfirst=True)
counties=["Yorkshire","Kent","Norfolk","Hampshire","Devon","Northumberland","Cornwall","Lincolnshire","Surrey","Oxfordshire","Suffolk","Sussex","Berkshire","Essex","Gloucestershire","Warwickshire","Wiltshire","Buckinghamshire","Dorset","Somerset","Cambridgeshire","Middlesex","Northamptonshire","Hertfordshire","Shropshire","Staffordshire","Nottinghamshire","Lancashire","Cheshire","Derbyshire","Cumberland","Huntingdonshire","Leicestershire","Channel Islands","Denbighshire","County Durham","Herefordshire","Flintshire","Bedfordshire","Westmorland","Worcestershire","Monmouthshire","Rutland","Caernarfonshire","Pembrokeshire","Brecknockshire","Cardiganshire","Radnorshire","Merionethshire","Anglesey","Glamorganshire","Carmarthenshire","Montgomeryshire"]
countries=["France","Ireland","Italy","Spain","Netherlands","Germany","Belgium","Portugal"]

def find_median_date(v) :
	return (v["numStartDate"]+((v["numEndDate"]-v["numStartDate"])/2)).year

def set_county_or_country(v,county_or_country) :
	if county_or_country in v["places"] :
		return 1;

df1["median_date"]=df1.apply(find_median_date,axis=1)
# df1["median_date"]=df1["numStartDate"]+((df1["numEndDate"]-df1["numStartDate"])/2)

for county in counties :
	df1[county]=df1.apply(set_county_or_country,axis=1,args=(county,))

for country in countries :
	df1[country]=df1.apply(set_county_or_country,axis=1,args=(country,))

newcols=counties.copy()
newcols.insert(0,"median_date")

# df2=df1.loc[df1["median_date"],counties]
# df3=df2.groupby(level=0)
df2=df1[newcols]
#df3=df2.groupby("median_date")
df3=df2[counties].sum()
df4=df2[counties][df2["median_date"]<1370].sum()
df5=df2[counties][df2["median_date"]>1370].sum()
# df4=df2[counties][index<1370].sum()
# df5=df2[counties][index>1370].sum()
#print(df3.sum())

df1.to_csv("SC_8_analysis.csv")
df2.to_csv("SC_8_by_county.csv")
#df3.sum().to_csv("SC_8_by_county_grouped_by_year.csv")
df3.to_csv("SC_8_summed_by_county.csv")
df4.to_csv("SC_8_summed_by_county_before_1370.csv")
df5.to_csv("SC_8_summed_by_county_after_1370.csv")

plot1=df3.plot.bar()
fig1=plot1.get_figure()
fig1.savefig("SC_8_summed_by_county.png")
plot2=df4.plot.bar()
fig2=plot2.get_figure()
fig2.savefig("SC_8_summed_by_county_before_1370.png")
plot3=df5.plot.bar()
fig3=plot3.get_figure()
fig3.savefig("SC_8_summed_by_county_after_1370.png")
