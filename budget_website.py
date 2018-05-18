from app import app, db
from app.models import User, Budget, LineItem, Spending

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Budget': Budget, 'LineItem': LineItem, 'Spending': Spending}
