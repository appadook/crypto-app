# Backend Directory Structure Documentation

## Overview
This document provides a detailed explanation of the purpose and functionality of each directory and file within the backend application, helping you understand how they work together and how to modify the code in the future.

### Directory Structure

1. **[.env](cci:7://file:///Users/kurtik/Projects/crypto-app/backend/.env:0:0-0:0)**
   - Contains environment variables for the application, such as API keys and configuration settings. This file is crucial for managing sensitive information and should not be committed to version control.

2. **[README.md](cci:7://file:///Users/kurtik/Projects/crypto-app/backend/README.md:0:0-0:0)**
   - Documentation for the backend application, including an overview, setup instructions, and usage details. It serves as a guide for developers and users to understand how to interact with the application.

3. **`__pycache__/`**
   - Stores compiled Python files to improve performance by avoiding recompilation of unchanged modules. This directory is automatically created by Python and should not be modified manually.

4. **`app/`**
   - The main application codebase.
   - **`__init__.py`**: Initializes the `app` package, allowing it to be treated as a module. It can also contain initialization code for the package.
   - **`config/`**: Configuration files.
     - **`__init__.py`**: Initializes the `config` package. It can also load configuration settings.
   - **`external/`**: Modules for external services.
     - **`__init__.py`**: Initializes the `external` package.
     - **`price_display.py`**: Handles the display of price data, formatting it for user interfaces or API responses.
     - **`price_tracker.py`**: Implements the `PriceTracker` class to manage and retrieve cryptocurrency prices, including methods for updating and fetching the latest prices.
     - **`strategies/`**: WebSocket strategies for connecting to external APIs.
       - **`__init__.py`**: Initializes the `strategies` package.
       - **`base_strategy.py`**: Defines an abstract base class for WebSocket connection strategies, ensuring that all strategies implement required methods.
       - **`coinapi_strategy.py`**: Implements the CoinAPI WebSocket strategy, including methods for connecting to the API and processing incoming price updates.
     - **`websocket_client.py`**: Handles the WebSocket client logic for connecting to the price tracking service, managing the connection lifecycle and message handling.
   - **`processors/`**: Contains classes that process incoming data.
     - **`base_processor.py`**: Defines an abstract base class for data processors, requiring implementations to define methods for processing and retrieving data.
   - **`routes/`**: API routes for the application.
     - **`__init__.py`**: Initializes the `routes` package.
     - **`routes.py`**: Contains definitions for API endpoints, handling incoming requests and returning appropriate responses.
   - **`utils/`**: Contains utility functions and classes that provide common functionality used throughout the application.
   
5. **[requirements.txt](cci:7://file:///Users/kurtik/Projects/crypto-app/backend/requirements.txt:0:0-0:0)**
   - Lists the dependencies required for the backend application, specifying the packages and their versions needed to run the application.

6. **[run.py](cci:7://file:///Users/kurtik/Projects/crypto-app/backend/run.py:0:0-0:0)**
   - The main entry point for running the backend application. This script typically initializes the application and starts the server.

7. **[structure.md](cci:7://file:///Users/kurtik/Projects/crypto-app/backend/structure.md:0:0-0:0)**
   - Intended to document the structure of the backend application, providing insights into the organization and purpose of each component.

8. **`test/`**
   - Contains test files for functionality.
   - **`data_received.txt`**: Likely contains sample data for testing purposes, used to simulate incoming messages or data.
   - **`websocket_test.py`**: Tests the WebSocket connection and price handling logic, ensuring that the application can connect to external services and process incoming data correctly.

9. **`venv/`**
   - Contains the virtual environment for the Python application, isolating dependencies from the global Python installation and ensuring that the application runs with the correct package versions.