from dataclasses import dataclass
from typing import Optional

@dataclass
class ChatRateLimit:
    rpm: int                    # Requests per minute
    tpm: int                    # Tokens per minute
    rpd: Optional[int] = None   # Requests per day
    tpd: Optional[int] = None   # Tokens per day

@dataclass
class ImageRateLimit:
    ipm: int # Images per minute
    
@dataclass
class RateLimitHeader:
    x_ratelimit_limit_requests: int
    x_ratelimit_limit_tokens: int
    x_ratelimit_remaining_requests: int
    x_ratelimit_remaining_tokens: int
    x_ratelimit_reset_requests: str # ex) 1s
    x_ratelimit_reset_tokens: str # ex) 6m 0s