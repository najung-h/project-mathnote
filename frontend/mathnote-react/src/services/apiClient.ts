/**
 * Axios 인스턴스 설정
 */

import axios from 'axios';
import { API_BASE_URL } from '@/constants';

// Axios 인스턴스 생성
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request 인터셉터
apiClient.interceptors.request.use(
  (config) => {
    // 요청 전 처리 (예: 토큰 추가)
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response 인터셉터
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // 에러 처리
    if (error.response) {
      console.error('API Error:', error.response.data);
    } else if (error.request) {
      console.error('Network Error:', error.message);
    }
    return Promise.reject(error);
  }
);
