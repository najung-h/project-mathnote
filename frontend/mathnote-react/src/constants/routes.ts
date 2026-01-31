/**
 * 라우트 경로 상수
 */

export const ROUTES = {
  HOME: '/',
  WELCOME: '/welcome',
  MAIN: '/main',
  NOTE: '/note/:taskId',
} as const;

// 라우트 경로 생성 헬퍼 함수
export const createNotePath = (taskId: string) => `/note/${taskId}`;
