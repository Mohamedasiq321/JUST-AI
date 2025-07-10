const express = require('express');
const multer = require('multer');
const path = require('path');
const router = express.Router();

// Multer setup
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'uploads/');  // relative to root
  },
  filename: function (req, file, cb) {
    cb(null, Date.now() + '-' + file.originalname);
  }
});
const upload = multer({ storage: storage });

// Dummy AI checker (you’ll replace with real Python/ML integration later)
const dummyHateSpeechCheck = (text) => {
  return text.includes("caste") || text.includes("hate");
};

router.post('/', upload.single('file'), async (req, res) => {
  try {
    const file = req.file;
    const text = req.body.text;

    let result = {
      isHate: false,
      reason: ''
    };

    if (text) {
      result.isHate = dummyHateSpeechCheck(text);
      result.reason = result.isHate ? "Text flagged for caste-based reference" : "Clean";
    } else if (file) {
      // TODO: Later call Python AI image hate checker here
      result.isHate = file.originalname.toLowerCase().includes("hate");
      result.reason = result.isHate ? "Image file flagged based on name pattern" : "Clean";
    }

    // Save to DB (if using model, add here)
    // You can use mongoose model like FlaggedContent.create()

    return res.json({
      success: true,
      file: file?.filename,
      text: text || null,
      result
    });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ success: false, error: 'Moderation failed' });
  }
});

module.exports = router;