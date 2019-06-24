import asyncio
import random
from contextlib import closing

from loggers import log
from nsq_proxy import NSQReader, NSQWriter


async def bring_dish(order):
    await asyncio.sleep(random.randint(1, 2))
    log.info(f'Order {order} has been brought')


async def watch_clients():
    log.info('Waiting for client orders...')
    writer = await NSQWriter(topic='client_orders').open()
    i = 0
    while True:
        await asyncio.sleep(random.randint(2, 6))
        order = f'Order {i}'
        log.info(f'Received client order: {order}')
        await writer.publish(order)
        i += 1


# async def watch_chef():
#     log.info('Watching for dishes...')
#     reader = await NSQReader(topic='processed_orders').open()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(watch_clients())
    loop.run_forever()
