# matchub

# how build

git clone --recurse-submodules https://github.com/tarcidio/matchub.git

docker-compose up -d

# how i build this module

git submodule add https://github.com/tarcidio/matchub-api matchub-api

git submodule add https://github.com/tarcidio/matchub-web matchub-web
