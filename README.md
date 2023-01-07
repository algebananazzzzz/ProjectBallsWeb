# ProjectBallsWeb
Writeup:

ProjectBalls(web) is a web application software project created to address the user story of providing freely available and on-the-go video editing softwares designed for coaches. The user action designed for is first uploading a video, then cutting the video into snippets, finally downloading the snippets. In essence, the project comprises of three main fuctions: cutting snippets from video, query snippets matching descriptions and download snippets.

The user first creates an account, then upload a video they wanna edit. They then proceed to cut the video in an interactive page, using specific control keys (e.g. s for start, space for end) to indicate start and end times for multiple snippets matching a specific gameplay tag (e.g. defense, sideline play), while being able to view the video and determine where to cut on the fly.

Afterwhich, users can query snippets matching a specific description (e.g. defense, sideline play) in the dashboard page, then download the snippet(s) one by one or all as a zip file.


# Deployment Requisites:

Docker or docker-compose installed in a Linux based machine

Set up:
1. Git clone this repository
```
git clone https://github.com/algebananazzzzz/ProjectBallsWeb.git
```

2. Change exposed port (optional)
```
nano docker-compose.yml
```
Then change exposed port number of 8000 to your preferred port in the web service in the field ports. By default, application is exposed to port 8000 of localhost.

3. Run docker commands

With docker-compose:
```
docker-compose build
docker-compose up
```
Or with docker:
```
docker compose build
docker compose up
```

# "Quick start" Requisites and Set up:

Python 3, Postgresql on port 5432, Redis on port 6379

1. Git clone this repository
```
git clone https://github.com/algebananazzzzz/ProjectBallsWeb.git
```

2. Within your preferred environment (venv), ensure all dependencies are downloaded
```
sudo apt install ffmpeg
pip install -r requirements.txt
```

3. Create a database in postgresql, and edit the credentials into .env file
```
nano .env
```

4. Deploy
```
python project_balls/manage.py makemigrations
python project_balls/manage.py migrate
python project_balls/manage.py runserver
```
