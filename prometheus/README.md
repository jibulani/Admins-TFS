# Описание выполнения дз по prometheus

Первое задание из дз было выполнено в соответствии с описанием.
Перед выполнением второго задания заранее создаем папки для логов сервисов prometheus и node_exporter:
```sh
$ mkdir -p /var/log/prometheus /var/log/node_exporter
```
Для выполнения второго задания было необходимо создать два .ini файла, которые будут использоваться супервизором для запуска prometheus и node_exporter.
Команда для запуска prometheus выглядит следующим образом:
```sh
command=/home/user28/prometheus-2.3.2.linux-amd64/prometheus
    --config.file=/home/user28/prometheus-2.3.2.linux-amd64/prometheus.yml
    --web.console.libraries=/home/user28/prometheus-2.3.2.linux-amd64/console_libraries
    --web.console.templates=/home/user28/prometheus-2.3.2.linux-amd64/consol
```
Команда для запуска node_exporter:
```sh
command=/home/user28/node_exporter-0.16.0.linux-amd64/node_exporter
```
После этого разрешаем автозапуск обоих приложений при запуске супервизора путем указания параметра autostart=true и прописываем логгирование для каждого из сервисов:
```sh
stdout_logfile=/var/log/[service_name]/stdout.log
stdout_logfile_maxbytes=60MB
stdout_logfile_backups=4
stdout_capture_maxbytes=4MB
stderr_logfile=/var/log/[service_name]/stderr.log
stderr_logfile_maxbytes=60MB
stderr_logfile_backups=4
stderr_capture_maxbytes=4MB
```
Созданные .ini файлы необходимо сохранить в папке /etc/supervisord.d/ для их видимости супервизором.
Чтобы изменения вступили в силу, выполним в консоли команды:
```sh
$ systemctl enable supervisord
$ systemctl start supervisord
$ supervisorctl reread
$ supervisorctl update
```
В результате выполнения команд супервизор запустит оба сервиса. Проверить их статус можно путем выполнения команды:
```sh
$ supervisorctl status
```