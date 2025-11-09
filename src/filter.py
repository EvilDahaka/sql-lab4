from typing import Any, Callable, get_type_hints
from sqlalchemy import Column

from src.database import Base


class FilterHeadler:
    def __init__(self, model: Base):
        self.model = model

    def __call__(self, **values):
        return self.to_conditions(values)

    def to_conditions(self, data: dict):
        conditions = []
        for field_name, op in data.items():
            # пропускаємо None або відсутні поля
            if op is None or not hasattr(self.model, field_name):
                continue
            if not isinstance(op, Op):
                op = eq(op)

            column: Column = getattr(self.model, field_name)
            cunc_func, v = op.operator, op.value

            conditions.append(cunc_func(column, v))
        return conditions


class Filter:
    def __init__(self, **kwargs):
        annotations = get_type_hints(self.__class__)
        self.__dict = {}
        for field, type_ in annotations.items():
            value = kwargs.get(field)
            operator_func = getattr(self.__class__, field, eq)  # беремо оператор або eq
            # якщо оператор — це функція з _operator_symbol, то викликаємо її
            if callable(operator_func) and hasattr(operator_func, "_operator"):
                value = operator_func(value)
            else:
                value = eq(value)
            self.__dict[field] = value
            setattr(self, field, value)

    def __repr__(self):
        fields = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({fields})"

    def to_dict(self):
        return self.__dict


from typing import Any, Callable
from sqlalchemy import Column


class Op:
    def __init__(self, value: Any, operator: Callable):

        self.value = value
        self.operator = operator

    def apply(self, col: Column):
        try:
            result = self.operator(col, self.value)
        except AttributeError as e:
            raise TypeError(
                f"Column '{col}' does not support this operator "
                f"({self.operator.__name__ if hasattr(self.operator, '__name__') else self.operator})"
            ) from e
        except TypeError as e:
            raise TypeError(
                f"Incompatible types for comparison: {type(col)} and {type(self.value)}"
            ) from e
        except Exception as e:
            raise RuntimeError(f"Unexpected error while applying operator: {e}") from e
        return result

    def __repr__(self):
        op_name = getattr(self.operator, "__name__", str(self.operator))
        return f"Op({op_name}, {self.value!r})"


def op_factory(operator):
    def wrapper(value=None):
        return Op(value=value, operator=operator)

    wrapper._operator = operator  # зберігаємо метадані
    return wrapper


eq = op_factory(lambda col, val: col == val)
neq = op_factory(lambda col, val: col != val)
gt = op_factory(lambda col, val: col < val)
lt = op_factory(lambda col, val: col > val)
gte = op_factory(lambda col, val: col <= val)
lte = op_factory(lambda col, val: col >= val)
like = op_factory(lambda col, val: col.like(val))
in_ = op_factory(lambda col, val: col.in_(val))
