from sqlalchemy import Column, Integer, String, select
from sqlalchemy.orm import declarative_base
from src.filter import Filter, FilterHeadler, eq, gt

Base = declarative_base()


class TestORM(Base):
    __tablename__ = "test"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)


def test_filter_basic():
    _filter = FilterHeadler(TestORM)
    conditions = _filter(name=eq("лол"), age=gt(18))

    # Переконуємось, що умови створилися
    assert isinstance(conditions, list)
    assert len(conditions) == 2

    # Перевіряємо внутрішню структуру умов
    cond_name = conditions[0]
    cond_age = conditions[1]

    assert cond_name.left.name == "name"
    assert cond_name.right.value == "лол"

    assert cond_age.left.name == "age"
    assert cond_age.right.value == 18


class TestFilter(Filter):
    name: str = eq()
    age: int = gt()


def test_Filter():
    _filter = FilterHeadler(TestORM)
    test_filter = TestFilter(name="лол", age=18)
    conditions = _filter(**test_filter.to_dict())

    # Переконуємось, що умови створилися
    assert isinstance(conditions, list)
    assert len(conditions) == 2

    # Перевіряємо внутрішню структуру умов
    cond_name = conditions[0]
    cond_age = conditions[1]

    assert cond_name.left.name == "name"
    assert cond_name.right.value == "лол"

    assert cond_age.left.name == "age"
    assert cond_age.right.value == 18
