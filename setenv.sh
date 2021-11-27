export FLASK_ENV=development
export FLASK_APP=flask_mongo.py

echo "Flask environment is: ${FLASK_ENV}"
echo "Flask app is: ${FLASK_APP}"

flask run