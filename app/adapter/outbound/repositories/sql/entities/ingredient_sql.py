from sqlalchemy import Column, DECIMAL, String, Sequence, Integer, Boolean


from app.adapter.outbound.repositories.sql.orm import database


class Ingredient(database.Base):
    __tablename__ = "ingredient"
    
    id = Column(
        Integer,
        Sequence('ingredient_id_seq', start=1, increment=1),
        primary_key=True
    )
    name = Column(String)
    price = Column(DECIMAL(5,2))
    product_category = Column(String)
    is_active = Column(Boolean)