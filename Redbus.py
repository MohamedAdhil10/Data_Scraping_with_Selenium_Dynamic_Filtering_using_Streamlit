import pandas as pd
import pymysql
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import time

# Kerala bus
lists_K=[]
df_K=pd.read_csv(r"D:/RedBus/df_K.csv")
for i,r in df_K.iterrows():
    lists_K.append(r["Route_name"])

#Andhra bus
lists_A=[]
df_A=pd.read_csv(r"D:/RedBus/df_A.csv")
for i,r in df_A.iterrows():
    lists_A.append(r["Route_name"])

#Telangana bus
lists_T=[]
df_T=pd.read_csv(r"D:/RedBus/df_T.csv")
for i,r in df_T.iterrows():
    lists_T.append(r["Route_name"])

#Goa bus
lists_G=[]
df_G=pd.read_csv(r"D:/RedBus/df_G.csv")
for i,r in df_G.iterrows():
    lists_G.append(r["Route_name"])

#Rajasthan bus
lists_R=[]
df_R=pd.read_csv(r"D:/RedBus/df_R.csv")
for i,r in df_R.iterrows():
    lists_R.append(r["Route_name"])


# South Bengal bus 
lists_SB=[]
df_SB=pd.read_csv(r"D:/RedBus/df_SB.csv")
for i,r in df_SB.iterrows():
    lists_SB.append(r["Route_name"])

# Haryana bus
lists_H=[]
df_H=pd.read_csv(r"D:/RedBus/df_H.csv")
for i,r in df_H.iterrows():
    lists_H.append(r["Route_name"])

#Assam bus
lists_AS=[]
df_AS=pd.read_csv(r"D:/RedBus/df_AS.csv")
for i,r in df_AS.iterrows():
    lists_AS.append(r["Route_name"])

#Uttar Pradesh bus
lists_UP=[]
df_UP=pd.read_csv(r"D:/RedBus/df_UP.csv")
for i,r in df_UP.iterrows():
    lists_UP.append(r["Route_name"])

#West Bengal bus
lists_WB=[]
df_WB=pd.read_csv(r"D:/RedBus/df_WB.csv")
for i,r in df_WB.iterrows():
    lists_WB.append(r["Route_name"])

#setting up streamlit page
st.set_page_config(page_title="RedBus", page_icon="🚌", layout="wide")


with st.sidebar:
    web = option_menu(
        menu_title="Main Menu",  # Required
        options=["Home", "Select the Bus"],  # Menu options
        icons=["house", "bus"],  # Icons for the menu options
        menu_icon="cast",  # Icon for the menu
        default_index=0,  # Default active menu option
    )

if web == "Home":
    st.title("Data Scraping with Selenium Dynamic Filtering using Streamlit")
    
    st.header("Objective")
    st.markdown(
        """
        - The project is about to build an interactive web application that seamlessly integrates web scraping, data management, and real-time visualization. Using Selenium, the project automates the extraction of dynamic content from web pages, such as bus routes and schedules, which are often rendered dynamically using JavaScript. The scraped data is stored in a structured database (e.g., MySQL) to ensure easy accessibility and future scalability.
        - The project also leverages Streamlit to create an intuitive user interface, allowing users to filter, search, and visualize the extracted data in real-time. By providing features like route selection and price comparison, it offers practical utility for end-users, such as travelers and transportation planners.
        - Ultimately, the aim is to demonstrate how web scraping and dynamic data filtering can be used to create efficient, user-friendly solutions that bridge the gap between raw data and actionable insights, enhancing decision-making and user experience.
        """
    )
    st.header("Overview:")
    st.subheader("Why Selenium?")
    st.markdown(
        """
        Selenium is a powerful tool for web scraping dynamic content. With the ability to interact with JavaScript-heavy pages, 
        it ensures that no data is left behind.
        """
    )

    st.subheader("Features:")
    st.markdown(
        """
        - Scrape dynamic content using **Selenium**.
        - Save the scraped data into databases for future use in **SQL**.
        - Visualize and filter the data interactively using **Streamlit**.
        """
    )

    st.subheader("Skills:")
    st.markdown(
        """
        Selenium, Python, MySQL, Streamlit
        """
    )
    
    st.subheader("Developed By:")
    st.markdown(
        """
        **Mohamed Adhil**
        """
    )


elif web == "Select the Bus":
    M = st.selectbox("States", ["Kerala", "Adhra Pradesh", "Telugana", "Goa", "Rajastan", 
                                          "South Bengal", "Haryana", "Assam", "Uttar Pradesh", "West Bengal"])
    
    col1,col2=st.columns(2)
    with col1:
        select_type = st.radio("Bus type", ("sleeper", "semi-sleeper", "others"))
    with col2:
        select_fare = st.radio("Bus fare", ("50-1000", "1000-2000", "2000 and above"))
    TIME=st.time_input("Time")

    # Kerala bus fare filtering
    if M == "Kerala":
        K = st.selectbox("List of routes",lists_K)

        def type_and_fare(Bustype, fare_range):
            conn = pymysql.connect(host="127.0.0.1", user="root", password="Asm@dhil01",database="RedBus_Details")
            my_cur = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

            # Define bus type condition
            if Bustype == "sleeper":
                Bustype_condition = "Bustype LIKE '%Sleeper%'"
            elif Bustype == "semi-sleeper":
                Bustype_condition = "Bustype LIKE '%A/c Semi Sleeper %'"
            else:
                Bustype_condition = "Bustype NOT LIKE '%Sleeper%' AND Bustype NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_routes
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{K}"
                AND {Bustype_condition} AND Start_time>='{TIME}'
                ORDER BY Price and Start_time DESC
            '''
            my_cur.execute(query)
            out = my_cur.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bustype", "Start_time", "End_time", "Total_duration",
                "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fare(select_type, select_fare)
        st.dataframe(df_result)


    #Andhra bus fare filtering
    if M=="Adhra Pradesh":
        A=st.selectbox("list of routes",lists_A)

        def type_and_fare_A(Bustype, fare_range):
            conn = pymysql.connect(host="127.0.0.1", user="root", password="Asm@dhil01",database="RedBus_Details")
            my_cur = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  

            # Define bus type condition
            if Bustype == "sleeper":
                Bustype_condition = "Bustype LIKE '%Sleeper%'"
            elif Bustype == "semi-sleeper":
                Bustype_condition = "Bustype LIKE '%A/c Semi Sleeper %'"
            else:
                Bustype_condition = "Bustype NOT LIKE '%Sleeper%' AND Bustype NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_routes
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{A}"
                AND {Bustype_condition} AND Start_time>='{TIME}'
                ORDER BY Price and Start_time DESC
            '''
            my_cur.execute(query)
            out = my_cur.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bustype", "Start_time", "End_time", "Total_duration",
                "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fare_A(select_type, select_fare)
        st.dataframe(df_result)


    #Telugana bus fare filtering
    if M=="Telugana":
        T=st.selectbox("list of routes",lists_T)

        def type_and_fare_T(Bustype, fare_range):
            conn = pymysql.connect(host="127.0.0.1", user="root", password="Asm@dhil01",database="RedBus_Details")
            my_cur = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  

            # Define bus type condition
            if Bustype == "sleeper":
                Bustype_condition = "Bustype LIKE '%Sleeper%'"
            elif Bustype == "semi-sleeper":
                Bustype_condition = "Bustype LIKE '%A/c Semi Sleeper %'"
            else:
                Bustype_condition = "Bustype NOT LIKE '%Sleeper%' AND Bustype NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_routes 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{T}"
                AND {Bustype_condition} AND Start_time>='{TIME}'
                ORDER BY Price and Start_time DESC
            '''
            my_cur.execute(query)
            out = my_cur.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bustype", "Start_time", "End_time", "Total_duration",
                "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fare_T(select_type, select_fare)
        st.dataframe(df_result)



    # Goa bus fare filtering
    if M=="Goa":
        G=st.selectbox("list of routes",lists_G)

        def type_and_fare_G(Bustype, fare_range):
            conn = pymysql.connect(host="127.0.0.1", user="root", password="Asm@dhil01",database="RedBus_Details")
            my_cur = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000
            
            # Define bus type condition
            if Bustype == "sleeper":
                Bustype_condition = "Bustype LIKE '%Sleeper%'"
            elif Bustype == "semi-sleeper":
                Bustype_condition = "Bustype LIKE '%A/c Semi Sleeper %'"
            else:
                Bustype_condition = "Bustype NOT LIKE '%Sleeper%' AND Bustype NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_routes 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{G}"
                AND {Bustype_condition} AND Start_time>='{TIME}'
                ORDER BY Price and Start_time DESC
            '''
            my_cur.execute(query)
            out = my_cur.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bustype", "Start_time", "End_time", "Total_duration",
                "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fare_G(select_type, select_fare)
        st.dataframe(df_result)

          

    #Rajasthan bus fare filtering       
    if M=="Rajasthan":
        R=st.selectbox("list of rotes",lists_R)

        def type_and_fare_R(bus_type, fare_range):
            conn = pymysql.connect(host="127.0.0.1", user="root", password="Asm@dhil01",database="RedBus_Details")
            my_cur = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  

            # Define bus type condition
            if Bustype == "sleeper":
                Bustype_condition = "Bustype LIKE '%Sleeper%'"
            elif Bustype == "semi-sleeper":
                Bustype_condition = "Bustype LIKE '%A/c Semi Sleeper %'"
            else:
                Bustype_condition = "Bustype NOT LIKE '%Sleeper%' AND Bustype NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_routes 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{R}"
                AND {Bustype_condition} AND Start_time>='{TIME}'
                ORDER BY Price and Start_time DESC
            '''
            my_cur.execute(query)
            out = my_cur.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bustype", "Start_time", "End_time", "Total_duration",
                "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fare_R(select_type, select_fare)
        st.dataframe(df_result)



    #South Bengal bus fare filtering
    if M=="South Bengal":
        SB=st.selectbox("list of rotes",lists_SB)

        def type_and_fare_SB(Bustype, fare_range):
            conn = pymysql.connect(host="127.0.0.1", user="root", password="Asm@dhil01",database="RedBus_Details")
            my_cur = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  

            # Define bus type condition
            if Bustype == "sleeper":
                Bustype_condition = "Bustype LIKE '%Sleeper%'"
            elif Bustype == "semi-sleeper":
                Bustype_condition = "Bustype LIKE '%A/c Semi Sleeper %'"
            else:
                Bustype_condition = "Bustype NOT LIKE '%Sleeper%' AND Bustype NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_routes 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{SB}"
                AND {Bustype_condition} AND Start_time>='{TIME}'
                ORDER BY Price and Start_time DESC
            '''
            my_cur.execute(query)
            out = my_cur.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bustype", "Start_time", "End_time", "Total_duration",
                "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fare_SB(select_type, select_fare)
        st.dataframe(df_result)



    if M=="Haryana":
        H=st.selectbox("list of rotes",lists_H)

        def type_and_fare_H(Bustype, fare_range):
            conn = pymysql.connect(host="127.0.0.1", user="root", password="Asm@dhil01",database="RedBus_Details")
            my_cur = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  

            # Define bus type condition
            if Bustype == "sleeper":
                Bustype_condition = "Bustype LIKE '%Sleeper%'"
            elif Bustype == "semi-sleeper":
                Bustype_condition = "Bustype LIKE '%A/c Semi Sleeper %'"
            else:
                Bustype_condition = "Bustype NOT LIKE '%Sleeper%' AND Bustype NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_routes 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{H}"
                AND {Bustype_condition} AND Start_time>='{TIME}'
                ORDER BY Price and Start_time DESC
            '''
            my_cur.execute(query)
            out = my_cur.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bustype", "Start_time", "End_time", "Total_duration",
                "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fare_H(select_type, select_fare)
        st.dataframe(df_result)




    #Assam bus fare filtering
    if M == "Assam":
        AS = st.selectbox("List of routes",lists_AS)

        def type_and_fare_AS(Bustype, fare_range):
            conn = pymysql.connect(host="127.0.0.1", user="root", password="Asm@dhil01",database="RedBus_Details")
            my_cur = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

            # Define bus type condition
            if Bustype == "sleeper":
                Bustype_condition = "Bustype LIKE '%Sleeper%'"
            elif Bustype == "semi-sleeper":
                Bustype_condition = "Bustype LIKE '%A/c Semi Sleeper %'"
            else:
                Bustype_condition = "Bustype NOT LIKE '%Sleeper%' AND Bustype NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_routes
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{AS}"
                AND {Bustype_condition} AND Start_time>='{TIME}'
                ORDER BY Price and Start_time DESC
            '''
            my_cur.execute(query)
            out = my_cur.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bustype", "Start_time", "End_time", "Total_duration",
                "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fare_AS(select_type, select_fare)
        st.dataframe(df_result)




    #Uttar Pradesh bus fare filtering
    if M == "Uttar pradesh":
        UP = st.selectbox("List of routes",lists_UP)

        def type_and_fare_UP(Bustype, fare_range):
            conn = pymysql.connect(host="127.0.0.1", user="root", password="Asm@dhil01",database="RedBus_Details")
            my_cur = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

            # Define bus type condition
            if Bustype == "sleeper":
                Bustype_condition = "Bustype LIKE '%Sleeper%'"
            elif Bustype == "semi-sleeper":
                Bustype_condition = "Bustype LIKE '%A/c Semi Sleeper %'"
            else:
                Bustype_condition = "Bustype NOT LIKE '%Sleeper%' AND Bustype NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_routes
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{UP}"
                AND {Bustype_condition} AND Start_time>='{TIME}'
                ORDER BY Price and Start_time DESC
            '''
            my_cur.execute(query)
            out = my_cur.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bustype", "Start_time", "End_time", "Total_duration",
                "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fare_UP(select_type, select_fare)
        st.dataframe(df_result)




    #West Bengal bus fare filtering
    if M == "West Bengal":
        WB = st.selectbox("List of routes",lists_WB)

        def type_and_fare_WB(Bustype, fare_range):
            conn = pymysql.connect(host="127.0.0.1", user="root", password="Asm@dhil01",database="RedBus_Details")
            my_cur = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

            # Define bus type condition
            if Bustype == "sleeper":
                Bustype_condition = "Bustype LIKE '%Sleeper%'"
            elif Bustype == "semi-sleeper":
                Bustype_condition = "Bustype LIKE '%A/c Semi Sleeper %'"
            else:
                Bustype_condition = "Bustype NOT LIKE '%Sleeper%' AND Bustype NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_routes
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{WB}"
                AND {Bustype_condition} AND Start_time>='{TIME}'
                ORDER BY Price and Start_time DESC
            '''
            my_cur.execute(query)
            out = my_cur.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bustype", "Start_time", "End_time", "Total_duration",
                "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fare_WB(select_type, select_fare)
        st.dataframe(df_result)
        