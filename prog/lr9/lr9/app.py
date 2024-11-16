from eve import Eve
from flask import request, jsonify
from flask_migrate import Migrate
from auth import JWTTokenFactoryHMAC
from bonus import BonusObserver
from migrations import db, User, Transaction
from middleware import token_required

app = Eve()

db.init_app(app)
migrate = Migrate(app, db)

factory = JWTTokenFactoryHMAC()

# Роут для регистрации пользователя
@app.route('/auth/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    
    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "User already exists"}), 400

    new_user = User(username=username)
    new_user.set_password(password=password)
    db.session.add(new_user)
    db.session.commit()

    # Используем фабрику для создания токена
    token = factory.create_token(user_id=new_user.id)
    
    return jsonify({"message": "User registered successfully", "access_token": token}), 201


@app.route('/auth/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401

    # Используем фабрику для создания токена
    token = factory.create_token(user_id=user.id, algorithm="HS256")

    return jsonify(access_token=token)


@app.route('/users/<user_id>/bonus', methods=['GET'])
@token_required
def get_bonus(current_user, user_id):
    if str(current_user) != str(user_id):
        return jsonify({"message": "Permission denied"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "bonus_level": user.bonus_level,
        "cashback_percentage": user.cashback_percentage
    })


@app.route('/users/<user_id>/transactions', methods=['POST'])
@token_required
def add_transaction(current_user, user_id):
    if str(current_user) != str(user_id):
        return jsonify({"message": "Permission denied"}), 403

    amount = request.json.get('amount')
    if not amount or amount <= 0:
        return jsonify({"message": "Amount must be a positive value"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Добавляем транзакцию и обновляем бонусы через Observer
    transaction = Transaction(user_id=user_id, amount=amount)
    db.session.add(transaction)

    observer = BonusObserver(user)
    observer.update(amount)

    db.session.commit()

    return jsonify({
        "message": "Transaction added",
        "new_bonus_level": user.bonus_level,
        "cashback_percentage": user.cashback_percentage
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
