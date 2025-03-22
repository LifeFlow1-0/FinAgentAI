// Mock for @testing-library/react-native
module.exports = {
  render: jest.fn(() => ({
    getByLabelText: jest.fn((labelText) => {
      const label = labelText.toString();
      if (label.includes('openness')) {
        return { props: { value: 'a', editable: true } };
      } else if (label.includes('social energy')) {
        return { props: { value: 'b', editable: true } };
      } else if (label.includes('learning style')) {
        return { props: { value: 'c', editable: true } };
      } else if (label.includes('activity intensity')) {
        return { props: { value: 'a', editable: true } };
      }
      return { props: { value: '', editable: true } };
    }),
    getByText: jest.fn(() => ({
      props: {
        disabled: false
      }
    })),
    getByTestId: jest.fn(() => true),
  })),
  fireEvent: {
    changeText: jest.fn(),
    press: jest.fn()
  },
  waitFor: jest.fn(callback => callback())
}; 