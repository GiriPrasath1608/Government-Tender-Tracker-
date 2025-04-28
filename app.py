import streamlit as st
import pandas as pd
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.title("Tender App")

path = r'D:\Tender app\data\User.csv'
Tender_path = r'D:\Tender app\data\All_Bid_List.csv'

# Load existing users
if os.path.exists(path):
    df_existing = pd.read_csv(path)
    df_existing = df_existing.loc[:, ['User Name', 'Password', 'Company Name', 'Company Address', 'Sector', 'PreviousWork', 'Capacity']]
    user_list = df_existing["User Name"].tolist()
else:
    df_existing = pd.DataFrame(columns=['User Name', 'Password', 'Company Name', 'Company Address', 'Sector', 'PreviousWork', 'Capacity'])
    user_list = []

if 'page' not in st.session_state:
    st.session_state.page = "home"

# Function to switch page
def go_to_profile(selected_user):
    st.session_state.page = "profile"
    st.session_state.selected_user = selected_user

    
if st.session_state.page == "home":
    
    selected_user = st.selectbox("Select your profile", user_list, placeholder="Select user")

    if selected_user:
        st.button("Go to Profile", on_click=go_to_profile, args=(selected_user,))

    def save_user(user_name,password,company_name,address,sector,previous_work,capacity):
        user_data = [{"User Name":user_name,
        "Password":password,
        "Company Name":company_name,
        "Company Address":address,
        "Sector": sector,
        "PreviousWork": previous_work,
        "Capacity" : capacity}]

        new_df = pd.DataFrame(user_data)

        path = r'D:\Tender app\data\User.csv'

        df_existing = pd.read_csv(path)

        df_existing = df_existing.loc[:, ['User Name', 'Password', 'Company Name', 'Company Address', 'Sector', 'PreviousWork', 'Capacity']]

        df_combined = pd.concat([df_existing, new_df],ignore_index=True)

        df_combined.to_csv(path,index=False)

        return True

    with st.expander('Create New User'):
        with st.form("Usesr Form"):
            user_name     = st.text_input("User Name")
            password      = st.text_input("Password")
            company_name  = st.text_input("Company Name")
            address       = st.text_input("Company Address")
            sector        = st.text_input("Sector")
            previous_work = st.text_input("Previous Work")
            capacity      = st.text_input("Capacity")

            if st.form_submit_button("Register"):
                response_save = save_user(user_name,password,company_name,address,sector,previous_work,capacity)
                
                if response_save:     
                    st.success('New User Created')
                    st.rerun()

elif st.session_state.page == "profile":

    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    selected_user = st.session_state.selected_user    

    user_details = df_existing[df_existing["User Name"] == selected_user]

    st.subheader(f"Profile of {selected_user}")

    if not user_details.empty:
        st.write("**Company Name:**", user_details.iloc[0]["Company Name"])
        st.write("**Company Address:**", user_details.iloc[0]["Company Address"])
        st.write("**Sector:**", user_details.iloc[0]["Sector"])
        st.write("**Previous Work:**", user_details.iloc[0]["PreviousWork"])
        st.write("**Capacity:**", user_details.iloc[0]["Capacity"])


    if st.button("Update data"):
        def scrap_data():
            url = 'https://bidplus.gem.gov.in/all-bids'
            driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
            driver.get(url)

            scraped_data = []

            # Loop through first 10 pages
            for page in range(1, 11):

                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                bids = soup.find('div', class_ = 'col-md-10 bids').find_all('div', class_ = 'card')

                for bid in bids:

                    # 0. BId no
                    bid_no = bid.a.text

                    # 1. Pdf link
                    bid_pdf_link = bid.a['href']
                    bid_pdf_link = 'https://bidplus.gem.gov.in' + bid_pdf_link

                    # 2. Item extraction
                    card_body = bid.find('div', class_='card-body')
                    item_text = ''

                    if card_body:
                        item_strong = card_body.find('strong', string='Items:')
                        if item_strong:
                            # Try to find an <a> tag after the <strong> tag
                            a_tag = item_strong.find_next('a')
                            if a_tag:
                                # Case 1: Item inside <a> tag (data-content attribute)
                                item_text = a_tag.get('data-content', '').strip()
                                if not item_text:
                                    item_text = a_tag.text.strip()  # Fallback if no data-content
                            else:
                                # Case 2: Item directly as text next to <strong> tag
                                item_text_node = item_strong.next_sibling
                                if item_text_node:
                                    item_text = item_text_node.strip()

                    # 3. Quantity
                    quantity_div = card_body.find('strong', string='Quantity:').find_next_sibling(text=True)
                    quantity = quantity_div.strip()

                    # 4. Department Name and Address
                    dept_row = card_body.find('strong', string='Department Name And Address:').parent.find_next_sibling('div').text
                    department = dept_row.strip()

                    # 5. Start Date
                    start_date_span = card_body.find('span', class_='start_date').text
                    start_date = start_date_span.strip()

                    # 6. End Date
                    end_date_span = card_body.find('span', class_='end_date').text
                    end_date = end_date_span.strip()

                    scraped_data.append([bid_no, bid_pdf_link, item_text,quantity, department, start_date, end_date])

                # next page
                
                if page < 10:    
                    # 2. Try to go to next page
                    try:
                        # Wait until next button is clickable
                        next_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.LINK_TEXT, 'Next'))  
                        )
                        next_button.click()
                        time.sleep(2)  # wait a bit for page to load
                    except:
                        print("No more pages. Scraping finished.")
                        break
                
            driver.quit()

            return scraped_data
        
        def create_df(data): 
            df = pd.DataFrame(data, columns = ['Bid no','link','Item','Quantity','Department','Start Date','End Date'])
            return df

        def update_csv(data):
            data.to_csv(r'D:\Tender app\data\All_Bid_List.csv')
            return True
        
        raw_data = scrap_data()

        created_df = create_df(raw_data)

        csv_response = update_csv(created_df)

        if csv_response:
            st.success("Data Scraped Succesfully")

    
    if st.button("Go to Tenders"):
        st.session_state.page = "Tenders"
        st.rerun()

    # Threshold slider
    threshold = st.slider("Select similarity threshold", min_value=0.0, max_value=1.0, value=0.5)

    if st.button("Find High Potential Tender"):
        # Load tenders
        Tender_path = r"D:\Tender app\data\All_Bid_List.csv"
        tender_df = pd.read_csv(Tender_path)

        # Your query (user inputs what they want to search for)
        query = user_details.iloc[0]["PreviousWork"]



        # Prepare TF-IDF
        tfidf = TfidfVectorizer(stop_words='english')

        # Fit transform all data + query
        tfidf_matrix = tfidf.fit_transform(tender_df['Item'].fillna(''))  # Fill NA if any
        query_vec = tfidf.transform([query])

        # Compute cosine similarity
        similarity_scores = cosine_similarity(query_vec, tfidf_matrix).flatten()

        # Add scores to dataframe
        tender_df['similarity'] = similarity_scores

        # Filter by threshold
        df_high_potential = tender_df[tender_df['similarity'] >= threshold].sort_values(by="similarity", ascending=False)

        st.write(f"### High Potential Tenders (Threshold ≥ {threshold})")
        for idx, row in df_high_potential.iterrows():
            with st.container(border=True):
                st.write(f"**Similarity Score:** {row['similarity']:.2f}")
                st.write(f"**Bid No:** {row['Bid no']}")
                st.write(f"**link:** {row['link']}")
                st.write(f"**Item:** {row['Item']}")
                st.write(f"**Quantity:** {row['Quantity']}")
                st.write(f"**Department:** {row['Department']}")
                st.write(f"**Start Date:** {row['Start Date']}")
                st.write(f"**End Date:** {row['End Date']}")

elif st.session_state.page == "Tenders":
    st.subheader("List of All Tenders")

    data= pd.read_csv(Tender_path)    
    df = pd.DataFrame(data)

    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()
    
    if st.button("Back to profile"):
        st.session_state.page = "profile"
        st.rerun()

    Bid_no = st.text_input("Search Bid NO")

    Department = st.selectbox('Department', df['Department'].unique())
    
    if st.button("Search"):
        
        df = df[(df['Bid no'] == Bid_no) | (df['Department']==Department)]
        df = df.reset_index(drop=True)

    for index in range(df.shape[0]):
        with st.container(border=True):
            st.write(f'Bid no:{df['Bid no'][index]}')
            st.write(f'link:{df['link'][index]}')
            st.write(f'Item:{df['Item'][index]}')
            st.write(f'Quantity:{df['Quantity'][index]}')
            st.write(f'Department:{df['Department'][index]}')
            st.write(f'Start Date:{df['Start Date'][index]}')
            st.write(f'End Date:{df['End Date'][index]}')



    

    




