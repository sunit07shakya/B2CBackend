# loanAccount/pagination.py
from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_size_query_param = 'page_size'  # Query param name to adjust page size from the front end
    max_page_size = 100  # Optional: maximum allowed page size
