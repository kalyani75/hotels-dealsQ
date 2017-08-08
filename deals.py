import os
import json

import sys
import time

from collections import defaultdict

from flask import Blueprint, jsonify, request, url_for, make_response, abort
from flask_cors import cross_origin

deals = Blueprint('deals', __name__)

from main import db
from main import dealsmodel
from main import searchqueue

@deals.errorhandler(400)
def not_found(error):
  return make_response(jsonify( { 'error': 'Bad request' }), 400)

@deals.errorhandler(404)
def not_found(error):
  return make_response(jsonify( { 'error': 'Not found' }), 404)

def getdeals(sessionid):
  query = dealsmodel.query.join(searchqueue, dealsmodel.hotelid == searchqueue.hotelid).add_columns(dealsmodel.id, dealsmodel.agency, 
   dealsmodel.hotelid, dealsmodel.roomtype, dealsmodel.fromdt, dealsmodel.todt, dealsmodel.price, dealsmodel.active)
  dealresults = query.filter(searchqueue.sessionid == sessionid).all()

  deals = []
  for result in dealresults:
    deal = {}

    deal['id'] = int(result.id)
    deal['agency'] = result.agency.encode("utf-8")
    deal['hotelid'] = int(result.hotelid)
    deal['roomtype'] = result.roomtype.encode("utf-8")
    deal['fromdt'] = str(result.fromdt)
    deal['todt'] = str(result.todt)
    deal['price'] = int(result.price)
    deal['active'] = int(result.active)

    deals.append(deal)

  db.session.remove()
  return deals

@deals.route('/api/v1.0/deals/alldeals', methods=['GET'])
@cross_origin()
def alldeals():
  deals = getdeals(request.args.get('sessionid'))
  return jsonify({ 'deals': deals })

@deals.route('/api/v1.0/deals/dealsbyhotel', methods=['GET'])
@cross_origin()
def dealsbyhotel():
  deals = getdeals(request.args.get('sessionid'))
  hoteldict = defaultdict(defaultdict)

  for deal in deals: 
    hoteldict[deal['hotelid']] = []

  for deal in deals: 
    hoteldict[deal['hotelid']].append(deal)

  return jsonify(hoteldict)

@deals.route('/api/v1.0/deals', methods=['POST'])
@cross_origin()
def createdeal():
  if not request.json or not 'price' in request.json or not 'id' in request.json:
    abort(400)
  
  deal = {
    'id': request.json['id'],
    'agency': request.json['agency'],
    'hotelid': request.json['hotelid'],    
    'roomtype': request.json['roomtype'],
    'fromdt': request.json['fromdt'].encode("utf-8"),
    'todt': request.json['todt'].encode("utf-8"),
    'price': request.json['price'],
    'active': request.json['active'],    
  }
  print deal
  newdeal = dealsmodel(deal['id'], deal['agency'], deal['hotelid'], deal['roomtype'], deal['fromdt'], deal['todt'], deal['price'], deal['active'])
  db.session.add(newdeal);

  db.session.commit()
  db.session.remove()

  return jsonify({ 'deal': deal }), 201  