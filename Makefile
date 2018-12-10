# Twempest Makefile for various and sundry tasks.

# This file is part of Twempest. Copyright 2018 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public
# License, version 3. Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

README.rst: README.md
	sed '/^Twitter to text.*"twempest"\.$$/d' README.md >README.tmp
	pandoc -f markdown -t rst -o README.rst README.tmp
	rm -f README.tmp

README.md: README-template.md twempest.config.sample twempest.template.sample twempest/__init__.py
	pipenv run ./build-readme.py

build: clean docs
	pipenv run ./setup.py sdist >/dev/null
	pipenv run ./setup.py bdist_wheel >/dev/null

bump:
	pipenv run ./bump-version.py
	@$(MAKE) deploy
	@echo "Commit the changes: git add . ; git commit -m<comment>"
	@echo "Tag the version: git tag -a <bumpedversion> -m<comment>"
	@echo "Push to GitHub: git push --follow-tags"
	@echo "Update homebrew formula version number and SHA."

clean:
	rm -fr dist/
	rm -fr build/
	rm -fr output/

cleantest:
	pipenv run ./setup.py cleantest

deploy:
	@$(MAKE) cleantest
	@$(MAKE) build
	$(eval DIST_WHL := $(shell ls dist/*.whl))
	$(eval DIST_TGZ := $(shell ls dist/*.tar.gz))
	#pipenv run twine register $(DIST_WHL)
	pipenv run twine upload $(DIST_WHL)
	pipenv run twine upload $(DIST_TGZ)

docs: README.rst
	pipenv run ./build-readme.py
	@$(MAKE)

test:
	pipenv run ./setup.py test
