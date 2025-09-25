workers = []


def add_worker(worker):
    workers.append(worker)


def remove_all_workers():
    global workers
    workers = []


def reset_workers():
    for worker in workers:
        worker.reset()


def workers_update(dt):
    for worker in workers:
        worker.update(dt)
