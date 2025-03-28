import os
import json
import requests
import csv
from dotenv import load_dotenv
from datetime import datetime, timedelta
from tabulate import tabulate

load_dotenv()
api_key = os.getenv('WEATHER_API_KEY')
base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

hanoi_districts = [
    "BaDinh", "HoanKiem", "TayHo", "LongBien", "CauGiay", "DongDa",
    "HaiBaTrung", "HoangMai", "ThanhXuan", "SonTay", "BaVi", "ChuongMy",
    "DanPhuong", "DongAnh", "GiaLam", "HoaiDuc", "MeLinh", "MyDuc",
    "PhuXuyen", "PhucTho", "QuocOai", "SocSon", "ThachThat", "ThanhOai",
    "ThanhTri", "ThuongTin", "UngHoa"
]

def fetch_weather_data(location='HoanKiem%20Hanoi', date='2025-01-01'):
    """
        Fetches hourly weather data for a specified location and date.

        :param location: A string representing the location (default: 'Hoan Kiem, Hanoi, Vietnam').
        :param date: A string representing the date for which weather data is requested.
        :return: A JSON object containing weather data if the request is successful,
                 otherwise, a dictionary with an error message.
    """
    request_url = f'{base_url}/{location}/{date}?key={api_key}&include=hours'
    response = requests.get(request_url)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to retrieve data. Status code: {response.status_code}"}


def extract_info(data: json):
    """
        Extracts key weather details from the API response, including datetime, location, precipitation, conditions, and icon.
        :param data: The JSON response from the weather API.
        :return: A list of dictionaries containing weather information for each hour.
    """
    weather_data = []
    for hour_data in data['days'][0]['hours']:
        weather_info = {
            'datetime':  f"{data['days'][0]['datetime']} {hour_data['datetime']}",
            'location': data.get('resolvedAddress', 'Unknown Location'),
            'precip': hour_data.get('precip', 'N/A'),
            'conditions': hour_data.get('conditions', 'N/A'),
            'icon': hour_data.get('icon', 'N/A'),
            'humidity': hour_data.get('humidity', 'N/A'),
            'wind speed': hour_data.get('wind speed', 'N/A')
            # Add other important info as needed
        }
        weather_data.append(weather_info)
    return weather_data


def show_data(data: list[dict]):
    """
       Displays weather data in a well-formatted table using tabulate.
    """
    if not data:
        print("No data available.")
        return

    print(tabulate(data, headers="keys", tablefmt="fancy_grid"))

def save_data_to_local(data: list[dict], date: str = '2025-01-01'):
    """
        Saves weather data to a local JSON file.

        :param data: A list of dictionaries containing weather details.
        :param date: The name of the file to save the data (default is 'weather_data.json').
    """
    # Save data to file json
    filename = f"weather_data_{date}.json"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving data to json: {e}")

    # Save data to file csv
    filename = f"weather_data_{date}.csv"
    try:
        fieldnames = data[0].keys() if data else []
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving data to csv: {e}")


def main():
    two_days_ago = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
    all_weather_data = []
    for district in hanoi_districts:
        data = fetch_weather_data(f'{district}%20Hanoi', two_days_ago)
        if data and 'error' not in data:
            extracted_data = extract_info(data)
            all_weather_data.extend(extracted_data)

    show_data(all_weather_data)
    save_data_to_local(all_weather_data, two_days_ago)


if __name__ == '__main__':
    main()





