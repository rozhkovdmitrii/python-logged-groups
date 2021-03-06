import threading
from logged_groups import logged_group, logging_context
import time


@logged_group("neon.classes")
class A:

    def __init__(self, **kws):
        self.info("Some information, keep focused on it")

    def do_stuff(self, value: int):
        try:
            self._do_stuff_impl(value)
        except BaseException as e:
            self.error(f"Failed to do stuff because of error: {e}")

    def _do_stuff_impl(self, value):
        self.debug(f"Doing stuff with value: {value}")
        if value > 1000:
            raise Exception(f"Value critically high: {value}")

        if value > 100:
            self.warning(f"Value higher than 100, it can be wrong: {value}")


@logged_group("classes")
class B:
    def __init__(self):
        for i in range(0, 5):
            self.debug("Spam spam spam spam spam ")


@logged_group("funcs")
def check_logger(*, logger):
    logger.info("Hoooray it's working!!!")


@logged_group("neon.funcs")
def parallel(*, logger):
    a = A(class_id=33)
    with logging_context(user_id="Max", mode="threaded"):
        try:
            for i in range(1, 10):
                time.sleep(1)
                a.do_stuff(i)
                if i == 5:
                    raise Exception("Something wrong")
        except Exception as e:
            logger.error(f"Got exception: \"{e}\"")
    a.do_stuff(777)


if __name__ == "__main__":
    a = A(class_id=33)

    tr = threading.Thread(target=parallel)
    tr.start()
    with logging_context(user_id="Alice") as ctx:
        a1 = A(class_id="1")
        a1.do_stuff(100)
        time.sleep(4)
        with logging_context(req_id="1", mode="support"):
            a1.do_stuff(101)
            a1.do_stuff(1001)
        a1.do_stuff(0)
    time.sleep(2)
    with logging_context(user_id="Bob", req_id="2", mode="processing"):
        b = B()
    time.sleep(2)
    check_logger()
    tr.join()
