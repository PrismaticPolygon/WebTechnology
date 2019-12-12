from app import create_app, db, cli
from app.models import User, Book, Rating

app = create_app()
cli.register(app)

@app.shell_context_processor
def make_shell_context():

    return {'db': db, 'User': User, 'Book': Book, 'Rating': Rating}