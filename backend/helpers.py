def get_paginated_data(request, selection, model, per_page=10):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * per_page
    end = start + per_page
    result = [model.format(item) for item in selection]
    total_items = len(result)
    return result[start:end], total_items