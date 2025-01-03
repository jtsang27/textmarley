import React, { useState } from 'react';
import { MessageSquare, Calendar, Brain, Database, CheckCircle2 } from 'lucide-react';

function App() {
  const [phoneNumber, setPhoneNumber] = useState('');
  const [agreed, setAgreed] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (agreed && phoneNumber) {
      setSubmitted(true);
    }
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-blue-50 to-white">
        <div className="container mx-auto px-4 py-16">
          <div className="max-w-3xl mx-auto text-center">
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
              Meet TextMarley
            </h1>
            <p className="text-xl text-gray-600 mb-8">
              Your AI friend, coach, and personal assistant - all through text messages
            </p>
            
            {/* Phone Number Form */}
            <div className="bg-white p-6 rounded-xl shadow-lg max-w-md mx-auto">
              {submitted ? (
                <div className="flex flex-col items-center text-blue-600 space-y-2">
                  <CheckCircle2 className="w-12 h-12" />
                  <p className="text-lg font-medium">Thanks for joining!</p>
                </div>
              ) : (
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div>
                    <input
                      type="tel"
                      placeholder="Enter your phone number"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      value={phoneNumber}
                      onChange={(e) => setPhoneNumber(e.target.value)}
                      required
                    />
                  </div>
                  <div className="flex items-start space-x-2">
                    <input
                      type="checkbox"
                      id="agree"
                      className="mt-1"
                      checked={agreed}
                      onChange={(e) => setAgreed(e.target.checked)}
                      required
                    />
                    <label htmlFor="agree" className="text-sm text-gray-600 text-left">
                      I agree to receive text messages from TextMarley. Message and data rates may apply.
                    </label>
                  </div>
                  <button
                    type="submit"
                    className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition duration-200"
                    disabled={!agreed || !phoneNumber}
                  >
                    Get Started
                  </button>
                </form>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="container mx-auto px-4 py-16">
        <h2 className="text-3xl font-bold text-center mb-12">How Marley Helps You</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          <FeatureCard
            icon={<MessageSquare className="w-8 h-8 text-blue-600" />}
            title="Smart Conversations"
            description="Natural conversations that understand context and remember your preferences"
            imageUrl="https://images.unsplash.com/photo-1577563908411-5077b6dc7624?auto=format&fit=crop&w=400"
          />
          <FeatureCard
            icon={<Calendar className="w-8 h-8 text-blue-600" />}
            title="Schedule Management"
            description="Effortlessly manage your calendar and never miss important dates"
            imageUrl="https://images.unsplash.com/photo-1506784365847-bbad939e9335?auto=format&fit=crop&w=400"
          />
          <FeatureCard
            icon={<Brain className="w-8 h-8 text-blue-600" />}
            title="Personal Coach"
            description="Get motivation and guidance for your personal goals"
            imageUrl="https://images.unsplash.com/photo-1552674605-db6ffd4facb5?auto=format&fit=crop&w=400"
          />
          <FeatureCard
            icon={<Database className="w-8 h-8 text-blue-600" />}
            title="Smart Memory"
            description="Your personal knowledge base that grows with you"
            imageUrl="https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=400"
          />
        </div>
      </div>
    </div>
  );
}

interface FeatureCardProps {
  icon: React.ReactNode;
  title: string;
  description: string;
  imageUrl: string;
}

function FeatureCard({ icon, title, description, imageUrl }: FeatureCardProps) {
  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden transition-transform hover:scale-105">
      <div className="h-48 overflow-hidden">
        <img src={imageUrl} alt={title} className="w-full h-full object-cover" />
      </div>
      <div className="p-6">
        <div className="mb-4">{icon}</div>
        <h3 className="text-xl font-semibold mb-2">{title}</h3>
        <p className="text-gray-600">{description}</p>
      </div>
    </div>
  );
}

export default App;