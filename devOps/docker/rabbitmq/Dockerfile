from rabbitmq:3.9-management

RUN rabbitmq-plugins enable --offline rabbitmq_mqtt rabbitmq_federation_management rabbitmq_stomp

COPY rabbitmq.conf /etc/rabbitmq/rabbitmq.conf