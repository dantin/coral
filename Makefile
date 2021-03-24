
.PHONY: test
test:
	@echo "Run unit tests"
	@tox

.PHONY: clean
clean:
	@echo "Clean temp files"
	@rm -f *.log
	@rm -rf htmlcov/
	@find . -type d -path ./.tox -prune -false -o -name '__pycache__' -print0 | xargs -0 rm -rf
