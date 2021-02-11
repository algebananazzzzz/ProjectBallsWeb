# ProjectBallsWeb
Software to create gameplay snippets

Requisites:
Docker installed in a Linux based machine

Set up:
1. Git clone this repository
2. Change directory into it, then create .env file
```
cat > .env
POSTGRES_DB=(your database name)
POSTGRES_USER=(your user)
POSTGRES_PASSWORD=(your password)
```
3. Change exposed port (optional)
```
nano docker-compose.yml
```
Then change port number of 8000 to your custom port

4. Run docker-compose commands
```
docker-compose build
docker-compose up
```

You're ready to host/do whatever shit you want now
