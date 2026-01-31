/**
 * Welcome Page - Tech 섹션
 */

export function TechSection() {
  return (
    <section id="tech" className="py-40 bg-white">
      <div className="max-w-7xl mx-auto px-8">
        {/* Header */}
        <div className="text-center mb-32">
          <span className="text-blue-600 font-black text-sm tracking-[0.3em] uppercase mb-4 block underline underline-offset-8">
            Technology Stack
          </span>
          <h2 className="text-5xl md:text-6xl font-black tracking-tighter">
            Dual-Track Parallel Engine
          </h2>
        </div>

        <div className="relative">
          {/* Center Line */}
          <div className="absolute left-1/2 top-0 bottom-0 w-1 parallel-line hidden lg:block -translate-x-1/2 rounded-full opacity-20" />

          <div className="grid lg:grid-cols-2 gap-16 lg:gap-32 relative">
            {/* Vision Pipeline */}
            <div className="space-y-12">
              <div className="flex items-center gap-4 justify-end lg:pr-4">
                <h3 className="text-3xl font-black text-blue-600 italic">
                  Vision Pipeline
                </h3>
                <div className="w-12 h-12 bg-blue-600 rounded-xl flex items-center justify-center text-white shadow-lg">
                  📸
                </div>
              </div>
              
              <div className="bg-slate-50 p-8 rounded-[2.5rem] border border-slate-100 hover:shadow-xl transition-all text-right">
                <p className="text-xs font-black text-blue-500 mb-2 uppercase tracking-widest">
                  Step 01. Scene Detection
                </p>
                <h4 className="text-xl font-bold mb-4 italic">
                  프레임 기반 슬라이드 탐지
                </h4>
                <p className="text-slate-500 text-sm leading-relaxed">
                  OpenCV를 사용하여 1fps 주기로 프레임을 추출, 화면의 시각적 유사도 변화를 감지해 '진짜 슬라이드'만 선별합니다.
                </p>
              </div>
              
              <div className="bg-slate-50 p-8 rounded-[2.5rem] border border-slate-100 hover:shadow-xl transition-all text-right">
                <p className="text-xs font-black text-blue-500 mb-2 uppercase tracking-widest">
                  Step 02. Mathematical OCR
                </p>
                <h4 className="text-xl font-bold mb-4 italic">
                  수식 LaTeX 변환
                </h4>
                <p className="text-slate-500 text-sm leading-relaxed">
                  이미지 속의 복잡한 수식을 구조적으로 파악하여 즉시 편집 가능한 LaTeX 코드로 디지털화합니다.
                </p>
              </div>
            </div>

            {/* Audio Pipeline */}
            <div className="space-y-12 lg:mt-24">
              <div className="flex items-center gap-4 lg:pl-4">
                <div className="w-12 h-12 bg-purple-600 rounded-xl flex items-center justify-center text-white shadow-lg">
                  🎙️
                </div>
                <h3 className="text-3xl font-black text-purple-600 italic">
                  Audio Pipeline
                </h3>
              </div>
              
              <div className="bg-slate-50 p-8 rounded-[2.5rem] border border-slate-100 hover:shadow-xl transition-all">
                <p className="text-xs font-black text-purple-500 mb-2 uppercase tracking-widest">
                  Step 01. Whisper STT
                </p>
                <h4 className="text-xl font-bold mb-4 italic">
                  고정밀 음성 텍스트화
                </h4>
                <p className="text-slate-500 text-sm leading-relaxed">
                  강사의 모든 설명을 Whisper AI를 통해 고정밀 텍스트로 변환하고 타임스탬프 정보를 부여합니다.
                </p>
              </div>
              
              <div className="bg-slate-50 p-8 rounded-[2.5rem] border border-slate-100 hover:shadow-xl transition-all">
                <p className="text-xs font-black text-purple-500 mb-2 uppercase tracking-widest">
                  Step 02. Context Fusion
                </p>
                <h4 className="text-xl font-bold mb-4 italic">
                  슬라이드 별 문맥 매핑
                </h4>
                <p className="text-slate-500 text-sm leading-relaxed">
                  Vision 데이터의 슬라이드 교체 시점과 오디오 스크립트를 결합하여, 각 슬라이드에 맞는 '해설 요약'을 자동 생성합니다.
                </p>
              </div>
            </div>
          </div>

          {/* Merge Section */}
          <div className="mt-32 relative text-center">
            <div className="inline-block p-10 bg-slate-900 rounded-[3rem] text-white shadow-2xl relative z-10 group hover:scale-105 transition-transform border border-slate-700">
              <div className="absolute -top-10 left-1/2 -translate-x-1/2 px-6 py-2 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full text-xs font-black uppercase tracking-widest">
                The Merge
              </div>
              <h4 className="text-2xl font-black mb-4">
                단권화 노트 자동 생성 완료
              </h4>
              <div className="flex justify-center gap-4 opacity-60">
                <span className="text-xs font-bold">PDF</span>
                <span className="text-xs font-bold">NOTION</span>
                <span className="text-xs font-bold">MARKDOWN</span>
              </div>
            </div>
            <div className="absolute inset-x-0 top-0 h-32 bg-blue-600/30 blur-[100px] -z-0" />
          </div>
        </div>
      </div>
    </section>
  );
}
