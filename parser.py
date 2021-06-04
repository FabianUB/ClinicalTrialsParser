import requests
import re
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time


def write_header():
  with open("studyentity.csv", mode='w') as file:
    fieldnames = ['id', 'ownerID', 'status', 'published', 'studyTitle', 'shortDescription', 'principalObjective',
                  'scientificContext', 'dataCollected', 'dataJustification', 'studyLogo', 'webPage', 'protocol', 'paper',
                  'socialMediaLinkedin']
    writer = csv.DictWriter(file, fieldnames)
    writer.writeheader()

def get_all_links_inside(url):
  driver = webdriver.Chrome()
  driver.implicitly_wait(30)
  driver.maximize_window()
  driver.get(url)
  webpages = []

  elems = driver.find_elements_by_xpath("//tr/td/a[@href]")

  for elem in elems:
    link = elem.get_attribute("href")
    index = link.find("show")
    link = link[:index+5] + "record/" + link[index+5:]
    webpages.append(link)
  return webpages

def get_all_links_outside(url):
  driver = webdriver.Chrome()
  driver.implicitly_wait(30)
  driver.maximize_window()
  driver.get(url)
  webpages = []

  elems = driver.find_elements_by_xpath("//tr/td/a[@href]")

  for elem in elems:
    link = elem.get_attribute("href")
    webpages.append(link)
  return webpages


def parse_trial(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    try:
        submitedDateSource = soup.find(text=re.compile("First Submitted Date"))
        submitedDate = submitedDateSource.parent.find_next_sibling("td").text
    except:
        submitedDate = ''
    try:
        idSource = soup.find_all(text=re.compile("NCT Number"))[-1]
        id = idSource.parent.find_next_sibling("td").text
    except:
        id = ''

    try:
        lastUpdateSource = soup.find(text=re.compile("Last Update Posted Date"))
        lastUpdate = lastUpdateSource.parent.find_next_sibling("td").text
    except:
        lastUpdate = ''

    try:
        titleSource = soup.find(text=re.compile("Brief Title"))
        title = titleSource.parent.find_next_sibling("td").text
    except:
        title = ''

    try:
        studyTypeSource = soup.find(text=re.compile("Study Type"))
        studyType = studyTypeSource.parent.find_next_sibling("td").text
    except:
        studyType = ''

    try:
        samplingMethodSource = soup.find(text=re.compile("Sampling Method"))
        samplingMethod = studyTypeSource.parent.find_next_sibling("td").text
    except:
        samplingMethod = ''

    try:
        briefSummarySource = soup.find(text=re.compile("Brief Summary"))
        briefSummary = briefSummarySource.parent.find_next_sibling("td").text
    except:
        briefSummary = ''

    try:
        biospecimenSource = soup.find(text=re.compile("Biospecimen"))
        biospecimen = biospecimenSource.parent.find_next_sibling("td").text
    except:
        biospecimen = ''

    try:
        populationSource = soup.find(text=re.compile("Study Population"))
        population = populationSource.parent.find_next_sibling("td").text
    except:
        population = ''

    try:
        interventionSource = soup.find(text=re.compile("Intervention"))
        intervention = interventionSource.parent.find_next_sibling("td").text
    except:
        intervention = ''

    try:
        recruitmentStatusSource = soup.find_all(text=re.compile("Recruitment Status"))[-1]
        recruitmentStatus = recruitmentStatusSource.parent.find_next_sibling("td").text
    except:
        recruitmentStatus = ''

    try:
        enrollmentSource = soup.find(text=re.compile("Actual Enrollment"))
        enrollment = interventionSource.parent.find_next_sibling("td").text
    except:
        enrollment = ''

    try:
        countrySource = soup.find(text=re.compile("Listed Location Countries"))
        country = countrySource.parent.find_next_sibling("td").text
    except:
        country = ''

    try:
        responsiblePartySource = soup.find_all(text=re.compile("Responsible Party"))[-1]
        responsibleParty = responsiblePartySource.parent.find_next_sibling("td").text
    except:
        responsibleParty = ''

    try:
        studySponsorSource = soup.find_all(text=re.compile("Study Sponsor"))[-1]
        studySponsor = studySponsorSource.parent.find_next_sibling("td").text
    except:
        studySponsor = ''

    try:
        collaboratorsSource =soup.find_all(text=re.compile("Collaborators"))[-1]
        collaborators = collaboratorsSource.parent.find_next_sibling("td").text
    except:
        collaborators = ''


    try:
        results = soup.find(id="results")
        resultsText = results.text
        if resultsText != "No Results Posted":
            link = results.find_all(href=True)[-1]
            link = link['href']
            resultsText = "https://www.clinicaltrials.gov/" + link

    except:
        results = ''
    try:
        with open("studyentity.csv", mode='a') as file:
            fieldnames = ['id', 'ownerID', 'status', 'published', 'studyTitle', 'shortDescription', 'principalObjective',
                          'scientificContext', 'dataCollected', 'dataJustification', 'studyLogo', 'webPage', 'protocol',
                          'paper',
                          'socialMediaLinkedin']
            writer = csv.DictWriter(file, fieldnames)
            row = {'id': id,
                   'ownerID': responsibleParty,
                   'status': recruitmentStatus,
                   'published': results,
                   'studyTitle': title,
                   'shortDescription': briefSummary,
                   'principalObjective': "NULL",
                   'scientificContext': "NULL",
                   'dataCollected': biospecimen,
                   'dataJustification': "NULL",
                   'studyLogo': "NULL",
                   'webPage': "NULL",
                   'protocol': studyType,
                   'paper': "NULL",
                   'socialMediaLinkedin': "NULL"}
            writer.writerow(row)
    except:
        print("There was an error with ID ", id)

categoriesLink = get_all_links_outside("https://www.clinicaltrials.gov/ct2/search/browse?brwse=cond_cat_BC01")

for link in categoriesLink:
    insideLinks = get_all_links_inside(link)
    for insideLink in insideLinks:
        parse_trial(insideLink)
        time.sleep(5)