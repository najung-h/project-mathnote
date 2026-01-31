/**
 * Welcome Page - Header
 */

import { Logo } from '@/components/common';
import { NAV_LINKS } from '@/constants';

interface WelcomeHeaderProps {
  onStartClick: () => void;
}

export function WelcomeHeader({ onStartClick }: WelcomeHeaderProps) {
  return (
    <header className="fixed top-0 w-full z-[100] bg-white/90 backdrop-blur-md border-b border-slate-100">
      <div className="max-w-7xl mx-auto px-8 h-20 flex items-center justify-between">
        <Logo size="lg" />
        
        <nav className="hidden lg:flex items-center gap-12 text-sm font-extrabold text-slate-500 uppercase tracking-widest">
          <a
            href={NAV_LINKS.WELCOME.PROBLEM}
            className="hover:text-blue-600 transition"
          >
            The Problem
          </a>
          <a
            href={NAV_LINKS.WELCOME.TECH}
            className="hover:text-blue-600 transition"
          >
            Parallel Engine
          </a>
          <a
            href={NAV_LINKS.WELCOME.OUTPUT}
            className="hover:text-blue-600 transition"
          >
            The Output
          </a>
          <button
            onClick={onStartClick}
            className="px-6 py-2.5 bg-slate-900 text-white rounded-full hover:bg-blue-600 transition shadow-xl shadow-slate-200"
          >
            Start MVP
          </button>
        </nav>
      </div>
    </header>
  );
}
