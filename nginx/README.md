# Описание выполнения дз по nginx
## 1. Простой html-сайт
Старт сервиса nginx был осуществлен введением команды
```sh
$ sudo nginx
```
Для разрешения автозапуска nginx при старте системы была введена команда
```sh
$ sudo systemctl enable nginx
```
После этого был создан конфигурационный файл /etc/nginx/conf.d/1-test.conf:
```sh
server {
    listen        80;
    server_name   test-1;
    root          /var/www/test-1;
    index         index.html;
}
```
Этот конфигурационный файл будет использоваться nginx поскольку в основном конфигурационном файле /etc/nginx/nginx.conf присутствует импорт конфигурационных файлов из папки conf.d:
```sh
include /etc/nginx/conf.d/*.conf;
```
Также в соответствии с заданием был создан файл /var/www/test-1/index.html и выполнены команды для добавления прав на чтение этого файла пользователем Nginx. После этого nginx был перезагружен.
Для того, чтобы запросы 'test-1' и 'test-2', отправленные с машины, на которой был установлен nginx, приходили на неё же, необходимо изменить файл /etc/hosts следующим образом:
```sh
127.0.0.1   test-1 test-2 localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
```
Далее сделаем так, чтобы файл /etc/nginx/nginx.conf был конфигом по умолчанию. Для этого в разделе server допишем default_server к каждому значению параметра listen
```sh
listen       80 default_server;
listen       [::]:80 default_server;
```
Чтобы на все запросы отдавался код 404 с телом 'No <имя сервера> server config found' изменим блок location / в файле /etc/nginx/nginx.conf следующим образом:
```sh
location / {
    return 404 "No $host server config found";
    internal;
}
```

## 2. Сборка и запуск Nginx с VTS-модулем
После сборки в соответствии с инструкцией необходимо отредактировать конфигурационные файлы nginx, чтобы получить метрики.
Сначала в файле /etc/nginx/nginx.conf в разделе http укажем директиву vhost_traffic_status_zone:
```sh
http {
    vhost_traffic_status_zone;
    ...
}
```
После этого в файле /etc/nginx/conf.d/1-test.conf допишем:
```sh
location /status {
    vhost_traffic_status_display;
    vhost_traffic_status_display_format prometheus;
}
```
После перезапуска nginx можно посмотреть вывод vts-модуля в формате prometheus после введения команды
```sh
$ curl test-1/status/format/prometheus 
```
Пример вывода:
```sh
...
nginx_vts_main_connections{status="accepted"} 4
nginx_vts_main_connections{status="active"} 1
nginx_vts_main_connections{status="handled"} 4
nginx_vts_main_connections{status="reading"} 0
nginx_vts_main_connections{status="requests"} 8
nginx_vts_main_connections{status="waiting"} 0
nginx_vts_main_connections{status="writing"} 1
...
```
Чтобы убедиться, что в системе nginx собран с модулем VTS можно ввести команду
```sh
$ nginx -V
```
Вывод данной команды покажет, с какими модулями был скомпилирован nginx
```sh
# nginx -V
nginx version: nginx/1.14.0
built by gcc 4.8.5 20150623 (Red Hat 4.8.5-28) (GCC)
built with OpenSSL 1.0.2k-fips  26 Jan 2017
TLS SNI support enabled
configure arguments: --prefix=/etc/nginx --sbin-path=/usr/sbin/nginx --modules-path=/usr/lib64/nginx/modules --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --pid-path=/var/run/nginx.pid --lock-path=/var/run/nginx.lock --http-client-body-temp-path=/var/cache/nginx/client_temp --http-proxy-temp-path=/var/cache/nginx/proxy_temp --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp --http-scgi-temp-path=/var/cache/nginx/scgi_temp --user=nginx --group=nginx --with-compat --with-file-aio --with-threads --with-http_addition_module --with-http_auth_request_module --with-http_dav_module --with-http_flv_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_mp4_module --with-http_random_index_module --with-http_realip_module --with-http_secure_link_module --with-http_slice_module --with-http_ssl_module --with-http_stub_status_module --with-http_sub_module --with-http_v2_module --with-mail --with-mail_ssl_module --with-stream --with-stream_realip_module --with-stream_ssl_module --with-stream_ssl_preread_module --add-module=./nginx-module-vts --with-cc-opt='-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -m64 -mtune=generic -fPIC' --with-ld-opt='-Wl,-z,relro -Wl,-z,now -pie'
```
В данном случае подстрока --add-module=./nginx-module-vts означает, что nginx собран с модулем VTS.













