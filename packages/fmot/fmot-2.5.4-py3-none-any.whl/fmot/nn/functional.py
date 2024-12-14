import torch
from torch import Tensor
from torch.nn import functional as F
from typing import Optional


def temporal_conv2d(
    input: Tensor,
    weight: Tensor,
    dilation_t: int = 1,
    dilation_band: int = 1,
    padding_band: int = 0,
    stride_band: int = 1,
    bias: Optional[Tensor] = None,
    groups: int = 1,
):
    d_band_out, d_band_in, kernel_band, kernel_t = weight.shape
    if bias is not None:
        assert bias.shape[0] == d_band_out
    d_band_in = d_band_in * groups

    tracing = input.ndim == 2
    if tracing:
        input = input.unsqueeze(-1)

    batch, channels_in, time = input.shape

    assert channels_in % d_band_in == 0
    num_bands = channels_in // d_band_in

    input = input.reshape(batch, num_bands, d_band_in, time)
    input = input.transpose(1, 2)

    # causal temporal padding
    pad_amount = (kernel_t - 1) * dilation_t
    input = F.pad(input, (pad_amount, 0))

    output = F.conv2d(
        input,
        weight,
        bias,
        stride=(stride_band, 1),
        dilation=(dilation_band, dilation_t),
        padding=(padding_band, 0),
        groups=groups,
    )
    output = output.transpose(1, 2)

    output = output.reshape(batch, -1, time)

    if tracing:
        output = output.squeeze(-1)

    return output
