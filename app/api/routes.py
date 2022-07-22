from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Sports, sport_schema, sports_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'wee':'oohh'}

@api.route('/sports', methods = ['POST'])
@token_required
def create_sport(current_user_token):
    sport = request.json['sport']
    genders = request.json['genders']
    games = request.json['games']
    season = request.json['season']
    ages = request.json['ages']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    sport = Sports(sport, genders, games, season, ages, user_token=user_token)

    db.session.add(sport)
    db.session.commit()

    response = sport_schema.dump(sport)
    return jsonify(response)

@api.route('/sports', methods = ['GET'])
@token_required
def get_sport(current_user_token):
    a_user = current_user_token.token
    sports = Sports.query.filter_by(user_token = a_user).all()
    response = sports_schema.dump(sports)
    return jsonify(response)

# Optional, (might not work)
# @api.route('/sports/<id>', methods = ['GET'])
# @token_required
# def get_single_sport(current_user_token, id):
#    sports = Sports.query.get(id)
#    response = sport_schema.dump(sports)
#        return jsonify(response)

@api.route('/sports/<id>', methods = ['GET', 'PUT'])
@token_required
def update_sport(current_user_token, id):
    sport = Sports.query.get(id)
    sport.sport = request.json['sport']
    sport.genders = request.json['genders']
    sport.games = request.json['games']
    sport.season = request.json['season']
    sport.ages = request.json['ages']
    sport.user_token = current_user_token.token

    db.session.commit()
    response = sport_schema.dump(sport)
    return jsonify(response)

@api.route('/sports/<id>', methods = ['DELETE'])
@token_required
def delete_sport(current_user_token, id):
    sport = Sports.query.get(id)
    db.session.delete(sport)
    db.session.commit()
    response = sport_schema.dump(sport)
    return jsonify(response)