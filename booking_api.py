from datetime import datetime, timedelta
import requests
import click
from dotenv import load_dotenv
import os

load_dotenv()

base_booking_url = 'https://booking.sandbox.redeam.io/v1.2'

@click.command()
@click.option('--sid', required=True, type=click.UUID, help='Supplier ID')
@click.option('--pid', required=True, type=click.UUID, help='Product ID')
@click.option('--start', default='now', type=click.DateTime(formats=['%Y-%m-%dT%H:%M:%SZ']))
@click.option('--end', default='day', type=click.DateTime(formats=['%Y-%m-%dT%H:%M:%SZ']))

def get_availability(sid, pid, start, end):

    if start != 'now':
        start = start.strftime('%Y-%m-%dT%H:%M:%SZ')

    if end != 'day':
        end = end.strftime('%Y-%m-%dT%H:%M:%SZ')

    # if start and end are default, convert to time strings
    if start == 'now' and end == 'day':
        start = datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
        end = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
    
    # if start is provided but end is default
    if start != 'now' and end == 'day':
        end = (datetime.fromisoformat(start[:-1]) + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
    
    # if start isnt provided but end is
    if start == 'now' and end != 'day':
        start = datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')

    url = f'{base_booking_url}/suppliers/{sid}/products/{pid}/availabilities'
    
    headers = {
        'X-API-Key': f'{os.getenv("API_KEY")}',
        'X-API-Secret': f'{os.getenv("API_SECRET")}'
    }

    querystring = {
        'end': f'{end}',
        'start': f'{start}'
    }
    
    # get availablities
    response = requests.request('GET', url, headers=headers, params=querystring)
    response_json = response.json()

    # turn byRate object into array we can iterate
    rates_array = response_json['availabilities']['byRate'].items()

    # get supplier metadata
    supplier_url = f'{base_booking_url}/suppliers/{sid}'
    response_supplier = requests.request("GET", supplier_url, headers=headers)
    response_supplier_json = response_supplier.json()

    supplier_name = response_supplier_json['supplier']['name']

    # get product metadata
    product_url = f'{base_booking_url}/suppliers/{sid}/products/{pid}'
    response_product = requests.request("GET", product_url, headers=headers)
    response_product_json = response_product.json()

    product_name = response_product_json['product']['name']

    click.echo(f'Fetching availabilities for {supplier_name}, {product_name}...')

    # iterate through all rates
    for rate in rates_array:
        # setting rate_id variable to the first value in array
        rate_id = rate[0]

        # setting url to rates API endpoint
        rates_url = f'{base_booking_url}/suppliers/{sid}/products/{pid}/rates/{rate_id}'

        # get rate data
        response_rate = requests.request('GET', rates_url, headers=headers)
        response_rate_json = response_rate.json()

        # pulling attraction name from rates API endpoint
        name = response_rate_json['rate']['name']

        # get availabilities
        availability_array = rate[1]['availability']
        
        # iterate availability_array
        for items in availability_array:

            # remove Z in iso string because python datetime cant process it
            stripped_start_string = items["start"][:-1]
            stripped_end_string = items["end"][:-1]

            # convert date strings to datetimes
            start_time_object = datetime.fromisoformat(stripped_start_string)
            end_time_object = datetime.fromisoformat(stripped_end_string)

            # format datetimes
            formatted_start = start_time_object.strftime('%m/%d/%Y %I:%M%p')
            formatted_end = end_time_object.strftime('%m/%d/%Y %I:%M%p')
            
            # final output
            click.echo(f'{name}, {formatted_start} - {formatted_end}, Capacity: {items["capacity"]}')
        click.echo('-------------------------')

if __name__ == '__main__':
    get_availability()