import React from 'react';
import { WaitlistForm } from './WaitlistForm';

export function Hero() {
  return (
    <div className="relative overflow-hidden bg-white">
      <div className="mx-auto max-w-7xl px-6 py-24 sm:py-32 lg:px-8">
        <div className="text-center">
          <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
            Don't Worry, Text Happy
          </h1>
          <p className="mt-6 text-lg leading-8 text-gray-600">
            Let TextMarley handle your schedule. Send a text, and our AI assistant takes care of the rest—reminders, 
            scheduling, and calendar management made effortless.
          </p>
          <WaitlistForm />
        </div>
      </div>
    </div>
  );
}