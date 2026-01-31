/**
 * Main Page - 비디오 플레이어 섹션
 */

interface VideoPlayerProps {
  title?: string;
  onSosClick?: (timestamp: number) => void;
}

export function VideoPlayer({ 
  title = '위상수학 제 3강 - 연속 사상의 이해',
  onSosClick 
}: VideoPlayerProps) {
  const handleSosClick = () => {
    // 현재 비디오 타임스탬프를 전달 (추후 실제 비디오 시간으로 대체)
    const currentTimestamp = 0;
    onSosClick?.(currentTimestamp);
  };

  return (
    <div className="relative aspect-video bg-black rounded-2xl overflow-hidden shadow-2xl border-4 border-white">
      {/* Video Placeholder */}
      <div className="absolute inset-0 flex flex-col items-center justify-center text-white bg-gradient-to-t from-black/60 to-transparent">
        {/* Play Button */}
        <div className="w-20 h-20 bg-white/20 rounded-full flex items-center justify-center backdrop-blur-md mb-4 cursor-pointer hover:scale-110 transition">
          <div className="w-0 h-0 border-t-[15px] border-t-transparent border-l-[25px] border-l-white border-b-[15px] border-b-transparent ml-2" />
        </div>
        <p className="text-sm opacity-80">{title}</p>
      </div>
      
      {/* SOS Button */}
      <button
        onClick={handleSosClick}
        className="absolute bottom-6 right-6 bg-red-500 hover:bg-red-600 text-white px-6 py-3 rounded-full font-bold shadow-lg flex items-center gap-2 transform active:scale-95 transition"
      >
        <span className="text-xl">🤯</span>
        <span>잘 모르겠어요! (SOS)</span>
      </button>
    </div>
  );
}
