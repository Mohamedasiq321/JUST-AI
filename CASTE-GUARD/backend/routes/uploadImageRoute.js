// routes/uploadImageRoute.js
const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const ImageReport = require('../models/imageReportModel');
const analyzeImage = require('../ml/imageAnalyzer');

const router = express.Router();

// Configure Multer
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    const uploadPath = path.join(__dirname, '../uploads');
    if (!fs.existsSync(uploadPath)) fs.mkdirSync(uploadPath);
    cb(null, uploadPath);
  },
  filename: function (req, file, cb) {
    cb(null, Date.now() + '-' + Math.round(Math.random() * 1e9) + path.extname(file.originalname));
  },
});
const upload = multer({ storage });

// Route to handle image upload and save to DB
router.post('/upload', upload.single('image'), async (req, res) => {
  const filePath = req.file.path;
  const filename = req.file.filename;

  // Dummy analysis result (replace with model later)
  const result = analyzeImage(req.file.path);


  try {
    const report = new ImageReport({
      filename,
      path: filePath,
      result,
    });

    await report.save();

    res.status(200).json({ filename, path: filePath, result });
  } catch (err) {
    console.error('Error saving image report:', err);
    res.status(500).json({ error: 'Server error while saving image report' });
  }
});

// Route to fetch all image reports
router.get('/reports', async (req, res) => {
  try {
    const reports = await ImageReport.find().sort({ uploadedAt: -1 });
    res.json(reports);
  } catch (err) {
    res.status(500).json({ error: 'Failed to fetch image reports' });
  }
});
// Filter image reports by result (e.g., Hate or No Hate)
router.get('/filter', async (req, res) => {
    const query = req.query.q;
    try {
      const filtered = await ImageReport.find({ result: { $regex: query, $options: 'i' } });
      res.json(filtered);
    } catch (err) {
      res.status(500).json({ error: 'Filter error' });
    }
  });
  
  // Get image hate speech stats
  router.get('/stats', async (req, res) => {
    try {
      const hateCount = await ImageReport.countDocuments({ result: { $regex: 'Hate Speech Detected', $options: 'i' } });
      const nonHateCount = await ImageReport.countDocuments({ result: { $regex: 'No Hate', $options: 'i' } });
  
      res.json({ hate: hateCount, nonHate: nonHateCount });
    } catch (err) {
      res.status(500).json({ error: 'Stats error' });
    }
  });
  
module.exports = router;
