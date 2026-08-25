import os
import logging
import json
import sys
from flask import Flask, render_template, request, jsonify
from config import config

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'name': record.name,
            'message': record.getMessage(),
        }
        if record.exc_info:
            log_record['exception'] = self.formatException(record.exc_info)
        return json.dumps(log_record, ensure_ascii=False)

def setup_logging(app):
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

def create_app(config_name='default'):
    # Échec rapide si une dépendance de parsing manque (12-Factor: fail fast)
    from services.file_parser import verifier_dependances
    verifier_dependances()

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    setup_logging(app)

    from routes import register_routes
    register_routes(app)
    
    return app

app = create_app(os.environ.get('FLASK_ENV', 'default'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
