# AI Log - Development Prompts

### 1. Parallel Fetching Architecture
**Prompt:**
 "Write a Python script using `aiohttp` and `asyncio.gather` that reads an `orders.json` file and fetches weather data concurrently for multiple cities using the OpenWeatherMap API. The API key must be loaded securely from a `.env` file."

### 2. Fault Tolerance & Error Handling
**Prompt:**
 "How can I handle API lookup errors (such as 404 Not Found for invalid city names) in `aiohttp` so that `asyncio.gather` continues processing the rest of the batch without crashing the script?"

### 3. Weather-Aware Apology Logic
**Prompt:**
 "Write a Python function called `generate_weather_apology(customer, city, description)` that takes a weather description (e.g., 'light rain', 'moderate snow') and returns a personalized delay notice."