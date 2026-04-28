FROM node

WORKDIR /usr/src/app


COPY back/api ./api
COPY back/assets ./assets
COPY back/config ./config
COPY back/tasks ./tasks
COPY back/views ./views

COPY back/package*.json ./
COPY back/*.js ./
COPY back/package*.json ./

RUN npm install

EXPOSE 3000
CMD [ "node", "app.js", "$MYSQLDB", "$DB", "$REDISDB", "$HOST", "$PORT", "$SMARTCONTRACTADDRESS"]

