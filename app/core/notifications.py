from app.models.notification import Notification

def create_notification(db, message, type_):
    notif = Notification(message=message, type=type_)
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif 