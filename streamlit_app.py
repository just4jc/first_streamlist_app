

import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError



my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Meanu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')


# Let's put a pick list here so they can pick the fruit they want to include 
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
#streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)

#New Section to display Fruityvice API response
#streamlit.header("Fruityvice Fruit Advice!")
#try:
#  fruit_choice = streamlit.text_input('What fruit would you like information about?')
#  if not fruit_choice:
#      #streamlit.write('The user entered ', fruit_choice)
#      streamlit.error("Please select a fruit to get information.")
#  else:
#      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
##      fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
#      # output it to the screen as table
#      streamlit.dataframe(fruityvice_normalized)
      
#except URLError as e:
#      streamlit.error()
    
#create repeatable code block
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
  
#New Section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)
except URLError as e:
      streamlit.error()
    
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")

#streamlit.text(fruityvice_response)
#streamlit.text(fruityvice_response.json())

# take the json version of the response and normalized it 


my_cur.execute("SELECT * from fruit_load_list")
#my_data_row = my_cur.fetchone()
my_data_rows = my_cur.fetchall()
#streamlit.text("Hello from Snowflake:")
#streamlit.text("The fruit load list contains:")
streamlit.header("The fruit load list contains:")
#streamlit.text(my_data_row)
#streamlit.dataframe(my_data_row)
streamlit.dataframe(my_data_rows)

# Allow the end user to add a fruit to the list
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
streamlit.write('Thanks for adding ', add_my_fruit)

#This will not work correctly, but just go with it for now
my_cur.execute("insert INTO FRUIT_LOAD_LIST values ('from streamlit')")

# don't run anything past here while we troubleshoot
streamlit.stop()
