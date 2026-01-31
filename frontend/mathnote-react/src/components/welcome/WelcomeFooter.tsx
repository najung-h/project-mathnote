/**
 * Welcome Page - Footer
 */

import { Logo } from '@/components/common';

export function WelcomeFooter() {
  return (
    <footer className="py-16 border-t border-slate-100 bg-slate-50">
      <div className="max-w-7xl mx-auto px-8 flex flex-col md:flex-row justify-between items-center gap-8">
        <Logo size="sm" />
        
        <p className="text-slate-400 text-sm font-medium">
          © 2026 MathNote. Global Hackathon Project for Innovation.
        </p>
        
        <div className="flex gap-8 text-sm font-bold text-slate-400 uppercase tracking-widest">
          <a href="#" className="hover:text-blue-600 transition">
            Github
          </a>
          <a href="#" className="hover:text-blue-600 transition">
            Team
          </a>
        </div>
      </div>
    </footer>
  );
}
