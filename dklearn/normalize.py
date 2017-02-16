from __future__ import absolute_import, division, print_function

from uuid import uuid4

from dask.base import normalize_token

from sklearn.base import BaseEstimator
from sklearn.model_selection._split import (BaseCrossValidator,
                                            _BaseKFold,
                                            BaseShuffleSplit,
                                            LeaveOneOut,
                                            LeaveOneGroupOut,
                                            LeavePOut,
                                            LeavePGroupsOut,
                                            PredefinedSplit,
                                            _CVIterableWrapper)


def normalize_random_state(random_state):
    if isinstance(random_state, int):
        return random_state
    return uuid4().hex


@normalize_token.register(BaseEstimator)
def normalize_BaseEstimator(est):
    return type(est).__name__, normalize_token(est.get_params())


@normalize_token.register(BaseCrossValidator)
def normalize_BaseCrossValidator(x):
    return uuid4().hex


@normalize_token.register(_BaseKFold)
def normalize_KFold(x):
    # Doesn't matter if shuffle is False
    rs = normalize_random_state(x.random_state) if x.shuffle else None
    return (type(x).__name__, x.n_splits, x.shuffle, rs)


@normalize_token.register(BaseShuffleSplit)
def normalize_ShuffleSplit(x):
    return (type(x).__name__, x.n_splits, x.test_size, x.train_size,
            normalize_random_state(x.random_state))


@normalize_token.register((LeaveOneOut, LeaveOneGroupOut))
def normalize_LeaveOneOut(x):
    return type(x).__name__


@normalize_token.register((LeavePOut, LeavePGroupsOut))
def normalize_LeavePOut(x):
    return (type(x).__name__, x.p if hasattr(x, 'p') else x.n_groups)


@normalize_token.register(PredefinedSplit)
def normalize_PredefinedSplit(x):
    return (type(x).__name__, x.test_fold)


@normalize_token.register(_CVIterableWrapper)
def normalize_CVIterableWrapper(x):
    return (type(x).__name__, x.cv)
