## Адаменко Семён Сергеевич, ИВТ 2.1  
# Лабораторная работа 6: Установка корпоративной вики и системы управления задачами

### 1. Введение

Целью лабораторной работы является изучение процесса установки и настройки корпоративной вики и системы управления задачами на локальном сервере. Задачи включают в себя выбор программного обеспечения, установку и настройку серверного окружения, а также оценку возможностей выбранных систем.

Выбранные системы:
- **Корпоративная вики**: MediaWiki
- **Система управления задачами**: Redmine

### 2. Процесс установки

#### Установка MediaWiki

**MediaWiki** — это система вики, которая часто используется для создания корпоративных баз знаний.

##### Шаг 1. Подготовка окружения

Для установки MediaWiki потребуется:
- Веб-сервер Apache
- База данных MySQL или MariaDB
- PHP с необходимыми расширениями

1. **Обновите систему**:
   ```bash
   sudo apt update
   sudo apt upgrade
   ```

2. **Установите Apache, PHP и MySQL**:
   ```bash
   sudo apt install apache2 mysql-server php php-mysql libapache2-mod-php php-intl php-mbstring php-xml php-json php-zip php-bz2
   ```

3. **Настройте MySQL**:
   Запустите MySQL и создайте базу данных для MediaWiki:
   ```bash
   sudo mysql -u root -p
   CREATE DATABASE mediawiki;
   CREATE USER 'wikiuser'@'localhost' IDENTIFIED BY 'yourpassword';
   GRANT ALL PRIVILEGES ON mediawiki.* TO 'wikiuser'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```

##### Шаг 2. Скачивание и установка MediaWiki

1. **Скачайте и распакуйте MediaWiki**:
   ```bash
   cd /var/www/html
   sudo wget https://releases.wikimedia.org/mediawiki/1.39/mediawiki-1.39.0.tar.gz
   sudo tar -xvzf mediawiki-1.39.0.tar.gz
   sudo mv mediawiki-1.39.0 mediawiki
   ```

2. **Настройте права доступа**:
   ```bash
   sudo chown -R www-data:www-data /var/www/html/mediawiki
   sudo chmod -R 755 /var/www/html/mediawiki
   ```

3. **Настройте Apache**:
   Создайте новый конфигурационный файл:
   ```bash
   sudo nano /etc/apache2/sites-available/mediawiki.conf
   ```
   Добавьте следующие строки:
   ```apache
   <VirtualHost *:80>
       DocumentRoot /var/www/html/mediawiki
       ServerName wiki.local

       <Directory /var/www/html/mediawiki>
           Options Indexes FollowSymLinks MultiViews
           AllowOverride All
           Require all granted
       </Directory>
   </VirtualHost>
   ```

4. **Активируйте сайт и перезагрузите Apache**:
   ```bash
   sudo a2ensite mediawiki.conf
   sudo systemctl reload apache2
   ```

##### Шаг 3. Завершение установки через веб-интерфейс

Перейдите по адресу `http://wiki.local` в браузере и следуйте инструкциям на экране для завершения установки. Укажите параметры базы данных, созданной ранее.

---

#### Установка Redmine

**Redmine** — это система управления задачами с поддержкой плагинов и диаграмм Gantt.

##### Шаг 1. Подготовка окружения

Для установки Redmine потребуется:
- Веб-сервер Apache или Nginx
- База данных (например, MySQL)
- Ruby и необходимые зависимости

1. **Установите зависимости**:
   ```bash
   sudo apt update
   sudo apt install apache2 libapache2-mod-passenger mysql-server ruby ruby-dev libmysqlclient-dev imagemagick libmagickwand-dev
   ```

2. **Установите Redmine**:
   Скачайте последнюю версию Redmine:
   ```bash
   cd /opt
   sudo git clone https://github.com/redmine/redmine.git
   sudo ln -s /opt/redmine /var/www/html/redmine
   ```

##### Шаг 2. Настройка базы данных

1. **Настройте MySQL**:
   Запустите MySQL и создайте базу данных:
   ```bash
   sudo mysql -u root -p
   CREATE DATABASE redmine CHARACTER SET utf8mb4;
   CREATE USER 'redmineuser'@'localhost' IDENTIFIED BY 'yourpassword';
   GRANT ALL PRIVILEGES ON redmine.* TO 'redmineuser'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```

2. **Конфигурация Redmine**:
   Перейдите в каталог Redmine и отредактируйте файл конфигурации:
   ```bash
   cd /opt/redmine
   cp config/database.yml.example config/database.yml
   nano config/database.yml
   ```
   Измените параметры на свои:
   ```yaml
   production:
     adapter: mysql2
     database: redmine
     host: localhost
     username: redmineuser
     password: "yourpassword"
     encoding: utf8mb4
   ```

##### Шаг 3. Настройка Apache

1. **Создайте конфигурацию для Apache**:
   Создайте новый конфигурационный файл:
   ```bash
   sudo nano /etc/apache2/sites-available/redmine.conf
   ```
   Добавьте следующие строки:
   ```apache
   <VirtualHost *:80>
       DocumentRoot /var/www/html/redmine/public
       ServerName redmine.local

       <Directory /var/www/html/redmine/public>
           Options FollowSymLinks
           AllowOverride All
           Require all granted
       </Directory>
   </VirtualHost>
   ```

2. **Активируйте сайт и перезагрузите Apache**:
   ```bash
   sudo a2ensite redmine.conf
   sudo systemctl reload apache2
   ```

##### Шаг 4. Завершение установки через веб-интерфейс

Перейдите по адресу `http://redmine.local` в браузере и следуйте инструкциям для завершения установки. Укажите настройки базы данных, созданной ранее.

---

### 3. Функциональный анализ

**MediaWiki:**
- Возможности:
  - Создание и редактирование страниц.
  - Использование шаблонов, категорий, добавление ссылок.
  - Управление доступом на уровне страниц и разделов.
  - Возможности интеграции через API (например, с Redmine).

**Redmine:**
- Возможности:
  - Создание задач, назначение исполнителей, управление метками.
  - Использование диаграмм Gantt для планирования.
  - Управление доступом на уровне пользователей и проектов.
  - Интеграция с другими системами через плагины и API.

### 4. (Опционально) Интеграция

Планируется настроить интеграцию между **Redmine** и **MediaWiki** через API, чтобы создать связь между задачами и документацией. Эта интеграция обеспечит актуальность данных и улучшит управление проектами.

### 5. Заключение

**MediaWiki** и **Redmine** — это мощные инструменты для управления знаниями и задачами в корпоративной среде. **MediaWiki** отлично подходит для создания корпоративных вики, а **Redmine** предоставляет все необходимые функции для управления задачами и проектами. Оба инструмента имеют гибкие возможности для настройки и управления доступом, что позволяет адаптировать их под специфические нужды организации.

### 6. Ссылки на использованные источники
- [MediaWiki Installation Guide](https://www.mediawiki.org/wiki/Manual:Installation_guide)
- [Redmine Installation Guide](https://www.redmine.org/projects/redmine/wiki/RedmineInstall)
