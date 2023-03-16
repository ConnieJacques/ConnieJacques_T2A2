from sqlalchemy import exc
from marshmallow import exceptions
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
        except exc.NoSuchTableError:
            return abort(404, description="Table not found. Please seed the database.")
        except KeyError:
            return abort(400, description="Field missing from request body.")
        except exc.NoResultFound:
            return abort(404, "No results found. Please check you are using a valid query method.")
        except exc.DataError:
            return abort(400, "No results found. Please check you are using a valid query method.")
        except AssertionError:
            return abort(400, description="New entry already exist in the database.")
        # except exceptions.ValidationError:
        #     return abort(400, description="Error in request body. Please check for spelling mistakes. Ensure all required fields are included. Dates must be formatted as DD-MM-YYYY")
        except exc.IntegrityError:
            return abort(400, description="Data entered in the request body matches an existing entry.")
        except AttributeError:
            return abort(400, "No results found. Please check your query is accurate.")
        # except exc.UnprocessableContentError:
            # return abort(422, message="Invalid bearer token.") 
    return function