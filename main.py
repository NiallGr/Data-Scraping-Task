# Import required module
import requests
import bs4
import re
from csv import writer

# Make Requests from Webpage
url = 'https://clutch.co/agencies/event'
result = requests.get(url).text
# Create soup object
soup = bs4.BeautifulSoup(result, 'lxml')

# Searching li tags for with provider class
list_of_companys = soup.find_all('li', class_='provider provider-row')

# Create CSV file
with open('Data_Scraping_Task_NG.csv', 'w', encoding='utf8', newline='') as f:
    thewriter = writer(f)

    # Creating Header for CSV file
    header = ['Company Name', 'Company Description', 'Company Rating', 'Company Reviews', "Min Project Budget",
              "Avg. Hourly Rate", "Company Size", 'Company Location', 'Company Contact', 'Contact Number',
              'Company Focus', 'company Website',
              ]
    # Write Header
    thewriter.writerow(header)

    # Number of result pages
    pages = 80

    # Loop through Pages (1 - 80)
    for page in range(1, pages + 1):
        # url + Current page +1 each loop
        url = f"https://clutch.co/agencies/event?page={page}"
        result = requests.get(url).text
        # Create soup object
        soup = bs4.BeautifulSoup(result, 'lxml')
        print(f"printing page {page}")

        # Loop through to assign data
        for company in list_of_companys:

            # Name
            company_name = company.find('a', class_='company_title directory_profile').string.strip()

            # Description
            company_description = company.find('p', class_='company_info__wrap tagline').string.strip()

            # Rating
            company_rating = company.find('span', class_='rating sg-rating__number').string.strip()

            # Review
            company_review_number = company.find('a', class_='reviews-link sg-rating__reviews directory_profile').string.strip()

            # Min project budget
            company_min_project_budget_parent = company.find('div', class_='list-item block_tag custom_popover')
            company_min_project_budget = company_min_project_budget_parent.find('span').get_text()

            # Avg. Hourly Rate
            Hour_And_size = company.find_all('div', class_='list-item custom_popover')
            company_avg_hourly_rate = Hour_And_size[0].get_text().strip()

            # Number of Staff member
            company_size_pre = Hour_And_size[1].get_text().strip()

            # Stops smaller number (2-9) turning into a date format - excel
            company_size = "'" + company_size_pre

            # Location
            company_location = company.find('span', class_='locality').text

            # Company Contact
            company_contact = company.find('a', class_="provider-detail-contact").get("href")

            # Percentage of company focus
            company_focus = company.find('div', class_="chart-label").get_text()
            company_focus_ = str(company_focus).strip()

            # Company Website
            company_website_pre = company.find('a', class_="website-link__item").get("href")

            # Added HyperLink tag for easier access in Excel
            company_website = "=HYPERLINK(\"" + company_website_pre + "\")"

            # Company Phone Number
            if ' ' in company_name:
                company_name_url = company_name.replace(" ", "-").lower()
            elif '/' in company_name:
                company_name_url = company_name.replace("/", "").lower()
            elif '&' in company_name:
                company_name_url = company_name.replace("&", "").lower()
            else:
                company_name_url = company_name.lower()

            # To find the contact number we need to request another url
            # Get custom url based on company name
            url1 = f"https://clutch.co/profile/{company_name_url}#summary"
            # Results in text
            result1 = requests.get(url1).text

            # Create soup of the new page containing extra information
            phonenumber = bs4.BeautifulSoup(result1, 'lxml')

            # Try, Pass (If url is not broken it will return a number, Else it will return phone number not found)
            try:
                finding_phone_bumber = phonenumber.find("section", class_='quick-menu active provider-row')
                company_contact_number = finding_phone_bumber.find("a", class_='contact phone_icon').string.strip()

            except:
                company_contact_number = " Not found "
                pass

            # # Searching section tags for social media class names
            # finding_Socials = phonenumber.find("section", class_='quick-menu active provider-row')
            #
            # #Check for LinkedIn
            # try:
            #     company_linkedIn = finding_phone_bumber.find("a", class_='profile-social-link linkedin').get("href")
            # except:
            #     company_linkedIn = " LinkedIn Not listed"
            #     pass
            #
            # #Check For Facebook
            # try:
            #     company_facebook = finding_phone_bumber.find("a", class_='profile-social-link facebook').get("href")
            # except:
            #     company_facebook = "Facebook Not Listed"
            #     pass
            #
            # #Check for Twiiter
            # try:
            #     company_twitter = finding_phone_bumber.find("a", class_='profile-social-link twitter').get("href")
            # except:
            #     company_twitter = "Twitter Not Listed"
            #     pass
            #
            # #Check for Youtube
            # try:
            #     company_youtube = finding_phone_bumber.find("a", class_='profile-social-link youtube').get("href")
            # except:
            #     company_youtube = "Youtube Not Listed"
            #     pass
            #
            # # Check for Instagram
            # try:
            #     company_instagram = finding_phone_bumber.find("a", class_='profile-social-link instagram').get("href")
            # except:
            #     company_instagram = "Youtube Not Listed"
            #     pass

            # Store values in Array
            company_total_info = [company_name, company_description, company_rating,
                                  company_review_number, company_min_project_budget, company_avg_hourly_rate,
                                  company_size, company_location, company_contact_number, company_contact, company_focus_,
                                  company_website,
                                  ]

            # Write array content to CSV file and begin the loop again.
            thewriter.writerow(company_total_info)

# When pages loop complete print "Finished"
print("Finished")