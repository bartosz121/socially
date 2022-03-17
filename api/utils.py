def get_paginated_queryset_response(paginator, request, queryset, serializer):
    paginated_qs = paginator.paginate_queryset(queryset, request)
    serializer_ = serializer(
        paginated_qs, many=True, context={"request": request}
    )
    return paginator.get_paginated_response(serializer_.data)
