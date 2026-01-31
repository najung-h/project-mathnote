/**
 * API 관련 상수 정의
 * 백엔드 FastAPI 서버와의 통신을 위한 설정값
 */

// 환경변수에서 API URL 가져오기 (기본값: localhost:8000)
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
export const API_PREFIX = '/api/v1';
export const STATIC_URL = `${API_BASE_URL}/static`;

// API 엔드포인트
export const API_ENDPOINTS = {
  // Health Check
  HEALTH: '/health',
  
  // Video API
  VIDEO: {
    FETCH_URL: `${API_PREFIX}/videos/fetch-url`,
    UPLOAD: `${API_PREFIX}/videos/upload`,
    PROCESS: (taskId: string) => `${API_PREFIX}/videos/${taskId}/process`,
    STATUS: (taskId: string) => `${API_PREFIX}/videos/${taskId}/status`,
  },
  
  // Note API
  NOTE: {
    GET: (taskId: string) => `${API_PREFIX}/notes/${taskId}`,
    DOWNLOAD: (taskId: string) => `${API_PREFIX}/notes/${taskId}/download`,
    NOTION: (taskId: string) => `${API_PREFIX}/notes/${taskId}/notion`,
  },
} as const;

// Task 상태
export const TASK_STATUS = {
  PENDING: 'pending',
  UPLOADED: 'uploaded',
  PROCESSING: 'processing',
  COMPLETED: 'completed',
  FAILED: 'failed',
} as const;

export type TaskStatus = typeof TASK_STATUS[keyof typeof TASK_STATUS];
