##  Cloth Shop Website ##


### Overwiew ###
The Cloth Shop Website is an e-commerce platform where users can create an account, log in, browse products, and add them to their basket. 
The main goal of the project is to develop web development skills and demonstrate a willingness to learn and improve. 
The project also aims to showcase testing skills by creating test cases and reporting bugs through manual and automated testing.

### Technologies Used ###

The project is built using Python, Flask, and HTML/CSS with addition of JS. The following libraries and frameworks were used:
1. Flask: a web application framework for Python
2. SQLAlchemy: a Python SQL toolkit that provides a set of high-level API for interacting with relational databases.
3. Pytest: a testing framework for Python that helps you write and run tests
4. Selenium: a web application testing framework that allows you to automate browser interactions
5. flask-smorest: validates the JSON endpoints against schemas and builds their OpenAPI document

### Installation and Usage ###
To install and run the project, follow these steps:

1. Download the Python 3 installer package from the official website and install it, if not installed on your local machine.
2. Clone the repository to your local machine.
3. Install the required packages by running ```pip install -r requirements.txt``` in your terminal.
4. Run the app by executing the main.py file.
5. Go to http://localhost:5000 on your web browser to view the app.

You can log in on a web using those accounts:
1. Username: test, Password: 123
2. Username: test123, Password: test123

! Email feature is not working properly. While the code has been established, it is important to note that a dedicated email address for sending user messages is currently unavailable because of lack of proper email adress that could send messages.

### API ###

The JSON endpoints live under `/api/v1`. They describe themselves: the OpenAPI document is
served at http://localhost:5000/api/openapi.json, and a browsable version of it at
http://localhost:5000/api/docs.

The request and reply shapes in that document are the same schemas the app validates and
serialises with, so the document cannot drift away from what the code actually accepts and
returns.

Two things are worth knowing:

1. Products are addressed by their integer id, for example `/api/v1/products/3`. An earlier
plan used the name-based URL the product page uses, `/cloth/product_detail/Blue-Jeans`, but
that name is the only thing the slug is built from: two products called the same thing share
one URL, and renaming a product breaks every link to it. The page keeps its readable URL and
the API uses ids throughout.
2. The `/api/docs` page loads Swagger UI from a CDN, so it needs internet access. The OpenAPI
document itself is served by the app and works offline.

Every failure replies with the same shape, `{"error": {"code", "message"}}`, and a real status
code: 400 for a request the API cannot accept, 401 when you are not logged in, 404 for
something that is not there, 409 for a review that already exists.

### Running with Docker ###

The container is the supported way to run the site as it would be served in
production: gunicorn rather than the Flask development server, and a non-root
user inside the image.

1. Copy `.env.example` to `.env` and set `SECRET_KEY`.
2. Run `docker compose up --build` from this directory.
3. Go to http://localhost:5000.

`docker compose down` stops the site and keeps the data; `docker compose down -v`
also deletes the database volume, so the next start seeds a fresh database.

#### Where the database lives ####

The database file is not part of the image. It lives in a named volume mounted
at `/data`, so it survives `docker compose down` and any number of rebuilds.
`DATABASE_URL` points at it (`sqlite:////data/mydb.db` - four slashes, because
the path is absolute). Outside the container the same setting defaults to
`Databases/mydb.db` next to this README.

#### How the database gets seeded ####

`docker-entrypoint.sh` runs `Web/create_database.py` on startup, but only when
the database file does not exist yet. The alternative was to bake a seeded
database into the image. Seeding at startup was chosen because a named volume
hides whatever the image holds at that path, so baked-in data only ever arrives
by the accident of Docker copying it into an empty volume on first run, and not
at all with a bind mount. Seeding from the entrypoint keeps the image free of
data, shows up in the container logs, and is the same shape as the migration
step a real deployment would run.

#### Notes ####

- Without `SECRET_KEY` the container exits on startup with an explanatory error.
  That is deliberate: production must not fall back to a throwaway key, because
  every restart would then invalidate all sessions.
- gunicorn runs two workers. SQLite serialises writes with a file lock, so more
  workers buy contention rather than throughput. A deployment that needs more
  belongs on a database server such as PostgreSQL.
- Session cookies are marked `Secure` in production, meaning the browser only
  returns them over HTTPS. Browsers treat `http://localhost` as trustworthy, so
  logging in works locally, but reaching the same container over a plain-HTTP
  LAN address will silently fail to keep you logged in.

### Documentation ###
For more information about project go to [Cloth Shop Website Project Documents](./Documents)

#### Cloth Shop Website Project Documentation #### 

The Cloth Shop Website Project Documentation is a comprehensive document that provides detailed information about the Cloth Shop Website project. 
It includes essential details such as the project's goals, objectives and an overview of the technology stack used for development. 

#### Jira Issues CSV ####

The Jira Issues CSV file contains a comprehensive list of all current issues present in Jira as of the 27th of June 2023. These issues include tasks, test cases and other items related to the Cloth Shop Website project.
The CSV file provides valuable information about each issue, including issue IDs, summaries, descriptions, priorities, and assignees. 


### Status ###
The project is currently under development, with ongoing improvements and updates planned for the future.
