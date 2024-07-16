from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

class LinkedinDriver:
    """
    A class to automate interactions with LinkedIn using Selenium.
    This class is used instead of BeautifulSoup due to some issues with the latter.
    """

    def _setup_driver(self):
        """
        Set up the Chrome driver with specific options.
        """
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--force-device-scale-factor=0.6")
        chrome_options.add_argument("--lang=en-US")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    def __init__(self, email, password, collected = 0):
        """
        Initialize the LinkedinDriver with user credentials.

        Args:
            email (str): User's LinkedIn email.
            password (str): User's LinkedIn password.
        """
        self.email = email
        self.password = password
        self._setup_driver()
        self.job_urls = []
        self.job_titles = []
        self.collected = 0
        self.page_index = 0
        self.listed_jobs = []

    def login(self) -> bool:
        """
        Log in to LinkedIn using the provided credentials.
        """
        self.driver.get("https://www.linkedin.com/login/")

        email_field = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
        email_field.send_keys(self.email, Keys.ENTER)
        psw_field = self.driver.find_element(By.ID, "password")
        psw_field.send_keys(self.password, Keys.ENTER)
        time.sleep(2)
        if(EC.presence_of_element_located((By.CLASS_NAME, "error-for-username")) or EC.presence_of_element_located((By.ID, "error-for-password"))):
            return False
        return True

    def search_easy_apply_jobs(self):
        """
        Navigate to the LinkedIn Easy Apply jobs search page.
        """
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "application-outlet")))
        self.driver.get("https://www.linkedin.com/jobs/search/?currentJobId=3971455036&f_AL=true&origin=JOB_SEARCH_PAGE_JOB_FILTER")
        time.sleep(6)

    def collect_jobs(self, page_index=0, pages=3):
        """
        Collect job listings from LinkedIn.

        Args:
            page_index (int): Starting page index for job collection.
            pages (int): Number of pages to collect jobs from.
        """
        if pages <= 0:
            return

        try:
            jobs = self.driver.execute_script("""
                let jobElements = document.querySelectorAll('ul.scaffold-layout__list-container > li');
                let jobs = [];
                jobElements.forEach((job) => {
                    let titleElement = job.querySelector('a.job-card-list__title');
                    let linkElement = job.querySelector('a.job-card-list__title');
                    if (titleElement && linkElement) {
                        let jobTitle = titleElement.innerText;
                        let jobLink = linkElement.href;
                        jobs.push({title: jobTitle, link: jobLink});
                    }
                });
                return jobs;
            """)

            for job in jobs:
                if job['title'] not in self.job_titles and job['link'] not in self.job_urls:
                    self.job_titles.append(job['title'])
                    self.job_urls.append(job['link'])

            self.collected += len(jobs)
            self.page_index = page_index + 25

            print(f"Collected {len(jobs)} jobs from page {page_index // 25 + 1}")
            print(f"Total jobs collected: {len(self.job_titles)}")

            if pages - 1 > 0:
                self.driver.get(f"https://www.linkedin.com/jobs/search/?currentJobId=3945795600&f_AL=true&origin=JOB_SEARCH_PAGE_JOB_FILTER&start={self.page_index}")
                time.sleep(10)
                self.collect_jobs(self.page_index, pages - 1)

        except Exception as e:
            print(f"Unable to collect more jobs: {str(e)}")


    def close(self):
        """
        Close the browser and end the session.
        """
        if self.driver:
            self.driver.quit()