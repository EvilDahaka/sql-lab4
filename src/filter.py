import logging
from typing import Any, Callable, TypeVar, Union, get_type_hints
from sqlalchemy import Column
from sqlalchemy.orm import Mapped

from src.database import Base

log = logging.getLogger(__name__)
C = TypeVar("C")
V = TypeVar("V")


class Op:
    def __init__(self, value: Any, operator: Callable[[C, V], bool], _types: Any = Any):
        if _types != Any:
            if not isinstance(value, _types):
                raise TypeError()

        self.value = value

        self.operator = operator

    def apply(self, col: Column):
        # Отримуємо Python тип з SQLAlchemy колонки
        python_type = col.type.python_type
        value_type = type(self.value)

        # Перевірка типів (пропускаємо для None та list для IN оператора)
        if self.value is not None and not isinstance(self.value, (list, tuple)):
            if value_type != python_type:
                raise TypeError(
                    f"Column '{col.name}' is {python_type.__name__}, not {value_type.__name__}"
                )

        try:
            result = self.operator(col, self.value)
        except AttributeError as e:
            raise TypeError(
                f"Column '{col}' does not support this operator "
                f"({self.operator.__name__ if hasattr(self.operator, '__name__') else self.operator})"
            ) from e
        except Exception as e:
            raise RuntimeError("Operator Error: ") from e

        return result

    def __repr__(self):
        op_name = getattr(self.operator, "__name__", str(self.operator))
        return f"Op({op_name}, {self.value!r})"


def op_factory(operator, annotations=Any):
    def wrapper(value=None):
        return Op(value=value, operator=operator)

    return wrapper


NUM = Union[float, int]
MASIVE = Union[set, list]

eq = op_factory(lambda col, val: col == val)
neq = op_factory(lambda col, val: col != val)
gt = op_factory(lambda col, val: col > val, NUM)
lt = op_factory(lambda col, val: col < val, NUM)
gte = op_factory(lambda col, val: col >= val, NUM)
lte = op_factory(lambda col, val: col <= val, NUM)
like = op_factory(lambda col, val: col.like(val))  # LIKE (пошук за зразком)
in_ = op_factory(lambda col, val: col.in_(val), MASIVE)  # IN (входить у список)


class Filter:
    def __init__(self, **kwargs):
        self.__dict = {}
        self.__init_attrs(**kwargs)

    def __init_attrs(self, **kwargs):
        annotations = get_type_hints(self.__class__)
        for field, type_ in annotations.items():

            value = kwargs.get(field)
            self.__add_value(field, value)

    def __add_attr(self, field: str, value: Op):
        self.__dict[field] = value
        setattr(self, field, value)

    def __add_value(self, field: str, value: Any):
        operator = getattr(self.__class__, field, eq())  # беремо оператор або eq
        # якщо оператор — це функція з _operator_symbol, то викликаємо її
        if isinstance(operator, Op):
            operator.value = value
            self.__add_attr(field, operator)
        else:
            raise ValueError(f"Invalid operater {operator}")

    def overload(self, **kwargs: Op):
        annotations = get_type_hints(self.__class__)
        for field, op in kwargs.items():
            type_ = annotations.get(field)
            if type_:
                if not isinstance(op.value, type_):
                    raise ValueError(
                        f"Field '{field}' must by '{type_}', not '{type(op)}'"
                    )
            self.__add_attr(field, op)

    def __repr__(self):
        fields = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({fields})"

    def to_dict(self) -> dict[str, Op]:
        return self.__dict


class FilterHeadler:
    def __init__(self, model: Base):
        self.model = model

    def __call__(self, values):
        return self.to_conditions(values)

    def to_conditions(self, _filter: Filter) -> list[Callable]:
        conditions = []
        for field_name, op in _filter.to_dict().items():
            column: Column = getattr(self.model, field_name, None)
            if not column:
                log.error(
                    f"Filter isn`t correct '%s',The field '%s' does not contain '%s'.",
                    _filter.__class__.__name__,
                    field_name,
                    self.model.__class__.__name__,
                )
                continue
            cunc_func, v = op.operator, op.value

            conditions.append(op.apply(column))
        return conditions
