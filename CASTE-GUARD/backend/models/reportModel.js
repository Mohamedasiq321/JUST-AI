import mongoose from 'mongoose';

const reportSchema = new mongoose.Schema(
  {
    text: { type: String, required: true },
    reason: { type: String, required: true },
    email: { type: String },
  },
  { timestamps: true }
);

const Report = mongoose.model('Report', reportSchema);
export default Report;