import os

import hydra
from omegaconf import DictConfig, OmegaConf

from heart_failure_prediction.config import PROJECT_ROOT


@hydra.main(config_path=os.path.join(PROJECT_ROOT, 'conf'), config_name='config')
def hydra_func(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))


if __name__ == '__main__':
    hydra_func()
