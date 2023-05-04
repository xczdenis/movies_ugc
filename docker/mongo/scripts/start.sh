#!/bin/bash

. /scripts/colors.sh
. /scripts/logger.sh
. /scripts/helpers.sh

log_info "Инициализируем конфиг-сервер"
mongosh --host mongo-configsvr01 --port 27017 --eval 'load("/scripts/init/init-configserver.js")'

log_info "Задержка 5 секунд перед инициализацией шардов"
sleep 5

log_info "Инициализируем шарды"
mongosh --host mongo-shard01-a --port 27017 --eval 'load("/scripts/init/init-shard01.js")'
mongosh --host mongo-shard02-a --port 27017 --eval 'load("/scripts/init/init-shard02.js")'

log_info "Задержка 5 секунд перед инициализацией маршрутизатора"
sleep 5

check_service "mongo-router01" "mongo-router01" "27017"
mongosh --host mongo-router01 --port 27017 --eval 'load("/scripts/init/init-router.js")'

#log_info "Задержка 5 секунд перед инициализацией базы данных"
#log_info "Включаем шардинг и настраиваем ключ шардинга"
#mongosh --host router01 --port 27017 --eval 'sh.enableSharding("MyDatabase")'
#
###mongosh --host router01 --port 27017 --eval 'db.adminCommand( { shardCollection: "MyDatabase.MyCollection", key: { oemNumber: "hashed", zipCode: 1, supplierId: 1 } } )'
##
##log_success "${color_success}Mongo cluster's initialization completed"
##echo ""
