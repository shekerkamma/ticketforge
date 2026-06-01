---
name: weather-fetcher-tokyo
description: Instructions for fetching current weather temperature data for Tokyo, Japan from Open-Meteo API
---

# Weather Fetcher Tokyo Skill

This skill provides instructions for fetching current weather data for Tokyo.

## Task

Fetch the current temperature for Tokyo, Japan in the requested unit (Celsius or Fahrenheit).

## Instructions

1. **Fetch Weather Data**: Use the available web tool or curl to get current weather data for Tokyo from the Open-Meteo API.

   For **Celsius**:
   - URL: `https://api.open-meteo.com/v1/forecast?latitude=35.6762&longitude=139.6503&current=temperature_2m&temperature_unit=celsius`

   For **Fahrenheit**:
   - URL: `https://api.open-meteo.com/v1/forecast?latitude=35.6762&longitude=139.6503&current=temperature_2m&temperature_unit=fahrenheit`

2. **Extract Temperature**: From the JSON response, extract the current temperature:
   - Field: `current.temperature_2m`
   - Unit label is in: `current_units.temperature_2m`

3. **Return Result**: Return the temperature value and unit clearly.

## Expected Output

After completing this skill's instructions:
```
Current Tokyo Temperature: [X]°[C/F]
Unit: [Celsius/Fahrenheit]
```

## Notes

- Only fetch the temperature, do not perform any transformations or write any files
- Open-Meteo is free, requires no API key, and uses coordinate-based lookups for reliability
- Tokyo coordinates: latitude 35.6762, longitude 139.6503
- Return the numeric temperature value and unit clearly
- Support both Celsius and Fahrenheit based on the caller's request
