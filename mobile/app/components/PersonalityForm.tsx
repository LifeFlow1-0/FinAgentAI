import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ActivityIndicator,
  StyleSheet,
  ScrollView,
  Alert,
} from 'react-native';

interface PersonalityFormProps {
  onSubmit: (data: PersonalityData) => void;
  isLoading?: boolean;
}

interface PersonalityData {
  openness: string;
  social_energy: string;
  learning_style: string;
  activity_intensity: string;
}

const PersonalityForm: React.FC<PersonalityFormProps> = ({ onSubmit, isLoading = false }) => {
  const [formData, setFormData] = useState<PersonalityData>({
    openness: '',
    social_energy: '',
    learning_style: '',
    activity_intensity: '',
  });

  const [errors, setErrors] = useState<Partial<Record<keyof PersonalityData, string>>>({});

  const validateField = (name: keyof PersonalityData, value: string) => {
    if (!value) {
      return 'This field is required';
    }
    if (!['a', 'b', 'c'].includes(value.toLowerCase())) {
      return 'Please enter a, b, or c';
    }
    return '';
  };

  const handleChange = (name: keyof PersonalityData, value: string) => {
    const error = validateField(name, value);
    setErrors(prev => ({
      ...prev,
      [name]: error,
    }));
    
    setFormData(prev => ({
      ...prev,
      [name]: value.toLowerCase(),
    }));
  };

  const resetForm = () => {
    setFormData({
      openness: '',
      social_energy: '',
      learning_style: '',
      activity_intensity: '',
    });
    setErrors({});
  };

  const handleSubmit = () => {
    // Validate all fields
    const newErrors: Partial<Record<keyof PersonalityData, string>> = {};
    let hasErrors = false;

    (Object.keys(formData) as Array<keyof PersonalityData>).forEach(key => {
      const error = validateField(key, formData[key]);
      if (error) {
        newErrors[key] = error;
        hasErrors = true;
      }
    });

    if (hasErrors) {
      setErrors(newErrors);
      Alert.alert('Validation Error', 'Please fill in all fields correctly');
      return;
    }

    onSubmit(formData);
    resetForm(); // Reset form after successful submission
  };

  // Check if any required field is empty
  const isFormIncomplete = Object.values(formData).some(value => !value);

  const renderInput = (
    name: keyof PersonalityData,
    label: string,
    placeholder: string
  ) => (
    <View style={styles.inputContainer}>
      <Text style={styles.label}>{label}</Text>
      <TextInput
        style={[
          styles.input,
          errors[name] ? styles.inputError : null,
        ]}
        value={formData[name]}
        onChangeText={(value) => handleChange(name, value)}
        placeholder={placeholder}
        placeholderTextColor="#666"
        autoCapitalize="none"
        editable={!isLoading}
        accessibilityLabel={label}
      />
      {errors[name] ? (
        <Text style={styles.errorText}>{errors[name]}</Text>
      ) : null}
    </View>
  );

  return (
    <ScrollView 
      style={styles.container}
      contentContainerStyle={styles.contentContainer}
      keyboardShouldPersistTaps="handled"
    >
      <Text style={styles.title}>Personality Profile</Text>
      
      {renderInput(
        'openness',
        'Openness to Experience',
        'Enter a, b, or c'
      )}
      
      {renderInput(
        'social_energy',
        'Social Energy',
        'Enter a, b, or c'
      )}
      
      {renderInput(
        'learning_style',
        'Learning Style',
        'Enter a, b, or c'
      )}
      
      {renderInput(
        'activity_intensity',
        'Activity Intensity',
        'Enter a, b, or c'
      )}

      <TouchableOpacity
        style={[
          styles.submitButton,
          isLoading || isFormIncomplete ? styles.submitButtonDisabled : null,
        ]}
        onPress={handleSubmit}
        disabled={isLoading || isFormIncomplete}
        accessibilityLabel="Submit"
      >
        {isLoading ? (
          <ActivityIndicator color="#FFFFFF" testID="loading-indicator" />
        ) : (
          <Text style={styles.submitButtonText}>Submit</Text>
        )}
      </TouchableOpacity>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  contentContainer: {
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 20,
    textAlign: 'center',
  },
  inputContainer: {
    marginBottom: 20,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 8,
  },
  input: {
    backgroundColor: '#fff',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    borderWidth: 1,
    borderColor: '#ddd',
  },
  inputError: {
    borderColor: '#ff3b30',
  },
  errorText: {
    color: '#ff3b30',
    fontSize: 14,
    marginTop: 4,
  },
  submitButton: {
    backgroundColor: '#007AFF',
    borderRadius: 8,
    padding: 16,
    alignItems: 'center',
    marginTop: 20,
  },
  submitButtonDisabled: {
    backgroundColor: '#999',
  },
  submitButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
});

export default PersonalityForm; 