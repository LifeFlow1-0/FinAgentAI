// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************

// Custom command to fill the entire personality form
Cypress.Commands.add('fillPersonalityForm', (values) => {
  const defaultValues = {
    openness: 'a',
    social_energy: 'b',
    learning_style: 'c',
    activity_intensity: 'a',
  };
  
  const formValues = { ...defaultValues, ...values };
  
  cy.get('[data-testid="openness-input"]').clear().type(formValues.openness);
  cy.get('[data-testid="social-energy-input"]').clear().type(formValues.social_energy);
  cy.get('[data-testid="learning-style-input"]').clear().type(formValues.learning_style);
  cy.get('[data-testid="activity-intensity-input"]').clear().type(formValues.activity_intensity);
});

// Custom command to submit form and wait for response
Cypress.Commands.add('submitPersonalityFormAndWait', () => {
  cy.get('[data-testid="submit-button"]').click();
  cy.wait('@submitPersonality');
}); 