from prometheus_client import Counter, Histogram, Gauge

TASKS_CREATED = Counter(
    "colivin_tasks_created_total", 
    "Total created tasks (including recurring iterations)", 
    ["space_id"]
)

TASKS_COMPLETED = Counter(
    "colivin_tasks_completed_total", 
    "Total completed tasks", 
    ["space_id"]
)

TASKS_OVERDUE = Counter(
    "colivin_tasks_overdue_total", 
    "Total overdue tasks completed", 
    ["space_id"]
)

TASK_TIME_TO_ACTION = Histogram(
    "colivin_task_time_to_action_seconds",
    "Time from task creation to completion",
    ["space_id"],
    buckets=(3600, 14400, 86400, 172800, 604800, float("inf"))
)

ACTIVE_SPACES_PERCENT = Gauge(
    "colivin_active_spaces_percent",
    "Percentage of spaces with >3 tasks and >1 active user last week"
)

USER_RETENTION_PERCENT = Gauge(
    "colivin_user_retention_percent",
    "User retention rate",
    ["period"]
)