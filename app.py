import streamlit as st
import numpy as np
import pandas as pd
import re
import streamlit.components.v1 as stc

@st.cache(allow_output_mutation=True)
def load_data(data):
    df = pd.read_csv(data, nrows=3500,na_filter=False)
    return df 

@st.cache(allow_output_mutation=True)
def getCategory(category):
    k = [""]
    for item in category:
        if not item in k:
            k.append(item)
    return k

@st.cache(allow_output_mutation=True)
def getState(state):
    k = [""]
    for item in state:
        if not item in k:
            k.append(item)
    return k

@st.cache(allow_output_mutation=True)
def getRecommend(search_term, category, state, rate1, rate2, df):
    df["Rating"] = pd.to_numeric(df["Rating"])
    results = df[(df.Category == category) & (df.State == state) & (df.Rating >= rate1) & (df.Rating <= rate2) & (df.Place_Name.str.contains(search_term,flags=re.IGNORECASE))] 
    recommend = results
    return recommend

#state, place_name, rating, description, website, location_link, address, phone_number, category, picture_link
htmlResult = '''
<div style="width:90%;height:100%;margin:1px;padding:5px;position:relative;border-radius:5px;border-bottom-right-radius: 60px;
box-shadow:0 0 15px 5px #ccc; background-color: #a8f0c6;
  border-left: 5px solid #6c6c6c;">

<p style="color:blue;"><span style="color:black;">&#127760;State:</span>{}</p>
<p style="color:blue;"><span style="color:black;">&#127961;Place Name:</span>{}</p>
<p style="color:blue;"><span style="color:black;">&#127775;Rating:</span>{}</p>
<p style="color:blue;"><span style="color:black;">&#128462;Description:</span>{}</p>
<p style="color:blue;"><span style="color:black;">🔗</span><a href="{}", target="_blank" rel="noreferrer noopener">Website</a></p>
<p style="color:blue;"><span style="color:black;">🔗</span><a href="{}", target="_blank" rel="noreferrer noopener">Location Link</a></p>
<p style="color:blue;"><span style="color:black;">&#127968;Address:</span>{}</p>
<p style="color:blue;"><span style="color:black;">&#128222;Phone Number:</span>{}</p>
<p style="color:blue;"><span style="color:black;">Category:</span>{}</p>
<p style="color:blue;"><span style="color:black;"></span><a href="{}", target ="_blank" rel="noreferrer noopener"><img src="{}" alt="Place Image" width="250" height="250"></img></a></p>
</div>
'''

st.title("Place Recommender")
menu = ["Home","Recommend","About"]
choice = st.sidebar.selectbox("Menu",menu)
df = load_data("Malaysia Tourist Attraction.csv")
df.columns = [c.replace(' ', '_') for c in df.columns]
if choice == "Home":
    st.subheader("Home")
    st.write("Welcome to Place Recommender Page")
elif choice == "Recommend":
    category = st.sidebar.selectbox("Category",getCategory(df["Category"]))
    state = st.sidebar.selectbox("State",getState(df["State"]))
    rating = ["4.0 - 5.0", "3.0 - 4.0", "2.0 - 3.0", "1.0 - 2.0", "0.0 - 1.0"]
    rate = st.sidebar.radio("Rating", rating)
    rate1 = rate2 = 0
    if(rate == "4.0 - 5.0"):
        rate1 = 4.0
        rate2 = 5.0
    elif rate == "3.0 - 4.0":
        rate1 = 3.0
        rate2 = 4.0
    elif rate == "2.0 - 3.0":
        rate1 = 2.0
        rate2 = 3.0
    elif rate == "1.0 - 2.0":
        rate1 = 1.0
        rate2 = 2.0
    elif rate == "0.0 - 1.0":
        rate1 = 0.0
        rate2 = 1.0
    st.subheader("Recommend Places")
    search_term = st.text_input("Search")
    if(st.button("Search")):
        if category == "":
            st.error('Please select category', icon="🚨")
        elif state == "":
            st.error('Please select state', icon="🚨")
        if not search_term == "":
            try:
                results = getRecommend(search_term, category, state, rate1, rate2, df)
                if len(results) == 0:
                    results = "Not Found"
                    st.warning(results)
                else:
                    st.subheader("Results")
                    if(len(results) > 5):
                        results = results.sample(n=5)
                    for row in results.iterrows():
                        state  = row[1][0]
                        place_name = row[1][1]
                        rating = row[1][2]
                        description = row[1][3]
                        website = row[1][4]
                        location_link = row[1][5]
                        address = row[1][6]
                        phone_number = row[1][7]
                        category = row[1][8]
                        picture_link = row[1][9]
                        stc.html(htmlResult.format(state, place_name, rating, description, website, location_link, address, phone_number, category, picture_link, picture_link), height=670 if not picture_link == "" else 450)
            except:
                results = "Not Found"
                st.warning(results)
        else:
            st.error('Please enter search term', icon="🚨")
else:
    st.subheader("About")
    st.text("Built with Streamlit & Pandas")