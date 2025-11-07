import os
import json
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

def scrape_profile_data(profile_links: list, output_file: str) -> list:
    profiles_data = [] # list of dict
    os.makedirs(os.path.dirname(output_file),exist_ok=True)
    for link in tqdm(profile_links):
        try:
            response = requests.get(link)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                name = soup.find("h1",class_ ="underlined").text.strip() if soup.find("h1",class_ ="underlined") else "N/A"
                title = soup.find("span",class_ = "spacify").text.strip() if soup.find("span",class_ = "spacify") else "N/A"
                department = [tag.text.strip() for tag in soup.select("a.linkify.squeezify.notxtstyle")]
                email = soup.find("a", href=lambda href: href and "mailto:" in href).text.strip() if soup.find("a", href=lambda href: href and "mailto:" in href) else "N/A"
                expertise = [soup.find("meta", attrs={"name": "description"})["content"].replace("Expert in", "").strip()]
                bio = soup.find("div", class_="profile-bio").text.strip() if soup.find("div", class_="profile-bio") else "N/A"

                profiles_data.append({
                    "name": name,
                    "title": title,
                    "department": department,
                    "email": email,
                    "expertise": expertise,
                    "bio":bio,
                    "profile_url": link
                })
            else:
                print(f"Failed to fetch {link}: Respnse {response.status_code}")
        except Exception as e:
            print(f"Error processing {link}: {e}")
        with open(output_file, "w") as f:
            json.dump(profiles_data, f,indent=4)

        print(f"Scraped data for {len(profiles_data)} profiles. Data saved to {output_file}")

if __name__ == "__main__":
    input_file = "data_new/json/uw_profiles.txt"
    output_file = "data_new/json/uw_profiles_data.json"
    with open(input_file, "r") as f:
        profile_links = [line.strip() for line in f.readlines() if line.strip()]
    scrape_profile_data(profile_links, output_file)