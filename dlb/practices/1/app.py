from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd 

app = Flask(__name__)

try:
    with open('best_wine_quality_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    with open('scaler.pkl', 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)
    print("Модель и стандартизатор успешно загружены.")
except FileNotFoundError:
    print("Ошибка: Убедитесь, что 'best_wine_quality_model.pkl' и 'scaler.pkl' находятся в той же директории, что и app.py")
    model = None
    scaler = None
except Exception as e:
    print(f"Произошла ошибка при загрузке модели или стандартизатора: {e}")
    model = None
    scaler = None

@app.route('/predict', methods=['POST'])
def predict():
    if model is None or scaler is None:
        return jsonify({'error': 'Модель или стандартизатор не загружены. Проверьте логи сервера.'}), 500

    try:
        data = request.get_json(force=True) 

        expected_columns = ['fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar',
                            'chlorides', 'free sulfur dioxide', 'total sulfur dioxide', 'density',
                            'pH', 'sulphates', 'alcohol']

        input_data_df = pd.DataFrame([data])

        for col in expected_columns:
            if col not in input_data_df.columns:
                input_data_df[col] = 0.0

        input_data_df = input_data_df[expected_columns]

        scaled_features = scaler.transform(input_data_df)

        prediction = model.predict(scaled_features)

        return jsonify({'quality_prediction': int(prediction[0])})

    except Exception as e:
        return jsonify({'error': f'Ошибка обработки запроса: {e}'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)