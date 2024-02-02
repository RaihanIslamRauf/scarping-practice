from bs4 import BeautifulSoup
import requests

url = 'https://www.agoda.com/search?city=512855&locale=en-us&ckuid=bcf3ee6e-85f3-45ca-875d-9338be044522&prid=0&currency=USD&correlationId=03de6b94-2fd9-410a-b26c-1601f3c4eff6&analyticsSessionId=4989292126398038756&pageTypeId=1&realLanguageId=1&languageId=1&origin=BD&cid=-1&userId=bcf3ee6e-85f3-45ca-875d-9338be044522&whitelabelid=1&loginLvl=0&storefrontId=3&currencyId=7&currencyCode=USD&htmlLanguage=en-us&cultureInfoName=en-us&machineName=sg-pc-6f-acm-web-user-55d998b4bd-ssgr7&trafficGroupId=4&sessionId=1ssp1xft0ebpetcixnuez1jk&trafficSubGroupId=4&aid=130243&useFullPageLogin=true&cttp=4&isRealUser=true&mode=production&browserFamily=Chrome&cdnDomain=agoda.net&checkIn=2024-02-09&checkOut=2024-02-10&rooms=1&adults=2&children=0&priceCur=USD&los=1&textToSearch=Chittagong&travellerType=1&familyMode=off&ds=rJtAyZNuIm8xvDGi&productType=-1'
res = requests.get(url)
html = res.text
soup = BeautifulSoup(html, 'html.parser')
line = soup.find_all('div',{'class':'a9178-box a9178-text-inherit a9178-fill-inherit a9178-inline               '})
for line in soup.find_all('h3',{'class':'sc-jrAGrp sc-kEjbxe eDlaBj dscgss'}):
   print(line.string)
