import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import math

class DeFiScraper:
    def __init__(self):
        self.base_url = "https://coinlaunch.space/projects/defi/"
        self.sort_param = "sort=-dateStart"
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--start-maximized')
        self.driver = uc.Chrome(options=options, version_main=132)
        self.wait = WebDriverWait(self.driver, 20)
        self.projects_per_page = 15
        self.all_projects = []
        self.project_names = set()  # Track project names
    
    def get_page_url(self, page_number):
        """Construct URL for a specific page with sorting"""
        if page_number == 1:
            return f"{self.base_url}?{self.sort_param}"
        return f"{self.base_url}?{self.sort_param}&page={page_number}"
    
    def get_project_description(self, url):
        """Get project description from its page"""
        try:
            print(f"Getting description from: {url}")
            
            # Navigate to project page
            self.driver.get(url)
            time.sleep(3)  # Wait for page load
            
            description = "N/A"
            
            # Try multiple selectors to find description
            selectors = [
                '.description-text',
                'div.wrap > p',
                'div.description p',
                'div.mb-48.description-text',
                '.project-description',
                '.wrap p',
                'div.wrap div p'
            ]
            
            for selector in selectors:
                try:
                    desc_element = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    text = desc_element.text.strip()
                    if text:
                        description = text
                        print(f"Found description using selector: {selector}")
                        break
                except:
                    continue
            
            return description
            
        except Exception as e:
            print(f"Error getting description: {e}")
            return "N/A"
    
    def get_row_data(self, row):
        """Extract data from a single table row"""
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) < 7:
                return None
            
            score = cells[0].text.strip()
            name_cell = cells[1]
            name = name_cell.text.strip()
            
            # Check if project already exists
            if name in self.project_names:
                return "duplicate"
            
            # Get URL from link
            try:
                link = name_cell.find_element(By.TAG_NAME, "a")
                url = link.get_attribute("href")
            except:
                print(f"No link found for project: {name}")
                return None
            
            start_date = cells[2].text.strip()
            end_date = cells[3].text.strip()
            status = cells[4].text.strip()
            total_raise = cells[6].text.strip()
            
            return {
                'score': score or "N/A",
                'name': name,
                'url': url,
                'start_date': start_date or "N/A",
                'end_date': end_date or "N/A",
                'status': status or "N/A",
                'total_raise': total_raise or "N/A"
            }
        except Exception as e:
            print(f"Error extracting row data: {e}")
            return None
    
    def get_table_rows(self):
        """Get all project rows from the table (skipping the extra rows)"""
        try:
            # Wait for table to load and get only project rows (those with links)
            rows = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tbody tr:has(a.clean-button)"))
            )
            return rows
        except Exception as e:
            print(f"Error getting table rows: {e}")
            return []
    
    def navigate_to_page(self, page_number):
        """Navigate to a specific page and verify the navigation was successful"""
        try:
            page_url = self.get_page_url(page_number)
            print(f"\nNavigating to page {page_number}: {page_url}")
            
            self.driver.get(page_url)
            time.sleep(3)  # Wait for page load
            
            # Verify we have rows on this page
            rows = self.get_table_rows()
            if not rows:
                print(f"No rows found on page {page_number}")
                return False
            
            print(f"Successfully navigated to page {page_number} with {len(rows)} rows")
            return True
            
        except Exception as e:
            print(f"Error navigating to page {page_number}: {e}")
            return False
    
    def get_projects_from_page(self, page_number):
        """Extract project information from the specified page"""
        try:
            # Navigate to the page
            if not self.navigate_to_page(page_number):
                return False
            
            # Get rows from current page
            rows = self.get_table_rows()
            if not rows:
                return False
            
            # First collect all project data from the page
            projects_to_process = []
            found_duplicate = False
            
            # Process each project row
            for row in rows:  # No need to skip rows now as we only get project rows
                try:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    
                    if len(cells) < 7:
                        continue
                    
                    # Extract all data at once
                    score = cells[0].text.strip()
                    name_cell = cells[1]
                    name = name_cell.text.strip()
                    
                    # Check for duplicate project
                    if name in self.project_names:
                        found_duplicate = True
                        break
                    
                    # Get URL
                    try:
                        link = name_cell.find_element(By.TAG_NAME, "a")
                        url = link.get_attribute("href")
                    except:
                        print(f"No link found for project: {name}")
                        continue
                    
                    # Get other data
                    start_date = cells[2].text.strip()
                    end_date = cells[3].text.strip()
                    status = cells[4].text.strip()
                    total_raise = cells[6].text.strip()
                    
                    # Store project data for processing
                    projects_to_process.append({
                        'score': score or "N/A",
                        'name': name,
                        'url': url,
                        'start_date': start_date or "N/A",
                        'end_date': end_date or "N/A",
                        'status': status or "N/A",
                        'total_raise': total_raise or "N/A"
                    })
                    
                except Exception as e:
                    print(f"Error collecting project data: {e}")
                    continue
            
            if found_duplicate:
                return False
            
            # Now process each project to get its description
            for project_data in projects_to_process:
                try:
                    # Get project description
                    description = self.get_project_description(project_data['url'])
                    project_data['description'] = description
                    
                    # Add to collections
                    self.all_projects.append(project_data)
                    self.project_names.add(project_data['name'])
                    
                    print(f"Project {len(self.all_projects)}: {project_data['name']} (Score: {project_data['score']}, Raise: {project_data['total_raise']})")
                    
                    # Save progress after each project
                    self.save_progress(self.all_projects)
                    
                except Exception as e:
                    print(f"Error processing project description: {e}")
                    continue
            
            if projects_to_process:
                print(f"Added {len(projects_to_process)} new projects from page {page_number}")
                return True
            
            return False
            
        except Exception as e:
            print(f"Error processing page {page_number}: {e}")
            return False
    
    def save_progress(self, projects):
        """Save current progress to file"""
        try:
            with open('project_list.json', 'w', encoding='utf-8') as f:
                json.dump(projects, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving progress: {e}")
    
    def scrape_project_list(self):
        """Main function to scrape project list"""
        try:
            print("Starting scraper (projects sorted by start date, latest first)")
            
            page = 1
            while True:
                print(f"\nProcessing page {page}...")
                
                # Process page and check if we should continue
                if not self.get_projects_from_page(page):
                    break
                
                page += 1
            
            print(f"\nScraping complete! Found {len(self.all_projects)} unique projects")
            return self.all_projects
            
        except Exception as e:
            print(f"Error in scraping process: {e}")
            return self.all_projects  # Return what we have so far
            
        finally:
            try:
                self.driver.quit()
            except Exception as quit_error:
                print(f"Error quitting driver: {quit_error}")

def main():
    scraper = DeFiScraper()
    projects = scraper.scrape_project_list()
    print("\nResults saved in project_list.json")

if __name__ == "__main__":
    main() 


