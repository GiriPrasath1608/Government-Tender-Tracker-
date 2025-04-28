# Government-Tender-Tracker-

Tender App 📑

A Streamlit-based web application for managing tender opportunities.
It allows companies to register, view their profiles, scrape tenders from the Government e-Marketplace (GeM), and find tenders that best match their previous work experience.

🔥 Features

    User Management:
    
    Create new users with company details.
    
    View profile information.
    
    Tender Scraping:
    
    Scrape latest tenders (bids) from GeM - All Bids page.
    
    Save the tenders into a local CSV file.

Tender Matching:

    Find tenders that are most similar to the user's previous projects using TF-IDF and Cosine Similarity.
    
    Adjust the similarity threshold dynamically.

Tender Search:

    Search tenders by Bid Number or Department.

    📂 Folder Structure
    bash
    Copy
    Edit
    Tender App/
    │
    ├── data/
    │   ├── User.csv              # Stores registered user details
    │   └── All_Bid_List.csv       # Stores all scraped tender data
    │
    ├── tender_app.py              # Main Streamlit app
    └── README.md                  # Project documentation (this file)

🛠️ Installation

    Clone the repository:
    
    git clone https://github.com/GiriPrasath1608/Government-Tender-Tracker-.git
    cd Government-Tender-Tracker-


Install dependencies:

    pip install -r requirements.txt

If requirements.txt is not available, manually install:

    pip install streamlit selenium pandas beautifulsoup4 scikit-learn webdriver-manager

Run the app:

    streamlit run tender_app.py

🚀 How to Use

    Open the app.
    
    Select an existing user or create a new user.
    
    View your profile information.
    
    Scrape tenders from GeM portal (scrapes 10 pages).
    
    Find high potential tenders based on your company's previous work.
    
    Browse through all tenders or search based on Bid Number or Department.

📋 Requirements

    Python 3.8+
    
    Google Chrome Browser
    
    ChromeDriver (auto-managed by webdriver-manager)

⚡ Key Technologies

    Frontend: Streamlit
    
    Backend: Python
    
    Web Scraping: Selenium, BeautifulSoup
    
    Data Storage: CSV files
    
    Similarity Matching: TF-IDF + Cosine Similarity (Scikit-learn)

📝 Notes

    Make sure your Chrome browser and webdriver-manager ChromeDriver versions are compatible.
    
    The tender scraping is designed for the GeM All Bids page layout.
    If GeM changes their website structure, the scraper might need updates.
    
    Always wait for a few seconds between page scrapes to avoid being blocked by the website.

Feel free to open an Issue or Pull Request if you have suggestions or improvements.

📧 Contact

    Developer: Giri Prasath
    
    Email: giriprasathm1608@gmail.com
    
    GitHub: GiriPrasath1608

⭐ Thank you for checking out the Tender App!
