import React, { useState } from 'react';
import { SafeAreaView, StatusBar, StyleSheet, Text, View } from 'react-native';
import PersonalityForm from './components/PersonalityForm';

const App = () => {
  const [userId] = useState(1); // In a real app, this would come from authentication

  const handleSubmit = async (data: any) => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/user-profile/personality', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-User-ID': userId.toString()
        },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        throw new Error('Failed to save personality profile');
      }

      console.log('Personality profile saved successfully!');
    } catch (error) {
      console.error('Error saving personality profile:', error);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" />
      <View style={styles.header}>
        <Text style={styles.title}>LifeFlow</Text>
        <Text style={styles.subtitle}>Personality Profile</Text>
      </View>
      <PersonalityForm onSubmit={handleSubmit} />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    padding: 20,
    backgroundColor: '#007AFF',
    alignItems: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
  },
  subtitle: {
    fontSize: 16,
    color: 'white',
    marginTop: 5,
  },
});

export default App; 