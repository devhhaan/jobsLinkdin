import requests
from bs4 import BeautifulSoup
import math
import pandas as pd
from urllib.parse import quote
from datetime import datetime, timedelta
from flask import Flask, request

app = Flask(__name__)


@app.route('/run_linkedInScrap_function', methods=['GET'])
def run_linkedInScrap_function():
    print('dev')
    # Get parameters from the request
    country = request.args.get('country')
    job_post = request.args.get('job_post')

    print("Country:", country)
    print("Job Post:", job_post)
   # Call your xyz_function with the parameters
    result = linkedin_scrapping_business_logic(country, job_post)
    return 'CSV GENERATING...'


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
def linkedin_scrapping_business_logic(country, job_post):
    l=[]
    o={}
    k=[]
    country_ = country
    country_encoded_string = quote(country_)

    jobPost_ = job_post
    jobPost_encoded_string = quote(jobPost_)
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}
    target_url='https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={}&location={}&geoId=102713980&currentJobId=3415227738&start={}'

    for i in range(0,math.ceil(100/25)):
        res = requests.get(target_url.format(jobPost_encoded_string,country_encoded_string,i))
        soup=BeautifulSoup(res.text,'html.parser')
        alljobs_on_this_page=soup.find_all("li")
        print(len(alljobs_on_this_page))
        for x in range(0,len(alljobs_on_this_page)):
            jobid = alljobs_on_this_page[x].find("div",{"class":"base-card"}).get('data-entity-urn').split(":")[3]
            l.append(jobid)


    target_url='https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'
    for j in range(0,len(l)):

        resp = requests.get(target_url.format(l[j]))
        soup=BeautifulSoup(resp.text,'html.parser')
        print(target_url.format(l[0]))
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
            company_linkedin_profile = soup.find("section", {"class": "top-card-layout"}).find("div", {"class": "top-card-layout__card"}).find("a")
            if company_linkedin_profile:
                print('1', company_linkedin_profile["href"])
                respInternal = requests.get(company_linkedin_profile["href"])
                respInternal.raise_for_status()  # This will raise an error if the request is not successful
                soupInternal = BeautifulSoup(respInternal.text, 'html.parser')
                company_website = soup.find("a", {"class": "link-no-visited-state"})
                o["companyLinkDinProfile"] = company_linkedin_profile["href"] if company_linkedin_profile else None
            else:
                print('2')
                o["companyLinkDinProfile"] = None
        except Exception as e:
            print('2')
            print('Error:', e)
        try:
            time_text = soup.find("span",{"class":"posted-time-ago__text"}).text.strip();
            dateOnPosted = convert_relative_time(time_text)
            o["postedOn"]= dateOnPosted
        except:
            o["postedOn"]=None
        k.append(o)
        o={}

    df = pd.DataFrame(k)
    df.to_csv('linkedinJobs.csv', index=False, encoding='utf-8')
if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app in debug mode
