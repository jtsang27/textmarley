import React from 'react';
import { Navigation } from './components/Navigation';
import { Features } from './components/Features';
import { Footer } from './components/Footer';
import { PhoneForm } from './components/PhoneForm';

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-white">
      <Navigation />
      
      <main className="container mx-auto px-6 pt-16 pb-24">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Boost Your Productivity with AI-Powered Text Assistant
          </h1>
          <p className="text-xl text-gray-600 mb-12">
            TextMarley helps you stay focused and get more done with intelligent text-based productivity tools
          </p>

          <PhoneForm />
          <Features />
        </div>
      </main>

      <Footer />
    </div>
  );
}

export default App;