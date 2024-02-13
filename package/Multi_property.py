import openai
import asyncio
import pandas as pd
import os


openai.api_key = "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"
path = os.getcwd()
surrounding_area_data = pd.read_csv(f"{path}/cleaned_data.csv")
property_csv = pd.read_csv(f"{path}/demo.csv")

#reading text for prompt
with open("raw_text.txt", "r",  encoding='utf-8') as f:
    text = f.read()

# Function to make openai api request
async def gpt_call(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates property descriptions."},
            {"role": "user", "content": prompt}
        ]
    )
    return response["choices"][0]["message"]["content"]


async def analyzer(prompt):
    analyzed_response = await gpt_call(prompt)
    return analyzed_response

async def content_generation(property_data):
    if property_data == None:
        return "No Economic data available in csv"
    genrated_text = await gpt_call(property_data)
    return genrated_text

data = asyncio.run(analyzer(text))


# Looping through dataframe row
for property in property_csv.iterrows():
    county = str(property[1]["county"]).strip()
    state = str(property[1]["state"]).strip()
    city = str(property[1]["city"]).strip()
    zip_code = str(property[1]["zip_code"]).strip()

    print(f"{county}, {state}, {city}, {zip_code}")
    features = property[1]["features"]
    property_type = property[1]["property_type"]
    asking_price = property[1]["asking_price"]
    investment_type = property[1]["investment_type"]
    square_footage = property[1]["size of property"]
    gla = property[1]["gla"]
    commercial_type = property[1]["commercial_type"]


    try:
        # filtering Economic data
        filtered_data = surrounding_area_data[
            (surrounding_area_data['county'] == county) &
            (surrounding_area_data['state'] == state) &
            (surrounding_area_data['city'] == city) &
            (surrounding_area_data['zipcode'] == zip_code)
        ].head(1)


        sarrounded_are = f"""
        'Households Average Household Size': {filtered_data.iloc[:, 5].iloc[0]},
        'High School Graduate Percentage': {filtered_data.iloc[:, 6].iloc[0]}
        'Bachelor\'s Degree Percentage': {filtered_data.iloc[:, 7].iloc[0]}
        'In Labor Force Percentage': {filtered_data.iloc[:, 8].iloc[0]}
        'Civilian Labor Force Percentage': {filtered_data.iloc[:, 9].iloc[0]}
        'Unemployment Rate Percentage': {filtered_data.iloc[:, 10].iloc[0]}
        'Income $15,000 to $24,999 Percentage': {filtered_data.iloc[:, 11].iloc[0]}
        'Income $25,000 to $34,999 Percentage': {filtered_data.iloc[:, 12].iloc[0]}
        'Income $35,000 to $49,999 Percentage': {filtered_data.iloc[:, 13].iloc[0]}
        'Income $50,000 to $74,999 Percentage': {filtered_data.iloc[:, 14].iloc[0]}
        'Income $75,000 to $99,999 Percentage': {filtered_data.iloc[:, 15].iloc[0]}
        'Income $100,000 to $149,999 Percentage': {filtered_data.iloc[:, 16].iloc[0]}
        'Income $150,000 to $199,999 Percentage': {filtered_data.iloc[:, 17].iloc[0]}
        'Income $200,000 or more Percentage': {filtered_data.iloc[:, 18].iloc[0]}
        'Median Household Income': {filtered_data.iloc[:, 19].iloc[0]}
        'Total Population Male Percentage': {filtered_data.iloc[:, 20].iloc[0]}
        'Total Population Female Percentage': {filtered_data.iloc[:, 21].iloc[0]}
        'Population 20 to 24 Years Percentage': {filtered_data.iloc[:, 22].iloc[0]}
        'Population 25 to 34 Years Percentage': {filtered_data.iloc[:, 23].iloc[0]}
        'Population 35 to 44 Years Percentage': {filtered_data.iloc[:, 24].iloc[0]}
        'Population 45 to 54 Years Percentage': {filtered_data.iloc[:, 25].iloc[0]}
        'Population 55 to 59 Years Percentage': {filtered_data.iloc[:, 26].iloc[0]}
        'Population 60 to 64 Years Percentage': {filtered_data.iloc[:, 27].iloc[0]}
        'Population 65 to 74 Years Percentage': {filtered_data.iloc[:, 28].iloc[0]}
        'Population 75 to 84 Years Percentage': {filtered_data.iloc[:, 29].iloc[0]}
        'Population 85 Years and Over Percentage': {filtered_data.iloc[:, 30].iloc[0]}
    """
        #Prompt for content
        text_prompt = f"""Now take reference of analyzed data and write more than 100 lines of content like that for the property details given below:

        Property Type: {property_type},
        Asking Price: {asking_price},
        Investment Type: {investment_type},
        Size of Property (in square footage): {square_footage},
        GLA (Gross Leasable Area): {gla},
        Country: {county},
        City: {city},
        State: {state},
        Zip Code: {zip_code},
        Features: {features}, 
        commercial type : {commercial_type}

        and the details of the surrounding area are given below. Do not include these details in the content; just create content by considering these details in your mind. These details are for your reference so you can make an advertisement content by taking all these into account.

        {sarrounded_are}
        
        Keep in mind that content should be more realistic and attractive so the buyer gets attracted to buy or rent the property, and make everything in detail so the buyer gets no confusion."""  
    except:
        text_prompt = None
    # Generating Content
    content = asyncio.run(content_generation(text_prompt))

    filename = f"{str(city)},{str(state)},{str(county)},{str(zip_code)}.txt"

    # Writing content into file
    with open(filename, 'w') as file:
        file.write(content)