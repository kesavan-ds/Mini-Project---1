import pandas as pd
import pymysql
from sqlalchemy import create_engine
import streamlit as st

engine = create_engine("mysql+pymysql://root:9095@127.0.0.1:3306/work1")

queries = {
    "1. Top 10 strongest earthquakes":
    """SELECT place, country, mag, depth_km FROM earthquake_data ORDER BY mag DESC LIMIT 10;""",
    
    "2. Top 10 deepest earthquakes":
    """SELECT place, country, mag, depth_km FROM earthquake_data ORDER BY depth_km DESC LIMIT 10;""",
    
    "3. Shallow earthquakes < 50 km and mag > 7.5": 
    """SELECT place, country, mag, depth_km, time FROM earthquake_data WHERE depth_km < 50 AND mag > 7.5 ORDER BY mag DESC;""",
    
    "4. Average depth per country": 
    """SELECT country, AVG(depth_km) AS avg_depth FROM earthquake_data GROUP BY country;""",
    
    "5. Average magnitude per magnitude type":
    """SELECT magType, ROUND(AVG(mag), 2) AS avg_magnitude FROM earthquake_data GROUP BY magType ORDER BY avg_magnitude DESC;""",
    
    "6. Year with most earthquakes": 
    """SELECT YEAR(time) AS year, COUNT(*) AS total_earthquakes FROM earthquake_data GROUP BY YEAR(time) ORDER BY total_earthquakes DESC LIMIT 1;""",
    
    "7. Month with most earthquakes":
    """SELECT MONTH(time) AS month, COUNT(*) AS total_earthquakes FROM earthquake_data GROUP BY MONTH(time) ORDER BY total_earthquakes DESC LIMIT 1;""",
    
    "8. Day with most earthquakes": 
    """SELECT DAYNAME(time) AS day_name, COUNT(*) AS total_earthquakes FROM earthquake_data GROUP BY DAYNAME(time) ORDER BY total_earthquakes DESC LIMIT 1;""",
    
    "9. Hour with most earthquakes":
    """SELECT HOUR(time) AS hour_of_day, COUNT(*) AS total_earthquakes FROM earthquake_data GROUP BY HOUR(time) ORDER BY hour_of_day;""",
    
    "10. Network with most earthquakes": 
    """SELECT net, COUNT(*) AS total_earthquakes FROM earthquake_data GROUP BY net ORDER BY total_earthquakes DESC LIMIT 1;""",
    
    "11. Countries with most casualties": 
    """__skip__""",
    
    "12. Countries with most economic losses":
    """__skip__""",
    
    "13. Average economic by alert level": 
    """__skip__""",
    
    "14. Earthquake status distribution": 
    """SELECT status, COUNT(*) AS total FROM earthquake_data GROUP BY status;""",
    
    "15. Earthquake types distribution": 
    """SELECT type, COUNT(*) AS total FROM earthquake_data GROUP BY type ORDER BY total DESC;""",
    
    "16. Earthquake types distribution (alternative)":
    """SELECT types, COUNT(*) AS total FROM earthquake_data GROUP BY types ORDER BY total DESC;""",
    
    "17. Average RMS and gap per continent.":
    """SELECT country, ROUND(AVG(rms),2) AS avg_rms, ROUND(AVG(gap),2) AS avg_gap
      FROM earthquake_data GROUP BY country;""",
    
    "18. Earthquakes with high reliability": 
    """SELECT place, mag, nst FROM earthquake_data WHERE nst > 100 ORDER BY nst DESC;""",
    
    "19. Tsunami events by year": 
    """SELECT YEAR(time) AS year, COUNT(*) AS tsunami_events FROM earthquake_data WHERE tsunami = 1 GROUP BY YEAR(time) ORDER BY year;""",
    
    "20. Earthquake alerts distribution": 
    """SELECT alert, COUNT(*) AS total FROM earthquake_data GROUP BY alert ORDER BY total DESC;""",
    
    "21. Countries with highest average magnitude":
    """SELECT country, ROUND(AVG(mag),2) AS avg_magnitude FROM earthquake_data GROUP BY country ORDER BY avg_magnitude DESC LIMIT 5;""",
    
    "22. Countries with varying depth focus": 
    """SELECT country, YEAR(time) AS year, MONTH(time) AS month FROM earthquake_data
    GROUP BY country, YEAR(time), MONTH(time) HAVING MIN(depth_km) < 70 AND MAX(depth_km) > 300;""",
    
    "23. Yearly earthquake growth rate": 
    """SELECT year, total_earthquakes, ROUND((total_earthquakes - LAG(total_earthquakes) OVER(ORDER BY year)) / LAG(total_earthquakes) 
    OVER(ORDER BY year) * 100,2) AS growth_rate_percent FROM (SELECT YEAR(time) AS year, COUNT(*) AS total_earthquakes FROM earthquake_data GROUP BY YEAR(time)) t;""",
    
    "24. Countries with highest seismic activity":
    """SELECT country, COUNT(*) AS total_earthquakes, ROUND(AVG(mag),2) AS avg_magnitude, ROUND(COUNT(*) * AVG(mag),2) AS seismic_score
    FROM earthquake_data GROUP BY country ORDER BY seismic_score DESC LIMIT 3;""",
    
    "25. Countries with highest average depth (equatorial)": 
    """SELECT country, ROUND(AVG(depth_km),2) AS avg_depth FROM earthquake_data WHERE latitude BETWEEN -5 AND 5 GROUP BY country ORDER BY avg_depth DESC;""",
    
    "26. Countries with highest shallow-to-deep ratio": 
    """SELECT country, SUM(CASE WHEN depth_km < 70 THEN 1 ELSE 0 END) AS shallow_count, SUM(CASE WHEN depth_km > 300 THEN 1 ELSE 0 END) AS deep_count,
    ROUND(SUM(CASE WHEN depth_km < 70 THEN 1 ELSE 0 END) / NULLIF(SUM(CASE WHEN depth_km > 300 THEN 1 ELSE 0 END),0),2) AS shallow_deep_ratio
    FROM earthquake_data GROUP BY country ORDER BY shallow_deep_ratio DESC;""",
    
    "27. Avg magnitude difference: tsunami vs non-tsunami":
    """SELECT tsunami, ROUND(AVG(mag),2) AS avg_magnitude FROM earthquake_data GROUP BY tsunami;""",
    
    "28. Events with lowest data reliability": 
    """SELECT place, country, rms, gap, ROUND((rms + gap)/2,2) AS error_score FROM earthquake_data ORDER BY error_score DESC LIMIT 20;""",
    
    "29. Consecutive earthquakes within 50 km and 1 hour": 
    """SELECT a.id AS quake1, b.id AS quake2, a.place, a.time, b.time FROM earthquake_data a JOIN earthquake_data b ON a.id < b.id 
    WHERE TIMESTAMPDIFF(HOUR,a.time,b.time) <= 1 AND (6371 * ACOS(COS(RADIANS(a.latitude)) * COS(RADIANS(b.latitude)) * COS(RADIANS(b.longitude)-RADIANS(a.longitude))
    + SIN(RADIANS(a.latitude)) * SIN(RADIANS(b.latitude)))) <= 50;""",
    
    "30. Countries with the most deep earthquakes": 
    """SELECT country, COUNT(*) AS deep_earthquakes FROM earthquake_data WHERE depth_km > 300 GROUP BY country ORDER BY deep_earthquakes DESC;"""
}


st.set_page_config(page_title="Earthquake Data Analysis", layout="wide")

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Project Introduction", "SQL Queries", "My Work & Exploration", "Creator Info"]
)

#1
if page == "Project Introduction":


    st.image(
    
    "https://images.unsplash.com/photo-1521295121783-8a321d551ad2",
    width=500
    )
    st.title("Earthquake Data Analysis ")
    st.write(
        "This project analyzes earthquake data collected from the USGS API using Python, MySQL, SQL, and Streamlit."
    )

    st.subheader(" Data Collection")

    st.write(
        "Earthquake data was collected from the USGS API in JSON format."
    )


    st.subheader(" Data Processing")

    st.write(
        "The JSON data was converted into a Pandas DataFrame for analysis."
    )


    st.subheader(" Data Cleaning")

    st.write(
        "Missing values and duplicate records were cleaned using Pandas."
    )


    st.subheader(" MySQL Storage")

    st.write(
        "The cleaned dataset was stored into a MySQL database."
    )


    st.subheader(" SQL Analysis")

    st.write(
        "SQL queries were used to analyze earthquake trends and magnitude."
    )

 #2 
elif page == "SQL Queries":
    st.title("Earthquake SQL Queries")
    st.write("Select a query from the dropdown below to see the results.")

    task = st.selectbox("Select a query to run", options=list(queries.keys()))

    if st.button("Run Query"):
        query = queries[task]
        if query == "__skip__":
            st.warning(f"'{task}' cannot be run — no casualty/economic column in this dataset.")
        else:
            try:
                df = pd.read_sql(query, engine)
                st.subheader(f"Results: {task}")
                st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"Query failed: {e}")

#3
elif page == "My Work & Exploration":
    st.title("My Work & Exploration")
 
    st.subheader("Data Source")
    st.write("I collected global earthquake data from the **USGS Earthquake API** and stored it in a MySQL database.")
 
    st.subheader("Tools I Used")
    st.write("- **Python** — main programming language")
    st.write("- **MySQL** — to store and query the data")
    st.write("- **Pandas** — to handle and display the data")
    st.write("- **Streamlit** — to build this web app")
 
    st.subheader("How I Worked")
    st.write("1. Downloaded earthquake data from USGS API")
    st.write("2. Loaded it into a MySQL database")
    st.write("3. Wrote 30 SQL queries to explore the data")
    st.write("4. Built this Streamlit app to show the results")
 
    st.subheader(" What I Found")
    st.write("- Most strong earthquakes happen in Japan, Chile, and Indonesia")
    st.write("- Earthquakes linked to tsunamis have higher average magnitude")
    st.write("- Shallow earthquakes (< 70 km deep) are more dangerous")
    st.write("- More earthquake records appear over the years — due to better sensors, not more quakes")
 
    st.subheader(" Problems I Faced")
    st.write("Queries 11 & 12 couldn't be done — the dataset has no casualty or economic loss columns.")
    st.write("Query 29 (finding nearby earthquake pairs) is slow because it compares every row with every other row.")
                 
#4
elif page == "Creator Info":
   
    st.subheader(" About Me")

    st.write(
        """
        • Name: Kesavan  
        • Learning Data Science and AI  
        • Interested in Data Analysis, SQL, Python, and Machine Learning  
         
        """
    )

    st.subheader(" Learning Platform")

    st.write(
        """
        • Currently learning Data Science from GUVI  
        • Practicing SQL, Pandas, Visualization, and Dashboard Development  
         
        """
    )

    st.subheader("Technologies Used")

    st.write(
        """
        • Python  
        • Pandas  
        • MySQL  
        • Streamlit  
        • SQLAlchemy  
        • VS Code  
        """
    )

    
