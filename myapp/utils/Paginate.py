def paginate_list(items, page, per_page=10):
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    paginated = items[start:end]

    return {
        "items": paginated,
        "total": total,
        "page": page,
        "pages": (total + per_page - 1) // per_page, 
        "per_page": per_page,
        "has_prev": page > 1,
        "has_next": end < total,
        "prev_page": page - 1,
        "next_page": page + 1
    }
