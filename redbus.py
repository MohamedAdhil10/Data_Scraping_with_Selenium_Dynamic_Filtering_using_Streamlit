import pandas as pd
import pymysql
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import time

# Kerala bus
lists_K = []
df_K = pd.read_csv(r"D:/RedBus/df_K.csv")
for i, r in df_K.iterrows():
    lists_K.append(r["Route_name"])

# Andhra bus
lists_A = []
df_A = pd.read_csv(r"D:/RedBus/df_A.csv")
for i, r in df_A.iterrows():
    lists_A.append(r["Route_name"])

# Telangana bus
lists_T = []
df_T = pd.read_csv(r"D:/RedBus/df_T.csv")
for i, r in df_T.iterrows():
    lists_T.append(r["Route_name"])

# Goa bus
lists_G = []
df_G = pd.read_csv(r"D:/RedBus/df_G.csv")
for i, r in df_G.iterrows():
    lists_G.append(r["Route_name"])

# Rajasthan bus
lists_R = []
df_R = pd.read_csv(r"D:/RedBus/df_R.csv")
for i, r in df_R.iterrows():
    lists_R.append(r["Route_name"])

# South Bengal bus
lists_SB = []
df_SB = pd.read_csv(r"D:/RedBus/df_SB.csv")
for i, r in df_SB.iterrows():
    lists_SB.append(r["Route_name"])

# Haryana bus
lists_H = []
df_H = pd.read_csv(r"D:/RedBus/df_H.csv")
for i, r in df_H.iterrows():
    lists_H.append(r["Route_name"])

# Assam bus
lists_AS = []
df_AS = pd.read_csv(r"D:/RedBus/df_AS.csv")
for i, r in df_AS.iterrows():
    lists_AS.append(r["Route_name"])

# Uttar Pradesh bus
lists_UP = []
df_UP = pd.read_csv(r"D:/RedBus/df_UP.csv")
for i, r in df_UP.iterrows():
    lists_UP.append(r["Route_name"])

# West Bengal bus
lists_WB = []
df_WB = pd.read_csv(r"D:/RedBus/df_WB.csv")
for i, r in df_WB.iterrows():
    lists_WB.append(r["Route_name"])

# Setting up Streamlit page
st.set_page_config(page_title="RedBus", page_icon="🚌", layout="wide")

with st.sidebar:
    web = option_menu(
        menu_title="Main Menu",
        options=["Home", "Select the Bus"],
        icons=["house", "bus"],
        menu_icon="cast",
        default_index=0,
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
    M = st.selectbox("States", ["Kerala", "Andhra Pradesh", "Telangana", "Goa", "Rajasthan", 
                                "South Bengal", "Haryana", "Assam", "Uttar Pradesh", "West Bengal"])

    #Kearala Busfare Filtering
    if M == "Kerala":
        K = st.selectbox("Select Route", lists_K)

        seat_type = st.selectbox("Select Seat Type", ["Seater", "Semi Sleeper", "Sleeper"])

        ratings = st.selectbox("Select Ratings", ["1 to 3", "3 to 4", "4 to 5"])

        start_time = st.selectbox("Select Start Time", [f"{i:02}:00" for i in range(24)])
        end_time = st.selectbox("Select End Time", [f"{i:02}:00" for i in range(24)])

        fare_range = st.selectbox("Select Fare Range", ["50 - 1000", "1000 - 2000", "2000 - 3000", "3000 and Above"])

        def type_and_fare(seat_type, ratings, start_time, end_time, fare_range):
            conn = pymysql.connect(
                host="127.0.0.1", user="root", password="Asm@dhil01", database="RedBus_Details"
            )
            my_cur = conn.cursor()

            if fare_range == "50 - 1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000 - 2000":
                fare_min, fare_max = 1000, 2000
            elif fare_range == "2000 - 3000":
                fare_min, fare_max = 2000, 3000
            else:
                fare_min, fare_max = 3000, 100000

            if seat_type == "Seater":
                seat_type_condition = "Bustype LIKE '%Seater%'"
            elif seat_type == "Semi Sleeper":
                seat_type_condition = "Bustype LIKE '%Semi Sleeper%'"
            else:
                seat_type_condition = "Bustype LIKE '%Sleeper%'"

            if ratings == "1 to 3":
                rating_min, rating_max = 1, 3
            elif ratings == "3 to 4":
                rating_min, rating_max = 3, 4
            else:
                rating_min, rating_max = 4, 5

            query = f'''
                SELECT ID, Busname, Bustype, Start_time, End_time, Total_duration,
                       Price, Seats_Available, Star_ratings, Route_link, Route_name
                FROM bus_routes
                WHERE Route_name = "{K}"
                AND Price BETWEEN {fare_min} AND {fare_max}
                AND Star_ratings BETWEEN {rating_min} AND {rating_max}
                AND Start_time >= "{start_time}" AND End_time <= "{end_time}"
                AND ({seat_type_condition})
                ORDER BY Price, Start_time
            '''
            my_cur.execute(query)
            out = my_cur.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Busname", "Seat Type", "Start Time", "End Time", "Total Duration",
                "Fare", "Seats Available", "Star_ratings", "Route Link", "Route Name"
            ])
            return df

        df_result = type_and_fare(seat_type, ratings, start_time, end_time, fare_range)
        st.dataframe(df_result)


    #Andhra Busfare Filtering
    if M == "Andhra Pradesh":
        A = st.selectbox("Select Route", lists_A)

        seat_type = st.selectbox("Select Seat Type", ["Seater", "Semi Sleeper", "Sleeper"])

        ratings = st.selectbox("Select Ratings", ["1 to 3", "3 to 4", "4 to 5"])

        start_time = st.selectbox("Select Start Time", [f"{i:02}:00" for i in range(24)])
        end_time = st.selectbox("Select End Time", [f"{i:02}:00" for i in range(24)])

        fare_range = st.selectbox("Select Fare Range", ["50 - 1000", "1000 - 2000", "2000 - 3000", "3000 and Above"])

        def type_and_fare_A(seat_type, ratings, start_time, end_time, fare_range):
            conn = pymysql.connect(
                host="127.0.0.1", user="root", password="Asm@dhil01", database="RedBus_Details"
            )
            my_cur = conn.cursor()

            if fare_range == "50 - 1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000 - 2000":
                fare_min, fare_max = 1000, 2000
            elif fare_range == "2000 - 3000":
                fare_min, fare_max = 2000, 3000
            else:
                fare_min, fare_max = 3000, 100000

            if seat_type == "Seater":
                seat_type_condition = "Bustype LIKE '%Seater%'"
            elif seat_type == "Semi Sleeper":
                seat_type_condition = "Bustype LIKE '%Semi Sleeper%'"
            else:
                seat_type_condition = "Bustype LIKE '%Sleeper%'"

            if ratings == "1 to 3":
                rating_min, rating_max = 1, 3
            elif ratings == "3 to 4":
                rating_min, rating_max = 3, 4
            else:
                rating_min, rating_max = 4, 5

            query = f'''
                SELECT ID, Busname, Bustype, Start_time, End_time, Total_duration,
                       Price, Seats_Available, Star_ratings, Route_link, Route_name
                FROM bus_routes
                WHERE Route_name = "{A}"
                AND Price BETWEEN {fare_min} AND {fare_max}
                AND Star_ratings BETWEEN {rating_min} AND {rating_max}
                AND Start_time >= "{start_time}" AND End_time <= "{end_time}"
                AND ({seat_type_condition})
                ORDER BY Price, Start_time
            '''
            my_cur.execute(query)
            out = my_cur.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Busname", "Seat Type", "Start Time", "End Time", "Total Duration",
                "Fare", "Seats Available", "Star_ratings", "Route Link", "Route Name"
            ])
            return df

        df_result = type_and_fare_A(seat_type, ratings, start_time, end_time, fare_range)
        st.dataframe(df_result)


    #Telangana Busfare Filtering
    if M == "Telangana":
        T = st.selectbox("Select Route", lists_T)

        seat_type = st.selectbox("Select Seat Type", ["Seater", "Semi Sleeper", "Sleeper"])

        ratings = st.selectbox("Select Ratings", ["1 to 3", "3 to 4", "4 to 5"])

        start_time = st.selectbox("Select Start Time", [f"{i:02}:00" for i in range(24)])
        end_time = st.selectbox("Select End Time", [f"{i:02}:00" for i in range(24)])

        fare_range = st.selectbox("Select Fare Range", ["50 - 1000", "1000 - 2000", "2000 - 3000", "3000 and Above"])

        def type_and_fare_T(seat_type, ratings, start_time, end_time, fare_range):
            conn = pymysql.connect(
                host="127.0.0.1", user="root", password="Asm@dhil01", database="RedBus_Details"
            )
            my_cur = conn.cursor()

            if fare_range == "50 - 1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000 - 2000":
                fare_min, fare_max = 1000, 2000
            elif fare_range == "2000 - 3000":
                fare_min, fare_max = 2000, 3000
            else:
                fare_min, fare_max = 3000, 100000

            if seat_type == "Seater":
                seat_type_condition = "Bustype LIKE '%Seater%'"
            elif seat_type == "Semi Sleeper":
                seat_type_condition = "Bustype LIKE '%Semi Sleeper%'"
            else:
                seat_type_condition = "Bustype LIKE '%Sleeper%'"

            if ratings == "1 to 3":
                rating_min, rating_max = 1, 3
            elif ratings == "3 to 4":
                rating_min, rating_max = 3, 4
            else:
                rating_min, rating_max = 4, 5

            query = f'''
                SELECT ID, Busname, Bustype, Start_time, End_time, Total_duration,
                       Price, Seats_Available, Star_ratings, Route_link, Route_name
                FROM bus_routes
                WHERE Route_name = "{T}"
                AND Price BETWEEN {fare_min} AND {fare_max}
                AND Star_ratings BETWEEN {rating_min} AND {rating_max}
                AND Start_time >= "{start_time}" AND End_time <= "{end_time}"
                AND ({seat_type_condition})
                ORDER BY Price, Start_time
            '''
            my_cur.execute(query)
            out = my_cur.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Busname", "Seat Type", "Start Time", "End Time", "Total Duration",
                "Fare", "Seats Available", "Star_ratings", "Route Link", "Route Name"
            ])
            return df

        df_result = type_and_fare_T(seat_type, ratings, start_time, end_time, fare_range)
        st.dataframe(df_result)


    #Goa Busfare Filtering
    if M == "Goa":
        G = st.selectbox("Select Route", lists_G)

        seat_type = st.selectbox("Select Seat Type", ["Seater", "Semi Sleeper", "Sleeper"])

        ratings = st.selectbox("Select Ratings", ["1 to 3", "3 to 4", "4 to 5"])

        start_time = st.selectbox("Select Start Time", [f"{i:02}:00" for i in range(24)])
        end_time = st.selectbox("Select End Time", [f"{i:02}:00" for i in range(24)])

        fare_range = st.selectbox("Select Fare Range", ["50 - 1000", "1000 - 2000", "2000 - 3000", "3000 and Above"])

        def type_and_fare_G(seat_type, ratings, start_time, end_time, fare_range):
            conn = pymysql.connect(
                host="127.0.0.1", user="root", password="Asm@dhil01", database="RedBus_Details"
            )
            my_cur = conn.cursor()

            if fare_range == "50 - 1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000 - 2000":
                fare_min, fare_max = 1000, 2000
            elif fare_range == "2000 - 3000":
                fare_min, fare_max = 2000, 3000
            else:
                fare_min, fare_max = 3000, 100000

            if seat_type == "Seater":
                seat_type_condition = "Bustype LIKE '%Seater%'"
            elif seat_type == "Semi Sleeper":
                seat_type_condition = "Bustype LIKE '%Semi Sleeper%'"
            else:
                seat_type_condition = "Bustype LIKE '%Sleeper%'"

            if ratings == "1 to 3":
                rating_min, rating_max = 1, 3
            elif ratings == "3 to 4":
                rating_min, rating_max = 3, 4
            else:
                rating_min, rating_max = 4, 5

            query = f'''
                SELECT ID, Busname, Bustype, Start_time, End_time, Total_duration,
                       Price, Seats_Available, Star_ratings, Route_link, Route_name
                FROM bus_routes
                WHERE Route_name = "{G}"
                AND Price BETWEEN {fare_min} AND {fare_max}
                AND Star_ratings BETWEEN {rating_min} AND {rating_max}
                AND Start_time >= "{start_time}" AND End_time <= "{end_time}"
                AND ({seat_type_condition})
                ORDER BY Price, Start_time
            '''
            my_cur.execute(query)
            out = my_cur.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Busname", "Seat Type", "Start Time", "End Time", "Total Duration",
                "Fare", "Seats Available", "Star_ratings", "Route Link", "Route Name"
            ])
            return df

        df_result = type_and_fare_G(seat_type, ratings, start_time, end_time, fare_range)
        st.dataframe(df_result)


    #Rajasthan Busfare filtering
    if M == "Rajasthan":
        R = st.selectbox("Select Route", lists_R)

        seat_type = st.selectbox("Select Seat Type", ["Seater", "Semi Sleeper", "Sleeper"])

        ratings = st.selectbox("Select Ratings", ["1 to 3", "3 to 4", "4 to 5"])

        start_time = st.selectbox("Select Start Time", [f"{i:02}:00" for i in range(24)])
        end_time = st.selectbox("Select End Time", [f"{i:02}:00" for i in range(24)])

        fare_range = st.selectbox("Select Fare Range", ["50 - 1000", "1000 - 2000", "2000 - 3000", "3000 and Above"])

        def type_and_fare_R(seat_type, ratings, start_time, end_time, fare_range):
            conn = pymysql.connect(
                host="127.0.0.1", user="root", password="Asm@dhil01", database="RedBus_Details"
            )
            my_cur = conn.cursor()

            if fare_range == "50 - 1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000 - 2000":
                fare_min, fare_max = 1000, 2000
            elif fare_range == "2000 - 3000":
                fare_min, fare_max = 2000, 3000
            else:
                fare_min, fare_max = 3000, 100000

            if seat_type == "Seater":
                seat_type_condition = "Bustype LIKE '%Seater%'"
            elif seat_type == "Semi Sleeper":
                seat_type_condition = "Bustype LIKE '%Semi Sleeper%'"
            else:
                seat_type_condition = "Bustype LIKE '%Sleeper%'"

            if ratings == "1 to 3":
                rating_min, rating_max = 1, 3
            elif ratings == "3 to 4":
                rating_min, rating_max = 3, 4
            else:
                rating_min, rating_max = 4, 5

            query = f'''
                SELECT ID, Busname, Bustype, Start_time, End_time, Total_duration,
                       Price, Seats_Available, Star_ratings, Route_link, Route_name
                FROM bus_routes
                WHERE Route_name = "{R}"
                AND Price BETWEEN {fare_min} AND {fare_max}
                AND Star_ratings BETWEEN {rating_min} AND {rating_max}
                AND Start_time >= "{start_time}" AND End_time <= "{end_time}"
                AND ({seat_type_condition})
                ORDER BY Price, Start_time
            '''
            my_cur.execute(query)
            out = my_cur.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Busname", "Seat Type", "Start Time", "End Time", "Total Duration",
                "Fare", "Seats Available", "Star_ratings", "Route Link", "Route Name"
            ])
            return df

        df_result = type_and_fare_R(seat_type, ratings, start_time, end_time, fare_range)
        st.dataframe(df_result)


    #South bengal Busfare Filtering
    if M == "South Bengal":
        SB = st.selectbox("Select Route", lists_SB)

        seat_type = st.selectbox("Select Seat Type", ["Seater", "Semi Sleeper", "Sleeper"])

        ratings = st.selectbox("Select Ratings", ["1 to 3", "3 to 4", "4 to 5"])

        start_time = st.selectbox("Select Start Time", [f"{i:02}:00" for i in range(24)])
        end_time = st.selectbox("Select End Time", [f"{i:02}:00" for i in range(24)])

        fare_range = st.selectbox("Select Fare Range", ["50 - 1000", "1000 - 2000", "2000 - 3000", "3000 and Above"])

        def type_and_fare_SB(seat_type, ratings, start_time, end_time, fare_range):
            conn = pymysql.connect(
                host="127.0.0.1", user="root", password="Asm@dhil01", database="RedBus_Details"
            )
            my_cur = conn.cursor()

            if fare_range == "50 - 1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000 - 2000":
                fare_min, fare_max = 1000, 2000
            elif fare_range == "2000 - 3000":
                fare_min, fare_max = 2000, 3000
            else:
                fare_min, fare_max = 3000, 100000

            if seat_type == "Seater":
                seat_type_condition = "Bustype LIKE '%Seater%'"
            elif seat_type == "Semi Sleeper":
                seat_type_condition = "Bustype LIKE '%Semi Sleeper%'"
            else:
                seat_type_condition = "Bustype LIKE '%Sleeper%'"

            if ratings == "1 to 3":
                rating_min, rating_max = 1, 3
            elif ratings == "3 to 4":
                rating_min, rating_max = 3, 4
            else:
                rating_min, rating_max = 4, 5

            query = f'''
                SELECT ID, Busname, Bustype, Start_time, End_time, Total_duration,
                       Price, Seats_Available, Star_ratings, Route_link, Route_name
                FROM bus_routes
                WHERE Route_name = "{SB}"
                AND Price BETWEEN {fare_min} AND {fare_max}
                AND Star_ratings BETWEEN {rating_min} AND {rating_max}
                AND Start_time >= "{start_time}" AND End_time <= "{end_time}"
                AND ({seat_type_condition})
                ORDER BY Price, Start_time
            '''
            my_cur.execute(query)
            out = my_cur.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Busname", "Seat Type", "Start Time", "End Time", "Total Duration",
                "Fare", "Seats Available", "Star_ratings", "Route Link", "Route Name"
            ])
            return df

        df_result = type_and_fare_SB(seat_type, ratings, start_time, end_time, fare_range)
        st.dataframe(df_result)


    #Haryana Busfare Filtering
    if M == "Haryana":
        H = st.selectbox("Select Route", lists_H)

        seat_type = st.selectbox("Select Seat Type", ["Seater", "Semi Sleeper", "Sleeper"])

        ratings = st.selectbox("Select Ratings", ["1 to 3", "3 to 4", "4 to 5"])

        start_time = st.selectbox("Select Start Time", [f"{i:02}:00" for i in range(24)])
        end_time = st.selectbox("Select End Time", [f"{i:02}:00" for i in range(24)])

        fare_range = st.selectbox("Select Fare Range", ["50 - 1000", "1000 - 2000", "2000 - 3000", "3000 and Above"])

        def type_and_fare_H(seat_type, ratings, start_time, end_time, fare_range):
            conn = pymysql.connect(
                host="127.0.0.1", user="root", password="Asm@dhil01", database="RedBus_Details"
            )
            my_cur = conn.cursor()

            if fare_range == "50 - 1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000 - 2000":
                fare_min, fare_max = 1000, 2000
            elif fare_range == "2000 - 3000":
                fare_min, fare_max = 2000, 3000
            else:
                fare_min, fare_max = 3000, 100000

            if seat_type == "Seater":
                seat_type_condition = "Bustype LIKE '%Seater%'"
            elif seat_type == "Semi Sleeper":
                seat_type_condition = "Bustype LIKE '%Semi Sleeper%'"
            else:
                seat_type_condition = "Bustype LIKE '%Sleeper%'"

            if ratings == "1 to 3":
                rating_min, rating_max = 1, 3
            elif ratings == "3 to 4":
                rating_min, rating_max = 3, 4
            else:
                rating_min, rating_max = 4, 5

            query = f'''
                SELECT ID, Busname, Bustype, Start_time, End_time, Total_duration,
                       Price, Seats_Available, Star_ratings, Route_link, Route_name
                FROM bus_routes
                WHERE Route_name = "{H}"
                AND Price BETWEEN {fare_min} AND {fare_max}
                AND Star_ratings BETWEEN {rating_min} AND {rating_max}
                AND Start_time >= "{start_time}" AND End_time <= "{end_time}"
                AND ({seat_type_condition})
                ORDER BY Price, Start_time
            '''
            my_cur.execute(query)
            out = my_cur.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Busname", "Seat Type", "Start Time", "End Time", "Total Duration",
                "Fare", "Seats Available", "Star_ratings", "Route Link", "Route Name"
            ])
            return df

        df_result = type_and_fare_H(seat_type, ratings, start_time, end_time, fare_range)
        st.dataframe(df_result)


    #Assam Busfare Filtering
    if M == "Assam":
        AS = st.selectbox("Select Route", lists_AS)

        seat_type = st.selectbox("Select Seat Type", ["Seater", "Semi Sleeper", "Sleeper"])

        ratings = st.selectbox("Select Ratings", ["1 to 3", "3 to 4", "4 to 5"])

        start_time = st.selectbox("Select Start Time", [f"{i:02}:00" for i in range(24)])
        end_time = st.selectbox("Select End Time", [f"{i:02}:00" for i in range(24)])

        fare_range = st.selectbox("Select Fare Range", ["50 - 1000", "1000 - 2000", "2000 - 3000", "3000 and Above"])

        def type_and_fare_AS(seat_type, ratings, start_time, end_time, fare_range):
            conn = pymysql.connect(
                host="127.0.0.1", user="root", password="Asm@dhil01", database="RedBus_Details"
            )
            my_cur = conn.cursor()

            if fare_range == "50 - 1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000 - 2000":
                fare_min, fare_max = 1000, 2000
            elif fare_range == "2000 - 3000":
                fare_min, fare_max = 2000, 3000
            else:
                fare_min, fare_max = 3000, 100000

            if seat_type == "Seater":
                seat_type_condition = "Bustype LIKE '%Seater%'"
            elif seat_type == "Semi Sleeper":
                seat_type_condition = "Bustype LIKE '%Semi Sleeper%'"
            else:
                seat_type_condition = "Bustype LIKE '%Sleeper%'"

            if ratings == "1 to 3":
                rating_min, rating_max = 1, 3
            elif ratings == "3 to 4":
                rating_min, rating_max = 3, 4
            else:
                rating_min, rating_max = 4, 5

            query = f'''
                SELECT ID, Busname, Bustype, Start_time, End_time, Total_duration,
                       Price, Seats_Available, Star_ratings, Route_link, Route_name
                FROM bus_routes
                WHERE Route_name = "{AS}"
                AND Price BETWEEN {fare_min} AND {fare_max}
                AND Star_ratings BETWEEN {rating_min} AND {rating_max}
                AND Start_time >= "{start_time}" AND End_time <= "{end_time}"
                AND ({seat_type_condition})
                ORDER BY Price, Start_time
            '''
            my_cur.execute(query)
            out = my_cur.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Busname", "Seat Type", "Start Time", "End Time", "Total Duration",
                "Fare", "Seats Available", "Star_ratings", "Route Link", "Route Name"
            ])
            return df

        df_result = type_and_fare_AS(seat_type, ratings, start_time, end_time, fare_range)
        st.dataframe(df_result)


    #Uttar Pradesh Busfare Filtering
    if M == "Uttar Pradesh":
        UP = st.selectbox("Select Route", lists_UP)

        seat_type = st.selectbox("Select Seat Type", ["Seater", "Semi Sleeper", "Sleeper"])

        ratings = st.selectbox("Select Ratings", ["1 to 3", "3 to 4", "4 to 5"])

        start_time = st.selectbox("Select Start Time", [f"{i:02}:00" for i in range(24)])
        end_time = st.selectbox("Select End Time", [f"{i:02}:00" for i in range(24)])

        fare_range = st.selectbox("Select Fare Range", ["50 - 1000", "1000 - 2000", "2000 - 3000", "3000 and Above"])

        def type_and_fare_UP(seat_type, ratings, start_time, end_time, fare_range):
            conn = pymysql.connect(
                host="127.0.0.1", user="root", password="Asm@dhil01", database="RedBus_Details"
            )
            my_cur = conn.cursor()

            if fare_range == "50 - 1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000 - 2000":
                fare_min, fare_max = 1000, 2000
            elif fare_range == "2000 - 3000":
                fare_min, fare_max = 2000, 3000
            else:
                fare_min, fare_max = 3000, 100000

            if seat_type == "Seater":
                seat_type_condition = "Bustype LIKE '%Seater%'"
            elif seat_type == "Semi Sleeper":
                seat_type_condition = "Bustype LIKE '%Semi Sleeper%'"
            else:
                seat_type_condition = "Bustype LIKE '%Sleeper%'"

            if ratings == "1 to 3":
                rating_min, rating_max = 1, 3
            elif ratings == "3 to 4":
                rating_min, rating_max = 3, 4
            else:
                rating_min, rating_max = 4, 5

            query = f'''
                SELECT ID, Busname, Bustype, Start_time, End_time, Total_duration,
                       Price, Seats_Available, Star_ratings, Route_link, Route_name
                FROM bus_routes
                WHERE Route_name = "{UP}"
                AND Price BETWEEN {fare_min} AND {fare_max}
                AND Star_ratings BETWEEN {rating_min} AND {rating_max}
                AND Start_time >= "{start_time}" AND End_time <= "{end_time}"
                AND ({seat_type_condition})
                ORDER BY Price, Start_time
            '''
            my_cur.execute(query)
            out = my_cur.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Busname", "Seat Type", "Start Time", "End Time", "Total Duration",
                "Fare", "Seats Available", "Star_ratings", "Route Link", "Route Name"
            ])
            return df

        df_result = type_and_fare_UP(seat_type, ratings, start_time, end_time, fare_range)
        st.dataframe(df_result)


    #West Bengal Busfare Filtering
    if M == "West Bengal":
        WB = st.selectbox("Select Route", lists_WB)

        seat_type = st.selectbox("Select Seat Type", ["Seater", "Semi Sleeper", "Sleeper"])

        ratings = st.selectbox("Select Ratings", ["1 to 3", "3 to 4", "4 to 5"])

        start_time = st.selectbox("Select Start Time", [f"{i:02}:00" for i in range(24)])
        end_time = st.selectbox("Select End Time", [f"{i:02}:00" for i in range(24)])

        fare_range = st.selectbox("Select Fare Range", ["50 - 1000", "1000 - 2000", "2000 - 3000", "3000 and Above"])

        def type_and_fare_WB(seat_type, ratings, start_time, end_time, fare_range):
            conn = pymysql.connect(
                host="127.0.0.1", user="root", password="Asm@dhil01", database="RedBus_Details"
            )
            my_cur = conn.cursor()

            if fare_range == "50 - 1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000 - 2000":
                fare_min, fare_max = 1000, 2000
            elif fare_range == "2000 - 3000":
                fare_min, fare_max = 2000, 3000
            else:
                fare_min, fare_max = 3000, 100000

            if seat_type == "Seater":
                seat_type_condition = "Bustype LIKE '%Seater%'"
            elif seat_type == "Semi Sleeper":
                seat_type_condition = "Bustype LIKE '%Semi Sleeper%'"
            else:
                seat_type_condition = "Bustype LIKE '%Sleeper%'"

            if ratings == "1 to 3":
                rating_min, rating_max = 1, 3
            elif ratings == "3 to 4":
                rating_min, rating_max = 3, 4
            else:
                rating_min, rating_max = 4, 5

            query = f'''
                SELECT ID, Busname, Bustype, Start_time, End_time, Total_duration,
                       Price, Seats_Available, Star_ratings, Route_link, Route_name
                FROM bus_routes
                WHERE Route_name = "{WB}"
                AND Price BETWEEN {fare_min} AND {fare_max}
                AND Star_ratings BETWEEN {rating_min} AND {rating_max}
                AND Start_time >= "{start_time}" AND End_time <= "{end_time}"
                AND ({seat_type_condition})
                ORDER BY Price, Start_time
            '''
            my_cur.execute(query)
            out = my_cur.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Busname", "Seat Type", "Start Time", "End Time", "Total Duration",
                "Fare", "Seats Available", "Star_ratings", "Route Link", "Route Name"
            ])
            return df

        df_result = type_and_fare_WB(seat_type, ratings, start_time, end_time, fare_range)
        st.dataframe(df_result)
