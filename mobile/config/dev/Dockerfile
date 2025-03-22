FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies (including dev dependencies)
RUN npm install

# Copy project files
COPY . .

# Set environment variables
ENV NODE_ENV=development
ENV API_URL=http://localhost:3000/api
ENV ENABLE_DEBUG=true
ENV APP_ENV=dev

# Expose ports for React Native development server
EXPOSE 19000 19001 19002

# Default command - can be overridden when running the container
# Use CMD npm test to run tests instead
CMD ["npm", "start"] 