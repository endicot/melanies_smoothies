# Import python packages
import streamlit as st 
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)


# Decode base64 → PEM bytes
pem_bytes = base64.b64decode(st.secrets["connections"]["snowflake"]["private_key_b64"])

# Load PEM → private key object
private_key = serialization.load_pem_private_key(
    pem_bytes,
    password=None,
    backend=default_backend(),
)

# Convert to DER (what Snowflake expects)
der_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),
)

session = Session.builder.configs({
    "account": st.secrets["connections"]["snowflake"]["account"],
    "user": st.secrets["connections"]["snowflake"]["user"],
    "private_key": der_bytes,
    "role": st.secrets["connections"]["snowflake"]["role"],
    "warehouse": st.secrets["connections"]["snowflake"]["warehouse"],
    "database": st.secrets["connections"]["snowflake"]["database"],
    "schema": st.secrets["connections"]["snowflake"]["schema"],
}).create()


# cnx = st.connection("snowflake")
# session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_name'))


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