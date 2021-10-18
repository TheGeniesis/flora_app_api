from src.services.core.rabbit.BasicBroker import BasicBroker


def watering():
    ramq = (BasicBroker()).get_broker()

    @ramq.queue(exchange_name='flask_rabmq', routing_key='flask_rabmq.watering')
    def consume(body):
        print(body)
        return True

    ramq.run_consumer()
