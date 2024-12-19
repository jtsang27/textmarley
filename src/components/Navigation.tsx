import React from 'react';
import { MessageSquareText } from 'lucide-react';

export const Navigation: React.FC = () => {
  return (
    <nav className="px-6 py-4">
      <div className="container mx-auto flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <MessageSquareText className="h-6 w-6 text-indigo-600" />
          <span className="text-xl font-bold text-gray-900">TextMarley</span>
        </div>
      </div>
    </nav>
  );
};