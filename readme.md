# Connie Jacques - API Webserver Project


### Database Set Up and Flask Instructions

This API has been built using Python3 on a Flask framework. The database used is PostgreSQL. Postgres must be installed and the database set up before the API can be used on a local host server. 

It is assumed that the user has PostgreSQL and psycopg2 installed and is familiar with its usage.

PostgreSQL runs on port 5432 by default. If you have PostgreSQL running on a different port, you will need to change the specified port in the DATABASE_URL statement in the .env file.

`
DATABASE_URL="postgresql+psycopg2://db_dev:123456@localhost:5432/stephen_king_db"
`

Change *localhost:5432* to the port number you are using for PostgreSQL, if different.


Create the database by executing the following command on the PostgreSQL command line:

`
CREATE DATABASE stephen_king_db;
`

If you wish to name the database something else, please be sure to change the database name in the .env file. The database is named in this file (as shown below) as stephen_king_db but it can be altered by changing the name to match your newly created database in PostgreSQL. 

`
DATABASE_URL="postgresql+psycopg2://db_dev:123456@localhost:5432/stephen_king_db"
`

Change *stephen_king_db* to your match the name you gave the new database in PostgreSQL.

Create a user for the database by executing the following command on the postgreSQL command line:

`
CREATE USER db_dev WITH PASSWORD '123456';
`

If you have an existing user that you wish to use, please change the DATABASE_URL statement in the .env file to reflect this. 

`
DATABASE_URL="postgresql+psycopg2://db_dev:123456@localhost:5432/stephen_king_db"
`

Change *db_dev:123456* to the name and password of the user you wish to use.

To grant privileges to the user to perform CRUD functionality on the new database, execute the following command on the PostgreSQL command line: 

`
GRANT ALL PRIVILEGES ON DATABASE stephen_king_db TO db_dev;
`

If your database or username is different please alter the command to reflect this.

Once this has been done, the database is ready to use.

Next, navigate to your copy of the *ConnieJacques_T2A2* directory on the terminal command line. Move into the folder and move again into the *src* directory.

Create a virtual environment by executing the following command on the command line:

`
python3 -m venv venv
`

Activate the virtual environment. This can be done on a POSIX computer by executing the following command on the command line:

`
source venv/bin/activate
`

Install the application dependencies by executing the following command on the command line:

`
pip3 install -r requirements.txt
`

You can now create and seed the tables for the database by executing the following on the command line:

Create tables:

`
flask db create
`

Seed tables:

`
flask db seed
`

And delete tables, if needed:

`
flask db drop
`

The default local host server port is used for this application. If you have your local host running on a different port, please change:

`
FLASK_RUN_PORT=5000
`

in the .flaskenv file to reflect this.

As the application is set up to use .env and .flaskenv files to access environmental variables, and the main file is named *app.py*, Flask will run if the following is executed on the command line:

`
flask run
`

You are now ready to use the API. Please see the endpoint documentation below for detailed instructions.

### R1. Identification of the problem you are trying to solve by building this particular app

This API Webserver Project will build an application to list published Stephen King books and the movie adaptations made from them. It will detail the books, including when they were first published, whether the author published them under his own name or under a pen name, the publisher, ISBN, and other interesting information. Many movies have been produced from the stories told in these books. This application will give users quick assess to information about which books have been made into movies, when, who directed them and how successful and popular they were. The users of this application will also have the ability to keep a record of the movies and books they themselves have pursued and leave a rating. Ratings are useful way for other fans of this author to prioritise the books and movies they wish to spend their time consuming next, as there is a large number of both available. As such, the problem this application attempts to solve is the need for a convenient way for fans to find out what is available and what other fans have enjoyed the most, to help them choose what to view or read next. 


### R2. Why is it a problem that needs solving?

Our modern society is a busy one. Many people are working to excess, burnt out, stressed out and in need of a way to relax at the end of the day. For many, reading books and watching movies is a great way to do this; however, the volume of reading and viewing material available can be overwhelming and make choosing something to spend time on difficult. Knowing that you are a fan of an author, director or genre already can help to narrow down the choices but sometimes there are still a lot of options available and being able to choose something we are confident we will enjoy can be challenging. 

This API will aid fans of Stephen King’s work, or the horror genre more broadly, to choose a way to spend their time. This author has published 65 novels, and approximately 86 movie adaptations have been made from them. A public API containing information about all of these options does not currently exist; however, it should because this would be a convenient way to access details about these books and movies, and their popularity amongst enthusiasts, would benefit fans. Plus, the additional benefit for an individual to keep track of what they have and have not read and watched previously is undeniably handy.


### R3. Why have you chosen this database system. What are the drawbacks compared to others?

For this project, I will be using the relational database management system PostgreSQL. 

A relational database management system will be used for this application as it will be essential to be able to easily and flexibly query the database to access the required data. By dividing the data into relevant tables, we can ensure that it is simple to perform highly specific queries while also preventing data corruption in duplication. The process of normalisation will ensure that data integrity can be easily maintained and enable scalability for the project to grow in the future. 

As a RDBMS, Postgres uses Primary and Foreign Keys to relate tables to one another. The benefit of  Postgres itself managing the auto-incrementation of Primary Keys reduces the likely of data integrity being lost due to user error when entires are deleted or modified. As PostgreSQL has its own built-in systems to prevent partial data deletion where cascading removal is or is not used, we can be assured that the information contained in the database accurately reflects the raw data. 

Because it is an object relational database system, PostgreSQL allows for the use of multimedia content and complex data types such as such as boolean, temporal (date/time) and universally unique identifiers (UUIDs), in addition to alphanumeric data (IONOS 2023). As an ORDBMS, Postgres expands on the traditional relational model with the inclusion of object relational mapping to enable data to be stored as objects for use with an object orientated programming language such as Python (IONOS 2023).

For this API project, I will be using JavaScript Object Notation (JSON) extensively to format data. As such, a database management system that can handle this is essential. Although additional external python packages, outside the standard Flask library, are required, Postgres is compatible with this. However, the need for adaptation to make this work could be considered a disadvantage.  

Some other benefits of PostgreSQL that have influenced my decision to use this DBMS and not another include:

- Open source, meaning it is free to use.
- SQL compliant, making it easy for me use SQL commands on the command line to check queries directly against the database (IONOS 2023).
- ACID (Atomicity, Consistency, Isolation, and Durability) compliance ensures reliability when transactions are performed on the database (MariaDB 2023).

Drawbacks:

- Relationships between tables must be correctly identified and Foreign Keys must be accurately  entered. This is not an issue with NoSQL databases. 
- Speed - Postgres can be slower than other RDBMS, including MySQL; however, performance can be influenced by a lot of factors, so this is not always true.
- Learning curve - although PostgreSQL is simple to use it does require some knowledge of object orientated program methodology, querying patterns and a general understanding of relational modelling. 
- Storage - as PostgreSQL stores data in tabular form the amount memory required to hold the data can be significant. 
- Complexity - a normalised relational database model can be complex as the information is split across many tables. Keeping track of the relationships between tables can be tedious. The need for more standalone and joining tables can become necessary if the data stored within the database diversifies over time, which will compound the issue (IONOS 2023).
- Decreased performance as data size increases - over time, it is common for a database to become very large. As Postgres is a relational database, queries are often made across several tables. The ability to do this is a key reason for using a relational database in the first place; however, when the database is large, complex queries can have a slow response time, especially if many users are accessing the database simultaneously (IONOS 2023).


### R4. Identify and discuss the key functionalities and benefits of an ORM

Object Relational Mapping (ORM) connects an object orientated program to a relational database (Abba 2022). Relational databases have functionality to create, read, update and delete (CRUD) information stored in tables. The ability to perform these operations is a key reason for using a relational database. This functionality can be utilised by performing transitions with SQL on the command line, but it can be more convenient to have code written into a program to do this. For this reason, an ORM tool is used to allow for direct interaction between the database and an Object Orientation Programming (OOP) language (Abba 2022). 

OOP languages use objects to represent data. These consist of classes (blueprints outlining what information is needed to define the object) and their instances (objects with this information filled in). A RDBMS represents data in a tabular format (tables made up of rows and columns). The term ‘object-relational independence mismatch’ is used to describe the fundamental differences that exist between these two paradigms, including the use of dissimilar data structures, divergence in the way data is interacted with, and basic conceptual distinctions (Tina 2020). To make these two seperate things work together, we need an ORM tool.

The process of converting data from the database into an object is called hydration. This is done by converting values from columns in a table into object properties (Tina 2020). A table’s column attributes form the base of a class and the individual values contained within the column are transcribed to become the specific properties of a class instantiation. For this reason, ORM tools are language specific. This webserver application will use the ORM tool SQLAlchemy with the database adaptor/driver psycopg2 to enable the use of the OOP language python with a PostgreSQL database.

In addition to performing these key functionaries, some of the benefits of using an ORM include:

- Instead of writing lengthy SQL commands, methods from the ORM are used. An ORM has many built-in methods for performing transitions on the database. These methods are shorter to write thus reducing the volume of code needed to perform an operation and encourage DRY coding practices. Once a developer in familiar with the methods available for a particular ORM, they can reduce development time (Abba 2022). This increase in productive is additionally beneficial as it reduces the cost to develop software. 
- An ORM abstracts away some of the tedious workings of querying the database allowing programmer to focus on performing the tasks without having to think too much about how it happens.
- An ORM tool adds a layer of removal to SQL queries within the code, as explicit SQL commands are not used. Because of this, an application utilising ORM can be more secure against malicious SQL injection attacks by third parties (Admin Globaldots 2021, Abba 2022).
- ORM tools allow for queries to be stated but not executed until they are called i.e. the logic for querying a database can be outlined in the OOP language but is not used until it is needed. This is known as lazy-loading (Imperva 2022).


### R5. Document all endpoints for your API

This API is instructed to run on local host port 5000 by default. If you are using a different port for you local host, please update the post number by changing:

`
FLASK_RUN_PORT=5000
`

in the .flaskenv file to your chosen port number.


Please be aware that all example images contain an alias named url, which represents:

`
http://127.0.0.1:5000
`

All end point’s described here must begin with the local host URL.



**Home**

*Description:*

Home route.

*Method:*

GET

*URL:*

/

*Search Parameters:*

None

*Request Body Requirements:*

None

*Authentication Required:*

None

*Expected Response:*

Welcome message

*Example Request:*

![/](./docs/endpoints/home-url.png)

*Example Response:*

![/](./docs/endpoints/home-response.png)


**Register**

*Description:*

Register a new user

*Method:*

POST

*URL:*

/auth/register

*Search Parameters:*

None

*Request Body Requirements:*

first_name = user's first name. Datatype = string
surname = user's surname. Datatype = string
email = user's email address. Must be unique; user's cannot share an email address. Datatype = string
password = user's desired password. Must be exactly 8 characters long. Datatype = string.


![Register Request Body](./docs/endpoints/register-rbody.png)

*Authentication Required:*

None

*Expected Response:*

Message: "You have successfully registered."

*Example Request:*

![Register](./docs/endpoints/register-url.png)

*Example Response:*

![Register](./docs/endpoints/register-response.png)


**Login**

*Description:*

Login for an existing user. Returns a JSON Web Token that is required to access restricted routes.

*Method:*

POST

*URL:*

/auth/login

*Search Parameters:*

None

*Request Body Requirements:*

email = user's email address that was used to register. Datatype = string
password = user's password that was used to register. Datatype = string


![Login - Request Body](./docs/endpoints/login-rbody.png)

*Authentication Required:*

None

*Expected Response:*

User's first_name and JWT token

*Example Request:*

![Login - URL](./docs/endpoints/login-url.png)

*Example Response:*

![Login - Response](./docs/endpoints/login-response.png)


**All Users**

*Description:*

Allow a user with admin privileges to see all registered users.

*Method:*

GET

*URL:*

/auth/user/all

*Search Parameters:*

None

*Request Body Requirements:*

None

*Authentication Required:*

Bearer token required
Type: JWT

*Expected Response:*

List of all registered users.
User's details will contain user_id, first_name, surname and admin status.

*Example Request:*

![All Users - URL](./docs/endpoints/all-users-url.png)

*Example Response:*

![All Users - Response](./docs/endpoints/all-users-response.png)


**User by Email**

*Description:*

Allow a user to search for their details in the database with their email address

*Method:*

GET

*URL:*

/auth/user/{email}

*Search Parameters:*

{email} = user's email address

*Request Body Requirements:*

None

*Authentication Required:*

Bearer token required
Type: JWT

*Expected Response:*

User's details containing user_id, first_name, surname and admin status.

*Example Request:*

![User by Email - URL](./docs/endpoints/auth-email-url.png)

*Example Response:*

![User by Email - Response](./docs/endpoints/auth-email-response.png)


**Admin Status**

*Description:*

Allow a user with admin privileges to change the admin status of a user

*Method:*

PUT

*URL:*

/auth/register/admin/{user_id}

*Search Parameters:*

{user_id} = user_id of the user whose admin status is to be changed.

*Request Body Requirements:*

admin = True/False. Datatype = boolean


![Change Admin Status - Request Body](./docs/endpoints/admin-rbody.png)

*Authentication Required:*

Bearer token required
Type: JWT

*Expected Response:*

Message: "Your admin privileges have changed."

*Example Request:*

![Change Admin Status - URL](./docs/endpoints/admin-url.png)

*Example Response:*

![Change Admin Status - Response](./docs/endpoints/admin-response.png)


**Update User**

*Description:*

Allow a registered user to change their first_name, surname, email and password.

*Method:*

PUT

*URL:*

/auth/user/update

*Search Parameters:*

None

*Request Body Requirements:*

first_name = user's first name. Datatype = string
surname = user's surname. Datatype = string
email = user's email address. Must be unique; user's cannot share an email address. Datatype = string
password = user's desired password. Must be exactly 8 characters long. Datatype = string.


![Update User - Request Body](./docs/endpoints/update-user-rbody.png)

*Authentication Required:*

Bearer token required
Type: JWT

*Expected Response:*

Message: "You have successfully updated your information."

*Example Request:*

![Update User - URL](./docs/endpoints/update-user-url.png)

*Example Response:*

![Update User - Response](./docs/endpoints/update-user-response.png)


**Unregister User**

*Description:*

Allow users to unregister/remove themselves from the database

*Method:*

DELETE

*URL:*

/auth/user/unregister/{email}

*Search Parameters:*

{email} = the email the user is registered with

*Request Body Requirements:*

None

*Authentication Required:*

Bearer token required
Type: JWT

*Expected Response:*

Message:  "User registration has been removed."

*Example Request:*

![Delete User - URL](./docs/endpoints/delete-user-url.png)

*Example Response:*

![Delete User - Response](./docs/endpoints/delete-user-response.png)


**All Books**

*Description:*

Allow anyone to get a list of all the books in the database

*Method:*

GET

*URL:*

/books/

*Search Parameters:*

None

*Request Body Requirements:*

None

*Authentication Required:*
None

*Expected Response:*

List of all the books in the database.
Each book's details will contain book_id, title, isbn, length, first_publication_date, copies_published, nested author with published_name and nested publisher with publisher_name

*Example Request:*

![All Books](./docs/endpoints/books-url.png)

*Example Response:*

![All Books](./docs/endpoints/books-response.png)


**Book Search - Query String**

*Description:*

Allow anyone to search for books in the database using a query string to search by title, length, author_id or publisher_id.

*Method:*

GET

*URL:*

/books/search{query string}

*Search Parameters:*

{query string} = a query string to match up title with book title, length with book length, author_id to match with all books containing that author_id or publisher_id to match with all books containing that publisher_id.

A query string must begin with a question mark and be followed by the search parameter (e.g. title) = expected match (e.g. the title of the book). If a space is required it must be replaced with '%20'.


![Book Query String - Example URL](./docs/endpoints/book-query-example-url.png)

![Book Query String - Example URL 2](./docs/endpoints/book-query-example2.png)

*Request Body Requirements:*

None

*Authentication Required:*

None

*Expected Response:*

Books matching the query string parameters.
The book's details will contain book_id, title, isbn, length, first_publication_date, copies_published, nested author with published_name and nested publisher with publisher_name.

If the query was:

![Book Query String - Example URL 2](./docs/endpoints/book-query-example2.png)

The expected output would be:

![Book Query String - Response](./docs/endpoints/book-query-response.png)

*Example Request:*

![Book Query String - URL 2](./docs/endpoints/book-query-example-url2.png)

*Example Response:*

The expected response for the url example above is:

![Book Query String - Response to match URL](./docs/endpoints/book-query-response2.png)


**Book Search ID or ISBN - Query String**

*Description:*

Allow anyone to search for a book by the book_id or unique isbn.

**Please note that the ISBN numbers used in the existing entries in the database are ISBN10 numbers for the first edition printing of each book.

*Method:*

GET

*URL:*

/books/search/{query string}

*Search Parameters:*

{query string} = either the book_id or ISBN number.

A query string must begin with a question mark and be followed by the search parameter (e.g. isbn) = expected match (e.g. the book's isbn).

*Request Body Requirements:*

None

*Authentication Required:*

None

*Expected Response:*

Books matching the query string parameters.
The book's details will contain book_id, title, isbn, length, first_publication_date, copies_published, nested author with published_name and nested publisher with publisher_name.

*Example Request:*

![Book Query String - book_id URL](./docs/endpoints/book-search-id-url.png)

![Book Query String - isbn URL](./docs/endpoints/book-search-isbn-url.png)

*Example Response:*

![Book Query String - Response](./docs/endpoints/book-search-response.png)


**Add Book**

*Description:*

Allow a user with admin privileges to add a new book to the database

*Method:*

POST

*URL:*

/books/add

*Search Parameters:*

None

*Request Body Requirements:*

title = book title. Datatype: string
isbn = book's unique isbn10. Datatype:string
length = number of pages. Datatype: string
first_publication_date = date of first publication. Datatype: DateTime. Formatted as DD/MM/YYYY inside quotation marks
copies_published = number of copies published for the isbn number. Datatype: integer
author_id = foreign key - author_id. Datatype: integer
publisher_id = foreign key - publisher_id. Datatype: integer


![Add Book - Request Body](./docs/endpoints/add-book-rbody.png)

*Authentication Required:*

Bearer token required
Type: JWT

*Expected Response:*

Message: "You have added a book to the table."

*Example Request:*

![Add Book - Request](./docs/endpoints/add-book-url.png)

*Example Response:*

![Add Book - Response](./docs/endpoints/add-book-response.png)


**Update Book**

*Description:*

Allow a user with admin privileges to change the details for an existing book in the database

*Method:*

PUT

*URL:*

/books/update/{book_id}

*Search Parameters:*

{book_id} = the book_id for the book whose details are to be changed

*Request Body Requirements:*

title = book title. Datatype: string
isbn = book's unique isbn10. Datatype: string
length = number of pages. Datatype: string
first_publication_date = date of first publication. Datatype: DateTime. Formatted as DD/MM/YYYY inside quotation marks
copies_published = number of copies published for the isbn number. Datatype: integer
author_id = foreign key - author_id. Datatype: integer
publisher_id = foreign key - publisher_id. Datatype: integer


![Change Book - Request Body](./docs/endpoints/add-book-rbody.png)

*Authentication Required:*

Bearer token required
Type: JWT

*Expected Response:*

Message: "You have successfully updated the database."

*Example Request:*

![Change Book - URL](./docs/endpoints/update-book-url.png)

*Example Response:*

![Change Book - Response](./docs/endpoints/update-book-response.png)


**Delete Book**

*Description:*

Allow a user with admin privileges to delete an existing book from the database

*Method:*

DELETE

*URL:*

/books/delete/{book_id}

*Search Parameters:*

{book_id} = the book_id for the book to be deleted

*Request Body Requirements:*

None

*Authentication Required:*

Bearer token required
Type: JWT

*Expected Response:*

Message: "You have successfully removed this book and associated information from the database."

*Example Request:*

![Delete Book - URL](./docs/endpoints/delete-book-url.png)

*Example Response:*

![Delete Book - Response](./docs/endpoints/delete-book-response.png)


**All Movies**

*Description:*

Allow anyone to get a list of all the movies in the database

*Method:*

GET

*URL:*

/movies/

*Search Parameters:*

None

*Request Body Requirements:*

None

*Authentication Required:*

None

*Expected Response:*

List of all the movies in the database.
Each movies's details will contain movie_id, title, release_date, length in minutes, box_office_ranking, nested director with director_name, nested production company with name and nested book with the title of the book the movie was adapted from.

*Example Request:*

![All Movies](./docs/endpoints/movies-url.png)

*Example Response:*

![All Movies](./docs/endpoints/movies-response.png)


**Movie Search - Query String**

*Description:*

Allow anyone to search for movies in the database using a query string to search by title, director_id, production_company_id or book_id.

*Method:*

GET

*URL:*

/movies/search{query string}

*Search Parameters:*

{query string} = a query string to match up title with movie title, director_id to match with all movies containing that director_id, production_company_id to match with all movies containing that production_company_id or book_id to match with all movies adapted from the book with that book_id.

A query string must begin with a question mark and be followed by the search parameter (e.g. title) = expected match (e.g. the title of the movie). If a space is required it must be replaced with '%20'.


![Movie Query String - Example URL](./docs/endpoints/movies-query-url-example.png)

![Movie Query String - Example URL 2](./docs/endpoints/movies-query-url-example2.png)

*Request Body Requirements:*

None

*Authentication Required:*

None

*Expected Response:*

Movies matching the query string parameters.
Each movies's details will contain movie_id, title, release_date, length in minutes, box_office_ranking, nested director with director_name, nested production company with name and nested book with the title of the book the movie was adapted from.

If the query was:

![Movie Query String - Example URL 2](./docs/endpoints/movies-query-url-example2.png)

The expected output would be:

![Movie Query String - Response](./docs/endpoints/movies-query-response.png)

*Example Request:*

![Movie Query String - URL 2](./docs/endpoints/movie-query-url-3.png)

*Example Response:*

The expected response for the url example above is:

![Movie Query String - Response to match URL](./docs/endpoints/movie-query-response2.png)


**Movie Search - movie_id**

*Description:*

Allow anyone to search for movies in the database by the movie_id.

*Method:*

GET

*URL:*

/movies/search/{movie_id}

*Search Parameters:*

{movie_id} = the movie_id for the movie in the database

*Request Body Requirements:*

None

*Authentication Required:*

None

*Expected Response:*

The corresponding movie for the movie_id provided.
The movie's details will contain movie_id, title, release_date, length in minutes, box_office_ranking, nested director with director_name, nested production company with name and nested book with the title of the book the movie was adapted from.

*Example Request:*

![Movie ID - URL](./docs/endpoints/movie-id-url.png)

*Example Response:*

The expected response for the url example above is:

![Movie ID - Response](./docs/endpoints/movie-id-response.png)


**Movie Search - Length**

*Description:*

Allow anyone to search for all movies in the database and order them by length in descending order.

*Method:*

GET

*URL:*

/movies/search/length

*Search Parameters:*

None

*Request Body Requirements:*

None

*Authentication Required:*

None

*Expected Response:*

All movies in the database in descending order from the longest to the shortest.
The movie's details will contain movie_id, title, release_date, length in minutes, box_office_ranking, nested director with director_name, nested production company with name and nested book with the title of the book the movie was adapted from.

*Example Request:*

![Movie length - URL](./docs/endpoints/movies-length-url.png)

*Example Response:*

The expected response for the url example above is:

![Movie length - Response](./docs/endpoints/movies-length-response.png)

**Movie Search - Ranking**

*Description:*

Allow anyone to search for all movies in the database and order them in descending order by box office ranking.

*Method:*

GET

*URL:*

/movies/search/ranking

*Search Parameters:*

None

*Request Body Requirements:*

None

*Authentication Required:*

None

*Expected Response:*

All movies in the database in order of box office ranking, from highest to lowest.
The movie's details will contain movie_id, title, release_date, length in minutes, box_office_ranking, nested director with director_name, nested production company with name and nested book with the title of the book the movie was adapted from.

*Example Request:*

![Movie ranking - URL](./docs/endpoints/movies-ranking-url.png)

*Example Response:*

The expected response for the url example above is:

![Movie length - Response](./docs/endpoints/movies-ranking-response.png)


**Add Movie**

*Description:*

Allow a user with admin privileges to add a new movie to the database

*Method:*

POST

*URL:*

/movies/add

*Search Parameters:*

None

*Request Body Requirements:*

title = book title. Datatype: string
release_date = date of release. Datatype: DateTime. Formatted as DD/MM/YYYY inside quotation marks
box_office_ranking = international box office ranking at date of addition to database. Datatype: integer
length = length of move in minutes. Datatype: string
director_id = foreign key - director_id. Datatype: integer
production_id = foreign key - production_id. Datatype:integer
book_id = foreign key - book_id. Datatype: integer


![Add Movie - Request Body](./docs/endpoints/add-movie-rbody.png)

*Authentication Required:*

Bearer token required
Type: JWT

*Expected Response:*

Message:  "You have added a movie to the table."

*Example Request:*

![Add Movie - Request](./docs/endpoints/add-movies-url.png)

*Example Response:*

![Add Movie - Response](./docs/endpoints/add-movies-response.png)


**Update Movie**

*Description:*

Allow a user with admin privileges to change the details for an existing movie in the database

*Method:*

PUT

*URL:*

/movies/update/{movie_id}

*Search Parameters:*

{movie_id} = the movie_id for the book whose details are to be changed

*Request Body Requirements:*

title = book title. Datatype: string
release_date = date of release. Datatype: DateTime. Formatted as DD/MM/YYYY inside quotation marks
box_office_ranking = international box office ranking at date of addition to database. Datatype: integer
length = length of move in minutes. Datatype: string
director_id = foreign key - director_id. Datatype: integer
production_id = foreign key - production_id. Datatype:integer
book_id = foreign key - book_id. Datatype: integer


![Change Movie - Request Body](./docs/endpoints/add-movie-rbody.png)

*Authentication Required:*

Bearer token required
Type: JWT

*Expected Response:*

Message:  "You have successfully updated the database."

*Example Request:*

![Update Movie - Request](./docs/endpoints/update-movie-url.png)

*Example Response:*

![Update Movie - Response](./docs/endpoints/update-movie-response.png)


**Delete Movie**

*Description:*

Allow a user with admin privileges to delete an existing movie from the database

*Method:*

DELETE

*URL:*

/movies/delete/{movie_id}

*Search Parameters:*

{movie_id} = the movie_id for the movie to be deleted

*Request Body Requirements:*

None

*Authentication Required:*

Bearer token required
Type: JWT

*Expected Response:*

Message: "You have successfully removed this movie and associated information from the database."

*Example Request:*

![Delete Movie - URL](./docs/endpoints/delete-movie-url.png)

*Example Response:*

![Delete Movie - Response](./docs/endpoints/delete-movie-response.png)


**All Authors**

*Description:*

Allow anyone to get a list of all the authors in the database

*Method:*

GET

*URL:*

/authors/

*Search Parameters:*

None

*Request Body Requirements:*

None

*Authentication Required:*

None

*Expected Response:*

List of all the authors in the database.
Each authors's details will contain author_id, title, pen_name, collaboration and collaborator_name

*Example Request:*

![All Authors](./docs/endpoints/authors-url.png)

*Example Response:*

![All Authors](./docs/endpoints/authors-response.png)


**Author Search - Query String**

*Description:*

Allow anyone to search for authors in the database using a query string to search by published_name, collaboration (true/false), pen_name (true/false) or collaborator_name.

*Method:*

GET

*URL:*

/authors/search{query string}

*Search Parameters:*

{query string} = a query string to match up title with published_name, collaboration (true/false), pen_name (true/false) or the name of a collaborator with collaborator_name.

A query string must begin with a question mark and be followed by the search parameter (e.g. title) = expected match (e.g. the title of the movie). If a space is required it must be replaced with '%20'.


![Author Query String - Example URL](./docs/endpoints/author-query-url.png)

*Request Body Requirements:*

None

*Authentication Required:*

None

*Expected Response:*

Movies matching the query string parameters.
Each movies's details will contain movie_id, title, release_date, length in minutes, box_office_ranking, nested director with director_name, nested production company with name and nested book with the title of the book the movie was adapted from.

If the query was:

![Author Query String - Example URL 2](./docs/endpoints/author-query-url.png)

The expected output would be:

![Author Query String - Response](./docs/endpoints/author-query-result.png)

*Example Request:*

![Author Query String - URL 2](./docs/endpoints/author-query-url2.png)

*Example Response:*

The expected response for the url example above is:

![Author Query String - Response to match URL](./docs/endpoints/author-query-result2.png)


**Author Search - author_id**

*Description:*

Allow anyone to search for an author in the database by their author_id.

*Method:*

GET

*URL:*

/authors/search/{author_id}

*Search Parameters:*

{author_id} = the author_id for the author in the database

*Request Body Requirements:*

None

*Authentication Required:*

None

*Expected Response:*

The corresponding author for the author_id provided.
The authors's details will contain author_id, title, pen_name, collaboration and collaborator_name

*Example Request:*

![Author ID - URL](./docs/endpoints/author-id-url.png)

*Example Response:*

The expected response for the url example above is:

![Author ID - Response](./docs/endpoints/author-query-result2.png)


**Add Author**

*Description:*

Allow a user with admin privileges to add a new author to the database

*Method:*

POST

*URL:*

/authors/add

*Search Parameters:*

None

*Request Body Requirements:*

published_name = published name of the author. Datatype: string
pen_name = whether a name was used or not. Datatype: boolean
collaborator_name = name of the collaborator or null. Datatype: string
collaboration = whether the book was written with a collaborator or not. Datatype: boolean


![Add Author - Request Body](./docs/endpoints/new-author-rbody.png)

*Authentication Required:*

Bearer token required
Type: JWT

*Expected Response:*

Message:  "You have added an author to the table."

*Example Request:*

![Add Author - Request](./docs/endpoints/new-author-url.png)

*Example Response:*

![Add Author - Response](./docs/endpoints/new-author-response.png)


**Update Author**

*Description:*

Allow a user with admin privileges to change the details for an existing author in the database

*Method:*

PUT

*URL:*

/authors/update/{author_id}

*Search Parameters:*

{author_id} = the author_id for the author whose details are to be changed

*Request Body Requirements:*

published_name = published name of the author. Datatype: string
pen_name = whether a name was used or not. Datatype: boolean
collaborator_name = name of the collaborator or null. Datatype: string
collaboration = whether the book was written with a collaborator or not. Datatype: boolean


![Change Author - Request Body](./docs/endpoints/new-author-rbody.png)

*Authentication Required:*

Bearer token required
Type: JWT

*Expected Response:*

Message:  "You have successfully updated this author in the database."

*Example Request:*

![Update Author - Request](./docs/endpoints/update-author-url.png)

*Example Response:*

![Update Author - Response](./docs/endpoints/update-author-response.png)


**All Publishers**

*Description:*

Allow anyone to get a list of all the publishers in the database

*Method:*

GET

*URL:*

/publishers/

*Search Parameters:*

None

*Request Body Requirements:*

None

*Authentication Required:*

None

*Expected Response:*

List of all the publishers in the database.
Each publishers's details will contain publisher_id and publisher_name

*Example Request:*

![All Publishers](./docs/endpoints/publishers-url.png)

*Example Response:*

![All Publishers](./docs/endpoints/publishers-response.png)


**Publishers Search - publisher_name**

*Description:*

Allow anyone to search for publishers in the database using the name of the publisher

*Method:*

GET

*URL:*

/publishers/search/name/{publisher_name}

*Search Parameters:*

{publisher_name} = name of the publisher in the database.

If a space is required it must be replaced with '%20'.

*Request Body Requirements:*

None

*Authentication Required:*

None

*Expected Response:*

Publishers matching the publisher_name.
The publishers's details will contain the publisher_name and publisher_id.

*Example Request:*

![Publisher Name - URL](./docs/endpoints/publisher-name-url.png)

*Example Response:*

The expected response for the url example above is:

![Publisher Name - Response](./docs/endpoints/publisher-name-response.png)


**Publisher Search - publisher_id**

*Description:*

Allow anyone to search for a publisher in the database by their publisher_id.

*Method:*

GET

*URL:*

/publishers/search/{publisher_id}

*Search Parameters:*

{publisher_id} = the publisher_id for the publisher in the database

*Request Body Requirements:*

None

*Authentication Required:*

None

*Expected Response:*

The corresponding publisher for the publisher_id provided.
The publishers's details will container the publisher_name and publisher_id.

*Example Request:*

![Publisher ID - URL](./docs/endpoints/publisher-id-url.png)

*Example Response:*

![Publisher ID - Response](./docs/endpoints/publisher-name-response.png)


**Add Publisher**

*Description:*

Allow a user with admin privileges to add a new publisher to the database

*Method:*

POST

*URL:*

/publishers/add

*Search Parameters:*

None

*Request Body Requirements:*

publisher_name = name of the publisher. Datatype: string


![Add Publisher - Request Body](./docs/endpoints/publisher-add-rbody.png)

*Authentication Required:*

Bearer token required
Type: JWT

*Expected Response:*

Message:  "You have added a publisher to the table."

*Example Request:*

![Add Publisher - Request](./docs/endpoints/publishser-add-url.png)

*Example Response:*

![Add Publisher - Response](./docs/endpoints/publisher-add-response.png)


**Update Publisher**

*Description:*

Allow a user with admin privileges to change the details for an existing publisher in the database

*Method:*

PUT

*URL:*

/publishers/update/{publisher_id}

*Search Parameters:*

{publisher_id} = the publisher_id for the publisher whose details are to be changed

*Request Body Requirements:*

publisher_name = name of the publisher. Datatype: string


![Change Publisher - Request Body](./docs/endpoints/publisher-add-rbody.png)

*Authentication Required:*

Bearer token required
Type: JWT

*Expected Response:*

Message:  "You have successfully updated the database."

*Example Request:*

![Update Publisher - Request](./docs/endpoints/publisher-update-url.png)

*Example Response:*

![Update Publisher - Response](./docs/endpoints/publisher-update-response.png)


**All Directors**

*Description:*

Allow anyone to get a list of all the directors in the database

*Method:*

GET

*URL:*

/directors/

*Search Parameters:*

None

*Request Body Requirements:*

None

*Authentication Required:*

None

*Expected Response:*

List of all the directors in the database.
Each directors's details will contain director_id and director_name

*Example Request:*

![All Directors](./docs/endpoints/directors-url.png)

*Example Response:*

![All Directors](./docs/endpoints/directors-response.png)


**Directors Search - director_name**

*Description:*

Allow anyone to search for directors in the database using the name of the director

*Method:*

GET

*URL:*

/directors/search/name/{director_name}

*Search Parameters:*

{director_name} = name of the director in the database.

If a space is required it must be replaced with '%20'.

*Request Body Requirements:*
None

*Authentication Required:*

None

*Expected Response:*

Directors matching the director_name.
The directors's details will container the director_name and director_id.

*Example Request:*

![Director Name - URL](./docs/endpoints/directors-name-url.png)

*Example Response:*

The expected response for the url example above is:

![Director Name - Response](./docs/endpoints/directors-name-response.png)


**Director Search - director_id**

*Description:*

Allow anyone to search for a publisher in the database by their director_id.

*Method:*

GET

*URL:*

/directors/search/{director_id}

*Search Parameters:*

{director_id} = the director_id for the director in the database

*Request Body Requirements:*

None

*Authentication Required:*

None

*Expected Response:*

The corresponding director for the director_id provided.
The director's details will contain the director_name and director_id.

*Example Request:*

![Director ID - URL](./docs/endpoints/director-id-url.png)

*Example Response:*

![Director ID - Response](./docs/endpoints/directors-name-response.png)


**Add Director**

*Description:*

Allow a user with admin privileges to add a new director to the database

*Method:*

POST

*URL:*

/directors/add

*Search Parameters:*

None

*Request Body Requirements:*

director_name = name of the director. Datatype: string


![Add Director - Request Body](./docs/endpoints/director-add-rbody.png)

*Authentication Required:*

Bearer token required
Type: JWT

*Expected Response:*

Message:  "You have added a director to the table."

*Example Request:*

![Add Director - Request](./docs/endpoints/director-add-url.png)

*Example Response:*

![Add Director - Response](./docs/endpoints/director-add-response.png)


**Update Director**

*Description:*

Allow a user with admin privileges to change the details for an existing director in the database

*Method:*

PUT

*URL:*

/directors/update/{director_id}

*Search Parameters:*

{director_id} = the director_id for the director whose details are to be changed

*Request Body Requirements:*

director_name = name of the director. Datatype: string


![Change Author - Request Body](./docs/endpoints/publisher-add-rbody.png)

*Authentication Required:*

Bearer token required
Type: JWT

*Expected Response:*

Message:  "You have successfully updated the database."

*Example Request:*

![Update Director - Request](./docs/endpoints/director-update-url.png)

*Example Response:*

![Update Director - Response](./docs/endpoints/director-update-response.png)


**All Production Companies**

*Description:*

Allow anyone to get a list of all the production companies in the database

*Method:*

GET

*URL:*

/production/

*Search Parameters:*

None

*Request Body Requirements:*

None

*Authentication Required:*

None

*Expected Response:*

List of all the production companies in the database.
Each production companies's details will contain production_id and production_name

*Example Request:*

![All Production Companies](./docs/endpoints/production-url.png)

*Example Response:*

![All Production Companies](./docs/endpoints/production-response.png)


**Production Company Search - production_name**

*Description:*

Allow anyone to search for production companies in the database using the name of the production company

*Method:*

GET

*URL:*

/production/search/name/{production_name}

*Search Parameters:*

{production_name} = name of the production company in the database.

If a space is required it must be replaced with '%20'.

*Request Body Requirements:*

None

*Authentication Required:*

None

*Expected Response:*

Production companies matching the production_id.
The production companies details will contain the production_name and production_id.

*Example Request:*

![Production Company Name - URL](./docs/endpoints/production-name-url.png)

*Example Response:*

The expected response for the url example above is:

![Production Company Name - Response](./docs/endpoints/production-name-response.png)


**Production Company Search - production_id**

*Description:*

Allow anyone to search for a production company in the database by their production_id.

*Method:*

GET

*URL:*

/production/search/{production_id}

*Search Parameters:*

{production_id} = the production_id for the production company in the database

*Request Body Requirements:*

None

*Authentication Required:*

None

*Expected Response:*

The corresponding production company for the production_id provided.
The production companies details will contain the production_name and production_id.

*Example Request:*


![Production ID - URL](./docs/endpoints/production-id-url.png)

*Example Response:*

![Production ID - Response](./docs/endpoints/production-id-response.png)


**Add Production Company**

*Description:*

Allow a user with admin privileges to add a new production company to the database

*Method:*

POST

*URL:*

/production/add

*Search Parameters:*

None

*Request Body Requirements:*

name = name of the production company. Datatype: string


![Add Production Company - Request Body](./docs/endpoints/add-production-rbody.png)

*Authentication Required:*

Bearer token required
Type: JWT

*Expected Response:*

Message:  "You have added a production company to the table."

*Example Request:*

![Add Production Company - Request](./docs/endpoints/add-production-url.png)

*Example Response:*

![Add Production Company - Response](./docs/endpoints/add-production-response.png)


**Update Production Company**

*Description:*

Allow a user with admin privileges to change the details for an existing production company in the database

*Method:*

PUT

*URL:*

/production/update/{production_id}

*Search Parameters:*

{production_id} = the production_id for the production company whose details are to be changed

*Request Body Requirements:*

name = name of the production company. Datatype: string


![Change Production Company - Request Body](./docs/endpoints/update-response-rbody.png)

*Authentication Required:*

Bearer token required
Type: JWT

*Expected Response:*

Message:  "You have successfully updated the database."

*Example Request:*

![Update Production - Request](./docs/endpoints/update-prodction-url.png)

*Example Response:*

![Update Production Company - Response](./docs/endpoints/update-production-response.png)


**Read - Average Rating**

*Description:*

Allow anyone to get the average rating of a book from the database by querying the read table.

*Method:*

GET

*URL:*

/read/rating/{book_id}

*Search Parameters:*

{book_id} = the book_id of the book you wish see the average rating for.

*Request Body Requirements:*

None

*Authentication Required:*

None

*Expected Response:*

Message: "The average rating of this book is: {average rating}"

*Example Request:*

![Average Rating](./docs/endpoints/read-rating-url.png)

*Example Response:*

![Average Rating](./docs/endpoints/read-rating-response.png)

**User's Read Ratings**

*Description:*

Allow a user to get a list of the books they have reviewed.

*Method:*

GET

*URL:*

/read/{user_id}

*Search Parameters:*

{user_id} = the user_id of the user wishing to their reviews

*Request Body Requirements:*

None

*Authentication Required:*

Bearer token required
Type: JWT

*Expected Response:*

List of all the user's reviews from the read table
Each review's details will contain the read_id, rating, nested book with title and nested user with first_name and surname

*Example Request:*

![Read ID](./docs/endpoints/read-id-url.png)

*Example Response:*

![Read ID](./docs/endpoints/read-id-response.png)


**Add Read Rating**

*Description:*

Allow a user with admin privileges to add a new review to the database

*Method:*

POST

*URL:*

/read/add

*Search Parameters:*

None

*Request Body Requirements:*

book_id = book_id for the book to review. Datatype: integer
rating = user's rating for the book. Datatype: integer


![Add Review - Request Body](./docs/endpoints/rating-add-rbody.png)

*Authentication Required:*

Bearer token required
Type: JWT

*Expected Response:*

Message:  "You have added a review."

*Example Request:*

![Add Review - Request](./docs/endpoints/rating-add-url.png)

*Example Response:*

![Add Review - Response](./docs/endpoints/rating-add-response.png)


**Update Read Rating**

*Description:*

Allow a user to the change the rating in one of their own reviews

*Method:*

PUT

*URL:*

/read/update/{read_id}

*Search Parameters:*

{read_id} = the read_id for the review the user wishes to change
 
*Request Body Requirements:*

rating = user's rating for the book. Datatype: integer


![Update Review - Request Body](./docs/endpoints/update-review-rbody.png)

*Authentication Required:*

Bearer token required
Type: JWT

*Expected Response:*

Message:  "You have successfully updated your rating for this book."

*Example Request:*

![Update Review - Request](./docs/endpoints/update-review-url.png)

*Example Response:*

![Update Review - Response](./docs/endpoints/update-review-response.png)


**Delete Read Review**

*Description:*

Allow a user to the delete one of their own reviews

*Method:*

DELETE

*URL:*

/read/delete/{read_id}

*Search Parameters:*

{read_id} = the read_id for the review to be deleted

*Request Body Requirements:*

None

*Authentication Required:*

Bearer token required
Type: JWT

*Expected Response:*

Message: "You have successfully deleted your review for this book."

*Example Request:*

![Delete Review - URL](./docs/endpoints/delete-review-url.png)

*Example Response:*

![Delete REview - Response](./docs/endpoints/delete-review-response.png)


**Watched - Average Rating**

*Description:*

Allow anyone to get the average rating of a movie from the database by querying the watched table.

*Method:*

GET

*URL:*

/watched/rating/{movie_id}

*Search Parameters:*

{movie_id} = the movie_id of the movie you wish see the average rating for.

*Request Body Requirements:*

None

*Authentication Required:*

None

*Expected Response:*

Message: "The average rating of this movie is: {average rating}"

*Example Request:*

![Average Rating](./docs/endpoints/watched-rating-url.png)

*Example Response:*

![Average Rating](./docs/endpoints/watched-rating-response.png)


**User's Watched Ratings**

*Description:*

Allow a user to get a list of the movies they have reviewed.

*Method:*

GET

*URL:*

/watched/{user_id}

*Search Parameters:*

{user_id} = the user_id of the user wishing to their reviews

*Request Body Requirements:*

None

*Authentication Required:*

Bearer token required
Type: JWT

*Expected Response:*

List of all the user's reviews from the watched table
Each review's details will contain the watched_id, rating, nested movie with title and nested user with first_name and surname

*Example Request:*

![Watched ID](./docs/endpoints/watched-id-url.png)

*Example Response:*

![Watched ID](./docs/endpoints/watched-id-response.png)


**Add Watched Rating**

*Description:*

Allow a user with admin privileges to add a new review to the database

*Method:*

POST

*URL:*

/watched/add

*Search Parameters:*

None

*Request Body Requirements:*

movie_id = movie_id for the movie to review. Datatype: integer
rating = user's rating for the book. Datatype: integer


![Add Review - Request Body](./docs/endpoints/watched-add-rbody.png)

*Authentication Required:*

Bearer token required
Type: JWT

*Expected Response:*

Message:  "You have added a review."

*Example Request:*

![Add Review - Request](./docs/endpoints/watched-add-url.png)

*Example Response:*

![Add Review - Response](./docs/endpoints/rating-add-response.png)

**Update Watched Rating**

*Description:*

Allow a user to the change the rating in one of their own reviews

*Method:*

PUT

*URL:*

/watched/update/{watched_id}

*Search Parameters:*

{watched_id} = the watched_id for the review the user wishes to change
 
*Request Body Requirements:*

rating = user's rating for the movie. Datatype: integer


![Update Review - Request Body](./docs/endpoints/update-review-rbody.png)

*Authentication Required:*

Bearer token required
Type: JWT

*Expected Response:*

Message:  "You have successfully updated your rating for this movie."

*Example Request:*

![Update Review - Request](./docs/endpoints/watched-update-url.png)

*Example Response:*

![Update Review - Response](./docs/endpoints/watched-update-response.png)


**Delete Watched Review**

*Description:*

Allow a user to the delete one of their own reviews

*Method:*

DELETE

*URL:*

/watched/delete/{watched_id}

*Search Parameters:*

{watched_id} = the watched_id for the review to be deleted

*Request Body Requirements:*

None

*Authentication Required:*

Bearer token required
Type: JWT

*Expected Response:*

Message: "You have successfully deleted your review for this movie."

*Example Request:*

![Delete Review - URL](./docs/endpoints/watched-delete-url.png)

*Example Response:*

![Delete REview - Response](./docs/endpoints/watched-delete-response.png)

### R6. An ERD for your app

![Stephen King DB ERD](./docs/stephen_king_db_erd.jpg)

### R7. Detail any third party services that your app will use

Flask: This application will be built on Flask, which is a python web application framework and is imported as a python module. Flask is a Webserver Gateway Interface (WSGI), meaning that it controls communication between servers and our python application (Python Basics 2021). 

Flask-SQLAlchemy: This application will utilise the ORM tool SQLAlchemy to control the relationships between our python objects and the tables in our PostgreSQL database. To use SQLAlchemy in this project, we will be using Flask-SQLAlchemy, which will be imported as a python module. Flask-SQLAlchemy is a specific extension for Flask to enable the use of SQLAlchemy. It provides the full range of functionality offered by SQLAlchemy but simplifies the execution of this specifically for a Flask application by providing handy defaults and helper methods for some common transactions performed on a relational database (Pallets 2010). The Model method from Flask-SQLAlchemy will be used to create models for this project. One benefit of using this method to create our models is that, although a custom name can be specified, it will automatically set the class name converted to camel case as table name in the database if we do not do this. The Column method will be used to define the columns in our tables so we can set a variable name as the column name, declare a primary key as an auto-incrementing integer that Flask-SQLAlchemy will manage for us, and specify a datatype (Integer, String, Text, DataTime, Float, Boolean, PickleType or LargeBinary) for each column to ensure data integrity is maintained (Pallets 2010). The Model method also allows us to outline the relationships between tables and define them as one-to-many by using the relationship() function in conjunction with the ForeignKey method or many-to-many by using the Tables and ForeignKey methods(Pallets 2010). 

Psycopg2: Psycopg2 is a popular database adapter used to connect Flask with a PostgreSQL database and enable communication between the two to be written in Python (PyPi 2022) and will be imported as a module for use in this project.

Flask-marshmallow: Flask-marshmallow is an integration tool used to enable Flask to work with the python library marshmallow. Python objects cannot be directly converted to json format, for this we need to use marshmallow. Marshmallow is used to convert complex datatypes (such as json formatted data) and objects into datatypes and objects that python can work with directly (Loria 2022). In our application, it will be used to validate data and serialise (convert) python objects into serialised objects which can be formatted in json, and to convert them back again (deserialisation). Flask-marshmallow is will also be used to generate schemas from our models. Schemas control what information from the database tables is displayed to the user. The flask-marshmallow method Schema will be used when defining the schemas for our project as this will allow us to use fields to specify exactly which fields (columns) to expose and the Nested method will be utilised imbed schemas for Foreign Keys within the output (Loria 2022).

Marshmallow-sqlalchemy: Marshmallow-sqlalchemy is used to integrate the python module marshmallow with flask-sqlalchemy (Loria 2023).

Flask-jwt-extended: JSON Web Tokens are used to authenticate a user in secure way. Instead of sending a user’s credentials with a request, a JWT is sent instead and this is verified against a secret key that is stored as an environment variable (Coder Academy 2023). The python package, flask-jwt-extended will be used in this project to enable us to do use JWTs for user authentication. The function create_access_token() will be used to generate a JWT, get_jwt_identity() will be used to verify a user is authenticated, and jwt_required() will be used to specify a route requires a JWT to access it (Loria 2022). These functions will be used with the JWTManager method to secure routes that have imbedded logic to make changes on our database. 

Flask-bcrypt: hashing is a way to encrypt sensitive information, such as passwords. As new technologies continue to be developed, so do malicious programs that can be used to hack applications with the goal of creating damage and/or stealing personal information (Countryman 2011). Because of this, a secure way to make an encryption more difficult to crack is needed. Bcrypt hashing will be used in this application because it is a ‘de-optimised’ hashing method, designed to be more tedious to crack. The python module flask-bcrypt will be imported for this and the function generate_password_hash({password}).decode(‘utf-8’) to secure passwords and assign them to a variable. 

os: The os library provides various operating system dependent functionalities. This project will use the enrivon.get() function from the os package to retrieve a user’s environment variables for the JWT secret key and database url. 

DateTime: The python package DateTime is used to create datetime objects and format them (Python Software Foundation 2023). The timedelta() function from the DateTime  library will be used to set and track expiry times for JSON Web Tokens used in our application. 


### R8. Describe your projects models in terms of the relationships they have with each other

There are nine models used in this project. As this API uses PostgreSQL, a ORDBMS, SQLAlchemy, a ORM tool, will be used to construct the relationships between models/tables. Foreign Keys are used to imbed a Primary Key from another table into a model, establishing a relationship between the two tables, where relevant data is stored in one table but is available in another. The SQLAlchemy relationship function is then used to further define the relationship and establish it as a one-to-one, one-to-many, many-to-one or many-to-many relationship. Join tables are required for many-to-many relationships and act an intermediary to connect a many-to-many relationship in the form of two one-to-many relationships, where the join table sits on the many side of the relation. The relationships are established as parent-child relations.

**User Model:**
The User model holds a user’s id, first name, surname, unique email address, password and admin status. It has a zero to many relationship with the Read and Watched models; a user can make zero or many entries in the Read and Watched tables. The relationship function is used to solidify the User model as the parent class, and uses the backref parameter to specify the zero-to-many relationship in one direction only. Cascading delete is used to remove all entries from the Read and Watched tables, if a correlating user entry is removed from the database. 

`
watched = db.relationship(‘Watched’, backref=‘user’, cascade=‘all, delete’)
read = db.relationship(‘Read’, backref=‘user’, cascade=‘all, delete’)
`

**Read Model:**
The Read model holds a user’s rating for a book and the id. The book_id from the Book table is used to specify which book the user is rating and user_id from the User table is used to specify which user owns the rating. It has many to zero relationships with the User and Book models and is a joining table for a many-to-many relationship between the User and Book models. Foreign Keys consisting of the Primary Keys for the User and Book tables are used to solidify the Read model as a child of the User and Book tables.

`
book_id = db.Column(db.Integer, db.ForeignKey(‘book.id’), nullable=False)
user_id = db.Column(db.Integer, db.ForeignKey(‘user.id’), nullable=False)
`

**Book Model:**
The Book models holds a book’s id, title, unique isbn number, length in pages, first publication date and the number of copies printed for that edition (corresponding with the isbn number). It has a zero to many relationship with the Read and Movie tables; a user can review zero or many books via the Read table and a book can be adapted into zero or many movies. The relationship function is used to solidify the Book model as the parent class to the Read model, and uses the backref parameter to specify the zero-to-many relationship with the Read model in one direction only. The relationship stated with the Movie model also establishes the Book model as the parent of the Movie class, and also uses the backref parameter, but to reference to the movie itself, rather than the book; because, the relationship is allowed to be bi-directional through the use the overlaps and single_parent parameters on the same relationship statement in the Movie table (that references back to the Book model); thus the relationship is allow to back flow so that if a book entry is removed from the table, all associated movie entries are also removed but the deletion of a movie entry will not remove the associated book entry.

`
read = db.relationship(‘Read’, backref=‘book’, cascade=‘all, delete-orphan’)
movie = db.relationship(‘Movie’, backref=‘movie’, cascade=‘all, delete-orphan’)
`

The Book model has many-to-one relationships with the with the Author and Publisher models. Foreign Keys consisting of the Primary Keys for the Author and Publisher models are used to solidify the Book table as the child of the Author and Publisher tables.

`
author_id = db.Column(db.Integer, db.ForeignKey(‘author.id’), nullable=False)
publisher_id = db.Column(db.Integer, db.ForeignKey(‘publisher.id’), nullable=False)
`

**Author Model:**
The Author model holds an author’s id, published name, collaboration status, pen name status and the name of a collaborator. It has a one-to-many relationship with the Book model; an author can belong to one or many books. The relationship function is used to solidify the Author model as the parent class, and uses the backref parameter to specify the one-to-many relationship in one direction only.

`
author = db.relationship(‘Book’, backref=‘author’)
`

**Publisher Model:**
The Publisher model holds a publisher’s id and name. It has a one-to-many relationship with the Book model; a publisher can belong to one or many books. The relationship function is used to solidify the Publisher model as the parent class, and uses the backref parameter to specify the one-to-many relationship in one direction only.

`
publisher = db.relationship(‘Book’, backref=‘publisher’)
`

**Watched Model:**
The Watched model holds a user’s rating for a movie and the id. The movie_id from the Movie table is used to specify which movie the user is rating and user_id from the User table is used to specify which user owns the rating. It has many to zero relationships with the User and Movie models and is a joining table for a many-to-many relationship between the User and Movie models. Foreign Keys consisting of the Primary Keys for the User and Movie tables are used to solidify the Watched model as a child of the User and Movie tables.

`
movie_id = db.Column(db.Integer, db.ForeignKey(‘movie.id’), nullable=False)
user_id = db.Column(db.Integer, db.ForeignKey(‘user.id’), nullable=False)
`

**Movie Model:**
The Movie models holds a movie’s id, title, release date, length in minutes and box office ranking. It has a zero to many relationship with the Watched table; a user can review zero or many movies via the Watched table. It has a many-to-one relationship with the Book table; a movie can be adapted from one book only. The relationship function is used to solidify the Move model as the parent class to the Watched model, and uses the backref parameter to specify the zero-to-many relationship with the Watched model in one direction only.

The relationship stated with the Book model establishes the Movie model as a child of the Book class. The relationship with the Book model is copied from the relationship established between the Book and Movie models in the Book model via a backref to the Movie model. The relationship statement in the Movie model to the Book model uses the overlaps and single_parent=True parameters to map directly to the relationship already established relationship in the Book model and defines the relationship between a movie and a book as a one-to-one relationship for the purpose of deletion. This allows for an associated entry to be removed from the Movie table when a book is deleted, but prevents associated book entries from being removed if an entry is deleted from the Movie table. 

`
watched = db.relationship(‘Watched’, backref=‘movie’, cascade=‘all, delete-orphan’)
book = db.relationship(‘Book’, overlaps=‘movie,movie’, single_parent=True, cascade=‘all, delete-orphan’)
`

The Movie model has many-to-one relationships with the with the Director and ProductionCompany models. Foreign Keys consisting of the Primary Keys for the Director and ProductionCompany models are used to solidify the Movie table as the child of the Director and ProductionCompany tables.

`
director_id = db.Column(db.Integer, db.ForeignKey(‘director.id’), nullable=False)
production_company_id = db.Column(db.Integer, db.ForeignKey(‘production_company.id’), nullable=False)
`

**Director Model:**
The Director model holds a dictior’s id and name. It has a one-to-many relationship with the Movie model; a director can belong to one or many movies. The relationship function is used to solidify the Director model as the parent class, and uses the backref parameter to specify the one-to-many relationship in one direction only.

`
director = db.relationship(‘Movie’, backref=‘director’)
`

**ProductionCompany Model:**
The ProductionCompany model holds a production companies id and name. It has a one-to-many relationship with the Movie model; a production company can belong to one or many movies. The relationship function is used to solidify the ProductionCompany model as the parent class, and uses the backref parameter to specify the one-to-many relationship in one direction only.

`
production = db.relationship(‘Movie’, backref=‘production’)
`


### R9. Discuss the database relations to be implemented in your application

Users:

- User will be required to register and login to access the Read and Watched tables. 
- Users will only be able to create a single account as their email address will need to be unique.
- Users will need to provide their full name and an email address, and set a password that is 8 characters long. 
- Users may be an admin. Only users with admin privileges will be able to modify the Books and Movies tables.
- Once logged in, a user can modify only their own entries in the Read and Watched tables. Users with admin privileges will not be able to modify entries in these tables; only the author of the entry can change it.
- Users has a zero or many relationship with Read. A user may not read any books, but may read a book without watching the movie adaptation.
- Users has a many to many relationship with Books. A user can read many books.
- Users has a zero or many relationship with Watched. A user may not watch any movies, but does not have to have read the original book to have seen the movie adaptation. 
- Users has a many to many relationship with Movies. A user can watch many movies.

Books:

- Books table will be public. A user does not need to be registered or logged in to view the content in this table. Only a user with admin privilege can modify this table.
- Books has a many to many relationship with Users. Many books can be read by many users.
- Books has a zero to many relationship with Read. A book may not be read.
- Books has a zero to many relationship with Movies. One book can be made into many movies, but may not be adapted into a movie at all.
- Books has a one to one relationship with Authors. One book must have one author. 
- Books has a one to one relationship with Publishers. One book must have one publisher.

Movies:

- Movies table will be public. A user does not need to be registered or logged in to view the content in this table. Only a user with admin privilege can modify this table.
- Movies has a many to many relationship with Users. Many movies can be watched by many users.
- Movies has a zero to many relationship with Watched. A movie may not be watched.
- Movies has a one to one relationship with Books. One movie must be based on one book.
- Movies has a one to one relationship with Directors. One movie must have one director.
- Movies has a one to one relationship with ProductionCompanies. One movie is produced by one production company.

Read:

- Once logged in, a user can review leave a rating between 1 - 10 for a book. 
- The Read table can only be viewed by logged in Users. Users can only modify their own entries.
- Read is a joining table for the many to many relationship between Users and Books.
- Read has a one to one relationship with Users. An entry in the Read table must belong to one user.
- Read has a one to one relationship with Books. An entry in the Read table must be about one book.

Watched:

- Once logged in, a user can review leave a rating between 1 - 10 for a movie.
- The Watched table can only be viewed by logged in Users. Users can only modify their own entries.
- Watched is a joining table for the many to many relationship between Users and Movies.
- Watched has a one to one relationship with Users. An entry in the Watched table must belong to one user.
- Watched has a one to one relationship with Movies. An entry in the Watched table must be about one movie.

Authors:

- Authors has a one to many relationship with Books. One author can write many books.
- A book can be collaborative work.
- An author can use a pen name.

Publishers:

- Publishers has a one to many relationship with Books. One publisher can publish many books.

Directors:

- Directors has a one to many relationship with Movies. One director can direct many movies.

ProductionCompanies:

- ProductionCompanies has a one to many relationship with Movies. One production company can produce many movies.


### R10. Describe the way tasks are allocated and tracked in your project

To structure the implementation of each step in undertaking this assessment, I have used a Trello board in the kanban project management style to help me visualise the steps I need to complete and manage my time in doing so.

**My Trello board is available here:**

[Trello Board](https://trello.com/b/LinWh3iO/api-webserver-project)

All tasks are allocated to myself, as this is an individual project.There are four categories: To Do, In Progress, Completed and Nice to Have. Each card contains a step to undertake, details of the actions to be completed, and a timeframe. The timeframe for completing each step is represented with a coloured label. The key for the labels is as follows:

- Green: can be completed in under 30 minutes
- Yellow: can be completed in under 2 hours
- Orange: can be completed in 2 - 4 hours.

I have broken the steps down into enough detail that no card should take longer than 4 hours to complete. All cards held equal weight in terms of their priority. The To Do tasks were placed from the top of the category down in the anticipated order of competition, so that tasks that needed to be done before another could be started were undertaken first. When a task was started in was moved to the In Progress tab, and moved again to the Completed tab once it was finished. As I was utilising a kanban project management style, tasks that were moved to the Completed category could be moved back to the In Progress tab, if a review of the completed work was needed. Many tasks could be In Progress at the same time.

The Nice to Have category contained only cards to add in entries for all published Stephen Books and all the movie adaptations that have been made from these. The plan was to include only the five oldest novels and movies in the minimal viable product (MVP) so as to ensure enough time to focus on getting the body of the assessment completed, and add the whole lot only if there was enough time to do so before the submission date. 

This planning method was highly successful in allowing me visualise the remaining workload, allocate appropriate time for each task and complete the project without forgetting to do any particular task.
The following screenshots were taken as I worked my through the project. Some show what is contain on an individual card, while others show overall progress. All of the cards can be accessed on Trello via the link provided above.

Start of the project

![Trello Board Start of Project](./docs/Trello-start1.png)
![Trello Board Start of Project](./docs/Trello-start2.png)
![Trello Board Start of Project](./docs/Trello-start3.png)
![Trello Board Start of Project](./docs/Trello-start4.png)
![Trello Board Start of Project](./docs/Trello-start5.png)
![Trello Board Start of Project](./docs/Trello-start6.png)

Questions for the readme.md file were answered, where possible, prior to beginning to code out the API

![Trello Board Readme in Progress](./docs/Trello-readme-qs.png)
![Trello Board Readme in Progress](./docs/Trello-readme-qs2.png)

Cards were made and completed for each section of the API to reflect the required MVC structure

![Trello Board Update - Start of Coding](./docs/Trello-coding1.png)
![Trello Board Update - Start of Coding - Working on Models](./docs/Trello-coding2-models.png)
![Trello Board Update - Working on Commands](./docs/Trello-coding3-commands.png)
![Trello Board Update - Working on Schemas](./docs/Trello-coding4-schemas.png)
![Trello Board Update - Working on Controllers](./docs/Trello-coding5-controllers.png)
![Trello Board Update - Working on Controllers and Error Handling](./docs/Trello-coding6-controllers.png)
![Trello Board Update - Controllers and Error Handling Completed](./docs/trello-update-controllers-errors.png)

Cards were marked off after coding was "completed" and the last of the documentation for the README was added
![Trello Board Update - R5 and R8 Underway](./docs/readme-finalisation.png)
![Trello Board Update - Endpoints and Model Relationships Completed](./docs/endpoints-relations-completed.png)
![Trello Board Update - Database Set Up and Flask Instructions/Read over README](./docs/setup-final-read.png)
![Trello Board Update - Ready to Submit](./docs/submit.png)

## References 

Abba, Ihechikara Vincent (2022) *What is an ORM – The Meaning of Object Relational Mapping Database Tools
*, Free Code Camp. Accessed at: https://www.freecodecamp.org/news/what-is-an-orm-the-meaning-of-object-relational-mapping-database-tools/ (Accessed on 26 February 2023)

Admin Globaldots (2021) *8 best practices to prevent SQL injection attacks*, GlobalDots. Accessed at: https://www.globaldots.com/resources/blog/8-best-practices-to-prevent-sql-injection-attacks/ (Accessed on 27 February 2023)

Coder Academy (2023) *JWT Authentication*, Flask Authentication, Coder Academy, Ed Lessons. Accessed at: https://edstem.org/au/courses/10081/lessons/27620/slides/195163 (Accessed on 1 March 2023)

Countryman, Max (2011) *Flask-Bcrypt*, Read the Docs. Accessed at: https://flask-bcrypt.readthedocs.io/en/1.0.1/ (Accessed on 1 March 2023)

Imperva (2022) *Lazy Loading*, Imperva Learning Center. Accessed at: https://www.imperva.com/learn/performance/lazy-loading/ (Accessed on 27 February 2023)

IONOS (2023) *PostgreSQL: a closer look at the object-relational database management system*, IONOS Digital Guide. Accessed at: https://www.ionos.com/digitalguide/server/know-how/postgresql/ (Accessed on 25 February 2023)

Loria, Steven (2022) *Basic Usage*, Read the Docs. Accessed at: https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/ (Accessed on 1 March 2023)

Loria, Steven (2022) *flask-marshmallow*, Read the Docs. Accessed at: https://flask-marshmallow.readthedocs.io/en/latest/ (Accessed on 1 March 2023)

Loria, Steven (2022) *marshmallow: simplified object serialization*, Read the Docs. Accessed at: https://marshmallow.readthedocs.io/en/stable/ (Accessed on 28 February 2023)

Loria, Steven (2023) *marshmallow-sqlalchemy*, Read the Docs. Accessed at: https://marshmallow-sqlalchemy.readthedocs.io/en/latest/ (Accessed on 28 February 2023)

MariaDB (2023) *What is ACID Compliance in a Database? What It Means and Why You Should Care*, MariaDB. Accessed at: https://mariadb.com/resources/blog/acid-compliance-what-it-means-and-why-you-should-care/ (Accessed on 25 February 2023)

Pallets (2010) *Declaring Models*, Pallets Projects. Accessed at: https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/ (Accessed on 1 March 2023)

Pallets (2010) *Flask-SQLAlchemy*, Pallets Projects. Accessed at: https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/ (Accessed on 28 February 2023)

PyPi (2022) *psycopg2 - Python-PostgreSQL Database Adapter*, Python Software Foundation. Accessed at: https://pypi.org/project/psycopg2/ (Accessed on 28 February 2023)

Python Basics (2021) *What is Flask Python*, Python Basics. Accessed at: https://pythonbasics.org/what-is-flask-python/ (Accessed on 28 February 2023)

Python Software Foundation (2023) *datetime — Basic date and time types*, Python Docs. Accessed at: https://docs.python.org/3/library/datetime.html (Accessed on 1 March 2023)

Tina (2020) *Introduction to Object-relational mapping: the what, why, when and how of ORM*, .dev. Accessed at: https://dev.to/tinazhouhui/introduction-to-object-relational-mapping-the-what-why-when-and-how-of-orm-nb2 (Accessed on 26 February 2023)