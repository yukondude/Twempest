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

brew: twempest/__init__.py
	pipenv run poet --formula twempest | pipenv run ./build-homebrew-formula.py >twempest.rb

bump:
	pipenv run bumpversion --allow-dirty patch twempest/__init__.py
	@$(MAKE) deploy
	@echo "Commit the changes: git add . ; git commit -m<comment>"
	@echo "Tag the version: git tag -a <bumpedversion> -m<comment>"
	@echo "Push to GitHub: git push --follow-tags"
	@echo "Update homebrew formula version number and SHA."

clean:
	rm -fr dist/
	rm -fr build/
	rm -fr output/
	rm -f twempest.rb

cleantest:
	pipenv run ./setup.py cleantest

deploy:
	@$(MAKE) cleantest
	@$(MAKE) build
	#pipenv run twine register dist/*.whl
	pipenv run twine upload dist/*.whl
	pipenv run twine upload dist/*.tar.gz

docs: README.rst
	pipenv run ./build-readme.py
	@$(MAKE)

test:
	pipenv run ./setup.py test
