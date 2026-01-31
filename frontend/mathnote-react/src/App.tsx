/**
 * 메인 App 컴포넌트
 */

import { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { WelcomePage, MainPage } from '@/pages';
import { ROUTES } from '@/constants';

function AppContent() {
  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
  const location = useLocation();

  // 페이지 전환 시 업로드 모달 열기 (Welcome -> Main 전환 시)
  useEffect(() => {
    if (location.state && (location.state as { openUploadModal?: boolean }).openUploadModal) {
      setIsUploadModalOpen(true);
      // state 초기화
      window.history.replaceState({}, document.title);
    }
  }, [location]);

  const handleOpenUploadModal = () => {
    setIsUploadModalOpen(true);
  };

  const handleCloseUploadModal = () => {
    setIsUploadModalOpen(false);
  };

  return (
    <Routes>
      <Route
        path={ROUTES.HOME}
        element={<Navigate to={ROUTES.WELCOME} replace />}
      />
      <Route
        path={ROUTES.WELCOME}
        element={<WelcomePage onOpenUploadModal={handleOpenUploadModal} />}
      />
      <Route
        path={ROUTES.MAIN}
        element={
          <MainPage
            isUploadModalOpen={isUploadModalOpen}
            onCloseUploadModal={handleCloseUploadModal}
            onOpenUploadModal={handleOpenUploadModal}
          />
        }
      />
    </Routes>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  );
}

export default App;
