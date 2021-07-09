
# Redeam Availability CLI

This is a command-line tool that fetches a list of available dates and times for the given supplier and product from the Redeam Booking API.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements. Requires Python 3+.

```bash
pip install -r requirements.txt
```
## Config

Create .env file

```bash
touch .env
```
And add API Key and API Secrets:

```bash
API_KEY=**********
API_SECRET=***********
```

## Usage

When run, the CLI will return a list of availabilities from the Redeam Availability CLI.
 
As an example, here is a sample usage string for the CLI application: 

```bash
Usage: booking_api.py [OPTIONS]

Options:
  --sid UUID                    Supplier ID  [required]
  --pid UUID                    Product ID  [required]
  --start [%Y-%m-%dT%H:%M:%SZ]
  --end [%Y-%m-%dT%H:%M:%SZ]
```

Run on python under booking_api.py. Input requires the UUID of the Supplier, the UUID of the Product, a start date/time (optional), and an end date/time (optional). If either/both dates are left blank, results will include default to today as a start date/time and end 24 hours after the start date/time.

Here's an example of what that could look like:

```python
python booking_api.py --sid=fc49b925-6942-4df8-954b-ed7df10adf7e --pid=02f0c6cb-77ae-4fcc-8f4d-99bc0c3bee18 --start=2021-07-10T21:00:00Z --end=2021-07-15T21:00:00Z
```

## Help
Please refer to click's help feature for more information:
```bash
python booking_api.py --help
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)