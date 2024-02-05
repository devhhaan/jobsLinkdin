import asyncio
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from datetime import datetime, timedelta
from proxybroker import Broker

# Manually set up asyncio event loop for Windows
if not asyncio.get_event_loop().is_running():
    asyncio.set_event_loop(asyncio.ProactorEventLoop())

# Function to get a rotating proxy
def get_rotating_proxy():
    proxies = []
    broker = Broker()
    tasks = asyncio.gather(broker.find(types=['HTTP', 'HTTPS'], limit=1))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)

    for proxy in tasks.result():
        proxies.append(f"{proxy.host}:{proxy.port}")

    return proxies[0]



l = []
o = {}
k = []
country = "India"
country_encoded_string = quote(country)

jobPost = "react js"
jobPost_encoded_string = quote(jobPost)

# Function to convert relative time to absolute time
def convert_relative_time(time_text):
    now = datetime.now()

    if "seconds" in time_text or "minutes" in time_text or "hours" in time_text:
        # For seconds, minutes, and hours, we can use the current time
        return now

    elif "day" in time_text:
        # Extract the number of days
        days_ago = int(time_text.split()[0])
        return now - timedelta(days=days_ago)

    elif "week" in time_text:
        # Extract the number of weeks
        weeks_ago = int(time_text.split()[0])
        return now - timedelta(weeks=weeks_ago)

    elif "month" in time_text:
        # Extract the number of months
        months_ago = int(time_text.split()[0])
        return now - timedelta(days=30 * months_ago)

    elif "year" in time_text:
        # Extract the number of years
        years_ago = int(time_text.split()[0])
        return now - timedelta(days=365 * years_ago)

    else:
        raise ValueError("Unsupported time format")


# Set up headers and target URL
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}

target_url = 'https://www.l8888888888888888888&location={}&geoId=102713980&currentJobId=3415227738&start={}'

# Loop through job postings
for i in range(0, 1):
    # Use rotating proxy for each request
    proxy = get_rotating_proxy()
    proxies = {"http": f"http://{proxy}", "https": f"https://{proxy}"}
    
    res = requests.get(target_url.format(jobPost_encoded_string, country_encoded_string, i), headers=headers, proxies=proxies)
    soup = BeautifulSoup(res.text, 'html.parser')
    alljobs_on_this_page = soup.find_all("li")
    print(len(alljobs_on_this_page))
    for x in range(0, len(alljobs_on_this_page)):
        jobid = alljobs_on_this_page[x].find("div", {"class": "base-card"}).get('data-entity-urn').split(":")[3]
        l.append(jobid)

# Set up the target URL for detailed job information
target_url = 'https://www.9999999999999999999999st/jobs/api/jobPosting/{}'

# Loop through job details
for j in range(0, 1):
    # Use rotating proxy for each request
    proxy = get_rotating_proxy()
    proxies = {"http": f"http://{proxy}", "https": f"https://{proxy}"}
    
    resp = requests.get(target_url.format(l[j]), headers=headers, proxies=proxies)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    try:
        o["company"]=soup.find("div",{"class":"top-card-layout__card"}).find("a").find("img").get('alt')
    except:
        o["company"]=None

    try:
        o["job-title"]=soup.find("div",{"class":"top-card-layout__entity-info"}).find("a").text.strip()
    except:
        o["job-title"]=None

    try:
        o["level"]=soup.find("ul",{"class":"description__job-criteria-list"}).find("li").text.replace("Seniority level","").strip()
    except:
        o["level"]=None
    try:
        o["jobPoster"]=soup.find("h3",{"class":"base-main-card__title"}).text.strip()
        try:
            o["jobPostersProfile"]=soup.find("div",{"class":"base-main-card__info"}).find("h4", {"class":"base-main-card__subtitle"}).text.strip()
        except:
            o["jobPostersProfile"]=None
    except:
        o["jobPoster"]=None
    try:
        company_linkedin_profile = soup.find("div", {"class": "top-card-layout__card"}).find("a")
        if company_linkedin_profile:
                print('1', company_linkedin_profile["href"])
                respInternal = requests.get(company_linkedin_profile["href"])
                print(respInternal.raise_for_status());
                soupInternal=BeautifulSoup(respInternal.text,'html.parser')
                company_website = soup.find("div",{"class":"org-top-card-primary-actions__inner"}).find("a");
                o["companyLinkDinProfile"] = company_website["href"] if company_website else None
        else:
            print('2')
            o["companyLinkDinProfile"] = None
    except:
        print('3')
        o["companyLinkDinProfile"] = None
    try:
        time_text = soup.find("span",{"class":"posted-time-ago__text"}).text.strip();
        dateOnPosted = convert_relative_time(time_text)
        o["postedOn"]= dateOnPosted
    except:
        o["postedOn"]=None

    print(o['companyLinkDinProfile'], o['postedOn']);
    k.append(o)
    o={}


# Convert the list of job details to a DataFrame and save it to a CSV file
df = pd.DataFrame(k)
df.to_csv('linkedinJobs.csv', index=False, encoding='utf-8')
