# Use Node.js image
FROM node:18

# Set working directory
WORKDIR /app

# Copy frontend files
COPY src /app

# Install dependencies and build
RUN npm install
RUN npm run build

# Install serve to serve built frontend
RUN npm install -g serve

# Expose frontend port
EXPOSE 3000

# Serve the frontend
CMD ["serve", "-s", "build", "-l", "3000"]