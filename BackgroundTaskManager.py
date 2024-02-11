import asyncio
import concurrent.futures
import logging

from settings import PROCESS_POOL_SIZE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskManager:
    def __init__(self):
        self.process_pool = concurrent.futures.ProcessPoolExecutor(max_workers=PROCESS_POOL_SIZE)
        self.futures = {}

    async def submit_task_with_key(self, key, task_func, *args, **kwargs):
        future = self.process_pool.submit(task_func, *args, **kwargs)
        self.futures[key] = future
        return future

    async def submit_task(self, task_func, *args, **kwargs):
        return self.process_pool.submit(task_func, *args, **kwargs)

    async def check_task_completed(self, key):
        if key not in self.futures.keys():
            raise
        if key in self.futures:
            return self.futures[key].done()
        else:
            return False

    async def get_task_result(self, key):
        if key in self.futures and self.futures[key].done():
            result = self.futures[key].result()
            del self.futures[key]  # Remove the future key
            return result
        else:
            raise ValueError("Task not completed or does not exist")

    def __stop(self):
        self.process_pool.shutdown(wait=True)

    async def execute_task_with_timeout(self, key, task_func, timeout, *args, **kwargs):
        loop = asyncio.get_event_loop()
        try:
            result = await asyncio.wait_for(
                loop.run_in_executor(self.process_pool, task_func, *args, **kwargs),
                timeout=timeout
            )
            self.futures[key] = result
            return result
        except concurrent.futures.TimeoutError:
            logger.error(f"Task {key} timed out after {timeout} seconds")
            raise
        except Exception as e:
            logger.error(f"Task {key} encountered an error: {e}")
            raise

    async def wait_for_all_tasks(self):
        concurrent.futures.wait(*self.futures.values())

    async def __check_and_stop(self):
        # Check if all tasks are completed
        if all(future for future in self.futures.values()):
            await self.__stop()

    async def output_task_status(self):
        task_status = {}
        for key, future in self.futures.items():
            task_status[key] = 'Completed' if future.done() else 'Not Completed'
        return task_status


task_manager = TaskManager()
