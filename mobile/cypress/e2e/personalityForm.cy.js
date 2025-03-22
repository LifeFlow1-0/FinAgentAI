/// <reference types="cypress" />

describe('Personality Form E2E Test', () => {
  beforeEach(() => {
    // Visit the page with the personality form
    cy.visit('/personality');
    
    // Set up API mocking for the backend calls
    cy.intercept('POST', '/api/personality', {
      statusCode: 200,
      body: { status: 'success', message: 'Personality data submitted successfully' }
    }).as('submitPersonality');
  });

  it('should fill in valid values and submit successfully', () => {
    // Fill in all the personality form fields
    cy.get('[data-testid="openness-input"]').type('a');
    cy.get('[data-testid="social-energy-input"]').type('b');
    cy.get('[data-testid="learning-style-input"]').type('c');
    cy.get('[data-testid="activity-intensity-input"]').type('a');
    
    // Submit the form
    cy.get('[data-testid="submit-button"]').click();
    
    // Verify loading state appears
    cy.get('[data-testid="loading-indicator"]').should('be.visible');
    
    // Validate backend receives the data with the correct payload
    cy.wait('@submitPersonality').its('request.body').should('deep.equal', {
      openness: 'a',
      social_energy: 'b',
      learning_style: 'c',
      activity_intensity: 'a'
    });
    
    // Confirm success message appears after submission
    cy.get('[data-testid="success-message"]').should('be.visible');
    cy.get('[data-testid="success-message"]').should('contain.text', 'Personality data submitted successfully');
    
    // Verify form was reset
    cy.get('[data-testid="openness-input"]').should('have.value', '');
    cy.get('[data-testid="social-energy-input"]').should('have.value', '');
    cy.get('[data-testid="learning-style-input"]').should('have.value', '');
    cy.get('[data-testid="activity-intensity-input"]').should('have.value', '');
  });

  it('should show validation errors for invalid input', () => {
    // Try to submit with empty fields
    cy.get('[data-testid="submit-button"]').click();
    
    // Check that button remains disabled
    cy.get('[data-testid="submit-button"]').should('be.disabled');
    
    // Fill with invalid value
    cy.get('[data-testid="openness-input"]').type('x');
    
    // Check error message appears
    cy.get('[data-testid="openness-error"]').should('be.visible');
    cy.get('[data-testid="openness-error"]').should('contain.text', 'Please enter a, b, or c');
  });

  it('should handle network errors gracefully', () => {
    // Override the intercept with an error response
    cy.intercept('POST', '/api/personality', {
      statusCode: 500,
      body: { error: 'Server error' }
    }).as('failedSubmit');
    
    // Fill in all the personality form fields
    cy.get('[data-testid="openness-input"]').type('a');
    cy.get('[data-testid="social-energy-input"]').type('b');
    cy.get('[data-testid="learning-style-input"]').type('c');
    cy.get('[data-testid="activity-intensity-input"]').type('a');
    
    // Submit the form
    cy.get('[data-testid="submit-button"]').click();
    
    // Wait for the failed request
    cy.wait('@failedSubmit');
    
    // Check error message appears
    cy.get('[data-testid="error-message"]').should('be.visible');
    cy.get('[data-testid="error-message"]').should('contain.text', 'Error submitting personality data');
  });
}); 