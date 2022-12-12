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
	DB_FILE := "data/species.sql"
endif

install: requirements.txt
	pip install -r requirements.txt || true

load: install $(DB_FILE)
	mysql -u $(MYSQL_USER) $(MYSQL_DB) < $(DB_FILE) || true

get_ancestors: load cli.py
	./cli.py get_ancestors

