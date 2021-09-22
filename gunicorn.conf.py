import multiprocessing
import os

bind = f"0.0.0.0:{os.environ['PORT']}"

if os.environ["MAX_WORKERS"]:
    max_workers = int(os.environ["MAX_WORKERS"])

workers = min(
    int(multiprocessing.cpu_count() * float(os.environ["WORKERS_PER_CORE"])),
    max_workers,
)
worker_class = "uvicorn.workers.UvicornWorker"

timeout = int(os.environ["TIMEOUT"])
