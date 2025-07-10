const mongoose = require('mongoose');

const postSchema = new mongoose.Schema({
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true,
  },
  content: { type: String },
  imageUrl: { type: String },
  result: { type: String, required: true }, // Hate / Not Hate
}, { timestamps: true });

module.exports = mongoose.model('Post', postSchema);