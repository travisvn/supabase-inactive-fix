FROM python:3.13-alpine

# Install cron
RUN apk add --no-cache dcron

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# Create log directory for cron
RUN mkdir -p /var/log/cron && touch /var/log/cron/cron.log

# Copy application files
COPY . .
COPY config.json ./

# Add crontab file
COPY crontab.txt /etc/crontabs/root

# Create entrypoint script
RUN echo '#!/bin/sh' > /entrypoint.sh && \
    echo 'crond -b -l 8 && tail -f /var/log/cron/cron.log' >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Run entrypoint script
CMD ["/entrypoint.sh"]