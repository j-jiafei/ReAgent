#!/usr/bin/env python3

import logging
from typing import Optional

import torch
from reagent.core.dataclasses import dataclass, field
from reagent.core.parameters import Seq2RewardTrainerParameters, param_hash
from reagent.model_managers.world_model_base import WorldModelBase
from reagent.net_builder.unions import ValueNetBuilder__Union
from reagent.net_builder.value.fully_connected import FullyConnected
from reagent.net_builder.value.seq2reward_rnn import Seq2RewardNetBuilder
from reagent.training.world_model.seq2reward_trainer import Seq2RewardTrainer
from reagent.workflow.reporters.seq2reward_reporter import Seq2RewardReporter
from reagent.workflow.types import PreprocessingOptions


logger = logging.getLogger(__name__)


@dataclass
class Seq2RewardModel(WorldModelBase):
    __hash__ = param_hash
    net_builder: ValueNetBuilder__Union = field(
        # pyre-fixme[28]: Unexpected keyword argument `Seq2RewardNetBuilder`.
        # pyre-fixme[28]: Unexpected keyword argument `Seq2RewardNetBuilder`.
        default_factory=lambda: ValueNetBuilder__Union(
            Seq2RewardNetBuilder=Seq2RewardNetBuilder()
        )
    )

    compress_net_builder: ValueNetBuilder__Union = field(
        # pyre-fixme[28]: Unexpected keyword argument `FullyConnected`.
        # pyre-fixme[28]: Unexpected keyword argument `FullyConnected`.
        default_factory=lambda: ValueNetBuilder__Union(FullyConnected=FullyConnected())
    )

    trainer_param: Seq2RewardTrainerParameters = field(
        default_factory=Seq2RewardTrainerParameters
    )

    preprocessing_options: Optional[PreprocessingOptions] = None

    # pyre-fixme[15]: `build_trainer` overrides method defined in `ModelManager`
    #  inconsistently.
    def build_trainer(self, use_gpu: bool) -> Seq2RewardTrainer:
        seq2reward_network = self.net_builder.value.build_value_network(
            self.state_normalization_data
        )
        trainer = Seq2RewardTrainer(
            seq2reward_network=seq2reward_network, params=self.trainer_param
        )
        return trainer

    def get_reporter(self) -> Seq2RewardReporter:
        return Seq2RewardReporter(self.trainer_param.action_names)

    def build_serving_module(self) -> torch.nn.Module:
        """
        Returns a TorchScript predictor module
        """
        raise NotImplementedError()
