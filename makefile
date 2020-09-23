all: run

run:
	python3 decode.py message.wav

test:
	python3 -m doctest decode.py

clean:
	rm -rf __pycache__