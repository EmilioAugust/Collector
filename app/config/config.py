class Config:
    broker_url = 'redis://localhost:6379/0'
    result_backend = 'redis://localhost:6379/1'
    result_expires = 3600
    task_serializer = 'json'
    result_serializer = 'json'
    broker_connection_retry = True
    broker_connection_max_retries = 10
    accept_content = ['json']
    timezone = 'UTC'
    enable_utc = True
    task_publish_retry = True

