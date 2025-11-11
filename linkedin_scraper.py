"""
LinkedIn Scraper for finding HR and hiring personnel
"""
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import config


class LinkedInScraper:
    """Scraper class for LinkedIn HR personnel search"""

    def __init__(self, email=None, password=None, headless=None):
        """
        Initialize the LinkedIn scraper

        Args:
            email (str): LinkedIn email
            password (str): LinkedIn password
            headless (bool): Run browser in headless mode
        """
        self.email = email or config.LINKEDIN_EMAIL
        self.password = password or config.LINKEDIN_PASSWORD
        self.headless = headless if headless is not None else config.HEADLESS_MODE
        self.driver = None
        self.wait = None

    def setup_driver(self):
        """Setup Chrome WebDriver with appropriate options"""
        chrome_options = Options()

        if self.headless:
            chrome_options.add_argument('--headless')

        # Additional options for stability
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

        # Initialize driver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(config.IMPLICIT_WAIT)
        self.driver.set_page_load_timeout(config.PAGE_LOAD_TIMEOUT)

        # Setup wait
        self.wait = WebDriverWait(self.driver, 10)

        print("✓ WebDriver initialized successfully")

    def login(self):
        """Login to LinkedIn"""
        if not self.email or not self.password:
            raise ValueError("LinkedIn credentials not provided. Please set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in .env file")

        try:
            print("Logging into LinkedIn...")
            self.driver.get(config.LINKEDIN_LOGIN_URL)
            time.sleep(2)

            # Enter email
            email_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            email_field.send_keys(self.email)

            # Enter password
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(self.password)

            # Click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()

            # Wait for login to complete
            time.sleep(5)

            # Check if login was successful
            if "feed" in self.driver.current_url or "mynetwork" in self.driver.current_url:
                print("✓ Successfully logged into LinkedIn")
                return True
            else:
                print("⚠ Login may have failed. Please check credentials or handle CAPTCHA manually.")
                time.sleep(10)  # Give time to handle CAPTCHA if needed
                return True

        except Exception as e:
            print(f"✗ Login failed: {str(e)}")
            return False

    def search_hr_personnel(self, company_name, max_results=100):
        """
        Search for HR personnel at a specific company

        Args:
            company_name (str): Name of the company
            max_results (int): Maximum number of results to retrieve

        Returns:
            list: List of dictionaries containing personnel information
        """
        print(f"\nSearching for HR personnel at {company_name}...")
        results = []

        try:
            # Build search URL for each HR keyword
            for keyword in config.HR_KEYWORDS[:5]:  # Limit to first 5 keywords to avoid too many requests
                if len(results) >= max_results:
                    break

                print(f"  Searching for: {keyword}")
                search_url = self._build_search_url(company_name, keyword)
                self.driver.get(search_url)
                time.sleep(random.uniform(config.MIN_PAGE_DELAY, config.MAX_PAGE_DELAY))

                # Scroll to load more results
                self._scroll_page()

                # Extract profile information
                page_results = self._extract_profiles()
                results.extend(page_results)

                print(f"    Found {len(page_results)} profiles")

                # Remove duplicates
                results = self._remove_duplicates(results)

                if len(results) >= max_results:
                    results = results[:max_results]
                    break

            print(f"\n✓ Total unique profiles found: {len(results)}")
            return results

        except Exception as e:
            print(f"✗ Error during search: {str(e)}")
            return results

    def _build_search_url(self, company_name, job_title):
        """Build LinkedIn search URL with filters"""
        base_url = "https://www.linkedin.com/search/results/people/"
        # Note: LinkedIn search parameters may need adjustment based on their current URL structure
        params = f"?keywords={job_title} {company_name}&origin=GLOBAL_SEARCH_HEADER"
        return base_url + params

    def _scroll_page(self, scrolls=3):
        """Scroll the page to load more content"""
        for i in range(scrolls):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(config.MIN_SCROLL_DELAY, config.MAX_SCROLL_DELAY))

    def _extract_profiles(self):
        """Extract profile information from current page"""
        profiles = []

        try:
            # Wait for search results to load
            time.sleep(3)

            # Get page source and parse with BeautifulSoup
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')

            # Find all profile cards (LinkedIn's structure may vary)
            profile_cards = soup.find_all('li', {'class': lambda x: x and 'reusable-search__result-container' in x})

            for card in profile_cards:
                try:
                    profile_data = self._parse_profile_card(card)
                    if profile_data:
                        profiles.append(profile_data)
                except Exception as e:
                    continue

            # Alternative: Try using Selenium to find elements
            if len(profiles) == 0:
                profiles = self._extract_profiles_selenium()

        except Exception as e:
            print(f"    Warning: Error extracting profiles: {str(e)}")

        return profiles

    def _extract_profiles_selenium(self):
        """Extract profiles using Selenium (alternative method)"""
        profiles = []

        try:
            # Find profile elements
            profile_elements = self.driver.find_elements(By.CSS_SELECTOR, ".reusable-search__result-container")

            for element in profile_elements:
                try:
                    name_elem = element.find_element(By.CSS_SELECTOR, ".entity-result__title-text a span[aria-hidden='true']")
                    name = name_elem.text.strip()

                    try:
                        title_elem = element.find_element(By.CSS_SELECTOR, ".entity-result__primary-subtitle")
                        title = title_elem.text.strip()
                    except:
                        title = "N/A"

                    try:
                        location_elem = element.find_element(By.CSS_SELECTOR, ".entity-result__secondary-subtitle")
                        location = location_elem.text.strip()
                    except:
                        location = "N/A"

                    try:
                        profile_link_elem = element.find_element(By.CSS_SELECTOR, ".entity-result__title-text a")
                        profile_url = profile_link_elem.get_attribute('href')
                    except:
                        profile_url = "N/A"

                    if name and name != "LinkedIn Member":
                        profiles.append({
                            'name': name,
                            'title': title,
                            'location': location,
                            'profile_url': profile_url
                        })

                except Exception as e:
                    continue

        except Exception as e:
            print(f"    Warning: Selenium extraction failed: {str(e)}")

        return profiles

    def _parse_profile_card(self, card):
        """Parse individual profile card"""
        try:
            # Extract name
            name_elem = card.find('span', {'class': lambda x: x and 'entity-result__title-text' in str(x)})
            name = name_elem.get_text(strip=True) if name_elem else "N/A"

            # Extract title
            title_elem = card.find('div', {'class': lambda x: x and 'entity-result__primary-subtitle' in str(x)})
            title = title_elem.get_text(strip=True) if title_elem else "N/A"

            # Extract location
            location_elem = card.find('div', {'class': lambda x: x and 'entity-result__secondary-subtitle' in str(x)})
            location = location_elem.get_text(strip=True) if location_elem else "N/A"

            # Extract profile URL
            link_elem = card.find('a', {'class': lambda x: x and 'app-aware-link' in str(x)})
            profile_url = link_elem.get('href') if link_elem else "N/A"

            if name and name != "LinkedIn Member":
                return {
                    'name': name,
                    'title': title,
                    'location': location,
                    'profile_url': profile_url
                }
        except Exception as e:
            return None

        return None

    def _remove_duplicates(self, profiles):
        """Remove duplicate profiles based on name and title"""
        seen = set()
        unique_profiles = []

        for profile in profiles:
            key = (profile.get('name', ''), profile.get('title', ''))
            if key not in seen:
                seen.add(key)
                unique_profiles.append(profile)

        return unique_profiles

    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("\n✓ Browser closed")
