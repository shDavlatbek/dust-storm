import asyncio
from datetime import datetime, timezone
import asyncpg
import json
from config import settings

# Database configuration
DATABASE_URL = settings.database_url_notasync

# Load JSON data
stations = json.load(open("data/stations.json"))

key_mapping = {
    "DATE": "date",
    "TAVG": "tavg",
    "TMIN": "tmin",
    "TMAX": "tmax",
    "HUMAVG": "havg",
    "HMIN": "hmin",
    "ETMIN": "etmin",
    "ETMAX": "etmax",
    "ETAVG": "etavg",
    "WINDAVG": "windavg",
    "WINDIMP": "windimp",
    "VISAVG": "visavg",
    "PRESAVG": "pavg",
    "PRESMIN": "pmin",
    "PRESMAX": "pmax",
    "POAVG": "poavg",
    "POMIN": "pomin",
    "POMAX": "pomax",
    "NIGHT": "night",
    "DAY": "day",
    "SUMMARY": "summary",
    "RAIN": "rain",
    "SNOW": "snow",
    "FOG": "fog",
    "DUSTSTORM": "duststorm"
}

async def insert_data():
    # Connect to the PostgreSQL database
    conn = await asyncpg.connect(DATABASE_URL)

    try:
        # Insert parameter data
        for station in stations:
            await conn.execute(
                '''
                INSERT INTO station (id, height, name, lon, lat, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                ON CONFLICT (id) DO NOTHING;
                ''',
                station["id"],
                station["height"],
                station["name"],
                station["lon"],
                station["lat"],
                datetime.now(),
                datetime.now()
            )
            with open(f"data/{station['name']}.json") as file:
                raw_parameters = json.load(file)
            for raw_parameter in raw_parameters:  # Iterate through the list
                parameter = {key_mapping[k]: v for k, v in raw_parameter.items() if k in key_mapping}

                # Insert parameter data
                await conn.execute(
                    '''
                    INSERT INTO parameter (
                        station, date, tavg, tmin, tmax, havg, hmin, etavg, etmin, etmax,
                        windavg, windimp, visavg, pavg, pmin, pmax, poavg, pomin, pomax,
                        night, day, summary, rain, snow, fog, duststorm
                    )
                    VALUES (
                        $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, 
                        $11, $12, $13, $14, $15, $16, $17, $18, $19,
                        $20, $21, $22, $23, $24, $25, $26
                    )
                    ''',
                    station["id"],
                    datetime.utcfromtimestamp(parameter["date"] / 1000),  # Convert milliseconds to seconds
                    parameter.get("tavg"),
                    parameter.get("tmin"),
                    parameter.get("tmax"),
                    parameter.get("havg"),
                    parameter.get("hmin"),
                    parameter.get("etavg"),
                    parameter.get("etmin"),
                    parameter.get("etmax"),   
                    parameter.get("windavg"),
                    parameter.get("windimp"),
                    parameter.get("visavg"),
                    parameter.get("pavg"),
                    parameter.get("pmin"),
                    parameter.get("pmax"),
                    parameter.get("poavg"),
                    parameter.get("pomin"),
                    parameter.get("pomax"),
                    parameter.get("night"),
                    parameter.get("day"),
                    parameter.get("summary"),
                    parameter.get("rain"),
                    parameter.get("snow"),
                    parameter.get("fog"),
                    parameter.get("duststorm")
                )

        
    finally:
        # Close the connection
        await conn.close()

# Run the script
asyncio.run(insert_data())