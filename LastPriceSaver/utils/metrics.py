import prometheus_client

db_connect_error = prometheus_client.Counter(
    'db_connect_error', 'Times it failed to create DB connection'
)

db_insert_error = prometheus_client.Counter(
    'db_insert_error', 'Times it failed to insert into the DB table'
)

db_commit_error = prometheus_client.Counter(
    'db_commit_error', 'Times it failed to commit changes into the db'
)

tda_quotes_error = prometheus_client.Counter(
    'tda_quotes_error', 'Times it failed to get quote data from TDA'
)

critical_quote_error = prometheus_client.Counter(
    'critical_quote_error', 'Times there was an error when asyncly trying to get and insert data, this may cause some sort of zombie process issue'
)

sleeper_inactive = prometheus_client.Counter(
    'sleeper_inactive', 'Times the script went to sleep because it was not within time range'
)

active_pulse = prometheus_client.Counter(
    'active_pulse', 'Times the script fetched new data from TDA - should be every second'
)

skipped_sleep = prometheus_client.Counter(
    'skipped_sleep', 'Times skipped sleeping due to higher than sleep latency'
)

skipped_sleep_duration = prometheus_client.Counter(
    'skipped_sleep_duration', 'Duration of time that overslept ocurred; resulting in skip sleep'
)

time_slept = prometheus_client.Counter(
    'time_slept', 'Total time spent sleeping'
)
