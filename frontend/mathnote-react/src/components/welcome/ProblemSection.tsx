/**
 * Welcome Page - Problem 섹션
 */

export function ProblemSection() {
  return (
    <section id="problem" className="py-40 bg-slate-900 text-white relative overflow-hidden">
      {/* Background Effect */}
      <div className="absolute top-0 right-0 w-1/2 h-full bg-blue-600/10 blur-[120px]" />
      
      <div className="max-w-7xl mx-auto px-8 relative z-10">
        <div className="grid lg:grid-cols-2 gap-24 items-center">
          {/* Left Content */}
          <div>
            <h2 className="text-5xl md:text-6xl font-black mb-12 tracking-tight">
              필기는 더 이상
              <br />
              <span className="text-blue-500">학습</span>이 아닙니다.
            </h2>
            
            <div className="space-y-12">
              {/* Problem 1 */}
              <div className="flex gap-6">
                <div className="text-4xl">🤯</div>
                <div>
                  <h4 className="text-2xl font-bold mb-2 text-slate-100">
                    인지 부하의 한계
                  </h4>
                  <p className="text-slate-400 text-lg leading-relaxed">
                    수식과 도표를 옮겨 적는 단순 노동 때문에 교수님의 고차원적인 통찰(Insight)을 놓칩니다.
                  </p>
                </div>
              </div>
              
              {/* Problem 2 */}
              <div className="flex gap-6">
                <div className="text-4xl">⏳</div>
                <div>
                  <h4 className="text-2xl font-bold mb-2 text-slate-100">
                    파편화된 복습 시간
                  </h4>
                  <p className="text-slate-400 text-lg leading-relaxed">
                    특정 개념을 찾기 위해 영상을 10초씩 앞뒤로 돌려보는 비효율적인 시간이 학습 시간의 40%를 차지합니다.
                  </p>
                </div>
              </div>
            </div>
          </div>
          
          {/* Right Stats */}
          <div className="grid grid-cols-2 gap-4">
            <div className="h-64 bg-slate-800 rounded-3xl border border-slate-700 p-8 flex flex-col justify-end">
              <p className="text-4xl font-black text-blue-500 mb-2">82%</p>
              <p className="text-sm font-bold text-slate-400 leading-tight">
                학생들이 필기 때문에
                <br />
                설명을 놓친 경험이 있음
              </p>
            </div>
            <div className="h-64 bg-slate-800 rounded-3xl border border-slate-700 p-8 mt-12 flex flex-col justify-end">
              <p className="text-4xl font-black text-purple-500 mb-2">15분</p>
              <p className="text-sm font-bold text-slate-400 leading-tight">
                1시간 강의에서 필기 내용을
                <br />
                정리하는 데 걸리는 추가 시간
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
