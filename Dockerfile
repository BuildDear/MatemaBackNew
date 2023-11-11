

# Копіювання скрипту entrypoint.sh
COPY entrypoint.sh /usr/src/app/entrypoint.sh

# Надання прав на виконання скрипту
RUN chmod +x /usr/src/app/entrypoint.sh

# Встановлення скрипту як точки входу
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

# Відкриття порту 8000
EXPOSE 8000
