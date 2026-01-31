/**
 * Welcome Page - Hero 섹션
 */

import { Button } from '@/components/common';

interface HeroSectionProps {
  onStartClick: () => void;
}

export function HeroSection({ onStartClick }: HeroSectionProps) {
  return (
    <section className="relative pt-52 pb-32 hero-pattern">
      <div className="max-w-7xl mx-auto px-8 text-center">
        {/* Badge */}
        <div className="inline-block px-6 py-2 bg-blue-50 border border-blue-100 rounded-full mb-10 shadow-sm">
          <span className="text-sm font-black text-blue-600 uppercase tracking-[0.2em]">
            Next-Gen Learning Tech
          </span>
        </div>
        
        {/* Title */}
        <h1 className="text-6xl md:text-8xl font-black leading-tight mb-10 tracking-tighter">
          수업은 편하게 <span className="italic text-blue-600">귀</span>로 듣고,
          <br />
          필기는 <span className="gradient-text italic">AI</span>가 끝냅니다.
        </h1>
        
        {/* Description */}
        <p className="text-xl md:text-2xl text-slate-500 mb-16 max-w-3xl mx-auto leading-relaxed font-medium">
          강의 영상 속 수식과 음성을 실시간으로 매핑하여
          <br />
          <strong>단권화된 마크다운 노트</strong>를 자동 생성하는 AI 솔루션
        </p>
        
        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-6">
          <Button
            variant="primary"
            size="xl"
            onClick={onStartClick}
            className="hover:-translate-y-2"
          >
            지금 바로 체험하기
          </Button>
          <Button
            variant="outline"
            size="xl"
          >
            데모 플레이
          </Button>
        </div>
      </div>
    </section>
  );
}
