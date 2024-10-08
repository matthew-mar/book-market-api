class UsersServiceException(Exception):
    FAILED_GET_USER_MESSAGE = "failed get user"

    FAILED_GET_FAVORITES = "failed get books from favorites"

    FAILED_ADD_TO_FAVORITES_MESSAGE = "failed add book to favorites"

    FAILED_REMOVE_FROM_FAVORITES_MESSAGE = "failed remove book from favorites"

    @staticmethod
    def failed_get_user():
        raise UsersServiceException(
            args=UsersServiceException.FAILED_GET_USER_MESSAGE
        )


class OrdersServiceException(Exception):
    FAILED_GET_FROM_SET = "failed get info from set"

    FAILED_ADD_TO_CART_MESSAGE = "failed add book to cart"

    FAILED_REMOVE_FROM_CART_MESSAGE = "failed remove book from cart"
