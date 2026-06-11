"""
CDSA-ATM src.multimodal — Multi-modal Encoders + Cross-modal Attention
=============================================================================

Scaffold for parallel modality encoders and a cross-modal attention +
gating fusion layer that produces the fused representation consumed
by `src.rl_agents`.

Modalities (Trajectory + ATS + ANSP):
  TrajectoryEncoder: 1D-CNN + LSTM over ADS-B trajectory windows
                       (position, velocity, altitude, vertical rate, heading)
  ATSEventEncoder:   Transformer over 15-class ATS occurrence typology
  ANSPCoordEncoder:  LSTM over ANSP coordination event sequences

Status: scaffolded (v2). Full implementation is planned under
TÜBİTAK 1001 ARDEB Project 4.
"""

from .encoders import TrajectoryEncoder, ATSEventEncoder, ANSPCoordEncoder  # noqa: F401
from .fusion import CrossModalAttentionFusion  # noqa: F401

__all__ = ['TrajectoryEncoder', 'ATSEventEncoder', 'ANSPCoordEncoder', "CrossModalAttentionFusion"]
