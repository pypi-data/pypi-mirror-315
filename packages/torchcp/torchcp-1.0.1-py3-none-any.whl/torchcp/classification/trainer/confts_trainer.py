# Copyright (c) 2023-present, SUSTech-ML.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import torch

from torchcp.classification.trainer.ts_trainer import TSTrainer
from torchcp.classification.trainer.model import TemperatureScalingModel
from torchcp.classification.loss.confts import ConfTS
from torchcp.classification.predictor import SplitPredictor
from torchcp.classification.score import APS

class ConfTSTrainer(TSTrainer):
    """Conformal Temperature Scaling Trainer.
    
    A trainer class that implements conformal prediction with temperature scaling
    for calibrating deep neural networks. Inherits from TSTrainer.
    
    Args:
        model: Base neural network model to be calibrated.
                Will be wrapped in TemperatureScalingModel.
        temperature: Initial temperature scaling parameter.
                    Higher values produce softer probability distributions.
        optimizer: Optimizer for only training the temperature.
        device: Device to run computations on.
                If None, will use GPU if available, else CPU.
        verbose: Whether to display training progress and metrics.
                Set False to suppress output.
        alpha: Significance level for ConfTS (0 to 1).
                Controls the expected error rate, smaller values 
                give more conservative predictions.

    Example:
        >>> model = ResNet18()
        >>> optimizer = torch.optim.Adam(model.parameters())
        >>> trainer = ConfTSTrainer(
        ...     model=model,
        ...     temperature=1.0,
        ...     optimizer=optimizer,
        ...     device='cuda'
        ... )
        >>> trainer.train(train_loader, val_loader)
    """

    def __init__(
            self,
            model: torch.nn.Module,
            temperature: float,
            optimizer: torch.optim.Optimizer,
            device: torch.device = None,
            verbose: bool = True,
            alpha: float = 0.1
            
    ):
        
        self.model = TemperatureScalingModel(model, temperature=temperature)
        optimizer = type(optimizer)([self.model.temperature], **optimizer.defaults)
        
        predictor = SplitPredictor(score_function=APS(score_type="softmax", randomized=False), model=self.model)
        confts = ConfTS(predictor=predictor, alpha=alpha, fraction=0.5)
                
        super().__init__(model, temperature, optimizer, confts, device = device, verbose = verbose)
        
        