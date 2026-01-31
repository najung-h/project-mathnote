/**
 * Main 페이지
 * 강의 분석 및 노트 프리뷰 페이지
 */

import { useState } from 'react';
import { MainHeader, VideoPlayer, LectureInfo, NotePreview } from '@/components/main';
import { UploadModal } from '@/components/upload';

interface MainPageProps {
  isUploadModalOpen: boolean;
  onCloseUploadModal: () => void;
  onOpenUploadModal: () => void;
}

export function MainPage({
  isUploadModalOpen,
  onCloseUploadModal,
  onOpenUploadModal,
}: MainPageProps) {
  // SOS 타임스탬프 저장 (추후 API 연동 시 사용)
  const [sosTimestamps, setSosTimestamps] = useState<number[]>([]);

  const handleSosClick = (timestamp: number) => {
    setSosTimestamps((prev) => [...prev, timestamp]);
    // TODO: API 호출하여 SOS 해설 요청
    console.log('SOS clicked at:', timestamp, 'Total SOS:', sosTimestamps.length + 1);
  };

  const handleUploadSuccess = (taskId: string) => {
    console.log('Upload success, task ID:', taskId);
    // TODO: 상태 폴링 시작 또는 노트 페이지로 이동
  };

  return (
    <div className="bg-slate-50 text-slate-900 min-h-screen font-inter">
      <MainHeader onUploadClick={onOpenUploadModal} />

      <main className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-12 gap-8">
          {/* Left Column - Video & Info */}
          <div className="col-span-12 lg:col-span-7 space-y-6">
            <VideoPlayer onSosClick={handleSosClick} />
            <LectureInfo />
          </div>

          {/* Right Column - Note Preview */}
          <div className="col-span-12 lg:col-span-5">
            <NotePreview />
          </div>
        </div>
      </main>

      {/* Upload Modal */}
      <UploadModal
        isOpen={isUploadModalOpen}
        onClose={onCloseUploadModal}
        onUploadSuccess={handleUploadSuccess}
      />
    </div>
  );
}
