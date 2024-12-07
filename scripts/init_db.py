from app import db, create_app
from app.models import User, Project, Image
import os

def init_db():
    app = create_app()
    
    # Ensure the upload directory exists
    upload_dir = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    with app.app_context():
        # Drop all existing tables
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        # Create a test user (optional)
        test_user = User(email='test@example.com')
        test_user.set_password('password123')
        db.session.add(test_user)
        
        # Create a sample project (optional)
        sample_project = Project(
            name='Sample Project',
            description='This is a sample project for testing.',
            user=test_user
        )
        db.session.add(sample_project)
        
        db.session.commit()
        
        print('Database initialized successfully!')

if __name__ == '__main__':
    init_db()