from flask import Flask, request, render_template, jsonify
import pandas as pd
import requests
import json

# Fetch all data of all pages
def fetch_all_pages(base_url, params):
    all_data = []  # List to store all records
    page = 1       # Start with the first page

    while True:
        # Update the page number in the parameters
        params['page'] = page
        response = requests.get(base_url, params=params)
        
        # Parse JSON and extract data
        data = response.json().get('data', [])
        
        if not data:  # If no data is returned, stop the loop
            break
        
        all_data.extend(data)  # Append current page's data to the list
        page += 1  # Increment page number for the next iteration

    # Convert the combined data into a DataFrame
    return pd.DataFrame(all_data)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/load_countries', methods=['GET'])
def loadCountriesDefault():
    try:
        response = requests.get('https://api.earthmeta.ai/api/countries')
        countries_data = response.json()
        countries_df = pd.DataFrame(countries_data)
        countries_df = countries_df[['name', 'president', 'rank', 'latitude', 'longitude']].fillna('N/A')
        countries_df['president_uid'] = countries_df['president'].str.get('uuid').fillna('N/A')
        countries_df['president'] = countries_df['president'].str.get('nickname').fillna('N/A')
        countries_df.columns = ['Country', 'President', 'Rank', 'latitude', 'longitude','President ID']
        return jsonify(countries_df.to_dict(orient='records'))
    except Exception as e:
        print(f"Error fetching countries: {e}")
        return jsonify({"error": "Unable to load countries"}), 500



@app.route('/load_cities', methods=['POST'])
def get_cities():
    user_id = request.form.get('user_id')
    base_url = 'https://api.earthmeta.ai/api/user/public/cities'
    params = {
        'uuid': user_id,
        'orderBy': 'Most_popular'
    }
    cities_df = fetch_all_pages(base_url, params)
    cities_df['country'] = cities_df['country'].str.get('name')
    cities_df = cities_df[['city_name', 'city_price', 'country','city_tier']]
    cities_df.columns = ['Name', 'Price (USD)', 'country', 'Tier']

    return jsonify(cities_df.to_dict(orient='records'))  # Convert DataFrame to JSON

@app.route('/load_lands', methods=['POST'])
def get_lands():
    user_id = request.form.get('user_id')
    base_url = 'https://api.earthmeta.ai/api/user/public/cities'
    params = {
        'uuid': user_id,
        'orderBy': 'Most_popular'
    }
    cities_df = fetch_all_pages(base_url, params)
   
    # Fetch cities data
    cities_df['country'] = cities_df['country'].str.get('name')
    cities_df = cities_df[['city_uuid', 'city_tier', 'country']].rename(columns={'city_tier': 'City Tier'})

    # Fetch lands data
    base_url = 'https://api.earthmeta.ai/api/user/public/lands'
    params = {
        'uuid': user_id,
        'orderBy': 'Most_popular'
    }
    lands_df = fetch_all_pages(base_url, params)

    if lands_df.empty:
        return jsonify({"error": "No lands found for this user."})

    # Convert lands data to a DataFrame
    lands_df['city_id'] = lands_df.city.str.get('uuid')
    lands_df = lands_df.merge(cities_df, left_on='city_id', right_on='city_uuid', how='left')
    
    lands_df['city'] = lands_df['city'].str.get('name')
    lands_df['category'] = lands_df['category'].str.get('title')
    lands_df['created_at'] = pd.to_datetime(lands_df['created_at']).dt.strftime('%Y-%m-%d\n%H:%M:%S')
    lands_df['on_sale'] = lands_df['on_sale'].astype(str).str.replace('1', 'Yes').str.replace('0', 'No')

    # Rename and reorder columns
    lands_df = lands_df.rename(
        columns={
            'name': 'Land Name',
            'area': 'Area',
            'price': 'Price (USD)',
            'on_sale': 'On Sale',
            'created_at': 'Created',
            'category': 'Category',
        }
    )
    lands_df = lands_df[['country', 'city', 'Land Name', 'Area', 'Price (USD)', 'On Sale', 'Created', 'Category']]

    # Convert to JSON and return
    return jsonify(lands_df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
