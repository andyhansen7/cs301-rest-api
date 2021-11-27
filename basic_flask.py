
# Imports
from flask import Flask, jsonify, redirect
from pymongo import MongoClient
from bson.json_util import ObjectId
import json

class IDJsonEncoder(json.JSONEncoder):
  def default(self, object):
    if isinstance(object, ObjectId):
      return str(object)
    return super(IDJsonEncoder, self).default(object)

# Create PyMongo Client
client = MongoClient()
db = client.db
collection = db['CS301']

# Create Flask App
app = Flask(__name__)

# Tell app to use our custom encoder, because ObjectIDs are non-serializable with the default json encoder
app.json_encoder = IDJsonEncoder


# Default landing page
@app.route('/')
def index():
  return 'RESTful API Implementation - Andy Hansen, CS301-002, Fall 2021'


# Homework Query Responses
@app.route('/HW<question_number>')
def show_homework_query_response(question_number):
  # Determine which problem to solve
  if question_number == '1':
    return str(collection.count())

  elif question_number == '2':
    docs = []
    for doc in collection.find({'milestones.stoneable.name': 'Zoho'}, {'twitter_username': 1, 'category_code': 1, '_id': 0}):
      docs.append(doc)
    return jsonify(docs)

  elif question_number == '3':
    docs = []
    for doc in collection.find(None, {'twitter_username': 1, '_id': 0}):
      docs.append(doc)
    return jsonify(docs)

  elif question_number == '4':
    docs = []
    for doc in collection.find({'number_of_employees': {'$gte': 5000}, 'founded_year': {'$gt': 2000}}, {'name': 1, 'founded_year': 1, 'number_of_employees': 1, 'total_money_raised': 1, '_id': 0}):
      docs.append(doc)
    return jsonify(docs)

  elif question_number == '6':
    docs = []
    for doc in collection.find({'founded_month': { '$exists': False } }, { '_id': 1 }):
      docs.append(doc)
    return jsonify(docs)

  elif question_number == '7':
    return str(collection.count({'funding_rounds.raised_amount': { '$gt': 5000000 } } ))

  elif question_number == '9':
    docs = []
    for doc in collection.find({ '$or':[ { 'founded_year': { '$gt': 2012 } },{ 'founded_year': { '$lt': 1805 } } ] }, { '_id': 0, 'name': 1,
'founded_year': 1 }).sort([('founded_year', -1), ('name', 1)]):
      docs.append(doc)
    return jsonify(docs)

  elif question_number == '10':
    docs = []
    for doc in collection.find({'founded_year': 1800, 'products.name': { '$exists': True } }, { 'name': 1, 'homepage_url': 1, 'number_of_employees': 1, 'products.name': 1, '_id': 0 }):
      docs.append(doc)
    return jsonify(docs)

  elif question_number == '12':
    return str(collection.find({'screenshots.attribution': None }).count())

  elif question_number == '13':
    res = collection.find(None, {'number_of_employees': 1, '_id': 0}).sort([('number_of_employees', -1)])
    return jsonify(res[0])

  else:
    return 'Invalid homework problem provided: ' + question_number


# Company Search Method
@app.route('/company/<company_name>')
def show_company_search(company_name):
  # Search for company
  docs = []
  for d in collection.find({ 'name': str(company_name) }):
    docs.append(d)

  # Sanity checks
  if len(docs) < 1:
    return 'No Company Found'

  else:
    return jsonify(docs)


# List Companies By Year Founded
@app.route('/list_companies_by_year/<founded_year>')
def list_companies_by_year_founded(founded_year):
  # Search for companies founded in the provided year
  docs = []
  for d in collection.find({'founded_year': int(founded_year)}):
    docs.append(d)

  # Sanity checks
  if int(founded_year) < 1000 or int(founded_year) > 9999:
    return str(founded_year) + ' is not a 4-digit number'

  elif len(docs) < 1:
    return 'No Companies Founded In The Year ' +  str(founded_year)

  else:
    return jsonify(docs)


# Count Companies By Year Founded
@app.route('/count_companies_by_year/<founded_year>')
def count_companies_by_year_founded(founded_year):
  # Count companies founded in the provided year
  count = collection.find({'founded_year': int(founded_year)}).count()

  # Sanity checks
  if int(founded_year) < 1000 or int(founded_year) > 9999:
    return str(founded_year) + ' is not a 4-digit number'

  elif count < 1:
    return 'No Companies Founded In The Year ' +  str(founded_year)

  else:
    return str(count)


# Redirect To Crunchbase
@app.route('/crunchbase/redirect/<company_name>')
def redirect_to_crunchbase(company_name):
  # Search for company
  docs = []
  for d in collection.find({ 'name': str(company_name) }):
    docs.append(d)

  # Sanity checks
  if len(docs) < 1:
    return 'No Company Found'

  else:
    url = str(docs[0]['crunchbase_url'])
    return redirect(url, code=302)
  