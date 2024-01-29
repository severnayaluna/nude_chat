from sqlalchemy import Column, MetaData, String, Table, Integer


meta = MetaData()


user = Table(
    'user',
    meta,
    Column(
        'id',
        Integer(),
        primary_key=True,
        index=True,
    ),
    Column(
        'name',
        String(100),
    ),
    Column(
        'bio',
        String(300),
    ),
    Column(
        'age',
        Integer(),
    ),
)

