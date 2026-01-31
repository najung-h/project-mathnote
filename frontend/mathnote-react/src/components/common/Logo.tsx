/**
 * 공통 UI 컴포넌트 - 로고
 */

import { APP_CONFIG } from '@/constants';

interface LogoProps {
  size?: 'sm' | 'md' | 'lg';
  showText?: boolean;
}

const sizeStyles = {
  sm: {
    icon: 'w-6 h-6 text-xs',
    text: 'text-lg',
  },
  md: {
    icon: 'w-8 h-8 text-sm',
    text: 'text-xl',
  },
  lg: {
    icon: 'w-10 h-10 text-xl',
    text: 'text-2xl',
  },
} as const;

export function Logo({ size = 'md', showText = true }: LogoProps) {
  const styles = sizeStyles[size];
  
  return (
    <div className="flex items-center gap-2">
      <div
        className={`
          ${styles.icon}
          bg-blue-600 rounded-xl flex items-center justify-center
          text-white font-black shadow-lg shadow-blue-200
        `}
      >
        M
      </div>
      {showText && (
        <span className={`${styles.text} font-black tracking-tighter italic`}>
          {APP_CONFIG.APP_NAME.replace('AI', '')}
          <span className="text-blue-600">AI</span>
        </span>
      )}
    </div>
  );
}
