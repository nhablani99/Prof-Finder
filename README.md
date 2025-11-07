Prof‑Finder

An intelligent search engine for university professors built with Python, LangChain and FAISS

📝 Overview

Prof‑Finder is a tool designed to help students quickly locate and learn about professors at a given university (initially built for the University of Waterloo). It leverages web scraping, document processing, vector embeddings and similarity search to deliver meaningful results—so instead of simply listing contact info, users can ask natural‑language questions like “Which professors specialize in machine learning and optimization?” and get ranked results.

🛠 Getting Started
Prerequisites

Python 3.x (tested on 3.10–3.13)

pip (to install dependencies)

(Optional) Virtual environment recommended.


Clone the repository:

git clone https://github.com/nhablani99/Prof‑Finder.git  
cd Prof‑Finder  


Install dependencies:

pip install ‑r requirements.txt  


Scrape initial data (if you plan to update or expand):

python prof_scraper.py  
python profile_scraper.py  


Pre‑process and build the vector store:

python data_preprocessor.py  
python create_vectorstore.py  


Run the UI / query interface:

python frontend.py  


Enter your query and get professor matches!
