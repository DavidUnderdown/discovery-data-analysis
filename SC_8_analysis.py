import pandas as pd;
import matplotlib.pyplot as plt;
import matplotlib.tight_layout as lyt;
import matplotlib;

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
# df4=df2[counties][df2["median_date"]<1370].sum()
# df5=df2[counties][df2["median_date"]>1370].sum()
print(df3)
df3=df3[df3 >= 25].sort_values(ascending=False)
print(df3)

df4=df2[df3.keys()][df2["median_date"]<1370].sum()#.sort_values(ascending=False)
df5=df2[df3.keys()][df2["median_date"]>1370].sum()#.sort_values(ascending=False)
# df4=df2[counties][index<1370].sum()
# df5=df2[counties][index>1370].sum()
#print(df3.sum())

df1.to_csv("SC_8_analysis.csv")
df2.to_csv("SC_8_by_county.csv")
#df3.sum().to_csv("SC_8_by_county_grouped_by_year.csv")
df3.to_csv("SC_8_summed_by_county.csv")
df4.to_csv("SC_8_summed_by_county_before_1370.csv")
df5.to_csv("SC_8_summed_by_county_after_1370.csv")


fig1, ax1 = plt.subplots()
axSubPlot1=df3.plot.bar(ax=ax1,color="xkcd:royal blue")#,figsize(15,14)
ax1.set_xlabel("Counties")
ax1.set_ylabel("Number of petitions")
ax1.yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator(n=10))
fig1.tight_layout()
fig1.savefig("SC_8_summed_by_county.png",bbox='tight',pad_inches=5)

fig2, ax2 = plt.subplots()
axSubPlot2=df4.plot.bar(ax=ax2,color="xkcd:red")#,figsize=(9,14)
ax2.set_xlabel("Counties")
ax2.set_ylabel("Number of petitions")
ax2.yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator(n=10))
fig2.tight_layout()
fig2.savefig("SC_8_summed_by_county_before_1370.png")

fig3, ax3 = plt.subplots()
axSubPlot3=df5.plot.bar(ax=ax3,color="xkcd:yellow")#,figsize=(9,14)
ax3.set_xlabel("Counties")
ax3.set_ylabel("Number of petitions")
ax3.yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator(n=10))
fig3.tight_layout()
fig3.savefig("SC_8_summed_by_county_after_1370.png")
