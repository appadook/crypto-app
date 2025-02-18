# Cryptocurrency Analytics App

## Overview
A real-time cryptocurrency analytics web application that fetches live prices of cryptocurrencies in various fiat currencies across multiple exchanges. The app calculates arbitrage opportunities in real-time and displays the results on a dynamic, user-friendly interface.

## Execution
start frontend first in a seperate terminal
```bash
cd frontend
npx expo start --ios
```

start backend in current terminal
- if you haven't already activated the virtual environment, activate it
```bash
cd backend
source venv/bin/activate
```

- start backend
```bash
cd backend
python start.py
```

---

## Tech Stack

### Frontend
- **React**: For building dynamic user interfaces.
- **Next.js**: For server-side rendering, static site generation, and optimized API routing.
- **Styling**: 
  - **Tailwind CSS**: Utility-first CSS framework.
  - Alternative: **Material-UI** for pre-designed, customizable UI components.
- **Hosting**: 
  - **Vercel**: For seamless deployment and automatic scaling.

### Backend
- **Framework**: 
  - **Flask**: Lightweight Python web framework for API routes and WebSocket management.
  - **Flask-SocketIO**: For real-time WebSocket communication.
- **Language**: Python
- **Hosting**:
  - **AWS Lambda**: Serverless compute for backend logic with automatic scaling.
  - Alternative: **DigitalOcean** for a traditional hosting approach.

### Data Source
- **API**: 
  - **CoinAPI**: Fetch live cryptocurrency prices and fiat exchange rates.
  - Integration: 
    - WebSocket for continuous real-time data streams.
    - REST API as a fallback or for auxiliary data.

---

## System Architecture

### Data Flow
1. **Frontend**:
   - Connects to the backend via REST API for initial data.
   - Listens to real-time updates from the backend via WebSocket.
   - Displays processed data, such as arbitrage opportunities, dynamically in the UI.

2. **Backend**:
   - Connects to **CoinAPI** via WebSocket to fetch live price data.
   - Processes the data to calculate arbitrage opportunities.
   - Sends the processed data to the frontend for display using WebSocket.

3. **API Integration**:
   - WebSocket connection to CoinAPI for live price updates.
   - REST API as a fallback for fetching static or one-time data.

---

## API Integration

### CoinAPI
- **Authentication**:
  - Use an API key to access CoinAPI.
  - Include the API key in the headers for all requests.

- **WebSocket Setup**:
  - **Endpoint**: `wss://ws.coinapi.io/v1/`
  - **Authentication**: Pass the API key during connection initialization.
  - **Data Received**: Real-time updates on cryptocurrency prices and exchange rates.

- **REST API Setup (Fallback)**:
  - **Base URL**: `https://rest.coinapi.io/v1/`
  - **Endpoints**:
    - `/exchangerate/{asset_id_base}/{asset_id_quote}`: Get the exchange rate between two assets.
    - `/assets`: Fetch a list of supported cryptocurrencies and fiat currencies.
  - **Headers**:
    ```json
    {
      "X-CoinAPI-Key": "YOUR_API_KEY"
    }
    ```

---

## Key Frameworks and Libraries

### Frontend
- React Native
- Expo
- Tailwind CSS or Material-UI

### Backend
- Flask
- Flask-SocketIO
- websocket-client (for WebSocket communication with CoinAPI)

