import os

import json
import redis

from flask import Blueprint, jsonify, request, url_for, make_response, abort
from flask_cors import cross_origin

deals = Blueprint('deals', __name__)

if 'VCAP_SERVICES' in os.environ: 
	vcap_services = json.loads(os.environ['VCAP_SERVICES'])

	for key, value in vcap_services.iteritems():   # iter on both keys and values
		if key.find('redis') > 0:
		  redis_info = vcap_services[key][0]
		
	cred = redis_info['credentials']
	uri = cred['uri'].encode('utf8')
  
	redis = redis.StrictRedis.from_url(uri + '/0')
else:
  redis = redis.StrictRedis(host=os.getenv('REDIS_HOST', 'localhost'), port=os.getenv('REDIS_PORT', 6379), db=0)
    
@deals.errorhandler(400)
def not_found(error):
  return make_response(jsonify( { 'error': 'Bad request' }), 400)

@deals.errorhandler(404)
def not_found(error):
  return make_response(jsonify( { 'error': 'Not found' }), 404)

@deals.route('/api/v1.0/deals/alldeals/<hotelid>', methods=['GET'])
@cross_origin()
def alldeals(hotelid):
  deals = []

  deal = '{"provider": "Booking.com", "price": 2000, "currency": "rupees"}'
  deals.append(deal)

  deal = '{"provider": "Expedia", "price": 2698, "currency": "rupees"}'
  deals.append(deal)

  return jsonify({ 'deals': deals }), 200