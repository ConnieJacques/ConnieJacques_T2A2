from sqlalchemy import exc
from flask import abort
from functools import wraps


# Decorator to handle most errors
def exception_handler(func):
    # Wrap function
    @wraps(func)
    def function(*args, **kwargs):
        try:
            # Call and return the function
            return func(*args, **kwargs)
        # Return helpful error messages, if function triggers an error
        except exc.DataError:
            return abort(400, description="Invalid parameter in query string")
        except exc.IntegrityError:
            return abort(400, description="Data entered in the request body matches an existing entry.")
        except exc.DatabaseError:
            return abort(404, description="PostgreSQL database connection not found.")
        except exc.NoSuchTableError:
            return abort(404, description="Table not found. Please seed the database.")
        except KeyError:
            return abort(400, description="Field missing from request body.")
        except exc.NoResultFound:
            return abort(404, "No results found. Please check you are using a valid query method.")
        except AssertionError:
            return abort(400, description="New entry already exist in the database.")
        except AttributeError:
            return abort(400, "No results found. Please check your query is accurate.")
    return function