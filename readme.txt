Introduction
============

A short example of how to setup to use Tornado's authentication decorator.
The /list/ GET is protected by this decorator and its content should only be
available to logged in users.


Module requirements
===================

pip install tornado sqlalchemy

Note: SQLAlchemy is not used much at this point, but is setup to use
a sqlite DB if necessary.

Session and User info can be retrieved from the DB, if the model is defined.
This is to come later.

