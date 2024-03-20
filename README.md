# erineapp-test

## Run App

This is bus station app, users can reserve and unreserve seat, admin can register bus and driver and manage them.

First, clone this repository.

```
git clone https://github.com/nycmeshnet/network-map.git
```

Open your terminal, and type this commands.

```
cd PRO

docker-compose build

docker-compose up -d
```

Then, the docker image will be created.

After that, follow this commands, you should create admin for django admin.

```
docker-compose exec web python manage.py createsuperuser
```

Then set the admin name, password, and email address.

Next, you should create db with follow command.

```
docker-compose exec web python manage.py migrate
```

After this, the backend server is up to now!

And you have to run frontend.

```
cd client

npm i

npm start
```

Frontend: http://127.0.0.1:8080

Backend Admin: http://127.0.0.1:8000/admin

## Test App

After run backend, follow these commands.

```
docker-compose exec web pytest
```

Regarding the frontend, follow these commands.

```
cd client

npm test
```
