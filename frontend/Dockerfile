FROM node:20-alpine

WORKDIR /app

# Install dependencies based on the preferred package manager
COPY package.json package-lock.json* ./
RUN npm ci

COPY . .

# Next.js telemetry
ENV NEXT_TELEMETRY_DISABLED 1

# Start development server
CMD ["npm", "run", "dev"]
