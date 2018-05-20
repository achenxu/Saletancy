
"""
Created on Fri Mar 30 20:11:45 2018

@author: canascasco
"""
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

pages = ["http://www.indiabusinesstoday.in/detail/wetecho-solutions-1-499929",
         "http://www.indiabusinesstoday.in/detail/my-envy-box-beauty-and-cosmetics-products-shopping-1-499930",
         "http://www.indiabusinesstoday.in/detail/techflow-enterprises-pvt-ltd-1-499923" ,
         "http://www.indiabusinesstoday.in/detail/voylla-fashions-pvt-ltd-jaipur-1-550530",
         "http://www.indiabusinesstoday.in/detail/watering-vacuum-pump-manufacturers-in-gujarat-481471",
         "http://www.indiabusinesstoday.in/detail/omr-sheet-software-1-445908",
         "http://www.indiabusinesstoday.in/detail/gemstones-1-499928",
         "http://www.indiabusinesstoday.in/detail/web-site-designing-1-499927",
         "http://www.indiabusinesstoday.in/detail/bulk-sms-499916",
         "http://www.indiabusinesstoday.in/detail/kc-enterprises-2-405313",
         "http://www.indiabusinesstoday.in/detail/pinpicker-499917",
         "http://www.indiabusinesstoday.in/detail/jrd-realtorss-551670",
         "http://www.indiabusinesstoday.in/detail/cms-computers-ltd-mumbai-976",
         "http://www.indiabusinesstoday.in/detail/watering-vacuum-pump-manufacturers-in-gujarat-481471",
         "http://www.indiabusinesstoday.in/detail/online-shopping-1-501800",
         "http://www.indiabusinesstoday.in/detail/my-fit-fuel-online-whey-protein-shopping-india-499925",
         "http://www.indiabusinesstoday.in/detail/force-one-systems-1-499922"]

#pages = ["http://www.indiabusinesstoday.in/detail/force-one-systems-1-499922"]

address, city, pincode, state, telephone, mobile_phone, website, contact_name, company_name, designation = [],[],[],[],[],[],[],[],[],[]

for item in pages:
    page = requests.get(item)
    # In order to parse this document we can use the BeautifulSoup library
    soup = BeautifulSoup(page.content, 'html.parser')

    company_name.append(soup.find('h1', class_ = "panel-title").text)   

    address_splitted = soup.find(itemprop = "address").text
    p = re.compile("(\.|\+|\:)")
    address_splitted = p.sub("", address_splitted)

    address.append(soup.find('span', itemprop = "streetAddress").text)
    city.append(soup.find('span', itemprop = "addressLocality").text)
    state.append(soup.find('span', itemprop = "addressRegion").text)
    
    pin = [int(s) for s in address_splitted.lower() if s.isdigit()]
    pincode.append(pin[len(pin)-6:])

    list_group_item = soup.find_all(class_ = 'list-group-item')
    contact = list_group_item[1].text.strip()
    role = '-'
    contact = ''.join([i for i in contact if not i.isdigit()])
    
    try:
        name_contact, role = contact.split(',')
    except ValueError:
        name_contact = contact
        
    if 'Click to Call' in name_contact:
        contact_name.append('')
        designation.append(role)
    else:
        contact_name.append(name_contact)
        designation.append(role)
    
    website.append(list_group_item[-1].text.strip())
    agenda_mobile = soup.find("span", id="click_to_call_no").text.strip()
      

    try:
        phone, tele = agenda_mobile.split(',')
        mobile_phone.append(phone.strip())
        telephone.append(tele.strip())
    except ValueError:
        if agenda_mobile[0] == "+":
            mobile_phone.append(agenda_mobile.strip())
            telephone.append("")
        else:
            telephone.append(agenda_mobile.strip())
            mobile_phone.append("")
    
    
df_result = pd.DataFrame(columns = ['Company Name','Contact Name','Designation',
                                    'Street Address', 'City', 'State', 'Pincode',
                                    'Email','Phone','Mobile','Website','Employee Size'])

df_result['Company Name'] = company_name
df_result['Contact Name'] = contact_name
df_result['Designation'] = designation
df_result['Street Address'] = address
df_result['City'] = city
df_result['State'] = state
df_result['Pincode'] = pincode
df_result['Phone'] = telephone
df_result['Mobile'] = mobile_phone
df_result['Website'] = website
   
df_result.to_csv('saletancy.csv.', sep='\t', encoding='utf-8')
    
writer = pd.ExcelWriter('saletancy.xlsx', engine='xlsxwriter')
# Convert the dataframe to an XlsxWriter Excel object.
df_result.to_excel(writer, sheet_name='Sheet1')
    
    
