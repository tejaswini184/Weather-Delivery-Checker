import os
import json
import logging
import asyncio
import aiohttp
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
DELAY_CONDITIONS = {"Rain", "Snow", "Extreme"}


def generate_weather_apology(customer: str, city: str, description: str) -> str:
    """Personalized delivery delay message."""
    desc = description.strip().lower()
    return (
        f"Hi {customer}, your order to {city} is delayed due to {desc}. "
        f"We appreciate your patience!"
    )


async def fetch_weather(session: aiohttp.ClientSession, city: str) -> dict | None:
    """Non-blocking fetch handling 404s gracefully without breaking the batch."""
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    try:
        async with session.get(BASE_URL, params=params, timeout=10) as resp:
            if resp.status == 200:
                return await resp.json()
            elif resp.status == 404:
                logger.warning("City not found: '%s' (Status 404)", city)
                return None
            else:
                logger.error("API error for '%s': Status %s", city, resp.status)
                return None
    except Exception as err:
        logger.error("Network or timeout exception for '%s': %s", city, err)
        return None


async def process_order(session: aiohttp.ClientSession, order: dict) -> dict:
    city = order.get("city")
    customer = order.get("customer")
    
    data = await fetch_weather(session, city)
    if not data:
        # Gracefully handle InvalidCity123: keeps script alive and logs the issue
        order["notes"] = f"Weather lookup failed for {city}"
        return order

    weather_entries = data.get("weather", [])
    if weather_entries:
        main_condition = weather_entries[0].get("main", "")
        description = weather_entries[0].get("description", main_condition)

        logger.info("Order %s (%s): %s (%s)", order["order_id"], city, main_condition, description)

        if main_condition in DELAY_CONDITIONS:
            order["status"] = "Delayed"
            order["apology_message"] = generate_weather_apology(customer, city, description)

    return order


async def main():
    if not API_KEY:
        raise ValueError("Missing OPENWEATHER_API_KEY in .env file.")

    with open("orders.json", "r", encoding="utf-8") as f:
        orders = json.load(f)

    # Parallel Fetching requirement: asyncio.gather triggers calls concurrently
    async with aiohttp.ClientSession() as session:
        tasks = [process_order(session, order) for order in orders]
        updated_orders = await asyncio.gather(*tasks)

    with open("orders.json", "w", encoding="utf-8") as f:
        json.dump(updated_orders, f, indent=2)

    logger.info("Finished processing all cities. Updated orders.json successfully.")


if __name__ == "__main__":
    asyncio.run(main())