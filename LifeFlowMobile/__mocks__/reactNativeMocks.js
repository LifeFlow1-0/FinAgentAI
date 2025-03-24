// Simple mock for React Native
jest.mock('react-native', () => ({
  View: 'View',
  Text: 'Text',
  TextInput: 'TextInput',
  TouchableOpacity: 'TouchableOpacity',
  ActivityIndicator: 'ActivityIndicator',
  StyleSheet: {
    create: jest.fn(() => ({
      container: {},
      input: {},
      button: {},
      buttonText: {},
      disabledButton: {},
      errorText: {},
      successText: {},
      loadingContainer: {}
    }))
  },
  Alert: {
    alert: jest.fn()
  }
}), { virtual: true });

// Mock for animated helpers
jest.mock('react-native/Libraries/Animated/NativeAnimatedHelper', () => ({}), { virtual: true }); 