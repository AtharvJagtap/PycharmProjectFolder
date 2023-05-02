"""Name: Your Name
CS230: Section XXX
Data: Which data set you used
Description:
This code creates an interactive app that allows users to explore rollercoaster data by state, city, and ride.
The app includes various statistics and visualizations that help users compare and contrast different rollercoaster rides.
"""


import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', 1000)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)

def getStateCityData():
    st.title('Your :red[_Rollercoaster!_] Guide :sunglasses:')
    name = st.text_input("Hi, welcome to the ultimate rollercoaster guide, what is your name?")
    st.write(name,", hope you are having a good day, alow this guide to finalize the rollercoaster ride that most interest's you.")
    df = pd.read_csv("rollercoasters.csv")
    state = df["State"]
    states = state.drop_duplicates()
    selected_states = st.selectbox("Select a state you are interested in:", states)
    st.write(name,", your selected state is:")
    st.write("- ",selected_states)
    stateData = df[df.State == selected_states]
    topSpeed = stateData["Top_Speed"]
    avgTopSpeed = topSpeed.mean()
    st.write("The average top-speed of rollercoasters in", selected_states, "is :", avgTopSpeed.round(), "mph")
    stateData["City_Park"] = stateData["City"] + " (" + stateData["Park"] + ")"
    max_years = stateData.groupby("City_Park")["Year_Opened"].max().reset_index()
    fig, ax = plt.subplots()
    ax.scatter(stateData["City_Park"], stateData["Year_Opened"], color='orange')
    ax.scatter(max_years["City_Park"], max_years["Year_Opened"], color='red')
    ax.set_xlabel("City(Park) in "+ selected_states)
    ax.set_ylabel("Year(s) when rollercoaster rides were opened")
    ax.set_title("Opening dates of rollercoaster rides per park in " + selected_states + " [old(orange) to new(red)]")
    plt.xticks(rotation=90)
    st.pyplot(fig)
    y_axis_columns = st.multiselect("Select characteristics you would like to compare in rollercoaster ride(s) in " + selected_states + " :", ["Top_Speed", "Max_Height", "Drop"])
    fig, ax = plt.subplots()
    for column in y_axis_columns:
        ax.scatter(stateData["City_Park"], stateData[column], label=column)
    ax.set_xlabel("City(Park) in " + selected_states)
    ax.set_ylabel("Top speed/ Maximum height/ Drop")
    ax.set_title("Comparison of rollercoasters' top speed(mph), maximum height(ft) and Drop(ft) of various parks in " + selected_states)
    ax.legend()
    plt.xticks(rotation=90)
    st.pyplot(fig)
    city = stateData["City"]
    cities = city.drop_duplicates()
    selected_cities = st.selectbox("Select a city you are interested in:", cities)
    st.write(name,", your selecetd city is:")
    st.write("- ",selected_cities)
    cityData = df[df.City == selected_cities]
    parks = cityData["Park"]
    park = parks.drop_duplicates().tolist()
    st.write("The ammusement park(s) in", selected_cities, "is: ")
    st.write("- " + "\n- ".join(park))
    rides = cityData["Coaster"]
    ride = rides.tolist()
    st.write("The rollercoaster ride(s) in", selected_cities, "are: ")
    st.write("- " + "\n- ".join(ride))
    selected_rides = st.radio("Select a ride you are interested in:", rides)
    st.write(name,", your selecetd ride is:")
    st.write("- ", selected_rides)
    mapData = df[df.Coaster == selected_rides]
    topSpeeds = mapData["Top_Speed"]
    topSpeeds2 = topSpeeds.tolist()
    st.write("The top speed of", selected_rides, "is: ")
    if not topSpeeds2:
        st.write("- No data available")
    else:
        st.write("- {:.2f} mph".format(topSpeeds2[0]))
    maxHeights = mapData["Max_Height"]
    maxHeight = maxHeights.tolist()
    st.write("The maximum height of", selected_rides, "is: ")
    if not maxHeight:
        st.write("- No data available")
    else:
        st.write("- {:.2f} ft".format(maxHeight[0]))
    drops = mapData["Drop"]
    drop = drops.tolist()
    st.write("The drop of", selected_rides, "is: ")
    if not drop:
        st.write("- No data available")
    else:
        st.write("- {:.2f} ft".format(drop[0]))
    lengths = mapData["Length"]
    length = lengths.tolist()
    st.write("The length of", selected_rides, "is: ")
    if not length:
        st.write("- No data available")
    else:
        st.write("- {:.2f} ft".format(length[0]))
    inversions = mapData["Num_of_Inversions"]
    inversion = inversions.tolist()
    st.write("The number of inversions in", selected_rides, "are: ")
    st.write("- {}".format(inversion[0]))
    st.write("Average Speed of ", selected_rides, "is:")
    mask = (mapData["Length"].notnull()) & (mapData["Duration"].notnull())
    avg_speed = mapData.loc[mask, "Length"] / mapData.loc[mask, "Duration"]
    mph = avg_speed/ 1.46666667
    if avg_speed.empty:
        st.write("- No data available")
    else:
        st.write("- {:.2f} mph".format(mph.values[0]))
    mapData2 = mapData.rename(columns={'Latitude': 'lat', 'Longitude': 'lon'})
    rides_loc = mapData2[['lat', 'lon']]
    st.write("The map will give you the location of", selected_rides, "rollercoaster ride in", selected_cities, ",", selected_states, ":")
    st.map(rides_loc)
    satisfaction = st.sidebar.slider("How satisfied are you with this guide?", min_value=1, max_value=5, key="satisfaction")
    st.write(f"You rated this guide {satisfaction} out of 5.")
    return df, states, cities, park, selected_states, selected_cities, rides

df, states, cities, park, selected_states, selected_cities, rides = getStateCityData()


