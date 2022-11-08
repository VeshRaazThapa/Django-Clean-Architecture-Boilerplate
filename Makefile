ip:
	pip install -e git+http://git@github.com/matrix-softech/django_cms_plugins.git#egg=local_plugins
b:
	docker-compose -f docker-compose.prod.yml build

change_owner:
	sudo chown -R matrix-pc2 ../digitalprofile
bud:
	docker-compose -f docker-compose.prod.yml up -d --build
buddev:
	sudo docker-compose -f docker-compose.dev.yml up -d --build

ud:
	docker-compose -f docker-compose.prod.yml up -d

udev:
	docker-compose -f docker-compose.dev.yml up -d
	#docker exec -it demo_web pip install mailchimp_marketing==3.0.48

rdev:
	python manage.py runserver

u:
	docker-compose -f docker-compose.prod.yml up

mm:
	docker exec -it demo_web python manage.py makemigrations
vps_m:
	ssh chilime@173.212.218.196 'cd /home/chilime/django/chilime && docker exec -i demo_web python manage.py migrate'
vps_m_merge:
	ssh chilime@173.212.218.196 'cd /home/chilime/django/chilime && docker exec -i demo_web python manage.py makemigrations --merge'
vps_scrape:
	ssh root@167.86.85.184 'cd /root/django_websites/chilime && docker exec -i demo_web python manage.py scrape'
m:
	docker exec -it demo_web python manage.py migrate

cs:
	docker exec -it demo_web python manage.py collectstatic --noinput

d:
	docker-compose -f docker-compose.prod.yml down

ddev:
	docker-compose -f docker-compose.dev.yml down

dv:
	docker-compose -f docker-compose.prod.yml down -v

ddv:
	docker-compose -f docker-compose.dev.yml down -v

sweb:
	docker exec -it demo_web python manage.py shell

bweb:
	docker exec -it demo_web bash

dweb:
	docker exec -it demo_db bash

csu:
	docker exec -it demo_web python manage.py createsuperuser
	docker exec -it demo_web python manage.py createsuperuser

nrw:
	docker exec -it demo_web npm run watch

nrp:
	docker exec -it demo_web npm run production

nrtw:
	docker exec -it demo_web npm run tailwind:watch

ni:
	docker exec -it demo_web npm install

lw:
	docker logs demo_web -f

ld:
	docker logs demo_db

r:
	docker restart demo_web
	docker restart demo_db

rweb:
	docker restart demo_web
	docker exec -it demo_web pip install -r dependencies/dev_requirements.txt
msg:
	docker exec -it demo_web  python manage.py makemessages

cmsg:
	docker exec -it demo_web  python manage.py compilemessages

idr:
	docker exec -it demo_web pip install -r dependencies/dev_requirements.txt

iar:
	docker exec -it demo_web pip install -r dependencies/apt_requirements.txt

dd:
	docker exec -t demo_db  pg_dump -c -U postgres > dump_data11.sql

dr:
	cat dump_data10.sql | sudo docker exec -i demo_db psql -U postgres

cmd:
	docker exec -it demo_web python manage.py commands


newdev:
	make buddev
	make dr

status:
	git status

push:
	git push origin

git:
	git add .
	git commit -m "$m"
	git push origin $b

fa:
	make cs
	make ni
	make nrp
	make nrtw

drs:
	rsync -avzP user@IP:/home/chilime/django/db_backups/dump_data10.sql chilime/
media_rsync:
     	rsync -avzP user@IP:/home/chilime/django/chilime/media chilime/

ch_own:
	sudo chown -R matrix-pc2 ../chilime
