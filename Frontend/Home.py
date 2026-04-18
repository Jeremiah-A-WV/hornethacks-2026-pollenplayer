import streamlit as st
import requests
from streamlit_lottie import st_lottie
from st_pages import Page, add_page_title, get_nav_from_toml
import http.client
from streamlit_geolocation import streamlit_geolocation as st_gl

# ------------------------------------------------------------------

# API Request

# url = https://api.ambeedata.com/latest/pollen/by-lat-lng
# API_key = st.secrets["ambee_API_key"]

# params = {
#     'lat': x get from user,
#     'lng': y get from user
# }


# headers = {
#     'x-api-key': st.secrets["ambee_API_key"],
#     'Content-type': "application/json"
# }



# response = requests.get(url, params=params, headers=headers)

# if response.status_code == 200:
#     data = response.json()
#     print(data) (only the counts for weed pollen, tree pollen, and grass pollen- calculate the average then: if  )
# else:
#     print(f"Error: {response.status_code}, {response.text}")


# ---------------------------------------------------------







# App title and animation
st.title("PollenPlayer")
    # example:
        # with st.echo():
            # st_lottie("https://assets5.lottiefiles.com/packages/lf20_V9t630.json")




def Home():
    st.title("Home")
    st.page_link("Music.py", query_params={"utm_source": "Home"})

    with st.form(key = "ZipCode: "):
        ZipCode = st.text_input("Zipcode")
        submitted = st.form_submit_button("Submit")

        if submitted:
            # compare zipcode to ambee api data location to determine to level of pollen in that area
            pass


   


    location = st_gl()

    st.write("Location: ")
    st.write(location)

    def getLocation():
       pass
    

pg = st.navigation([Home, "Music.py"])

pg.run()








