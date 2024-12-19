import { useState } from 'react';
import { submitPhoneNumber } from '../utils/api';

export const usePhoneSubmit = () => {
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submitPhone = async (phoneNumber: string) => {
    try {
      await submitPhoneNumber(phoneNumber);
      setSubmitted(true);
      setError(null);
    } catch (err) {
      setError('Failed to submit phone number. Please try again.');
      setSubmitted(false);
    }
  };

  return { submitPhone, submitted, error };
};