install:
	apt-get install -y sqlite python3 python3-requests python3-nmap
	pip3 install pysqlite3 ipaddress
createdb:
	python3 crea_base.py
