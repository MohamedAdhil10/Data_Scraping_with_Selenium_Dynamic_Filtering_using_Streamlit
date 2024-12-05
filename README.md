# Data-Scraping-with-Selenium-Dynamic-Filtering-using-Streamlit
 ## Introduction
* The project is about to build an interactive web application that seamlessly integrates web scraping, data management, and real-time visualization. Using Selenium, the project automates the extraction of dynamic content from web pages, such as bus routes and schedules, which are often rendered dynamically using JavaScript. The scraped data is stored in a structured database (e.g., MySQL) to ensure easy accessibility and future scalability.
* The project also leverages Streamlit to create an intuitive user interface, allowing users to filter, search, and visualize the extracted data in real-time. By providing features like route selection and price comparison, it offers practical utility for end-users, such as travelers and transportation planners.
* Ultimately, the aim is to demonstrate how web scraping and dynamic data filtering can be used to create efficient, user-friendly solutions that bridge the gap between raw data and actionable insights, enhancing decision-making and user experience.

## Domain 
* Transportation

## SKILL-TAKEAWAY
* Python scripting,Selenium,Data Collection,Data Management using SQL,Streamlit
  
## TECHNOLOGY USED
* Python 3.10.11
* MySQL 8.0
* Streamlit
* Selenium

## FEATURES OF APPLICATION

## Retrive the Bus Information:
      Selenium is a versatile tool for automating web browsers, making it ideal for web scraping tasks. To extract bus details from RedBus, Selenium can automate tasks such as filling out search fields, clicking buttons, waiting for pages to load, and retrieving the required information from the results.

 ## Store data in database:
   * The collected bus details data was transformed into pandas dataframes. Before that, a new database and tables were created using the MySQL connector. With the help of MySQL, the data was inserted into the respective tables. The database could be accessed and managed in the MySQL environment.

## Web app - streamlit:
   * With the help of Streamlit, you can create an interactive application similar to RedBus by designing a user-friendly interface that allows users to search for bus routes, view available buses, and get details like departure times and prices

## PACKAGES AND LIBRARIES
* pandas as pd
* pymysql
* import time
* streamlit as st
* import datetime
* from streamlit_option_menu import option_menu
* from selenium import webdriver


 
     

                                
    

