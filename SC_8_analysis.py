import pandas as pd;                #version 0.22.0, data analysis package, gives us "super spreadsheet" capabilities, everything Excel can do and more
import matplotlib.pyplot as plt;    #sub module of below
import matplotlib;                  #version 2.1.2, plotting package, some parts are subclassed by pandas, but importing directly gives more control over output

## Create DataFrame by reading in CSV file originally created by calling Discovery API from discovery_api_SearchRecords.py
## Make sure dates are recognised as such during the load
df1=pd.read_csv(r"..\DiscoveryAPI\myRecords.csv",parse_dates=["numStartDate","numEndDate"],infer_datetime_format=True,dayfirst=True,dtype={"addressees":str})
## Set up list of counties and countries expected to be found in data (would be good to find an external source for these)
counties=["Yorkshire","Kent","Norfolk","Hampshire","Devon","Northumberland","Cornwall","Lincolnshire","Surrey","Oxfordshire","Suffolk","Sussex","Berkshire","Essex","Gloucestershire","Warwickshire","Wiltshire","Buckinghamshire","Dorset","Somerset","Cambridgeshire","Middlesex","Northamptonshire","Hertfordshire","Shropshire","Staffordshire","Nottinghamshire","Lancashire","Cheshire","Derbyshire","Cumberland","Huntingdonshire","Leicestershire","Channel Islands","Denbighshire","County Durham","Herefordshire","Flintshire","Bedfordshire","Westmorland","Worcestershire","Monmouthshire","Rutland","Caernarfonshire","Pembrokeshire","Brecknockshire","Cardiganshire","Radnorshire","Merionethshire","Anglesey","Glamorganshire","Carmarthenshire","Montgomeryshire"]
countries=["France","Ireland","Italy","Spain","Netherlands","Germany","Belgium","Portugal"]

def find_median_date(v) :
	'''Given the start and end dates, take the median year given for the petition for purposes of charting'''
	return (v["numStartDate"]+((v["numEndDate"]-v["numStartDate"])/2)).year

def set_county_or_country(v,county_or_country) :
	'''Prepare for charting by checking the places column to see if county or country is mentioned (can be more than one of each)'''
	if county_or_country in v["places"] :
		return 1;

def normalise_adressees(v) :
	'''Set addressee to title case and other normalisation for analysis'''
	v["addressees"]=str(v["addressees"]).title().strip(" .?").replace("And","and").replace("Of","of").replace("In","in").replace("The","the").replace("This","this").replace("'S","'s").replace("Other","other").replace("His","his")
	return v["addressees"]

def make_plot(pSeries, file_type, kind, x_label="", y_label="", **kwargs ) :
	'''Set up plot given input series, the output file_type, the kind of plot wanted, x and y labels if wanted (default to blank), and any  other keywords (need to be recognised by matplotlib)'''
	fig, ax = plt.subplots()
	if kind=="pie" :
		ax.set_aspect("equal")
		# ax.legend()
	axSubPlot=pSeries.plot(kind=kind,ax=ax,**kwargs)
	ax.set_title(pSeries.name.replace("_"," "))
	ax.set_xlabel(x_label)
	ax.set_ylabel(y_label)
	ax.yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator(n=10))
	fig.tight_layout()
	fig.savefig(pSeries.name+file_type,bbox='tight',pad_inches=5)

def group_not_knowns(df) :
	'''Take a list of values that all indicate that no addressee is known, and group them together as one'''
	NotKnowns=["Nan","None Specified","Lost","Missing","Not Specified","None"]
	df.loc["Unknown or lost"]=df.loc[df.index.intersection(NotKnowns)].sum()
	df.drop(index=df.index.intersection(NotKnowns),inplace=True)
	return df

## Get the median year so we have a single year for each petition
df1["median_date"]=df1.apply(find_median_date,axis=1)

## Create column in DataFrame for each county, then for each row count if that county mentioned
for county in counties :
	df1[county]=df1.apply(set_county_or_country,axis=1,args=(county,))

## Same for countries
for country in countries :
	df1[country]=df1.apply(set_county_or_country,axis=1,args=(country,))

## Build a new list from the counties list, then add median_date to the start of the list
newcols=counties.copy()
newcols.insert(0,"median_date")

## create a new DataFrame taken from the  median_date and counties columns only of the original DataFrame
df2=df1[newcols]

## Now sum up the totals for each county within the DataFrame (which gives us a Series as an output).  Sort the series into descending order by totals
## Give Series a name (which will be used to create file names and title for the chart we produce)
s1=df2[counties].sum()
s1=s1[s1 >= 25].sort_values(ascending=False)
s1.rename("SC_8_petitions_summed_by_county",inplace=True)

## A second Series, first filter the DataFrame down to only petitions before 1370, then sum by county
s2=df2[s1.keys()][df2["median_date"]<1370].sum()
s2.rename("SC_8_petitions_summed_by_county_before_1370",inplace=True)

## A third Series, this time for petition after 1370 summed by county
s3=df2[s1.keys()][df2["median_date"]>1370].sum()
s3.rename("SC_8_petitions_summed_by_county_after_1370",inplace=True)

## Save our Series to csv files for reference.
s1.to_csv(s1.name+".csv")
s2.to_csv(s2.name+".csv")
s3.to_csv(s3.name+".csv")

## A couple of variables for things that will be common to all the charts we're about to produce.
## Images of the charts will be saved as PNG, the y axes for each chart will be labelled "Number of Petitions"
file_type=".png"
y_label="Number of petitions"

## Produce a bar chart from our first Series (using function above), make the bars blue
make_plot(s1, file_type, kind="bar", y_label=y_label, color="xkcd:royal blue" )

## Produce a bar chart from our first Series (using function above), make the bars red
make_plot(s2, file_type, kind="bar", y_label=y_label, color="xkcd:red" )

## Produce a bar chart from our first Series (using function above), make the bars yellow
make_plot(s3, file_type, kind="bar", y_label=y_label, color="xkcd:yellow" )

## Now analyse by addressee of petitions instead
df3=df1[["median_date","addressees"]]
df3=df3.sort_values("addressees")
df3["addressees"]=df3.apply(normalise_adressees,axis=1)
df3["addressee_count"]=1

## Sum grouped by addressee type
df4=df3[["addressees","addressee_count"]].groupby("addressees").sum().sort_values(by="addressee_count",ascending=False)
## Group together a variety of addressees that basically mean we don't know the addressee
df4=group_not_knowns(df4)
## Group together the odds and ends with low totals as "other"
df4.loc["Other"]=df4[df4["addressee_count"]<14].sum()
indexToOtherGroup=df4[df4["addressee_count"]<14].index
indexToRemainderGroup=df4[df4["addressee_count"]>=14].index
df4=df4[df4["addressee_count"]>=14]
# print(df4.describe)
s4=df4.squeeze()
s4.rename("SC_8_petitions_summed_by_addressee",inplace=True)
make_plot(s4,file_type,kind="pie",rotatelabels=True)#,aspect="equal",y="addressee_count",subplots=True,labels=None
# df4.to_csv("SC_8_petitions_summed_by_addressees.csv")
s4.to_csv("SC_8_petitions_summed_by_addressees.csv")

df5=df3[df3["median_date"]>1370][["addressees","addressee_count"]].groupby("addressees").sum().sort_values(by="addressee_count",ascending=False)
df5=group_not_knowns(df5)
## Not working, want to get the list of index values from the df4 query and apply them to df5 in a way that doesn't care if some values not in df5
df5.loc["Other"]=df5.loc[df5.index.intersection(indexToOtherGroup)].sum()
df5=df5.loc[df5.index.intersection(indexToRemainderGroup)]
df5.to_csv("SC_8_petitions_summed_by_addressees_after_1370.csv")

df6=df3[df3["median_date"]<1370][["addressees","addressee_count"]].groupby("addressees").sum().sort_values(by="addressee_count",ascending=False)
df6=group_not_knowns(df6)
## Not working, want to get the list of index values from the df4 query and apply them to df5 in a way that doesn't care if some values not in df5
df6.loc["Other"]=df6.loc[df5.index.intersection(indexToOtherGroup)].sum()
df6=df6.loc[df6.index.intersection(indexToRemainderGroup)]
df6.to_csv("SC_8_petitions_summed_by_addressees_before_1370.csv")

df1.to_csv("SC_8_petitions_analysis.csv")
df2.to_csv("SC_8_petitions_by_county.csv")
