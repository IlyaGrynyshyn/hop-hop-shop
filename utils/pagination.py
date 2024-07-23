from rest_framework import pagination
from rest_framework.response import Response


class Pagination(pagination.PageNumberPagination):
    page_size = 8

    def get_paginated_response(self, data):
        return Response(
            {
                "items_count": self.page.paginator.count,
                "pages_link": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "items": data,
            }
        )
