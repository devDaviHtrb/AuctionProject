def get_columns_names(model):
    return [column.name for column in model.__table__.columns if column.name != "id"]