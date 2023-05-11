# base image
FROM node:16-buster-slim

RUN mkdir /app
WORKDIR /app

COPY . /app
# Install dependencies
RUN npm install --force

# Build Angular app
RUN npm install -g @angular/cli@15.0.0
RUN ng build

EXPOSE 4200

CMD npm start
# CMD ["node", "server.js"]
