const mongoose = require('mongoose');

const PostSchema = new mongoose.Schema({
  userId:    { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  content:   { type: String, required: true },
  imageUrl:  { type: String },
}, { timestamps: true });

module.exports = mongoose.model('Post', PostSchema);
