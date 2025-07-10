const mongoose = require('mongoose');

const analysisSchema = new mongoose.Schema({
  username: { type: String, required: true },
  text: { type: String },
  imagePath: { type: String },
  hateSpeechDetected: { type: Boolean, required: true },
  reason: { type: String, required: true }
}, { timestamps: true });

module.exports = mongoose.model('Analysis', analysisSchema);
