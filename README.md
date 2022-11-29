# Fashion Campus

Backend repository for Final Project Startup Campus

## Built With

- [Flask](https://flask.palletsprojects.com/en/2.2.x/) v2.2.2
- [Flask-Restx](https://flask-restx.readthedocs.io/en/latest/) v1.0.3
- [Flask-Cors](https://flask-cors.readthedocs.io/en/latest/) v3.0.10
- [Requests](https://requests.readthedocs.io/en/latest/) v2.28.1
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/) v3.0.2
- [psycopg2-binary](https://www.psycopg.org/docs/) v2.9.3
- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) v3.1.0
- [google-cloud-storage](https://cloud.google.com/storage/docs/reference/libraries#client-libraries-install-python) v2.1.0
- [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/en/1.0.1/) v1.0.1
- [PyJWT](https://pyjwt.readthedocs.io/en/stable/) v1.7.1
- [Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html) v5.2.7
- [redis](https://pypi.org/project/redis/) v4.3.5
- [image-prediction](https://github.com/rizanqardafil/fashion-mnist)

# How to run a Fashion-Campus locally

## Initial Setup

Please ensure that the tools listed below are installed.

- [ ] Code editor for example [Visual Studio Code](https://code.visualstudio.com/)
- [ ] Version control [Git](https://git-scm.com/)
- [ ] [Docker](https://www.docker.com/) and [docker compose](https://docs.docker.com/compose/). In this project, we're using Docker Compose v2.12.0, see for [installation](https://docs.docker.com/compose/install/linux/#install-the-plugin-manually).

## Clone repository

Run the following command in your terminal.

```
git clone https://gitlab.com/andrifanky/fashion-campus.git
```

## Change environment

After cloning the fashion-campus repository, launch your code editor and navigate to the fashion-campus folder. Before running fashion-campus on your local machine, modify the following settings.

Open the `.env` file, then modify it
- IMAGE_PREDICTION_URL=http://`127.0.0.1`:5050

## Run Fashion-Campus

Then open the code editor's terminal.

Type `docker info` to see if Docker is running

and execute the following command.

```
cd <base_folder_path_fashion_campus>
docker compose -f docker-compose-local.yml up
```

You can now access the fashion-campus web application by going to http://127.0.0.1:3000.