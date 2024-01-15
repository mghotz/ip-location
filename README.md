## Project Overview
This repository contains a Python script for managing IP data using Redis. The script downloads, extracts, and processes an IP geolocation database, storing the processed data in a Redis database for efficient querying and retrieval.

## Key Features
- Downloads IP geolocation database
- Extracts data from compressed files
- Converts IP addresses to integer format for efficient storage
- Stores IP ranges and related data in Redis
- Provides functionality for flushing Redis database and performing range queries

## Prerequisites
To run this script, ensure you have the following installed:
- Python 3.x
- Redis server
- Required Python libraries: `redis`, `requests`, `dotenv`

## Installation
1. Clone the repository:
   ```
   git clone [repository URL]
   ```
2. Install required Python libraries:
   ```
   pip install redis requests python-dotenv
   ```

## Configuration
Create a `.env` file in the project root directory with the following structure:
```
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=4
REDIS_PASSWORD=[Your Redis Password]
```
Replace `[Your Redis Password]` with your actual Redis password.

## Usage
Run the script using Python:
```
python [script_name].py
```
Replace `[script_name]` with the name of the script file.

## How it Works
- The script initializes a Redis client with configuration from the `.env` file.
- It downloads the IP geolocation database and extracts the CSV data.
- The data is processed and stored in Redis in a structured format.
- It provides functions to add, query, and manage data within Redis.

## Contributing
Contributions to this project are welcome. Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature.
3. Commit your changes.
4. Push to the branch.
5. Open a pull request.

## License
This project is licensed under GNU GENERAL PUBLIC LICENSE. See the LICENSE file for more details.