import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 51.5074,
	"longitude": -0.1278,
	"daily": ["uv_index_max", "temperature_2m_max", "temperature_2m_min", "wind_speed_10m_max", "wind_gusts_10m_max", "sunrise", "daylight_duration", "sunset", "sunshine_duration", "moonrise", "moonset", "showers_sum", "snowfall_sum"],
	"hourly": ["temperature_2m", "rain", "showers", "snowfall", "precipitation_probability", "precipitation", "visibility", "cloud_cover", "wind_speed_10m", "wind_direction_180m", "wind_gusts_10m", "temperature_80m", "soil_temperature_6cm", "soil_moisture_3_to_9cm", "uv_index", "is_day", "sunshine_duration", "freezing_level_height", "direct_radiation", "terrestrial_radiation", "direct_normal_irradiance", "temperature_100hPa", "dew_point_975hPa", "relative_humidity_500hPa", "cloud_cover_700hPa", "wind_speed_900hPa", "wind_direction_250hPa", "geopotential_height_950hPa"],
	"models": ["best_match", "ukmo_global_deterministic_10km"],
	"current": ["temperature_2m", "is_day", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m", "rain", "showers", "snowfall"],
	"minutely_15": ["temperature_2m", "visibility", "wind_gusts_10m", "precipitation", "lightning_potential", "is_day", "direct_radiation", "terrestrial_radiation", "rain", "snowfall", "sunshine_duration", "wind_speed_80m", "wind_direction_80m"],
	"timezone": "Europe/London",
	"forecast_days": 14,
	"wind_speed_unit": "mph",
	"past_minutely_15": 4,
}
responses = openmeteo.weather_api(url, params = params)

# Days without a moonrise or moonset return this value instead of a timestamp
missing_int64 = 9223372036854775807

# Process 1 location and 2 models
for response in responses:
	print(f"\nCoordinates: {abs(response.Latitude())}°{'S' if response.Latitude() < 0 else 'N'} {abs(response.Longitude())}°{'W' if response.Longitude() < 0 else 'E'}")
	print(f"Elevation: {response.Elevation()} m asl")
	print(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}")
	print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")
	print(f"Model Nº: {response.Model()}")
	
	# Process current data. The order of variables needs to be the same as requested.
	current = response.Current()
	current_temperature_2m = current.Variables(0).Value()
	current_is_day = current.Variables(1).Value()
	current_wind_speed_10m = current.Variables(2).Value()
	current_wind_direction_10m = current.Variables(3).Value()
	current_wind_gusts_10m = current.Variables(4).Value()
	current_rain = current.Variables(5).Value()
	current_showers = current.Variables(6).Value()
	current_snowfall = current.Variables(7).Value()
	
	print(f"\nCurrent time: {current.Time()}")
	print(f"Current temperature_2m: {current_temperature_2m}")
	print(f"Current is_day: {current_is_day}")
	print(f"Current wind_speed_10m: {current_wind_speed_10m}")
	print(f"Current wind_direction_10m: {current_wind_direction_10m}")
	print(f"Current wind_gusts_10m: {current_wind_gusts_10m}")
	print(f"Current rain: {current_rain}")
	print(f"Current showers: {current_showers}")
	print(f"Current snowfall: {current_snowfall}")
	
	# Process minutely_15 data. The order of variables needs to be the same as requested.
	minutely_15 = response.Minutely15()
	minutely_15_temperature_2m = minutely_15.Variables(0).ValuesAsNumpy()
	minutely_15_visibility = minutely_15.Variables(1).ValuesAsNumpy()
	minutely_15_wind_gusts_10m = minutely_15.Variables(2).ValuesAsNumpy()
	minutely_15_precipitation = minutely_15.Variables(3).ValuesAsNumpy()
	minutely_15_lightning_potential = minutely_15.Variables(4).ValuesAsNumpy()
	minutely_15_is_day = minutely_15.Variables(5).ValuesAsNumpy()
	minutely_15_direct_radiation = minutely_15.Variables(6).ValuesAsNumpy()
	minutely_15_terrestrial_radiation = minutely_15.Variables(7).ValuesAsNumpy()
	minutely_15_rain = minutely_15.Variables(8).ValuesAsNumpy()
	minutely_15_snowfall = minutely_15.Variables(9).ValuesAsNumpy()
	minutely_15_sunshine_duration = minutely_15.Variables(10).ValuesAsNumpy()
	minutely_15_wind_speed_80m = minutely_15.Variables(11).ValuesAsNumpy()
	minutely_15_wind_direction_80m = minutely_15.Variables(12).ValuesAsNumpy()
	
	minutely_15_data = {
		"date": pd.date_range(
			start = pd.to_datetime(minutely_15.Time(), unit = "s", utc = True),
			end =  pd.to_datetime(minutely_15.TimeEnd(), unit = "s", utc = True),
			freq = pd.Timedelta(seconds = minutely_15.Interval()),
			inclusive = "left"
		).tz_convert(response.Timezone().decode())
	}
	
	minutely_15_data["temperature_2m"] = minutely_15_temperature_2m
	minutely_15_data["visibility"] = minutely_15_visibility
	minutely_15_data["wind_gusts_10m"] = minutely_15_wind_gusts_10m
	minutely_15_data["precipitation"] = minutely_15_precipitation
	minutely_15_data["lightning_potential"] = minutely_15_lightning_potential
	minutely_15_data["is_day"] = minutely_15_is_day
	minutely_15_data["direct_radiation"] = minutely_15_direct_radiation
	minutely_15_data["terrestrial_radiation"] = minutely_15_terrestrial_radiation
	minutely_15_data["rain"] = minutely_15_rain
	minutely_15_data["snowfall"] = minutely_15_snowfall
	minutely_15_data["sunshine_duration"] = minutely_15_sunshine_duration
	minutely_15_data["wind_speed_80m"] = minutely_15_wind_speed_80m
	minutely_15_data["wind_direction_80m"] = minutely_15_wind_direction_80m
	
	minutely_15_dataframe = pd.DataFrame(data = minutely_15_data)
	print("\nMinutely15 data\n", minutely_15_dataframe)
	
	# Process hourly data. The order of variables needs to be the same as requested.
	hourly = response.Hourly()
	hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
	hourly_rain = hourly.Variables(1).ValuesAsNumpy()
	hourly_showers = hourly.Variables(2).ValuesAsNumpy()
	hourly_snowfall = hourly.Variables(3).ValuesAsNumpy()
	hourly_precipitation_probability = hourly.Variables(4).ValuesAsNumpy()
	hourly_precipitation = hourly.Variables(5).ValuesAsNumpy()
	hourly_visibility = hourly.Variables(6).ValuesAsNumpy()
	hourly_cloud_cover = hourly.Variables(7).ValuesAsNumpy()
	hourly_wind_speed_10m = hourly.Variables(8).ValuesAsNumpy()
	hourly_wind_direction_180m = hourly.Variables(9).ValuesAsNumpy()
	hourly_wind_gusts_10m = hourly.Variables(10).ValuesAsNumpy()
	hourly_temperature_80m = hourly.Variables(11).ValuesAsNumpy()
	hourly_soil_temperature_6cm = hourly.Variables(12).ValuesAsNumpy()
	hourly_soil_moisture_3_to_9cm = hourly.Variables(13).ValuesAsNumpy()
	hourly_uv_index = hourly.Variables(14).ValuesAsNumpy()
	hourly_is_day = hourly.Variables(15).ValuesAsNumpy()
	hourly_sunshine_duration = hourly.Variables(16).ValuesAsNumpy()
	hourly_freezing_level_height = hourly.Variables(17).ValuesAsNumpy()
	hourly_direct_radiation = hourly.Variables(18).ValuesAsNumpy()
	hourly_terrestrial_radiation = hourly.Variables(19).ValuesAsNumpy()
	hourly_direct_normal_irradiance = hourly.Variables(20).ValuesAsNumpy()
	hourly_temperature_100hPa = hourly.Variables(21).ValuesAsNumpy()
	hourly_dew_point_975hPa = hourly.Variables(22).ValuesAsNumpy()
	hourly_relative_humidity_500hPa = hourly.Variables(23).ValuesAsNumpy()
	hourly_cloud_cover_700hPa = hourly.Variables(24).ValuesAsNumpy()
	hourly_wind_speed_900hPa = hourly.Variables(25).ValuesAsNumpy()
	hourly_wind_direction_250hPa = hourly.Variables(26).ValuesAsNumpy()
	hourly_geopotential_height_950hPa = hourly.Variables(27).ValuesAsNumpy()
	
	hourly_data = {
		"date": pd.date_range(
			start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
			end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
			freq = pd.Timedelta(seconds = hourly.Interval()),
			inclusive = "left"
		).tz_convert(response.Timezone().decode())
	}
	
	hourly_data["temperature_2m"] = hourly_temperature_2m
	hourly_data["rain"] = hourly_rain
	hourly_data["showers"] = hourly_showers
	hourly_data["snowfall"] = hourly_snowfall
	hourly_data["precipitation_probability"] = hourly_precipitation_probability
	hourly_data["precipitation"] = hourly_precipitation
	hourly_data["visibility"] = hourly_visibility
	hourly_data["cloud_cover"] = hourly_cloud_cover
	hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
	hourly_data["wind_direction_180m"] = hourly_wind_direction_180m
	hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m
	hourly_data["temperature_80m"] = hourly_temperature_80m
	hourly_data["soil_temperature_6cm"] = hourly_soil_temperature_6cm
	hourly_data["soil_moisture_3_to_9cm"] = hourly_soil_moisture_3_to_9cm
	hourly_data["uv_index"] = hourly_uv_index
	hourly_data["is_day"] = hourly_is_day
	hourly_data["sunshine_duration"] = hourly_sunshine_duration
	hourly_data["freezing_level_height"] = hourly_freezing_level_height
	hourly_data["direct_radiation"] = hourly_direct_radiation
	hourly_data["terrestrial_radiation"] = hourly_terrestrial_radiation
	hourly_data["direct_normal_irradiance"] = hourly_direct_normal_irradiance
	hourly_data["temperature_100hPa"] = hourly_temperature_100hPa
	hourly_data["dew_point_975hPa"] = hourly_dew_point_975hPa
	hourly_data["relative_humidity_500hPa"] = hourly_relative_humidity_500hPa
	hourly_data["cloud_cover_700hPa"] = hourly_cloud_cover_700hPa
	hourly_data["wind_speed_900hPa"] = hourly_wind_speed_900hPa
	hourly_data["wind_direction_250hPa"] = hourly_wind_direction_250hPa
	hourly_data["geopotential_height_950hPa"] = hourly_geopotential_height_950hPa
	
	hourly_dataframe = pd.DataFrame(data = hourly_data)
	print("\nHourly data\n", hourly_dataframe)
	
	# Process daily data. The order of variables needs to be the same as requested.
	daily = response.Daily()
	daily_uv_index_max = daily.Variables(0).ValuesAsNumpy()
	daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
	daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
	daily_wind_speed_10m_max = daily.Variables(3).ValuesAsNumpy()
	daily_wind_gusts_10m_max = daily.Variables(4).ValuesAsNumpy()
	daily_sunrise = daily.Variables(5).ValuesInt64AsNumpy()
	daily_daylight_duration = daily.Variables(6).ValuesAsNumpy()
	daily_sunset = daily.Variables(7).ValuesInt64AsNumpy()
	daily_sunshine_duration = daily.Variables(8).ValuesAsNumpy()
	daily_moonrise = daily.Variables(9).ValuesInt64AsNumpy()
	daily_moonset = daily.Variables(10).ValuesInt64AsNumpy()
	daily_showers_sum = daily.Variables(11).ValuesAsNumpy()
	daily_snowfall_sum = daily.Variables(12).ValuesAsNumpy()
	
	daily_data = {
		"date": pd.date_range(
			start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
			end =  pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
			freq = pd.Timedelta(seconds = daily.Interval()),
			inclusive = "left"
		).tz_convert(response.Timezone().decode())
	}
	
	daily_data["uv_index_max"] = daily_uv_index_max
	daily_data["temperature_2m_max"] = daily_temperature_2m_max
	daily_data["temperature_2m_min"] = daily_temperature_2m_min
	daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
	daily_data["wind_gusts_10m_max"] = daily_wind_gusts_10m_max
	daily_data["sunrise"] = pd.to_datetime(daily_sunrise, unit = "s", utc = True).tz_convert(response.Timezone().decode())
	daily_data["daylight_duration"] = daily_daylight_duration
	daily_data["sunset"] = pd.to_datetime(daily_sunset, unit = "s", utc = True).tz_convert(response.Timezone().decode())
	daily_data["sunshine_duration"] = daily_sunshine_duration
	daily_moonrise = pd.Series(daily_moonrise).mask(daily_moonrise == missing_int64)
	daily_data["moonrise"] = pd.to_datetime(daily_moonrise, unit = "s", utc = True).dt.tz_convert(response.Timezone().decode())
	daily_moonset = pd.Series(daily_moonset).mask(daily_moonset == missing_int64)
	daily_data["moonset"] = pd.to_datetime(daily_moonset, unit = "s", utc = True).dt.tz_convert(response.Timezone().decode())
	daily_data["showers_sum"] = daily_showers_sum
	daily_data["snowfall_sum"] = daily_snowfall_sum
	
	daily_dataframe = pd.DataFrame(data = daily_data)
	print("\nDaily data\n", daily_dataframe)
	
