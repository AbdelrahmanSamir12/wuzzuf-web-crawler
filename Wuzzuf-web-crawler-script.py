import pandas as pd
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from tqdm import tqdm

def start_selenuim():
    """
    this function starts selenuim web driver only once to make the script faster
    and returns an object of chrome driver
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    # options.add_argument('--headless')
    options.add_argument('window-size=50x50');
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(800, 800)
    return driver

def load_page_selenuim(link):
    driver.get(link);
    return BeautifulSoup(driver.page_source)

def load_page_requests(link):
    page = requests.get(link)
    src = page.content
    soup = BeautifulSoup(src,"lxml")
    return soup

def find_results_num(link):
    pure_page = load_page_selenuim(link)
    return int(pure_page.find("strong").text.replace(",",""))


def do_job_page_scraping(link):
    soup = load_page_selenuim("https://wuzzuf.net" + link)

    section1 = soup.find("section", {"class": "css-dy1y6u"})
    try:
        title = section1.find("h1").text
    except:
        title = section1.find("h1", {"class": "css-f9uh36"}).text

    try:
        company = section1.find("a", {"class": "css-p7pghv"}).text
        c_link = section1.find("a", {"class": "css-p7pghv"}).attrs["href"]
    except:
        company = "Confidential Company"
        c_link = "Confidential Company"

    post = section1.find("span", {"class": "css-182mrdn"}).text
    job_title.append(title)
    company_name.append(company)
    company_link.append(c_link)
    posted.append(post)

    section2 = soup.find("section", {"class": "css-3kx5e2"})
    job_details = section2.find_all("span", {"class": "css-4xky9y"})

    experience.append(job_details[0].text)
    career_level.append(job_details[1].text)
    education_level.append(job_details[2].text)

    if (len(job_details) == 4):
        salary.append(job_details[3].text)
    else:
        salary.append(job_details[4].text)

    categories = section2.find("div", {"class": "css-13sf2ik"}).find_all("span", {"class": "css-158icaa"})
    skills = section2.find("div", {"class": "css-s2o0yh"}).find_all("span", {"class": "css-158icaa"})
    categories_text = ""
    skill_text = ""
    for cat in categories:
        categories_text += cat.text + " | "
    for skill in skills:
        skill_text += skill.text + " | "

    job_category.append(categories_text[:-3])
    skills_and_tools.append(skill_text[:-3])


def do_full_scrapping(search):
    global jobs_num
    jobs_num = find_results_num(f"https://wuzzuf.net/search/jobs/?a=hpb%7Cspbg&q={search}")
    print(f"{jobs_num} jobs results has been found")
    global count
    count = 0
    for i in tqdm(range(0,(jobs_num //15)+1)):
        try:
            soup = load_page_requests(f"https://wuzzuf.net/search/jobs/?a=hpb%7Cspbg&q={search}&start={i}")
        except:
            continue
        l = soup.find_all("h2",{"class":"css-m604qf"})
        loc = soup.find_all("div",{"class":"css-d7j1kk"})
        for lo in loc :
            location.append(lo.find("span").text)
        for li in l :
            link = li.find("a").attrs['href']
            links.append("https://wuzzuf.net"+link)
            do_job_page_scraping(link)
            driver.refresh()
            count+=1


def save_data(search):
    data = {
        "Job title": job_title,
        "Company name": company_name,
        "Location": location,
        "posted": posted,
        "Experience": experience,
        "Career Level": career_level,
        "Education Level": education_level,
        "Salary": salary,
        "Job Categories": job_category,
        "Skills and Tools": skills_and_tools,
        "Job link": links,
        "Company Link": company_link
    }

    final_data = pd.DataFrame(data)
    final_data.to_csv(f"Wuzzuf_{search}.csv", index=False)
    print("website scrapping done succesfully")
    print("------------------------------------------------------")
    print("____________________Script Summary____________________")
    print(f" {count} jobs scrapped")
    print(f" {jobs_num - count} jobs not scrapped")
    print(f" The data has been saved in Wuzzuf_{search}.csv")
    print("--------------------------------------------------------")


def save_data_error(search, error):
    data = {
        "Job title": job_title[0:count],
        "Company name": company_name[0:count],
        "Location": location[0:count],
        "posted": posted[0:count],
        "Experience": experience[0:count],
        "Career Level": career_level[0:count],
        "Education Level": education_level[0:count],
        "Salary": salary[0:count],
        "Job Categories": job_category[0:count],
        "Skills and Tools": skills_and_tools[0:count],
        "Job link": links[0:count],
        "Company Link": company_link[0:count]
    }

    final_data_error = pd.DataFrame(data)
    final_data_error.to_csv(f"Wuzzuf_{search}.csv", index=False)
    print("Error has occured !")
    print(error)
    print("------------------------------------------------------")
    print("____________________Script Summary___________________")
    print(f" {count} jobs scrapped ")
    print(f" {jobs_num - count} jobs not scrapped")
    print(f" The data has been saved in Wuzzuf_{search}.csv")
    print("--------------------------------------------------------")


def main_script():
    print("Wuzzuf.net website scrapping")
    search = input(
        "type the search keyword you want to scrap -if you want to scrap all the website data press enter - :")
    global driver
    driver = start_selenuim()

    global links, location, job_title, company_name, company_link, location, posted, details, experience, career_level, education_level, salary, job_category, skills_and_tools

    links = []
    job_title = []
    company_name = []
    company_link = []
    location = []
    posted = []
    details = []
    experience = []
    career_level = []
    education_level = []
    salary = []
    job_category = []
    skills_and_tools = []

    try:
        do_full_scrapping(search)
        save_data(search)
    except Exception as error:
        save_data_error(search, error)

main_script()
