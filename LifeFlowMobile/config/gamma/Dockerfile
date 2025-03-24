FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy project files
COPY . .

# Set environment variables
ENV NODE_ENV=production
ENV API_URL=https://gamma-api.lifeflow.app/api
ENV ENABLE_DEBUG=true
ENV APP_ENV=gamma

# Build the app
RUN npm run build

# Expose port for the server
EXPOSE 3000

# Start server
CMD ["npm", "run", "serve"] 