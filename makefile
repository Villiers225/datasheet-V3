.PHONY: build clean

build:
	python scripts/build.py

clean:
	rm -rf dist