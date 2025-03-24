import React, { useState } from 'react';
import { SafeAreaView, StatusBar, StyleSheet, Text, View, Alert } from 'react-native';
import PersonalityForm from './components/PersonalityForm';

type PersonalityData = {
  openness: string;
  social_energy: string;
  learning_style: string;
  activity_intensity: string;
};

// API host configuration
const API_HOST = '192.168.1.5:8000'; // Your machine's IP address

const App = () => {
  const [userId] = useState(1); // In a real app, this would come from authentication
  const [isLoading, setIsLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const handleSubmit = async (data: PersonalityData) => {
    setIsLoading(true);
    setSuccessMessage(null);
    
    try {
      console.log('Submitting to:', `http://${API_HOST}/api/v1/user-profile/personality`);
      
      // First try to update the profile with PUT request
      let response = await fetch(`http://${API_HOST}/api/v1/user-profile/personality`, {
        method: 'PUT', // Try updating first
        headers: {
          'Content-Type': 'application/json',
          'X-User-ID': userId.toString()
        },
        body: JSON.stringify(data)
      });

      // If PUT failed with 404 (No profile exists), try creating a new one with POST
      if (response.status === 404) {
        console.log('No existing profile found, creating a new one');
        response = await fetch(`http://${API_HOST}/api/v1/user-profile/personality`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-User-ID': userId.toString()
          },
          body: JSON.stringify(data)
        });
      }

      if (!response.ok) {
        console.error('Server responded with:', response.status);
        const responseText = await response.text();
        console.error('Response body:', responseText);
        
        // Special handling for 409 Conflict (Profile already exists)
        if (response.status === 409) {
          Alert.alert(
            "Profile Already Exists",
            "A personality profile already exists for this user. Would you like to update it instead?",
            [
              {
                text: "Cancel",
                style: "cancel"
              },
              {
                text: "Update",
                onPress: async () => {
                  try {
                    setIsLoading(true);
                    const updateResponse = await fetch(`http://${API_HOST}/api/v1/user-profile/personality`, {
                      method: 'PUT',
                      headers: {
                        'Content-Type': 'application/json',
                        'X-User-ID': userId.toString()
                      },
                      body: JSON.stringify(data)
                    });
                    
                    if (updateResponse.ok) {
                      console.log('Personality profile updated successfully!');
                      setSuccessMessage('Profile updated successfully!');
                    } else {
                      console.error('Failed to update profile:', await updateResponse.text());
                      throw new Error('Failed to update personality profile');
                    }
                  } catch (error) {
                    console.error('Error updating profile:', error);
                  } finally {
                    setIsLoading(false);
                  }
                }
              }
            ]
          );
          return; // Exit early since we're handling with an Alert
        }
        
        throw new Error('Failed to save personality profile');
      }

      console.log('Personality profile saved successfully!');
      setSuccessMessage('Profile saved successfully!');
    } catch (error) {
      console.error('Error saving personality profile:', error);
      throw error; // Propagate the error to the PersonalityForm component
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" />
      <View style={styles.header}>
        <Text style={styles.title}>LifeFlow</Text>
        <Text style={styles.subtitle}>Personality Profile</Text>
      </View>
      {successMessage && (
        <View style={styles.successContainer}>
          <Text style={styles.successText}>{successMessage}</Text>
        </View>
      )}
      <PersonalityForm onSubmit={handleSubmit} isLoading={isLoading} />
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
  successContainer: {
    backgroundColor: '#DFF2BF',
    padding: 10,
    margin: 10,
    borderRadius: 5,
  },
  successText: {
    color: '#4F8A10',
    textAlign: 'center',
  }
});

export default App; 