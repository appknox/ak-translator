# Build stage
FROM node:18-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine as production

WORKDIR /app
RUN npm install -g serve
COPY --from=build /app/dist ./dist

EXPOSE $PORT
CMD serve -s dist -l $PORT