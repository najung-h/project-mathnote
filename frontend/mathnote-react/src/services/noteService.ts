/**
 * Note API 서비스
 */

import { apiClient } from './apiClient';
import { API_ENDPOINTS } from '@/constants';
import type { NoteResponse, NoteDownloadResponse } from '@/types';

export const noteService = {
  /**
   * 완료된 노트 데이터 조회
   */
  getNote: async (taskId: string): Promise<NoteResponse> => {
    const response = await apiClient.get<NoteResponse>(
      API_ENDPOINTS.NOTE.GET(taskId)
    );
    return response.data;
  },

  /**
   * 노트 다운로드 링크 생성
   */
  getDownloadLink: async (taskId: string): Promise<NoteDownloadResponse> => {
    const response = await apiClient.get<NoteDownloadResponse>(
      API_ENDPOINTS.NOTE.DOWNLOAD(taskId)
    );
    return response.data;
  },

  /**
   * 노션으로 노트 전송
   */
  syncToNotion: async (taskId: string): Promise<{ notion_page_url: string }> => {
    const response = await apiClient.post<{ notion_page_url: string }>(
      API_ENDPOINTS.NOTE.NOTION(taskId)
    );
    return response.data;
  },
};
