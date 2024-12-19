import React from 'react';
import { Sparkles, Zap, Clock } from 'lucide-react';
import { FeatureCard } from './FeatureCard';

const features = [
  {
    icon: Sparkles,
    title: 'AI-Powered',
    description: 'Smart suggestions and automated task management'
  },
  {
    icon: Zap,
    title: 'Lightning Fast',
    description: 'Instant responses and quick task completion'
  },
  {
    icon: Clock,
    title: 'Time-Saving',
    description: 'Streamlined workflows and automated routines'
  }
];

export const Features: React.FC = () => {
  return (
    <div className="grid md:grid-cols-3 gap-8 mt-20">
      {features.map((feature, index) => (
        <FeatureCard key={index} {...feature} />
      ))}
    </div>
  );
};