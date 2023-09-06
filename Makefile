PYTHON=python3

all:

install:
	${PYTHON} setup.py install --optimize=1 --record=install_log.log --user

test:
	${PYTHON} -m pytest

clean:
	find -depth -name __pycache__ -type d -exec rm -r -- {} \;
	find -depth -name "*.log" -type f -exec rm -rf -- {} \;
	find -depth -name "*_cache" -type d -exec rm -rf -- {} \;
	find -depth -name "__logs__" -type d -exec rm -rf -- {} \;
	find -depth -name "*_cache" -type f -exec rm -rf -- {} \;
	find -depth -name "*.pyc" -type f -exec rm -rf -- {} \;
	find -depth -name "*.dat" -type f -exec rm -rf -- {} \;
	rm -rf dist build projectman.egg-info

.PHONE: clean test
