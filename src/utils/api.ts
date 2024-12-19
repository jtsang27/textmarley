const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000';

export const submitPhoneNumber = async (phoneNumber: string) => {
  const response = await fetch(`${API_URL}/api/subscribe`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ phoneNumber }),
  });

  if (!response.ok) {
    throw new Error('Failed to submit phone number');
  }

  return response.json();
};