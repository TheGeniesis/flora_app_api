# from src.services.core.rabbit.BasicBroker import BasicBroker
# from flask import current_app
#
#
def watering():
    pass
#     ramq = (BasicBroker()).get_broker()
#
#     with current_app.app_context():
#         @ramq.queue(exchange_name='amq.topic', routing_key='amq_topic.watering')
#         def consume(body):
#             print(body)
#             return True
#
#     ramq.run_consumer()
