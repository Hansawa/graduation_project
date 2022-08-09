"""

"""
import multiprocessing
import time

from proxy_pool.processors.getter import Getter
from proxy_pool.processors.tester import Tester


class Scheduler:
    """

    """
    __existed_process = {}

    @staticmethod
    def _getter_loop():
        """

        :return:
        """
        loop = 0
        getter = Getter()
        while True:
            getter.run()
            loop += 1
            print(f'getter loop: {loop}')
            time.sleep(60 * 60)

    @staticmethod
    def _tester_loop():
        loop = 0
        tester = Tester()
        while True:
            tester.run()
            loop += 1
            print(f'tester loop: {loop}')
            time.sleep(60 * 60)

    def run_process(self, process_name):
        """

        :return:
        """
        if process_name not in ['getter', 'tester']:
            return f'there is no {process_name} process here'
        if self.__existed_process.get(process_name) is None:
            p = multiprocessing.Process(name=process_name, target=eval(f'self._{process_name}_loop'))
            self.__existed_process[process_name] = p
            p.start()
            return str(p.pid)
        else:
            return f'{process_name} process already existed'

    def stop_process(self, process_name):
        if self.__existed_process.get(process_name) is not None:
            p = self.__existed_process.pop(process_name)
            p.terminate()
            p.join()
            return f'{process_name} have been closed'
        else:
            return f'{process_name} process does not exist'


if __name__ == '__main__':
    pass
