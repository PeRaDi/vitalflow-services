FROM python:3.9

RUN apt-get update && apt-get install -y rabbitmq-server supervisor

# Optional: clean up after apt
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose RabbitMQ AMQP port (5672) and management UI (optional, 15672)
EXPOSE 5672 15672

HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=5 \
  CMD rabbitmq-diagnostics check_port_connectivity || exit 1

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]