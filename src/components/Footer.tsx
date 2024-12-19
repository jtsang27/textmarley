import React from 'react';
import { PhoneCall } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-50 py-8">
      <div className="container mx-auto px-6 text-center text-gray-600">
        <div className="flex items-center justify-center space-x-2 mb-4">
          <PhoneCall className="h-4 w-4" />
          <span>Contact us: hello@textmarley.com</span>
        </div>
        <p>© 2024 TextMarley. All rights reserved.</p>
      </div>
    </footer>
  );
};