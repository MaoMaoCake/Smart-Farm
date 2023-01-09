FROM node:19.4.0 AS build

# install dependencies
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

# copy  all files into the image
COPY . .

RUN npm run build

# only copy the build app
FROM node:19.4.0

WORKDIR /app

COPY --from=build /app/build ./
COPY . .

RUN npm install

EXPOSE 3000
CMD ["node", "."]