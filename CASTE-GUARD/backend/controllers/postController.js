const Post = require('../models/postModel');

const analyzePost = async (req, res) => {
  const { content } = req.body;

  if (!content) return res.status(400).json({ message: 'Content is required' });

  // Dummy logic
  const result = content.toLowerCase().includes('caste') ? 'Hate Speech Detected' : 'No Hate Speech';

  // Save to DB
  const newPost = await Post.create({
    user: req.user.id,
    content,
    result,
  });

  res.json({
    content: newPost.content,
    result: newPost.result,
    id: newPost._id,
  });
};
