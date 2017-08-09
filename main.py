import os

from flask import Flask
from flask_cors import CORS

from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

from deals import deals
app.register_blueprint(deals, url_prefix='/hotels.com')

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

if 'VCAP_SERVICES' in os.environ: 
  vcap_services = json.loads(os.environ['VCAP_SERVICES'])

  uri = ''
  for key, value in vcap_services.iteritems():   # iter on both keys and values
	  if key.find('mysql') > 0 or key.find('cleardb') > 0:
	    mysql_info = vcap_services[key][0]
		
	    cred = mysql_info['credentials']
	    uri = cred['uri'].encode('utf8')
  
  app.config['SQLALCHEMY_DATABASE_URI'] = uri 
else:
  app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@mysql:3306/sys'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class dealsmodel(db.Model):
  __tablename__ = "deals"

  id = db.Column(db.Integer, primary_key = True)
  agency = db.Column(db.String(256))
  hotelid = db.Column(db.Integer)
  roomtype = db.Column(db.String(128))
  fromdt = db.Column(db.Date)
  todt = db.Column(db.Date)
  price = db.Column(db.Integer)
  active = db.Column(db.Integer)

  def __init__(self, id, agency, hotelid, roomtype, fromdt, todt, price, active):
    self.id = id
    self.agency = agency
    self.hotelid = hotelid
    self.roomtype = roomtype
    self.fromdt = fromdt
    self.todt = todt
    self.price = price
    self.active = active

class searchqueue(db.Model):
  __tablename__ = "searchqueue"

  id = db.Column(db.Integer, primary_key = True)
  sessionid = db.Column(db.String(512))
  hotelid = db.Column(db.Integer)

  def __init__(self, sessionid, hotelid):
    self.sessionid = sessionid
    self.hotelid = hotelid

  def __repr__(self):
    return '<Row %r %r>' % self.sessionid, self.hotelid

port = os.getenv('PORT', '9013')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port), debug=True)