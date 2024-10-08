#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)
#  a class that inherits from Resource
class Home(Resource):
    def get(self):
        # creating a response dict
        response_dict = {
            "message": "Welcome to the Newsletter RESTful API",
        }
        # creating and returning a response
        response = make_response(response_dict, 200)
        return response
    pass

#  adding the resource for the Home class
api.add_resource(Home, "/")

#  a class that inherits from Resource
class Newsletters(Resource):
    #  a get method to retrieve all newsletters from the database
    def get(self):
        #  creating a list of all the newsletters
        newsletters_dict = [newsletter.to_dict() for newsletter in Newsletter.query.all()]
        #  creating and returning a respose
        response = make_response(newsletters_dict, 200)
        return response


    #  a post method to create records to the database
    def post(self):
        # creating a new dictionary
        new_newsletter = Newsletter(
            title = request.form["title"],
            body = request.form["body"]
        )
        #  adding and commiting the new newsletter to the database
        db.session.add(new_newsletter)
        db.session.commit()

        # using to dict to make the new newsletter to a dictionary
        newsletter_dict = new_newsletter.to_dict()

        #  creating and returning a response 
        response = make_response(newsletter_dict, 201)
        return response
    pass

# adding a resource for the Newsletter class
api.add_resource(Newsletters, "/newsletters")

# creating a class called NewsLetterById that inherits from Resource
class NewsLetterById(Resource):
    #  creating a get method- gets a newsletter based on the id
    def get(self, id):
        # querying the database and filtering by the id
        newsletter = Newsletter.query.filter_by(id = id).first()
        # using to_dict() to make the newsletter to a dictionary
        newsletter_dict = newsletter.to_dict()
        # creating and returning a response
        response = make_response(newsletter_dict, 200)
        return response
    pass

#  adding a resource for the NewsLetterById class
api.add_resource(NewsLetterById, "/newsletters/<int:id>")

if __name__ == '__main__':
    app.run(port=5555, debug=True)
