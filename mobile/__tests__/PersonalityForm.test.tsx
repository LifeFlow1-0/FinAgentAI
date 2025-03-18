import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import PersonalityForm from '../PersonalityForm';

jest.mock('react-native/Libraries/Animated/NativeAnimatedHelper');

describe('PersonalityForm', () => {
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
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ status: 'success' }),
      })
    );

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
}); 