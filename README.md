# Weather-Aware Delivery Delay Checker

An asynchronous Python pipeline that reads an order batch (`orders.json`), queries live weather conditions concurrently via the OpenWeatherMap API, and flags potential transit delays with personalized notification messages.

## Features

- **Concurrent API Fetching:** Uses `asyncio` and `aiohttp.ClientSession` to query weather data for all destinations simultaneously via `asyncio.gather`.
- **Fault Tolerance & Resilience:** Non-blocking error handling logs issues for invalid destinations (e.g., HTTP 404 for `InvalidCity123`) without breaking the processing pipeline.
- **Dynamic Apology Generation:** Automatically tags orders with a `Delayed` status and generates a personalized apology string when adverse conditions (`Rain`, `Snow`, `Extreme`) are detected.
- **Secure Configuration:** Decoupled credential management via `python-dotenv` and `.gitignore`.

## Tech Stack

- **Python 3.10+**
- **aiohttp** (Asynchronous HTTP client)
- **python-dotenv** (Environment variable management)
- **OpenWeatherMap API** (Current Weather Data)

## Project Structure

```text
weather-delivery-checker/
├── .gitignore
├── .env                  # Excluded from version control
├── requirements.txt
├── main.py
├── orders.json           # Order dataset (input and output)
├── AI_LOG.md             # AI engineering prompts log
└── README.md
