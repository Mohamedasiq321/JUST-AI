const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');
const Content = require('../models/contentModel');

const moderateContent = async (req, res) => {
  try {
    const file = req.file;
    const text = req.body.text;

    let contentType, contentPathOrText;

    if (file) {
      contentType = file.mimetype.startsWith('image') ? 'image' : 'unknown';
      contentPathOrText = path.join(__dirname, '../../uploads/', file.filename);
    } else if (text) {
      contentType = 'text';
      contentPathOrText = text;
    } else {
      return res.status(400).json({ error: 'No content provided' });
    }

    // Path to your dummy AI script
    const pythonScript = path.join(__dirname, '../../social_platform_clean/dummy_moderation.py');

    const pythonProcess = spawn('python', [pythonScript, contentType, contentPathOrText]);

    let result = '';

    pythonProcess.stdout.on('data', (data) => {
      result += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error('Python stderr:', data.toString());
    });

    pythonProcess.on('close', async (code) => {
      try {
        const parsed = JSON.parse(result);

        const newContent = new Content({
          content: file ? file.filename : text,
          type: parsed.type,
          isHate: parsed.isHate,
          confidence: parsed.confidence,
          timestamp: new Date()
        });

        await newContent.save();

        res.json({ message: 'Content moderated', result: parsed });
      } catch (error) {
        console.error('Error parsing Python output:', error);
        res.status(500).json({ error: 'Failed to process content' });
      }
    });

  } catch (error) {
    console.error('Moderation error:', error);
    res.status(500).json({ error: 'Server error' });
  }
};

module.exports = {
  moderateContent
};
