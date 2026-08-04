# Import python packages
import streamlit as st 
import os
# from snowflake.snowpark.context import get_active_session
from cryptography.hazmat.primitives import serialization
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """)
# st.write(
#   """Replace this example with your own code!
#   **And if you're new to Streamlit,** check
#   out our easy-to-follow guides at
#   [docs.streamlit.io](https://docs.streamlit.io).
#   """
# )

# st.markdown("""
# - :page_with_curl: [Streamlit open source documentation](https://docs.streamlit.io)
# - :snowflake: [Streamlit in Snowflake documentation](https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit)
# - :books: [Demo repo with templates](https://github.com/Snowflake-Labs/snowflake-demo-streamlit)
# - :memo: [Streamlit in Snowflake release notes](https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake)
# """)

# option = st.selectbox(
#     "What is your favorite fruit?",
#     ("Banana", "Strawberries", "Peaches"),
# )

# st.write("Your favorite fruit is:", option)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

pem_key = st.secrets["connections"]["snowflake"]["private_key"].strip().encode("utf-8")

private_key = serialization.load_pem_private_key(
    pem_key,
    password=None,
    backend=default_backend(),
)

private_key_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),
)

params = {
    "account": st.secrets["connections"]["snowflake"]["account"],
    "user": st.secrets["connections"]["snowflake"]["user"],
    "private_key": private_key_bytes,
    "role": st.secrets["connections"]["snowflake"]["role"],
    "warehouse": st.secrets["connections"]["snowflake"]["warehouse"],
    "database": st.secrets["connections"]["snowflake"]["database"],
    "schema": st.secrets["connections"]["snowflake"]["schema"],
}

session = Session.builder.configs(params).create()

# session = get_active_session()
# private_key = serialization.load_pem_private_key(
#     st.secrets["connections"]["snowflake"]["private_key"].encode(),
#     password=None,
# )

raise SystemExit

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_name'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen+ ' '

    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_string + """',
                            '""" + name_on_order + """')"""
    # st.write(my_insert_stmt)
    # st.stop()

# st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
# if ingredients_string:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")
