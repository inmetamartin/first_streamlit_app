import streamlit
import pandas
import snowflake.connector
import requests
from urllib.error import URLError

streamlit.title('My parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

streamlit.header('Fruitivice Fruit Advice')

def get_data(fChoice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)    
  # normalizes json to table 
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  streamlit.write('The user entered ', fruit_choice)
  if not fruit_choice:
    streamlit.error("Select a fruit to get information")
  else:
      # prints the dataframe to streamlit
      fNormalized = get_data(fruit_choice)
      streamlit.dataframe(fNormalized)
except URLError as e:
  streamlit.error()


#streamlit.stop()

streamlit.header("The fruit load list contains")

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_values('" + new_fruit +"')")
    return "Thanks for adding "+ new_fruit

if streamlit.button("Get Fruit Load List add your fav"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)
  #my_cur = my_cnx.cursor()
  #streamlit.header('Additional fruits')
  try:
    add_my_fruit = streamlit.text_input('What fruit would you like to add?')
    stramlit.write("--- adding " + add_my_fruit)
    if not add_my_fruit:
      streamlit.error("select a fruit to add")
    else:
      insert_row_snowflake(add_my_fruit)
      

  
  
#  streamlit.write('Thanks for adding ', add_my_fruit)

#my_cur.execute("insert into fruit_load_list values('from streamlit')")



