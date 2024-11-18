import requests
import pygal
import lxml.etree as ET
import webbrowser
from datetime import datetime

api_key = '85JKE4L4NY64JYSU' 

def main():
    again = True
    while again:
        while True:
            symbol = input("Enter the stock symbol you are looking for: ")
            if validate_symbol(symbol):
                break
            else:
                print("Invalid symbol. Please enter 1-7 capitalized alphanumeric characters.")
        print("Chart Types")
        print("------------")
        print("1. Bar")
        print("2. Line\n")
        while True:
            try:
                chart = int(input("Enter the chart type you want (1, 2): "))
                if validate_chart_type(chart):
                    break
                else:
                    print("Please enter 1 or 2")
            except ValueError:
                print("Please enter a numeric value (1 or 2)")
        params = {
            'function': '',
            'symbol': symbol,
            'apikey': api_key,
            'outputsize': 'full'
        }
        print("Select the Time Series of the chart you want to Generate")
        print("--------------------------------------------------------")
        print("1. Intraday")
        print("2. Daily")
        print("3. Weekly")
        print("4. Monthly\n")
        time_series_map = {
            1: "TIME_SERIES_INTRADAY",
            2: "TIME_SERIES_DAILY",
            3: "TIME_SERIES_WEEKLY",
            4: "TIME_SERIES_MONTHLY"
        }
        while True:
            try:
                time_series_input = int(input("Enter the time series option (1, 2, 3, 4): "))
                if validate_time_series(time_series_input):
                    time_series = time_series_map[time_series_input]
                    params['function'] = time_series
                    if time_series_input == 1:
                        while True:
                            interval = input("Enter the interval (1min, 5min, 15min, 30min, 60min): ")
                            if interval in ["1min", "5min", "15min", "30min", "60min"]:
                                params['interval'] = interval
                                break
                            else:
                                print("invalid input")
                    break
                else:
                    print("Please enter a 1, 2, 3, or 4")
            except ValueError:
                print("Invalid input. Please enter a number (1, 2, 3, or 4).")
        if time_series_input != 1:
            while True:
                date_input= input("Enter the start Date (YYYY-MM-DD): ")
                try:
                    if validate_date(date_input):
                        start_date = datetime.strptime(date_input, "%Y-%m-%d")
                        break
                except ValueError:
                    print("Invalid input. Please use YYYY-MM-DD")
            while True:
                date_input = input("Enter the end Date (YYYY-MM-DD): ")
                try:
                    if(validate_date(date_input)):
                        end_date = datetime.strptime(date_input, "%Y-%m-%d")
                        if end_date > start_date:
                            break
                        else:
                            print("End date must be later than start date")
                    else:
                        raise ValueError
                except ValueError:
                    print("Invalid input. Please use YYYY-MM-DD")
        else:
            while True:
                date_input= input("Enter the start Date (YYYY-MM-DD HH:MM:SS): ")
                try:
                    start_date = datetime.strptime(date_input, "%Y-%m-%d %H:%M:%S")
                    break
                except ValueError:
                    print("Invalid input. Please use YYYY-MM-DD HH-MM-SS")
            while True:
                date_input = input("Enter the end Date (YYYY-MM-DD HH:MM:SS): ")
                try:
                    end_date = datetime.strptime(date_input, "%Y-%m-%d %H:%M:%S")
                    if end_date > start_date:
                        break
                    else:
                        print("End date must be later than start date")
                except ValueError:
                    print("Invalid input. Please use YYYY-MM-DD HH-MM-SS")
        url = 'https://www.alphavantage.co/query'

        response = requests.get(url, params=params)
        data = response.json()
        filtered_data = filter_data_by_date(data, start_date, end_date)
        create_chart(filtered_data, chart, symbol)
        while True:
            repeat = input("Would you like to perform another calculation? (y/n) ")
            if repeat.lower() == "y" or repeat.lower() == "yes":
                again = True
                break
            elif repeat.lower() == "n" or repeat.lower() == "no":
                again = False
                break
            else:
                print("Invalid input, please type y or n")

def validate_symbol(symbol):
    return symbol.isalpha() and symbol.isupper() and 1 <= len(symbol) <= 7

def validate_chart_type(chart_input):
    return chart_input in [1,2]

def validate_time_series(time_series_input):
    return time_series_input in [1, 2, 3, 4]

def validate_date(date_input):
    try:
        datetime.strptime(date_input, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def filter_data_by_date(data, start_date, end_date):
    time_series_data = None
    for key in data.keys():
        if 'Time Series' in key:
            time_series_data = data[key]
            break

    if time_series_data is None:
        print("No time series data found")
        return{}
    date = None
    filtered_data = {}
    for date_str, daily_data in time_series_data.items(): 
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except:
            date = datetime.strptime(date_str, "%Y-%m-%d")
        if start_date <= date <= end_date:
            filtered_data[date_str] = daily_data
    return filtered_data

def create_chart(data, chart_type, symbol):
    dates = sorted(data.keys())
    open_prices = [float(data[date]['1. open']) for date in dates]
    high_prices = [float(data[date]['2. high']) for date in dates]
    low_prices = [float(data[date]['3. low']) for date in dates]
    close_prices = [float(data[date]['4. close']) for date in dates]
    if chart_type == 1:
        chart = pygal.Bar(title = f'{symbol} Stock Prices', x_label_rotation = 20)
    else:
        chart = pygal.Line(tite=f'{symbol} Stock Proces', x_label_rotation = 20)
    chart.x_labels = dates
    chart.add('Open', open_prices)
    chart.add('High', high_prices)
    chart.add('Low', low_prices)
    chart.add('Close', close_prices)
    finished_chart = chart.render().decode('utf-8')
    html_content = f"""
    <html>
        <head>
            <title>{symbol} Stock Prices Chart</title>
        </head>
        <body>
            {finished_chart}
        </body>
    </html>
    """
    with open("chart.html", "w") as f:
        f.write(html_content)
    webbrowser.open("chart.html")

if __name__ == "__main__":
    main()