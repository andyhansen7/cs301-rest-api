
# Imports
from flask import Flask, jsonify
from pymongo import MongoClient
from bson.json_util import ObjectId
import json

class MyEncoder(json.JSONEncoder):

  def default(self, obj):
    if isinstance(obj, ObjectId):
      return str(obj)
    return super(MyEncoder, self).default(obj)

  # Create PyMongo Client
client = MongoClient() #connects to the local host, default port mongo server (which is what we have!)
db = client.db
collection = db['CS301']

# Create Flask App
app = Flask(__name__)
app.json_encoder = MyEncoder

@app.route('/')
def index():
  return 'REST API Implementation - Andy Hansen'

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
  elif len(docs) > 1:
    return 'Multiple companies found, something is very wrong'
  else:
    return jsonify(docs[0])

