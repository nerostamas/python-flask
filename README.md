#Running the app:
Script to start & clean up app: <br/>
`./start.sh` <br/>
Parameters:
- up: to start application, by default app will run on 8080 and create an default user as username is admin, password is admin. <br/>
- down: to clean up app

ex: `./syart.sh -p up` <br/>

after start app successfully. You can see the app at http://localhost:808 with the UI.

The app have some basic unit test to validate features, please take a look at test folders: <br/>
- testAuth
- testUser
- testTicketAndComment

You also view the database at http://localhost:8081 (default database will have name `sample` and you can change in `docker-compose.yml`)

Tech stack: `reactjs` `flask` `mongodb` `Docker`