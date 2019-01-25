FROM node AS build

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:stable
COPY --from=build /app/dist/ /var/www
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
CMD ["nginx" , "-g", "daemon off;"]
