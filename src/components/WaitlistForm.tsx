import React, { useState } from 'react';
import { PhoneInput } from './PhoneInput';

export function WaitlistForm() {
  const [phone, setPhone] = useState('');
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus('loading');
    
    // Simulate API call
    setTimeout(() => {
      setStatus('success');
      setPhone('');
    }, 1000);
  };

  return (
    <div className="mt-10 flex flex-col items-center gap-4">
      <form onSubmit={handleSubmit} className="flex w-full max-w-md gap-x-4">
        <PhoneInput
          value={phone}
          onChange={setPhone}
          disabled={status === 'loading'}
          className="min-w-0 flex-auto"
        />
        <button
          type="submit"
          disabled={!phone || status === 'loading'}
          className="flex-none rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {status === 'loading' ? 'Joining...' : 'Join Waitlist'}
        </button>
      </form>
      {status === 'success' && (
        <p className="text-sm text-green-600">
          Thanks for joining! We'll text you when it's your turn.
        </p>
      )}
    </div>
  );
}