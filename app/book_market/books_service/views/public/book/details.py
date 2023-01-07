from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import DjangoPaginator
from rest_framework.response import Response
from rest_framework.request import Request

from books_service.serializers.requests import BooksFilterRequestSerializer
from books_service.exceptions.mappers import BookMapperException
from books_service.serializers.models import BookSerializer
from books_service.serializers.responses import (
    PaginatedBookListResponseSerializer,
    FavoriteProductsResponseSerializer,
)
from books_service.mappers import BookMapper

from common.serializers.requests import PaginationRequestSerializer
from common.exceptions.internal import UsersServiceException
from common.services import UsersService
from common.exceptions.service import (
    BadRequestException,
    ValidationException, 
    NotFoundException,
)

from uuid import UUID


@api_view(http_method_names=["GET"])
def detail(request: Request, book_id: UUID) -> Response:
    try:
        book = BookMapper.get_by_id(id=book_id)
    except BookMapperException as e:
        raise NotFoundException(detail=e.args[0])
    
    response_serializer = BookSerializer(instance=book)

    return Response(data=response_serializer.data)


@api_view(http_method_names=["GET"])
def paginate(request: Request) -> Response:
    request_serializer = BooksFilterRequestSerializer(request=request)

    books = BookMapper.filter_books(
        filter_param="created_at", 
        filter_order=request_serializer.order
    )

    paginator = DjangoPaginator(
        object_list=books, 
        per_page=request_serializer.page_size
    )

    if paginator.num_pages < request_serializer.page:
        raise ValidationException(
            detail=f"page too large max - {paginator.num_pages}"
        )
    
    response_serializer = PaginatedBookListResponseSerializer(
        paginator=paginator,
        page_number=request_serializer.page
    )

    return Response(data=response_serializer.data)


@api_view(http_method_names=["GET"])
@permission_classes(permission_classes=[IsAuthenticated])
def favorites(request: Request) -> Response:
    request_serializer = PaginationRequestSerializer(request=request)

    try:
        favorites_list = UsersService.get_from_favorites(
            jwt_token=request.headers.get("Authorization"),
            page=request_serializer.page,
            page_size=request_serializer.page_size
        )
    except UsersServiceException as e:
        raise BadRequestException(detail=e.args[0])
    
    books = BookMapper.find_by_ids(ids=favorites_list.books)
    if len(books) != len(favorites_list.books):
        raise BadRequestException(detail="failed get books from favorites")
    
    response_serializer = FavoriteProductsResponseSerializer(
        favorites=favorites_list, 
        books=books
    )

    return Response(data=response_serializer.data)
