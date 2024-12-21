import React from 'react';
import { MessageSquareText } from 'lucide-react';

export function Header() {
  return (
    <header className="w-full py-6">
      <div className="container mx-auto px-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <MessageSquareText className="h-8 w-8 text-indigo-600" />
          <span className="text-xl font-bold">TextMarley</span>
        </div>
      </div>
    </header>
  );
}