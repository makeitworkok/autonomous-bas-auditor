from __future__ import annotations

import argparse
import logging
import sys
import time

from .config import load_config
from .fake_payload import build_fake_payload
from .poster import post_with_retry
from .spool import SpoolQueue


def setup_logger(level: str) -> logging.Logger:
    logger = logging.getLogger("edge_collector")
    logger.setLevel(level.upper())
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def drain_spool(spool: SpoolQueue, config, logger: logging.Logger) -> None:
    for file_path in spool.iter_files():
        payload = spool.read(file_path)
        logger.info("Draining spooled payload %s", file_path.name)
        if post_with_retry(payload, config, logger):
            spool.remove(file_path)
        else:
            logger.warning("Could not drain %s, keeping file", file_path.name)
            return


def run_once(config, spool: SpoolQueue, logger: logging.Logger) -> None:
    payload = build_fake_payload(config)

    if post_with_retry(payload, config, logger):
        return

    path = spool.enqueue(payload)
    logger.warning("Queued payload to spool: %s", path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Autonomous BAS Edge Collector (Phase 2 MVP)")
    parser.add_argument("--once", action="store_true", help="Run one collection/post cycle and exit")
    parser.add_argument(
        "--max-cycles",
        type=int,
        default=0,
        help="Maximum number of loop cycles before exit (0 means unlimited)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = load_config()
    logger = setup_logger(config.log_level)
    spool = SpoolQueue(config.spool_dir)

    if config.drain_spool_on_start:
        drain_spool(spool, config, logger)

    if args.once:
        run_once(config, spool, logger)
        return 0

    logger.info("Starting collector loop with interval=%s seconds", config.poll_interval_seconds)
    cycles = 0
    while True:
        run_once(config, spool, logger)
        cycles += 1
        if args.max_cycles > 0 and cycles >= args.max_cycles:
            logger.info("Reached max cycles (%s), exiting collector loop", args.max_cycles)
            return 0
        time.sleep(config.poll_interval_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
