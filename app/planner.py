from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import distinct
from app.database import SessionLocal
from app.models import Space, Task, Event, User
from app.metrics import ACTIVE_SPACES_PERCENT, USER_RETENTION_PERCENT

def calculate_metrics():
    db = SessionLocal()
    try:
        now = datetime.now()
        week_ago = now - timedelta(days=7)

        all_spaces = db.query(Space.id).all()
        total_spaces_count = len(all_spaces)
        if total_spaces_count > 0:
            active_count = 0
            for (s_id,) in all_spaces:
                created = db.query(Task).filter(Task.space_id == s_id, Task.created_at >= week_ago).count()
                completed = db.query(Event).filter(Event.space_id == s_id, Event.event_type == "TASK_COMPLETED", Event.created_at >= week_ago).count()
                active_people = db.query(distinct(Event.user_id)).filter(Event.space_id == s_id, Event.created_at >= week_ago).count()

                if created > 3 and completed > 3 and active_people > 1:
                    active_count += 1
            
            ACTIVE_SPACES_PERCENT.set((active_count / total_spaces_count) * 100)

        def get_retention(days):
            start_cohort = now - timedelta(days=days + 1)
            end_cohort = now - timedelta(days=days)
            cohort_users = db.query(User.id).filter(User.created_at >= start_cohort, User.created_at < end_cohort).all()
            
            if not cohort_users: 
                return 0.0
            
            cohort_ids = [u[0] for u in cohort_users]
            active_today = db.query(distinct(Event.user_id)).filter(
                Event.user_id.in_(cohort_ids), 
                Event.created_at >= (now - timedelta(days=1))
            ).count()
            
            return (active_today / len(cohort_ids)) * 100

        USER_RETENTION_PERCENT.labels(period="2_days").set(get_retention(2))
        USER_RETENTION_PERCENT.labels(period="7_days").set(get_retention(7))

    except Exception as e:
        print(f"[METRICS SCHEDULER ERROR]: {e}")
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(calculate_metrics, 'interval', minutes=15, next_run_time=datetime.now())
    scheduler.start()