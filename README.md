# EMAILAPP

## Сервис для рассылки сообщений клиентам

### Перед началом работы необходимо сделать следующее:
Для наччала необходимо содать файл .env с параметрами программы, за основу можно взять  файл .env_example.

### Далее необходимо выполнить команду для создания группы "Manager":
 - Для Windows: python manage.py groups
 - Для Linux: python3 manage.py groups

### Для запуска планировщика заданий необходимо выполнить следующую команду:
 - Для Windows: python manage.py runjobs
 - Для Linux: python3 manage.py runjobs

### Для создания суперпользователя необходимо выполнить следующую команду:
  - Для Windows: python manage.py csu
  - Для Linux: python3 manage.py csu

    Данная команда создаст супер пользователя admin@gmail.com с паролем 123qweASD 
  