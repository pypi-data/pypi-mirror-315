from dataclasses import dataclass
from megatron.core.transformer import TransformerConfig


@dataclass
class DeepSeekV2TransformerConfig(TransformerConfig):

    n: int = None

    enable_shared_expert: bool = False

    q_lora_rank: int = None

    kv_lora_rank: int = 512

    qk_nope_head_dim: int = 128

    qk_rope_head_dim: int = 64

    v_head_dim: int = 128

    num_shared_experts: int = 2

    moe_layer_freq: int = 1

    rotary_base: int = 10000  

    rotary_scaling_factor: int = 40  

    max_position_embeddings: int = 163840

    moe_aux_loss_coeff: float = 0.0 #1e-2 #0.0

    moe_ffn_hidden_size: int = 1408 #TODO v2和lite不一样，写死不知道可不可以
