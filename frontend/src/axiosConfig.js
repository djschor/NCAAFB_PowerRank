import axios from 'axios';

const instance = axios.create({
  baseURL: 'https://shrouded-shore-60391.herokuapp.com', // Replace with the URL of your proxy server
  withCredentials: true, // Optional: if you need to send cookies with your requests
  headers: {
    'Content-Type': 'application/json', // Optional: set default headers for all requests
  },
});

export default instance;
