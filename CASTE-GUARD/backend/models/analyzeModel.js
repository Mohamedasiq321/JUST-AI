const mongoose = require('mongoose');

const analyzeSchema = new mongoose.Schema({
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
  },
  text: {
    type: String,
    required: true,
  },
  hateSpeechDetected: {
    type: Boolean,
    required: true,
  },
  reason: {
    type: String,
  },
  analyzedAt: {
    type: Date,
    default: Date.now,
  },
});

module.exports = mongoose.model('Analysis', analyzeSchema);
