import numpy as np
import torch

from CAT.strategy.abstract_strategy import AbstractStrategy
from CAT.model import AbstractModel
from CAT.dataset import AdapTestDataset


class MFIStrategy(AbstractStrategy):

    def __init__(self):
        super().__init__()

    @property
    def name(self):
        return 'Maximum Fisher Information Strategy'

    def adaptest_select(self, model: AbstractModel, adaptest_data: AdapTestDataset):
        assert hasattr(model, 'get_iif'), \
            'the models must implement get_iif method'
        selection = {}
        for sid in range(adaptest_data.num_students):
            untested_questions = np.array(list(adaptest_data.untested[sid]))
            untested_iif = []
            for qid in untested_questions:
                untested_iif.append(model.get_iif(sid, qid))
            j = np.argmax(untested_iif)
            selection[sid] = untested_questions[j]
        return selection