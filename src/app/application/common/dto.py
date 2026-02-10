from dataclasses import dataclass
from typing import dataclass_transform


@dataclass_transform(
    frozen_default=True,
    eq_default=False,
    kw_only_default=True,
)
def dto[InteractorClsT](interactor_cls: type[InteractorClsT]) -> type[InteractorClsT]:  # data transfer object
    return dataclass(
        kw_only=True,
        eq=False,
        match_args=False,
        frozen=True,
        slots=True,
    )(interactor_cls)
