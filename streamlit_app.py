# Import python packages
import streamlit as st
import requests
import pandas as pd
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

my_dataframe = session.table(
    "smoothies.public.fruit_options"
).select(
    col("FRUIT_NAME"),
    col("SEARCH_ON")
)

pd_df = my_dataframe.to_pandas()

fruit_names = pd_df["FRUIT_NAME"].tolist()

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_names,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on = pd_df.loc[
            pd_df["FRUIT_NAME"] == fruit_chosen,
            "SEARCH_ON"
        ].iloc[0]

        st.subheader(fruit_chosen + ' Nutrition Information')

        smoothiefroot_response = requests.get(
            "https://my.smoothiefroot.com/api/fruit/" + search_on
        )

        sf_df = st.dataframe(
            data=smoothiefroot_response.json(),
            use_container_width=True
        )
        
    submit = st.button('Submit Order')
    if submit:
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                            values ('""" + ingredients_string + """','""" + name_on_order + """') """

      #  st.write(my_insert_stmt)

        session.sql(my_insert_stmt).collect()

        st.success('Your Smoothie is ordered!', icon="✅")
