FROM node:18.15-alpine
RUN apk add bash curl
WORKDIR /app
COPY web/ .
RUN npm ci
RUN npm run build
