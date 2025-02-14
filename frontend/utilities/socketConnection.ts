// frontend/socketConnection.js
import { io } from 'socket.io-client';

// Replace with your backend URL/port (see [backend/run.py](backend/run.py))
const socket = io('http://11.23.7.104:5000', {
  transports: ['websocket']
});

// Connection handlers
socket.on('connect', () => {
  console.log('Connected to backend');
});

socket.on('disconnect', () => {
  console.log('Disconnected from backend');
});

// Listen to custom events (example from [backend/app/websocket/events.py](backend/app/websocket/events.py))
socket.on('client data', (data) => {
  console.log('Price update received:', data);
});

export default socket;