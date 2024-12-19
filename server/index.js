import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import twilio from 'twilio';

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

const twilioClient = twilio(
  process.env.TWILIO_ACCOUNT_SID,
  process.env.TWILIO_AUTH_TOKEN
);

app.post('/api/subscribe', async (req, res) => {
  try {
    const { phoneNumber } = req.body;
    
    // Send welcome message using Twilio
    await twilioClient.messages.create({
      body: 'Hello, my name is Marley! Welcome to TextMarley, your AI productivity assistant.',
      from: process.env.TWILIO_PHONE_NUMBER,
      to: `+1${phoneNumber}` // Assuming US numbers, adjust as needed
    });

    res.json({ success: true });
  } catch (error) {
    console.error('Error sending message:', error);
    res.status(500).json({ error: 'Failed to send message' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});