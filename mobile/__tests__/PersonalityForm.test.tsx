/// <reference types="jest" />
// @ts-nocheck - TODO: Fix TypeScript configuration for Jest tests
import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import { Alert } from 'react-native';
import PersonalityForm from '../app/components/PersonalityForm';

jest.mock('react-native/Libraries/Animated/NativeAnimatedHelper');
jest.mock('react-native/Libraries/Alert/Alert', () => ({
  alert: jest.fn(),
}));

describe('PersonalityForm', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('updates state correctly when user types input', () => {
    const { getByLabelText } = render(<PersonalityForm onSubmit={jest.fn()} />);

    fireEvent.changeText(getByLabelText(/openness/i), 'a');
    fireEvent.changeText(getByLabelText(/social energy/i), 'b');
    fireEvent.changeText(getByLabelText(/learning style/i), 'c');
    fireEvent.changeText(getByLabelText(/activity intensity/i), 'a');

    expect(getByLabelText(/openness/i).props.value).toBe('a');
    expect(getByLabelText(/social energy/i).props.value).toBe('b');
    expect(getByLabelText(/learning style/i).props.value).toBe('c');
    expect(getByLabelText(/activity intensity/i).props.value).toBe('a');
  });

  test('renders all personality input fields', () => {
    const { getByLabelText } = render(<PersonalityForm onSubmit={jest.fn()} />);

    expect(getByLabelText(/openness/i)).toBeTruthy();
    expect(getByLabelText(/social energy/i)).toBeTruthy();
    expect(getByLabelText(/learning style/i)).toBeTruthy();
    expect(getByLabelText(/activity intensity/i)).toBeTruthy();
  });

  test('disables submit button when fields are missing', () => {
    const { getByText, getByLabelText } = render(<PersonalityForm onSubmit={jest.fn()} />);

    fireEvent.changeText(getByLabelText(/openness/i), 'a');
    fireEvent.changeText(getByLabelText(/social energy/i), 'b');
    fireEvent.changeText(getByLabelText(/learning style/i), '');

    expect(getByText(/submit/i).props.disabled).toBe(true);
  });

  test('shows error for invalid dropdown values', async () => {
    const { getByText, getByLabelText } = render(<PersonalityForm onSubmit={jest.fn()} />);

    fireEvent.changeText(getByLabelText(/openness/i), 'x'); // Invalid value

    fireEvent.press(getByText(/submit/i));

    expect(await getByText(/please enter a, b, or c/i)).toBeTruthy();
  });

  test('resets state after successful submission', async () => {
    const { getByText, getByLabelText } = render(<PersonalityForm onSubmit={jest.fn()} />);

    fireEvent.changeText(getByLabelText(/openness/i), 'a');
    fireEvent.changeText(getByLabelText(/social energy/i), 'b');
    fireEvent.changeText(getByLabelText(/learning style/i), 'c');
    fireEvent.changeText(getByLabelText(/activity intensity/i), 'a');

    fireEvent.press(getByText(/submit/i));

    await waitFor(() => {
      expect(getByLabelText(/openness/i).props.value).toBe('');
      expect(getByLabelText(/social energy/i).props.value).toBe('');
      expect(getByLabelText(/learning style/i).props.value).toBe('');
      expect(getByLabelText(/activity intensity/i).props.value).toBe('');
    });
  });
  
  // New test cases
  
  test('displays validation error when missing required fields', () => {
    const { getByText } = render(<PersonalityForm onSubmit={jest.fn()} />);
    
    // Try to submit with empty fields
    fireEvent.press(getByText(/submit/i));
    
    // Check if Alert was called with validation error message
    expect(Alert.alert).toHaveBeenCalledWith(
      'Validation Error',
      'Please fill in all fields correctly'
    );
  });
  
  test('calls onSubmit with correct data when form is valid', () => {
    const mockSubmit = jest.fn();
    const { getByText, getByLabelText } = render(<PersonalityForm onSubmit={mockSubmit} />);
    
    // Fill all form fields
    fireEvent.changeText(getByLabelText(/openness/i), 'a');
    fireEvent.changeText(getByLabelText(/social energy/i), 'b');
    fireEvent.changeText(getByLabelText(/learning style/i), 'c');
    fireEvent.changeText(getByLabelText(/activity intensity/i), 'a');
    
    // Submit the form
    fireEvent.press(getByText(/submit/i));
    
    // Verify onSubmit was called with correct data
    expect(mockSubmit).toHaveBeenCalledWith({
      openness: 'a',
      social_energy: 'b',
      learning_style: 'c',
      activity_intensity: 'a'
    });
  });
  
  test('handles loading state properly during submission', () => {
    const { getByLabelText, getByTestId } = render(
      <PersonalityForm onSubmit={jest.fn()} isLoading={true} />
    );
    
    // Check that inputs are disabled during loading
    expect(getByLabelText(/openness/i).props.editable).toBe(false);
    expect(getByLabelText(/social energy/i).props.editable).toBe(false);
    expect(getByLabelText(/learning style/i).props.editable).toBe(false);
    expect(getByLabelText(/activity intensity/i).props.editable).toBe(false);
    
    // Check that loading indicator is displayed
    expect(getByTestId('loading-indicator')).toBeTruthy();
  });
}); 