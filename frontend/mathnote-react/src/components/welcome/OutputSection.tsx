/**
 * Welcome Page - Output 섹션
 */

export function OutputSection() {
  return (
    <section id="output" className="py-40 bg-slate-50">
      <div className="max-w-7xl mx-auto px-8">
        <div className="grid lg:grid-cols-12 gap-16 items-center">
          {/* Left Content */}
          <div className="lg:col-span-5">
            <h2 className="text-5xl font-black mb-8 leading-tight italic tracking-tighter">
              "사용자가 누른 <span className="text-blue-600">SOS</span>,
              <br />
              AI가 마침표를 찍습니다."
            </h2>
            <p className="text-lg text-slate-600 leading-relaxed mb-10 font-medium">
              단순한 요약을 넘어, 사용자가 이해하지 못한 찰나의 순간을 포착합니다. 
              SOS 타임스탬프를 기준으로 해당 구간의 비전/오디오 데이터를 재학습하여 
              심층적인 보충 해설을 제공합니다.
            </p>
            <div className="p-6 bg-white rounded-2xl border border-blue-100 shadow-sm italic text-blue-600 font-bold">
              "이 부분은 고유값 분해의 기하학적 의미에 대한 설명입니다. 행렬 A를..."
            </div>
          </div>
          
          {/* Right Preview */}
          <div className="lg:col-span-7">
            <div className="bg-white rounded-[3rem] p-4 shadow-3xl border border-slate-200 transform rotate-2 hover:rotate-0 transition-transform duration-700">
              <div className="bg-slate-900 rounded-[2.5rem] p-8 aspect-[4/3] flex flex-col justify-between">
                <div className="flex justify-between items-center border-b border-slate-800 pb-6">
                  <span className="text-slate-400 text-sm font-bold">
                    Final Note Preview
                  </span>
                  <div className="flex gap-2">
                    <div className="w-3 h-3 rounded-full bg-slate-700" />
                    <div className="w-3 h-3 rounded-full bg-slate-700" />
                  </div>
                </div>
                <div className="space-y-6 flex-1 pt-8">
                  <div className="h-8 bg-slate-800 rounded-lg w-1/2" />
                  <div className="h-4 bg-slate-800 rounded-lg w-full" />
                  <div className="h-4 bg-slate-800 rounded-lg w-5/6" />
                  <div className="h-32 bg-blue-600/20 rounded-2xl border border-blue-500/30 flex items-center justify-center text-blue-400 font-black italic">
                    $\LaTeX$ RENDERED CONTENT
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
