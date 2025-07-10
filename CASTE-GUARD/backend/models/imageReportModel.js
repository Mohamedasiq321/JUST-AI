// models/imageReportModel.js
const mongoose = require('mongoose');

const imageReportSchema = new mongoose.Schema({
  filename: String,
  path: String,
  result: String,
  uploadedAt: {
    type: Date,
    default: Date.now,
  },
});

module.exports = mongoose.model('ImageReport', imageReportSchema);
