.PHONY: test test-online

test:
	python3 Tests/run_all.py

test-online:
	python3 Tests/run_all.py --online
