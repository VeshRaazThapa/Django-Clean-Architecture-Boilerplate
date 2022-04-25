

## Basic Usage
1. First run **`make newdev`** to start up the project for first time.
2. go to http://localhost:5001/admin
3. username:admin76, password:admin76
Checkout the [commands](#commands) section for more usage.


## initial setup
1.run make bud(this builds the docker project)
2.run make dr

Alternatively:
run make newdev

## Preview
A default Django project resides in `root` directory. So, when you start the project, you will see the following screen in `5001` port:
http://localhost:5001/

## Commands
To use this project, run this commands:

0. `make newdev` to build the project and use the backup dump_data.sql in the root folder
1. `make b` to build the project and starting containers.
2. `make bud` to build the project.(build and up in detached mode)
3. `make u` to start containers if project has been up already.
4. `make d` to stop containers.
5. `make dv` to stop containers and remove volumes.
6. `make sweb` to shell access web container.
7. `make csu` to put static files in static directory.
8. `make nrw` to run npm run watch.
9. `make nrp` to run npm run production.
10. `make lw` to log access web container.
11. `make ld` to log access db container.
12. `make rs` to restart web and db container.
13. `make dd` to dumb db container as dump_data.sql in the root directory.
14. `make dr` to restore db container data from dump_data.sql file in the root directory.
15. `make udev` to start container in development mode (when container seem to be slow, this will help run little faster).