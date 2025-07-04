from app.extension import csrf
from flask import Blueprint

api_csrf_exempt = Blueprint('api_csrf_exempt', __name__)

# This blueprint can be used to register CSRF-exempt API endpoints if needed.
