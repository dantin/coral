
.PHONY: test
test:
	@echo "Run unit tests"
	@tox

.PHONY: clean
clean:
	@echo "Clean temp files"
	@rm -f *.log *.csv *.jl
	@rm -rf htmlcov/
	@find . -type d -path ./.tox -prune -false -o -name '__pycache__' -print0 | xargs -0 rm -rf


update-demo:
	@echo "Update pages"
	@curl https://github.com/vim/vim --output ./misc/pages/landing_page.html
	@curl https://github.com/vim/vim/releases --output ./misc/pages/release_page.html
