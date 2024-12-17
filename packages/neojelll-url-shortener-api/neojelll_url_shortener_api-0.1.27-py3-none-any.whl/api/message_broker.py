from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from .logger import configure_logger
from loguru import logger
from dotenv import load_dotenv
import asyncio
import os
import json


load_dotenv()

configure_logger()


class BrokerProducer:
    def __init__(self) -> None:
        self.producer = AIOKafkaProducer(
            bootstrap_servers=f"{os.environ["BROKER_HOST"]}:{os.environ["BROKER_PORT"]}",
            value_serializer=lambda x: json.dumps(x).encode('utf-8'),
        )

    async def __aenter__(self):
        await self.producer.start()
        return self

    async def send_data(self, data: dict) -> None:
        try:
            logger.debug(f'Send data to broker, params: {repr(data)}')
            await self.producer.send_and_wait(os.environ['SHORTENER_TOPIC_NAME'], data)
            logger.debug(f'Successfully send data to broker: {data}')
        except Exception as e:
            logger.debug(f'Error when send data to broker: {e}')

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self.producer.flush()
        await self.producer.stop()


class BrokerConsumer:
    def __init__(self):
        self.consumer = AIOKafkaConsumer(
            os.environ['TASK_TOPIC_NAME'],
            bootstrap_servers=f"{os.environ['BROKER_HOST']}:{os.environ['BROKER_PORT']}",
            enable_auto_commit=False,
            group_id='group_2',
            auto_offset_reset='earliest',
        )

    async def __aenter__(self):
        await self.consumer.start()
        return self

    async def consume_data(self, task_num: str) -> None | str:
        try:
            logger.debug('Start consuming data')
            timeout = 20
            start_time = asyncio.get_event_loop().time()
            while True:
                try:
                    msg = await asyncio.wait_for(self.consumer.__anext__(), timeout)
                except asyncio.TimeoutError:
                    logger.warning('Timeout: no messages were processed.')
                    return None
                current_time = asyncio.get_event_loop().time()
                if current_time - start_time > timeout:
                    logger.warning('Timeout: no messages were processed.')
                    return None
                logger.debug('Start consuming data with task_topic')
                if msg.value is not None:
                    data: dict = json.loads(msg.value.decode('utf-8'))
                    if 'task' in data and data['task'] == task_num:
                        logger.debug('start if task')
                        short_url = data.get('short_url')
                        if short_url:
                            logger.debug('start if short_url')
                            await self.consumer.commit()
                            logger.debug(
                                f'Completed consuming data. Returned short_url: {short_url}'
                            )
                            return short_url
                    logger.debug(
                        f"Message received but task_num does not match: {data.get('task')}"
                    )
                else:
                    logger.warning('Received a message with None value')
                    return None
        except Exception as e:
            logger.error(f'Error when consuming data from kafka: {e}')

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.consumer.stop()
