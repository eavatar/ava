

pack: pack/srv_pkg.spec
	rm -rf dist/ava
	docker run --rm -it -v "`pwd`:/app" eavatar/builder  /bin/bash -c "cd /app && make pack_in_container"


pack_in_container:
	pip install -r requirements.txt
	cp -a /app /app_pack
	chown -R ava:ava /app_pack
	su - ava -c "cd /app_pack && ./pack/build_srv_pkg.sh"
	cp -rf /app_pack/dist/ava /app/dist/
