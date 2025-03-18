import React, { useState } from 'react';
import { View, StyleSheet, Alert } from 'react-native';
import PersonalityForm from './PersonalityForm';

interface PersonalityProfileContainerProps {
  userId: number;
}

const PersonalityProfileContainer: React.FC<PersonalityProfileContainerProps> = ({ userId }) => {
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (formData: any) => {
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/v1/user-profile/personality', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-User-ID': userId.toString()
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to save personality profile');
      }

      Alert.alert(
        'Success',
        'Personality profile saved successfully!',
        [{ text: 'OK' }]
      );
    } catch (error) {
      Alert.alert(
        'Error',
        error instanceof Error ? error.message : 'An unexpected error occurred',
        [{ text: 'OK' }]
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <PersonalityForm 
        onSubmit={handleSubmit}
        isLoading={isLoading}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
});

export default PersonalityProfileContainer; 