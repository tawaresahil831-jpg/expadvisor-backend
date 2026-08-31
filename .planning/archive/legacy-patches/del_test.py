import sys
sys.path.insert(0, '/Users/sahiltaware415/expadvisor-backend')
from app import create_app
from app.extensions import db
from app.models.experience import Experience
from app.models.like import Like
from app.models.comment import Comment
from app.models.notification import Notification

app = create_app()
with app.app_context():
    test_exps = Experience.query.filter(Experience.title.ilike('%Test Experience%')).all()
    for e in test_exps:
        Like.query.filter_by(experience_id=e.experience_id).delete()
        Comment.query.filter_by(experience_id=e.experience_id).delete()
        Notification.query.filter_by(experience_id=e.experience_id).delete()
        db.session.delete(e)
    db.session.commit()
    print(f"Deleted {len(test_exps)} test experiences.")
