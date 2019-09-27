

config=config.yml
db_url=mongodb://localhost:27017/db

fill:
	python -m fill_db "$(config)" "$(db_url)"

open_browser:
	open -a "/Applications/Google Chrome.app" 'http://localhost:8090/graphiql'

start:
	config=$(config) docker-compose up