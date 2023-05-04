# Use official Node.js image as a base to build frontend
FROM node:16 as frontend-build

WORKDIR /frontend
COPY frontend/package.json frontend/yarn.lock ./
RUN yarn install
COPY frontend/ ./
RUN yarn build

# Use official Python image to build backend
FROM python:3.9-slim

ENV PORT 8080
WORKDIR /backend

# Copy requirements.txt and install dependencies
COPY backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend/ .

# Copy frontend build folder from the first stage
COPY --from=frontend-build /frontend/dist /backend/static

# Start the application
CMD ["python", "main.py"]
