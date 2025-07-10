const mongoose = require('mongoose');

const analysisSchema = new mongoose.Schema({
  text: {
    type: String,
    required: true
  },
  hateSpeechDetected: {
    type: Boolean,
    required: true
  },
  reason: {
    type: String
  },
  user: {
    type: String, // You can use ObjectId later when user model is ready
    required: true
  },
  timestamp: {
    type: Date,
    default: Date.now
  }
});

module.exports = mongoose.model('Analysis', analysisSchema);
