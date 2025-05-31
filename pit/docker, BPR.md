# Адаменко Семён Сергеевич, ИВТ 2.1

1) Пишем приложение на Golang с двумя простыми ручками
![alt text](image-24.png)
2) Также делаем Dockerfile под amd64
![alt text](image-25.png)

- Пуши на docker.hub
![alt text](image-29.png)

3) После pull и настройки nginx конфига на проксирование к контейнеру запускаем на удаленном сервере 
![alt text](image-26.png)

4) Теперь нам доступно приложение написанное на Go через браузер:
![alt text](image-27.png)

5) Проверка работоспособности POST запроса
![alt text](image-28.png)

DockerHub ссылка:
https://hub.docker.com/repository/docker/paniccaaa/go-echo-app/general