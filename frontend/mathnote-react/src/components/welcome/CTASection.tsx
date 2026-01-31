/**
 * Welcome Page - CTA 섹션
 */

import { Button } from '@/components/common';

interface CTASectionProps {
  onStartClick: () => void;
}

export function CTASection({ onStartClick }: CTASectionProps) {
  return (
    <section id="experience" className="py-40 bg-white hero-pattern">
      <div className="max-w-4xl mx-auto px-8 text-center">
        <h2 className="text-6xl font-black mb-10 tracking-tighter">
          혁신적인 학습의
          <br />
          <span className="gradient-text">첫 프레임</span>을 만드세요.
        </h2>
        <p className="text-xl text-slate-500 mb-16 font-medium leading-relaxed">
          지금 바로 강의 영상을 업로드하고, AI가 만드는
          <br />
          단권화 노트를 무료로 확인해보세요.
        </p>
        <Button
          variant="secondary"
          size="xl"
          onClick={onStartClick}
          className="hover:-translate-y-2"
        >
          무료로 분석 시작하기
        </Button>
        <p className="mt-10 text-slate-400 text-sm font-bold uppercase tracking-widest italic">
          ※ MVP VERSION 1.0.0 AVAILABLE
        </p>
      </div>
    </section>
  );
}
