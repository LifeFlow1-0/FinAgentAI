FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies - only production dependencies
RUN npm install --production

# Copy project files
COPY . .

# Set environment variables
ENV NODE_ENV=production
ENV API_URL=https://api.lifeflow.app/api
ENV ENABLE_DEBUG=false
ENV APP_ENV=production

# Build the app
RUN npm run build

# Expose port for the server
EXPOSE 3000

# Start server
CMD ["npm", "run", "serve"] 