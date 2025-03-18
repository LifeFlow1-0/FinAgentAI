import React, { useState } from 'react';
import { Box, Button, Container, LinearProgress, Typography, Paper } from '@mui/material';

interface Question {
  id: string;
  text: string;
  options: {
    value: 'a' | 'b' | 'c';
    text: string;
  }[];
}

const questions: Question[] = [
  {
    id: 'openness',
    text: 'How do you approach new experiences?',
    options: [
      { value: 'a', text: 'I prefer familiar routines and traditions' },
      { value: 'b', text: 'I enjoy a mix of familiar and new experiences' },
      { value: 'c', text: 'I actively seek out new and different experiences' }
    ]
  },
  {
    id: 'social_energy',
    text: 'How do you recharge your energy?',
    options: [
      { value: 'a', text: 'I prefer quiet time alone' },
      { value: 'b', text: 'I enjoy both social and alone time equally' },
      { value: 'c', text: 'I feel energized by being around others' }
    ]
  },
  {
    id: 'learning_style',
    text: 'How do you prefer to learn new things?',
    options: [
      { value: 'a', text: 'Through visual aids and reading' },
      { value: 'b', text: 'Through a combination of methods' },
      { value: 'c', text: 'Through hands-on practice and experience' }
    ]
  },
  {
    id: 'activity_intensity',
    text: 'What level of activity do you prefer in your daily life?',
    options: [
      { value: 'a', text: 'I prefer calm and relaxed activities' },
      { value: 'b', text: 'I enjoy a moderate level of activity' },
      { value: 'c', text: 'I thrive on high-energy and dynamic activities' }
    ]
  }
];

interface PersonalityQuestionnaireProps {
  userId: number;
  onComplete: () => void;
}

export const PersonalityQuestionnaire: React.FC<PersonalityQuestionnaireProps> = ({
  userId,
  onComplete
}) => {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState<Record<string, 'a' | 'b' | 'c'>>({});
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const progress = (currentQuestion / questions.length) * 100;

  const handleAnswer = (value: 'a' | 'b' | 'c') => {
    setAnswers(prev => ({
      ...prev,
      [questions[currentQuestion].id]: value
    }));

    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(prev => prev + 1);
    }
  };

  const handleSubmit = async () => {
    if (Object.keys(answers).length < questions.length) {
      setError('Please answer all questions before proceeding');
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      const response = await fetch('/api/v1/user-profile/personality', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          ...answers
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to save personality data');
      }

      onComplete();
    } catch (err) {
      setError('Something went wrong. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const question = questions[currentQuestion];

  return (
    <Container maxWidth="sm">
      <Box sx={{ my: 4 }}>
        <LinearProgress variant="determinate" value={progress} sx={{ mb: 4 }} />

        <Paper elevation={3} sx={{ p: 4 }}>
          <Typography variant="h5" component="h2" gutterBottom>
            {question.text}
          </Typography>

          <Box sx={{ mt: 3 }}>
            {question.options.map((option) => (
              <Button
                key={option.value}
                variant={answers[question.id] === option.value ? "contained" : "outlined"}
                color="primary"
                fullWidth
                sx={{ mb: 2 }}
                onClick={() => handleAnswer(option.value)}
              >
                {option.text}
              </Button>
            ))}
          </Box>

          {currentQuestion === questions.length - 1 && (
            <Box sx={{ mt: 4 }}>
              <Button
                variant="contained"
                color="primary"
                fullWidth
                onClick={handleSubmit}
                disabled={isSubmitting}
              >
                {isSubmitting ? 'Saving...' : 'Complete'}
              </Button>
            </Box>
          )}

          {error && (
            <Typography color="error" sx={{ mt: 2 }}>
              {error}
            </Typography>
          )}
        </Paper>
      </Box>
    </Container>
  );
}; 