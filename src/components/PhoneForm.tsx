import React, { useState } from 'react';
import { usePhoneSubmit } from '../hooks/usePhoneSubmit';

export const PhoneForm: React.FC = () => {
  const [phoneNumber, setPhoneNumber] = useState('');
  const { submitPhone, submitted, error } = usePhoneSubmit();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await submitPhone(phoneNumber);
    setPhoneNumber('');
  };

  return (
    <div className="max-w-md mx-auto bg-white rounded-xl shadow-lg p-6 mb-12">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-2">
            Get Early Access
          </label>
          <div className="flex gap-2">
            <input
              type="tel"
              id="phone"
              value={phoneNumber}
              onChange={(e) => setPhoneNumber(e.target.value)}
              placeholder="Enter your phone number"
              className="flex-1 rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
              pattern="[0-9]{10}"
              required
            />
            <button
              type="submit"
              className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
            >
              Join Waitlist
            </button>
          </div>
        </div>
        {submitted && (
          <p className="text-green-600 text-sm">Thanks! We'll text you soon.</p>
        )}
        {error && (
          <p className="text-red-600 text-sm">{error}</p>
        )}
      </form>
    </div>
  );
};