import express from 'express';
import Report from '../models/reportModel.js';

const router = express.Router();

router.post('/', async (req, res) => {
  try {
    const { text, reason, email } = req.body;

    if (!text || !reason) {
      return res.status(400).json({ message: 'Text and reason are required' });
    }

    const report = new Report({ text, reason, email });
    await report.save();

    res.status(201).json({ message: 'Report submitted successfully' });
  } catch (error) {
    console.error('Error saving report:', error.message);
    res.status(500).json({ message: 'Internal server error' });
  }
});

export default router;
