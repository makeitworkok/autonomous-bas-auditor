from __future__ import annotations

import logging
import time

import requests

from .config import CollectorConfig


def post_payload(payload: dict, config: CollectorConfig) -> requests.Response:
    headers = {
        "Authorization": f"Bearer {config.bearer_token}",
    }
    return requests.post(
        config.api_url,
        json=payload,
        headers=headers,
        timeout=config.request_timeout_seconds,
    )


def post_with_retry(payload: dict, config: CollectorConfig, logger: logging.Logger) -> bool:
    attempt = 1
    while attempt <= config.max_retries:
        try:
            response = post_payload(payload, config)
            if 200 <= response.status_code < 300:
                logger.info("POST succeeded (status=%s)", response.status_code)
                return True

            logger.warning(
                "POST failed (status=%s, body=%s)",
                response.status_code,
                response.text,
            )
        except requests.RequestException as exc:
            logger.warning("POST exception on attempt %s: %s", attempt, exc)

        if attempt < config.max_retries:
            sleep_seconds = config.backoff_seconds * (2 ** (attempt - 1))
            logger.info("Retrying in %s seconds", sleep_seconds)
            time.sleep(sleep_seconds)
        attempt += 1

    return False
