// backend/ml/imageAnalyzer.js

const fs = require('fs');
const path = require('path');

// Dummy image analysis logic
function analyzeImage(filePath) {
  const fileName = path.basename(filePath).toLowerCase();

  // Fake logic: if image name has "hate", flag it
  if (fileName.includes('hate')) {
    return 'Hate Speech Detected in Image';
  }

  return 'No Hate Speech Detected in Image';
}

module.exports = analyzeImage;
