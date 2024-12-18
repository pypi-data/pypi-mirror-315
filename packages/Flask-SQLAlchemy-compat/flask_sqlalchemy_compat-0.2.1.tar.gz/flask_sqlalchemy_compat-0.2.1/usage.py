# -*- coding: UTF-8 -*-
"""
Usage
=====
@ Flask SQLAlchemy Compat - Examples

Author
------
Yuchen Jin (cainmagi)
cainmagi@gmail.com

License
-------
MIT License

Description
-----------
The implementation of services based on Flask SQLAlchemy Lite.
"""

try:
    from typing import List
except ImportError:
    from builtins import list as List

import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
import flask_sqlalchemy_compat as fsc


class _Base(sa_orm.MappedAsDataclass, sa_orm.DeclarativeBase): ...


engine_options = {
    "connect_args": {"check_same_thread": False},
    "poolclass": sa.pool.StaticPool,
}


# Use either one of the following options to see the performance.

# Use Flask SQLAlchemy style
#
# db = fsc.get_flask_sqlalchemy(_Base, engine_options=engine_options)
# Base = db.Model

# Use Flask SQLAlchemy Lite style
#
db, Base = fsc.get_flask_sqlalchemy_lite(_Base, engine_options=engine_options)


class NewModel(Base):
    __tablename__ = "new_model"

    id: sa_orm.Mapped[int] = sa_orm.mapped_column(init=False, primary_key=True)
    name: sa_orm.Mapped[str] = sa_orm.mapped_column()

    # Test many-to-many mapping.
    values: sa_orm.Mapped[List["NumericalModel"]] = sa_orm.relationship(
        back_populates="model", default_factory=list
    )

    def __repr__(self):
        return "{0}(id={1}, name={2}, n_vals={3})".format(
            self.__class__.__name__, self.id, self.name, len(self.values)
        )


class NumericalModel(Base):
    __tablename__ = "numerical_model"

    id: sa_orm.Mapped[int] = sa_orm.mapped_column(init=False, primary_key=True)
    value: sa_orm.Mapped[float] = sa_orm.mapped_column()

    model_id: sa_orm.Mapped[int] = sa_orm.mapped_column(
        sa.ForeignKey("new_model.id", ondelete="cascade"), nullable=False
    )
    model: sa_orm.Mapped[NewModel] = sa_orm.relationship(back_populates="values")

    def __repr__(self):
        return "{0}(id={1}, value={2}, model={3})".format(
            self.__class__.__name__, self.id, self.value, self.model.name
        )


if __name__ == "__main__":
    import os
    import flask
    import logging

    logging.basicConfig(
        format="%(asctime)s,%(msecs)03d %(name)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        level=logging.INFO,
    )
    logger = logging.getLogger("flask-sqlalchemy-compat").getChild("example")
    logger.setLevel(logging.INFO)

    app = flask.Flask(
        __name__,
        instance_path=os.path.abspath(
            os.path.join(os.path.dirname(__file__), "instance")
        ),
    )
    app.config.update(
        {
            # Only used by Flask SQLAlchemy Lite
            "SQLALCHEMY_ENGINES": {"default": "sqlite://"},
            # Only used by Flask SQLAlchemy
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
        }
    )
    db.init_app(app)

    with app.app_context():
        Base.metadata.drop_all(db.engine)
        Base.metadata.create_all(db.engine)

        logger.info("Start to add testing data.")

        model = NewModel(name="only-pos")
        NumericalModel(value=1, model_id=model.id, model=model)
        NumericalModel(value=1.2, model_id=model.id, model=model)
        NumericalModel(value=5.5, model_id=model.id, model=model)
        db.session.add(model)

        model = NewModel(name="only-neg")
        NumericalModel(value=-1, model_id=model.id, model=model)
        NumericalModel(value=-1.2, model_id=model.id, model=model)
        NumericalModel(value=-5.5, model_id=model.id, model=model)
        db.session.add(model)

        model = NewModel(name="mixed")
        NumericalModel(value=1, model_id=model.id, model=model)
        NumericalModel(value=1.2, model_id=model.id, model=model)
        NumericalModel(value=-5.5, model_id=model.id, model=model)
        db.session.add(model)

        db.session.commit()

        logger.info("Start to query data.")

        logger.info("Query by name.")
        model = db.session.scalar(sa.select(NewModel).filter(NewModel.name == "mixed"))
        assert model is not None
        assert model.name == "mixed"
        logger.info("Queried: {0}".format(model))

        logger.info("Query all models having positive values.")
        models = db.session.scalars(
            sa.select(NewModel)
            .join(NumericalModel, NewModel.values)
            .filter(NumericalModel.value > 0)
            .group_by(NewModel.id)
        ).all()
        logger.info("Queried: {0}".format(models))

        logger.info("Query all models having negative values.")
        models = db.session.scalars(
            sa.select(NewModel)
            .join(NumericalModel, NewModel.values)
            .filter(NumericalModel.value < 0)
            .group_by(NewModel.id)
        ).all()
        logger.info("Queried: {0}".format(models))

        logger.info("Query all models having both positive and negative values.")
        sub_q = (
            sa.select(NewModel.id)
            .join(NumericalModel, NewModel.values)
            .filter(NumericalModel.value < 0)
            .group_by(NewModel.id)
            .scalar_subquery()
        )
        models = db.session.scalars(
            sa.select(NewModel)
            .filter(NewModel.id.in_(sub_q))
            .join(NumericalModel, NewModel.values)
            .filter(NumericalModel.value > 0)
            .group_by(NewModel.id)
        ).all()
        logger.info("Queried: {0}".format(models))
