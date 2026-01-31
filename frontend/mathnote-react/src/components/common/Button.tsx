/**
 * 공통 UI 컴포넌트 - 버튼
 */

import type { ButtonHTMLAttributes, ReactNode } from 'react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg' | 'xl';
  children: ReactNode;
  fullWidth?: boolean;
}

const variantStyles = {
  primary:
    'bg-blue-600 text-white hover:bg-blue-700 shadow-xl shadow-blue-200',
  secondary:
    'bg-slate-900 text-white hover:bg-blue-600 shadow-2xl',
  outline:
    'bg-white border-2 border-slate-200 text-slate-900 hover:bg-slate-50',
  ghost:
    'text-slate-600 hover:bg-slate-100',
} as const;

const sizeStyles = {
  sm: 'px-4 py-2 text-sm',
  md: 'px-5 py-2 text-sm',
  lg: 'px-8 py-4 text-lg',
  xl: 'px-12 py-6 text-xl',
} as const;

export function Button({
  variant = 'primary',
  size = 'md',
  children,
  fullWidth = false,
  className = '',
  ...props
}: ButtonProps) {
  return (
    <button
      className={`
        font-bold rounded-2xl transition-all duration-200
        ${variantStyles[variant]}
        ${sizeStyles[size]}
        ${fullWidth ? 'w-full' : ''}
        ${className}
      `}
      {...props}
    >
      {children}
    </button>
  );
}
