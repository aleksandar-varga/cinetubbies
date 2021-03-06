import Axios from 'axios';

const PREFIX = 'auth/';
const ENDPOINTS = {
  LOGIN: 'login/',
  REGISTER: 'register/',
  CHANGE_PASSWORD: 'change-password/',
  LOGOUT: 'logout/',
  ME: 'me/',
  SET_PASSWORD: 'set-password/'
};

export default {
  register(data) {
    return Axios.post(PREFIX + ENDPOINTS.REGISTER, data);
  },

  login(data) {
    return Axios.post(PREFIX + ENDPOINTS.LOGIN, data);
  },

  changePassword(data) {
    return Axios.put(PREFIX + ENDPOINTS.CHANGE_PASSWORD, data);
  },

  logout() {
    return Axios.post(PREFIX + ENDPOINTS.LOGOUT);
  },

  fetchActiveUser() {
    return Axios.get(PREFIX + ENDPOINTS.ME);
  },

  setPassword(data) {
    return Axios.post(PREFIX + ENDPOINTS.SET_PASSWORD, data);
  }
};
