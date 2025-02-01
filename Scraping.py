from selenium import webdriver
from selenium.webdriver.edge.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

class Scraping:
    def __init__(self, webdriver_path):
        # Initialiser le WebDriver Edge
        service = Service(webdriver_path)
        self.driver = webdriver.Edge(service=service)

    def scrape_page(self, soup, job_titles, companies, locations, salaries, job_types, experiences):
        # Fonction pour extraire les informations d'une page
        job_links = []
        for job_card in soup.find_all('div', class_='job_seen_beacon'):
            link = job_card.find('a', href=True)
            if link:
                job_links.append(link['href'])  # Collecter les liens des offres

        # Extraire les détails pour chaque lien de job
        for job_link in job_links:
            if not job_link.startswith('http'):
                job_link = 'https://www.indeed.com' + job_link  # Compléter l'URL

            self.driver.get(job_link)  # Aller à la page de l'offre d'emploi
            time.sleep(5)  # Attendre que la page charge

            # Récupérer le code HTML de la page de l'offre
            job_html_content = self.driver.page_source
            job_soup = BeautifulSoup(job_html_content, 'html.parser')

            # Titre du job
            title = job_soup.find('h1', class_='jobsearch-JobInfoHeader-title')
            job_titles.append(title.get_text(strip=True) if title else 'Title Not Listed')

            # Nom de l'entreprise
            company_name_tag = job_soup.find('a', class_='css-1ioi40n e19afand0')
            company_name = company_name_tag.get_text(strip=True) if company_name_tag else 'Company Not Listed'
            companies.append(company_name)

            # Localisation
            location = job_soup.find('div', {'data-testid': 'inlineHeader-companyLocation'})
            locations.append(location.get_text(strip=True) if location else 'Location Not Listed')

            # Salaire
            salary_tag = job_soup.find('div', {'role': 'group', 'aria-label': 'Pay'})
            if salary_tag:
                salary_div = salary_tag.find('div', class_='js-match-insights-provider-tvvxwd')
                salaries.append(salary_div.get_text(strip=True) if salary_div else 'Salary Not Listed')
            else:
                salaries.append('Salary Not Listed')

            # Type de travail
            job_type_tag = job_soup.find('div', {'role': 'group', 'aria-label': 'Job type'})
            if job_type_tag:
                job_type_div = job_type_tag.find('div', class_='js-match-insights-provider-tvvxwd')
                job_types.append(job_type_div.get_text(strip=True) if job_type_div else 'Job Type Not Listed')
            else:
                job_types.append('Job Type Not Listed')

            # Expérience requise
            description_text = job_soup.get_text(separator=" ")
            experience_match = re.search(r'(\d+)\+?\s*year[s]?\s*experience', description_text, re.IGNORECASE)
            if experience_match:
                experiences.append(experience_match.group(1) + "+ years")
            else:
                experiences.append('0')  # "0" si l'expérience n'est pas listée

    def scrape_jobs_with_pagination(self, job_title, location, num_pages):
        # Fonction pour scraper plusieurs pages de jobs
        job_titles = []
        companies = []
        locations = []
        salaries = []
        job_types = []
        experiences = []

        for page in range(num_pages):
            if page == 0:
                URL = f'https://www.indeed.com/jobs?q={job_title}&l={location}'
            else:
                start = page * 10
                URL = f'https://www.indeed.com/jobs?q={job_title}&l={location}&start={start}'

            self.driver.get(URL)
            time.sleep(5)  # Attendre que la page charge

            html_content = self.driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')

            # Scraper la page actuelle
            self.scrape_page(soup, job_titles, companies, locations, salaries, job_types, experiences)

        # Créer un DataFrame avec toutes les informations extraites
        df = pd.DataFrame({
            'Job Title': job_titles,
            'Company': companies,
            'Location': locations,
            'Salary': salaries,
            'Job Type': job_types,
            'Experience Required': experiences
        })

        return df

    def scrape_multiple_jobs_and_locations(self, job_location_list, num_pages=2):
        # Scraper pour plusieurs titres de jobs et localisations
        for job, location in job_location_list:
            print(f"Scraping {job} jobs in {location}...")
            df = self.scrape_jobs_with_pagination(job, location, num_pages)

            filename = f'{job}_jobs_in_{location}.csv'.replace(' ', '_')
            df.to_csv(filename, index=False)
            print(f"Saved data to {filename}")

    def close(self):
        # Fermer le driver après avoir terminé le scraping
        self.driver.quit()
