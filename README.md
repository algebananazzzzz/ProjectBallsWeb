# ProjectBallsWeb
Writeup:

ProjectBalls(web) is a web application software project created to address the user story of providing freely available and simplistic video editing softwares designed for coaches. The user action designed for is first uploading a video, then cutting the video into snippets, finally downloading the snippets. In essence, the project comprises of three main fuctions: edit video, query snippets matching descriptions and download snippets. 

The user first creates an account and create videos that can denote a particular game, in which they can upload a video they wanna edit. The user can then proceed to cut the video in an interactive page, allowing the user to control specific keys (e.g. s for start, space for end) to indicate start and end times for multiple snippets matching a specific gameplay type (e.g. defense, sideline play) in a go, while being able to view the video and determine where to cut on the fly. 

After the software finished cutting the snippets in the backend, users can query snippets matching a specific description (e.g. defense, sideline play) across all boards (in dashboard page) or within a board, then download the snippet(s) one by one or all as a zip file. The user can customise the controls in the configuration page. 

Requisites:

Docker and docker-compose installed in a Linux based machine

Set up:
1. Git clone this repository
```
git clone https://github.com/algebananazzzzz/ProjectBallsWeb.git
```

2. Change exposed port (optional)
```
nano docker-compose.yml
```
Then change port number of 8000 to your custom port in the web service. 

3. Run docker-compose commands
```
docker-compose build
docker-compose up
```
Or:
1. If you're familiar with docker, just pull the latest docker image from dockerhub and build it
```
https://hub.docker.com/r/dzqx/projectballsweb
```

You're ready to host the web application at port 8000 now
