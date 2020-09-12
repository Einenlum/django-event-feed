celery_test:
	DJANGO_SETTINGS_MODULE=eventfeed.settings_test celery -A eventfeed worker -B -l info

test:
	DJANGO_SETTINGS_MODULE=eventfeed.settings_test pytest
