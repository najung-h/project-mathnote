/**
 * Main Page - 강의 정보 섹션
 */

interface LectureInfoProps {
  title?: string;
  description?: string;
  tags?: string[];
}

export function LectureInfo({
  title = '강의 정보',
  description = '이 강의는 선형대수학의 핵심인 고유값과 고유벡터의 기하학적 의미를 다룹니다. 진행 중 이해가 안 가는 부분은 SOS 버튼을 눌러주세요.',
  tags = ['Mathematics', 'Linear Algebra'],
}: LectureInfoProps) {
  return (
    <div className="bg-white rounded-2xl p-6 shadow-sm border border-slate-200">
      <h2 className="text-lg font-bold mb-4 flex items-center gap-2">
        <span className="w-2 h-6 bg-blue-600 rounded-full" />
        {title}
      </h2>
      
      <div className="flex gap-4">
        {tags.map((tag, index) => (
          <span
            key={index}
            className={`px-3 py-1 text-xs font-semibold rounded-md border ${
              index === 0
                ? 'bg-blue-50 text-blue-600 border-blue-100'
                : 'bg-slate-50 text-slate-600 border-slate-100'
            }`}
          >
            {tag}
          </span>
        ))}
      </div>
      
      <p className="mt-4 text-slate-600 text-sm leading-relaxed">
        {description}
      </p>
    </div>
  );
}
