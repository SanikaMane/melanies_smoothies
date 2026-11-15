# Import python packages
import streamlit as st
import requests
from streamlit.connections import SnowflakeConnection
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("🥤 Customize Your Smoothie! 🥤")

st.write(
    """
    Choose the fruits you want in your custom Smoothie!
    """
)

# Add a text input for the name on the smoothie
name_on_order = st.text_input(
    "Name on smoothie:",
    "Type your name here"
)

st.write("The name on your Smoothie will be:", name_on_order)

conn = st.connection("snowflake")
session = conn.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
fruit_names = my_dataframe.to_pandas()["FRUIT_NAME"].tolist()

#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_names,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    submit = st.button('Submit Order')

    if submit:
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                            values ('""" + ingredients_string + """','""" + name_on_order + """') """

      #  st.write(my_insert_stmt)

        session.sql(my_insert_stmt).collect()

        st.success('Your Smoothie is ordered!', icon="✅")

# New section to display smoothie fruit nutrition information

smoothiefroot_response = requests.get(
    "https://my.smoothiefroot.com/api/fruit/watermelon"
)

st.text(smoothiefroot_response.json())
