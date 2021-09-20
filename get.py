import re
from collections import Counter 
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv
import string

testurl="https://affordablehousing.com/detroit-mi/section8-owners/"


bedrooms = input("Enter # of bedrooms (1-5) ")
bathrooms=input("# of bathrooms (1-5) ")
type=input("Enter Property Type (Apartment, Condo, Townhouse, Single Family Home) press enter for no specification ")
type=type.lower()

if len(type)>0:
    type=type+"/"
url=f"https://affordablehousing.com/detroit-mi/{bedrooms}-bed/{bathrooms}-bath/{type}section8-owners/"
#need to build url based on parameters, going to start with simple base scrape though


page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")



pricedivs =soup.find_all("div", {"class": "tnresult--price"})
address=soup.find_all("div", {"class": "tnresult--propertyaddress"})
sizedivs= soup.find_all("div", {"class": "tnresult--bedbath"})

url2=f"https://affordablehousing.com/detroit-mi/{bedrooms}-bed/{bathrooms}-bath/{type}section8-owners/page-2/"
page = urlopen(url2)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

pricedivs2 =soup.find_all("div", {"class": "tnresult--price"})
address2=soup.find_all("div", {"class": "tnresult--propertyaddress"})
sizedivs2= soup.find_all("div", {"class": "tnresult--bedbath"})



sizes=[]
for element in sizedivs:
    split_list=str(element).split("<em>")
    bed=split_list[0][-2:]
    bed=str(bed)+"Bed| "
    bath=split_list[2][-2:]
    bath=str(bath)+"Bath| "
    if len(split_list)>=5:
        sqft=split_list[4][-4:]
        sqft=str(sqft)+"Sqft"
        sizeObj=bed+bath+sqft
    else:
        sizeObj=bed+bath
    sizes.append(sizeObj)

sizes2=[]
for element in sizedivs2:
    split_list=str(element).split("<em>")
    bed=split_list[0][-2:]
    bed=str(bed)+"Bed| "
    bath=split_list[2][-2:]
    bath=str(bath)+"Bath| "
    if len(split_list)>=5:
        sqft=split_list[4][-4:]
        sqft=str(sqft)+"Sqft"
        sizeObj=bed+bath+sqft
    else:
        sizeObj=bed+bath
    sizes2.append(sizeObj)
    #final=split_list[1][-1:]+"Bed"+split_list[5]+"Bath"





boolCheck=len(pricedivs)==len(sizedivs)==len(address)
check2=len(pricedivs2)==len(sizedivs2)==len(address2)

val=0
final_list=[]
if boolCheck and check2:
    if len(pricedivs)==0:
        print("No Listings with given parameters")
    while val<len(address):
        tempDict={
            "Address":address[val].string,
            "Price": pricedivs[val].string,
            "Size":sizes[val]
        }
        tempDict2={
            "Address":address2[val].string,
            "Price": pricedivs2[val].string,
            "Size":sizes2[val]
        }
        final_list.append(tempDict)
        final_list.append(tempDict2)

        val+=1

breakpoint()

for value in final_list:
    add=str(value["Address"])
    add=add.replace(" ","-")
    add=add.replace(",","")
    url=f"https://affordablehousing.com/detroit-mi/{add}"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    test=soup.find("div", {"class": "prem--owner--phn"})
    split1=str(test).split(">")
    split2=split1[3].split("(")
    number=split2[1][0:13]
    number=number.replace(")","")
    number=number.replace("-"," ")
    value["Phone Number"]=number
        




keys=final_list[0].keys()
a_file=open("housing_options.csv", "w")
dict_writer = csv.DictWriter(a_file, keys)
dict_writer.writeheader()
dict_writer.writerows(final_list)
a_file.close()   







