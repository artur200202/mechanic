from flask import Flask
from .models import db
from .extensions import ma, limiter, cache
from .blueprints.customers import customer_bp
from .blueprints.mechanics import mechanic_bp
from .blueprints.service_tickets import service_ticket_bp


def create_app(config_name):
    
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')
    
    # initialize extensions (plugging them in)
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    #Register blueprints
    app.register_blueprint(customer_bp, url_prefix='/customers')
    app.register_blueprint(mechanic_bp, url_prefix='/mechanics')
    app.register_blueprint(service_ticket_bp, url_prefix='/service_tickets')
    
    return app