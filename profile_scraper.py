import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

def get_base_url(url: str) -> str:
    return "/".join(url.split("/")[:3])


def scrape_profile_links(faculty_urls: list, output_path: str) -> list:
    profiles = []
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    for url in tqdm(faculty_urls):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                base_url = get_base_url(url)
                links = soup.select("a.viewprofile")
                links = [link["href"] for link in links]
                full_links = [base_url + link if link.startswith("/") else link for link in links]
                profiles.extend(full_links)
            else:
                print(f"Failed to retrive url: status_code {response.status_code}")
        except Exception as e:
            print(f"Error processing {url}: {e}")

    profiles = list(set(profiles))  # Remove duplicates
    with open(output_path, "w") as f:
        f.write("\n".join(profiles))

    print(f"Scraped {len(profiles)} profile links. Successfully saved to the output file: {output_path}") 
    return profiles

if __name__ == "__main__":
    faculty_urls = [
        "https://experts.uwaterloo.ca/faculties/Faculty%20of%20Arts",
        "https://experts.uwaterloo.ca/faculties/Faculty%20of%20Engineering",
        "https://experts.uwaterloo.ca/faculties/Faculty%20of%20Environment",
        "https://experts.uwaterloo.ca/faculties/Faculty%20of%20Health",
        "https://experts.uwaterloo.ca/faculties/Faculty%20of%20Mathematics",
        "https://experts.uwaterloo.ca/faculties/Faculty%20of%20Science",
        "https://experts.uwaterloo.ca/colleges/Conrad%20Grebel%20University%20College",
        "https://experts.uwaterloo.ca/colleges/Renison%20University%20College",
        "https://experts.uwaterloo.ca/colleges/St.%20Jerome's%20University",
        "https://experts.uwaterloo.ca/colleges/St.%20Paul's%20University%20College",
        "https://experts.uwaterloo.ca/colleges/United%20College"
        
    ]
    output_path = "data_new/json/uw_profiles.txt"
    scrape_profile_links(faculty_urls, output_path)