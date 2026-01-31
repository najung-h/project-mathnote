/**
 * Welcome 페이지
 * 랜딩 페이지 - 정적 콘텐츠 + CTA 버튼으로 업로드 모달 열기
 */

import { useNavigate } from 'react-router-dom';
import {
  WelcomeHeader,
  HeroSection,
  ProblemSection,
  TechSection,
  OutputSection,
  CTASection,
  WelcomeFooter,
} from '@/components/welcome';
import { ROUTES } from '@/constants';

interface WelcomePageProps {
  onOpenUploadModal: () => void;
}

export function WelcomePage({ onOpenUploadModal }: WelcomePageProps) {
  const navigate = useNavigate();

  const handleStartClick = () => {
    // 메인 페이지로 이동하면서 업로드 모달 열기
    navigate(ROUTES.MAIN);
    onOpenUploadModal();
  };

  return (
    <div className="bg-white text-slate-900 overflow-x-hidden font-pretendard">
      <WelcomeHeader onStartClick={handleStartClick} />
      <HeroSection onStartClick={handleStartClick} />
      <ProblemSection />
      <TechSection />
      <OutputSection />
      <CTASection onStartClick={handleStartClick} />
      <WelcomeFooter />
    </div>
  );
}
