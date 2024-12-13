"""Implementations of detection algorithms."""

from typing import Literal, Dict, Callable
from .utils import load_model
from .methods import log_likelihood, log_rank, likelihood_logrank_ratio, fast_detect_gpt
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

DETECTION_FUNCS: Dict[str, Callable[[torch.Tensor, torch.Tensor], float]] = {
    "loglikelihood": log_likelihood,
    "logrank": log_rank,
    "detectllm": likelihood_logrank_ratio,
    "fastdetectgpt": fast_detect_gpt,
}
THRESHOLDS: Dict[str, float] = {
    "loglikelihood": -1.8,
    "logrank": -0.8,
    "detectllm": 2.14,
    "fastdetectgpt": 1.9,
}

DetectionMethod = Literal["loglikelihood", "logrank", "detectllm", "fastdetectgpt"]


def detect_ai_text(
    text: str,
    method: DetectionMethod = "fastdetectgpt",
    threshold: float = None,
    detection_model: str = "Qwen/Qwen2.5-1.5B",
) -> int:
    """Detect if `text` is written by human or ai.

    Args:
        text (str): The text to check.
        method (DetectionMethod, optional), default='fastdetectgpt': Detection method to use, must be one of ['loglikelihood', 'logrank', 'detectllm', 'fastdetectgpt']
        threshold (float | None, optional), default=None: Decision threshold for `method` to use. If not provided, a default value will be used based on `method`.
        detection_model (str, optional), default=Qwen/Qwen2.5-1.5B: Huggingface Repo name for the model that `method` will use to generate logits.

    Returns:
        int: 0 if human generated 1 if machine generated.

    Raises:
        ValueError: If method is not one of ['loglikelihood', 'logrank', 'detectllm', 'fastdetectgpt'].
    """
    if not text:
        return 0

    device: str = "cuda" if torch.cuda.is_available() else "cpu"
    model: AutoModelForCausalLM
    tokenizer: AutoTokenizer
    model, tokenizer = load_model(detection_model)

    tokens: torch.Tensor = tokenizer(
        text,
        return_tensors="pt",
        padding=True,
        return_token_type_ids=False,
    ).to(device)

    if method not in DETECTION_FUNCS or method not in THRESHOLDS:
        raise ValueError(
            f"In detect_ai_text `method` must be one of ['loglikelihood', 'logrank', 'detectllm', 'fastdetectgpt'], but got {method}"
        )

    method_func: Callable[[torch.Tensor, torch.Tensor], float] = DETECTION_FUNCS[method]
    if threshold is None:
        threshold = THRESHOLDS[method]

    labels: torch.Tensor = tokens.input_ids[:, 1:]  # remove bos token
    with torch.no_grad():
        logits: torch.Tensor = model(**tokens).logits[
            :, :-1
        ]  # remove next token logits
    pred: float = method_func(labels, logits)

    return 0 if pred < threshold else 1
