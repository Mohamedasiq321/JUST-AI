const express = require('express');
const router = express.Router();
const Post = require('../models/postModel');
const authMiddleware = require('../middleware/authMiddleware');

// Get all posts (admin view)
router.get('/', authMiddleware, async (req, res) => {
  const posts = await Post.find().populate('user', 'username email');
  res.json(posts);
});

// Get my posts only
router.get('/my', authMiddleware, async (req, res) => {
  const posts = await Post.find({ user: req.user.id });
  res.json(posts);
});
// Get all reports (for admin or general display)
router.get('/reports', async (req, res) => {
    try {
      const reports = await Post.find().populate('user', 'username email');
      res.json(reports);
    } catch (err) {
      res.status(500).json({ error: 'Error fetching reports' });
    }
  });
  
  // Get reports submitted by logged-in user
  router.get('/my-reports', authMiddleware, async (req, res) => {
    try {
      const reports = await Post.find({ user: req.user.id });
      res.json(reports);
    } catch (err) {
      res.status(500).json({ error: 'Error fetching your reports' });
    }
  });
  // Filter reports by keyword in content (optional)
router.get('/filter', async (req, res) => {
    try {
      const keyword = req.query.q || '';
      const results = await Post.find({ content: { $regex: keyword, $options: 'i' } });
      res.json(results);
    } catch (err) {
      res.status(500).json({ error: 'Filter failed' });
    }
  });
  
  // Delete a report by ID (basic delete, later we’ll limit to admin)
  router.delete('/delete/:id', async (req, res) => {
    try {
      const deleted = await Post.findByIdAndDelete(req.params.id);
      if (!deleted) return res.status(404).json({ error: 'Report not found' });
      res.json({ message: 'Deleted successfully' });
    } catch (err) {
      res.status(500).json({ error: 'Delete failed' });
    }
  });
  
  // Stats - Count of Hate vs Non-Hate
  router.get('/stats', async (req, res) => {
    try {
      const hate = await Post.countDocuments({ result: 'Hate Speech Detected' });
      const nonHate = await Post.countDocuments({ result: 'Clean' });
      res.json({ hate, nonHate });
    } catch (err) {
      res.status(500).json({ error: 'Stats error' });
    }
  });
  
module.exports = router;