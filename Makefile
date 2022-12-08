ifndef $(MYSQL_USER)
	MYSQL_USER := ASI322
endif
ifndef $(MYSQL_DB)
	MYSQL_DB := ASI322
endif
ifndef $(MYSQL_HOST)
	MYSQL_HOST := localhost
endif
ifndef $(DB_FILE)
	DB_FILE := species.sql
endif

install: requirements.txt
	pip install -r requirements.txt || true

load: install species.sql
	mysql -u $(MYSQL_USER) $(MYSQL_DB) < $(DB_FILE) || true

get_parents: load
	./utils.py get_parents

save:
	mysqldump -u $(MYSQL_USER) $(MYSQL_DB) > $(shell ./utils.py iter_filename $(DB_FILE))

