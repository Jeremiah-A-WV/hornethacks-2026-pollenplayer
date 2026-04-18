import streamlit as st
import requests
from streamlit_lottie import st_lottie
from st_pages import Page, add_page_title, get_nav_from_toml
import http.client
from streamlit_geolocation import streamlit_geolocation as st_gl

# ------------------------------------------------------------------

# For API Request

url = 'https://api.ambeedata.com/latest/pollen/by-lat-lng'
API_key = st.secrets["ambee_API_key"]


headers = {
    'x-api-key': st.secrets["ambee_API_key"],
    'Content-type': "application/json"
}



# ---------------------------------------------------------







# App title and animation
st.title("PollenPlayer")
    # example:
        # with st.echo():
            # st_lottie("https://assets5.lottiefiles.com/packages/lf20_V9t630.json")






def Home():
    st.title("Home")
    # st.page_link("Music.py", query_params={"utm_source": "Home"})

    st.write("Where are you? Click the button below, and submit to find out! ")
    location = st_gl()
    st.write(location)
    
    submit = st.button("Submit")

    def getLocation():
       lat = location['latitude']
       lng = location['longitude']
       st.write(lat)
       st.write(lng)
       params[lat] = lat
       params[lng] = lng

    with st.form(key = "ZipCode: "):
        ZipCode = st.text_input("Zipcode")
        
        submitted = st.form_submit_button("Submit")

        if submitted:
            # compare zipcode to ambee api data location to determine to level of pollen in that area
            if submitted:
                if location is None:
                    st.error("Location not available. Please allow location access.")
                    return

                lat = location.get("latitude")
                lng = location.get("longitude")

                st.write(f"Latitude: {lat}")
                st.write(f"Longitude: {lng}")

                params = {
                "lat": lat,
                "lng": lng
            }
                
            # API Request

            response = requests.get(url, params=params, headers=headers)

            


            if response.status_code == 200:
                data = response.json()
            else:
                print(f"Error: {response.status_code}, {response.text}")

            pollen = data['data'][0]['Count']
            grass_pollen = pollen.get('grass_pollen')
            tree_pollen = pollen.get('tree_pollen')
            weed_pollen = pollen.get('weed_pollen')

            st.write("grass: ", grass_pollen, "\ntree: ", tree_pollen, "\nweed: ", weed_pollen)




   

    
    

pg = st.navigation([Home, "Music.py"])

pg.run()








