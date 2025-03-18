import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { PersonalityQuestionnaire } from '../PersonalityQuestionnaire';

// Mock fetch
global.fetch = jest.fn();

describe('PersonalityQuestionnaire', () => {
  const mockOnComplete = jest.fn();
  const defaultProps = {
    userId: 1,
    onComplete: mockOnComplete,
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders the first question initially', () => {
    render(<PersonalityQuestionnaire {...defaultProps} />);
    
    expect(screen.getByText('How do you approach new experiences?')).toBeInTheDocument();
    expect(screen.getByText('I prefer familiar routines and traditions')).toBeInTheDocument();
  });

  it('shows progress bar at 0% initially', () => {
    render(<PersonalityQuestionnaire {...defaultProps} />);
    
    const progressBar = screen.getByRole('progressbar');
    expect(progressBar).toHaveAttribute('aria-valuenow', '0');
  });

  it('advances to next question when an option is selected', () => {
    render(<PersonalityQuestionnaire {...defaultProps} />);
    
    fireEvent.click(screen.getByText('I prefer familiar routines and traditions'));
    
    expect(screen.getByText('How do you recharge your energy?')).toBeInTheDocument();
  });

  it('updates progress bar when advancing questions', () => {
    render(<PersonalityQuestionnaire {...defaultProps} />);
    
    fireEvent.click(screen.getByText('I prefer familiar routines and traditions'));
    
    const progressBar = screen.getByRole('progressbar');
    expect(progressBar).toHaveAttribute('aria-valuenow', '25');
  });

  it('shows submit button on last question', () => {
    render(<PersonalityQuestionnaire {...defaultProps} />);
    
    // Answer all questions
    fireEvent.click(screen.getByText('I prefer familiar routines and traditions'));
    fireEvent.click(screen.getByText('I prefer quiet time alone'));
    fireEvent.click(screen.getByText('Through visual aids and reading'));
    
    expect(screen.getByText('Complete')).toBeInTheDocument();
  });

  it('submits data successfully', async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ id: 1 }),
    });

    render(<PersonalityQuestionnaire {...defaultProps} />);
    
    // Answer all questions
    fireEvent.click(screen.getByText('I prefer familiar routines and traditions'));
    fireEvent.click(screen.getByText('I prefer quiet time alone'));
    fireEvent.click(screen.getByText('Through visual aids and reading'));
    fireEvent.click(screen.getByText('I prefer calm and relaxed activities'));
    
    fireEvent.click(screen.getByText('Complete'));
    
    await waitFor(() => {
      expect(mockOnComplete).toHaveBeenCalled();
    });
  });

  it('shows error message on submission failure', async () => {
    (global.fetch as jest.Mock).mockRejectedValueOnce(new Error('Failed'));

    render(<PersonalityQuestionnaire {...defaultProps} />);
    
    // Answer all questions
    fireEvent.click(screen.getByText('I prefer familiar routines and traditions'));
    fireEvent.click(screen.getByText('I prefer quiet time alone'));
    fireEvent.click(screen.getByText('Through visual aids and reading'));
    fireEvent.click(screen.getByText('I prefer calm and relaxed activities'));
    
    fireEvent.click(screen.getByText('Complete'));
    
    await waitFor(() => {
      expect(screen.getByText('Something went wrong. Please try again.')).toBeInTheDocument();
    });
  });

  it('prevents submission if not all questions are answered', async () => {
    render(<PersonalityQuestionnaire {...defaultProps} />);
    
    // Only answer first question
    fireEvent.click(screen.getByText('I prefer familiar routines and traditions'));
    
    // Try to submit (by manipulating the component to show the submit button)
    const submitButton = screen.queryByText('Complete');
    if (submitButton) {
      fireEvent.click(submitButton);
    }
    
    expect(global.fetch).not.toHaveBeenCalled();
  });
}); 