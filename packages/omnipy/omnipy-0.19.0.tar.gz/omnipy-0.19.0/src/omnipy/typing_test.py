from typing import Generic, TypeVar

from typing_extensions import reveal_type

from omnipy import Dataset, Model

ssd = Model[int]
reveal_type(ssd)
ld = Model[str]
reveal_type(ld)
ljn = Model[str]('sd')
reveal_type(ljn)
dds = ljn.upper()
ljn.dsdsd()
reveal_type(dds)
data = Dataset[Model[str]]()
reveal_type(data['s'])

ll = Model[list[int]]([123])

ll.append(23)
print(ll.to_json(pretty=True))
data.load

T = TypeVar('T')


class A(Generic[T]):
    def __init__(self, t: T):
        self.t = t


class B(A[T], Generic[T]):
    ...


reveal_type(A[int])
reveal_type(B[int])
reveal_type(list[int])

from omnipy import JsonModel

reveal_type(JsonModel)
s = JsonModel({'a': 1})
reveal_type(s)
a = JsonModel({'sd': [123, 'a']})

asd = Model[dict[str, int]]({'a': 1})
reveal_type(asd)

from omnipy import PandasModel

b = PandasModel()
reveal_type(b)
b.pivot

from omnipy import StrDataset

c = StrDataset()
c['asd'] = 'asd'
reveal_type(c[0])