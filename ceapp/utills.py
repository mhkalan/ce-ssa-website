from rest_framework.response import Response
from rest_framework import status


def status200response(data):
    return Response(
                {
                    'status': status.HTTP_200_OK,
                    "msg": "عملیات موفقیت‌آمیز بود",
                    "data": data
                },
                status=status.HTTP_200_OK
            )


def status500response():
    return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "msg": "متاسفانه سرور دچار اخنلال شده است",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


def status404response(msg):
    return Response(
                    {
                        'status': status.HTTP_404_NOT_FOUND,
                        "msg": msg,
                    },
                    status=status.HTTP_404_NOT_FOUND
                )


def status201response(data):
    return Response(
                {
                    'status': status.HTTP_201_CREATED,
                    "msg": "عملیات موفقیت‌آمیز بود",
                    "data": data
                },
                status=status.HTTP_201_CREATED
            )


def status401response():
    return Response(
                    {
                        'status': status.HTTP_401_UNAUTHORIZED,
                        'msg': 'این کاربز ادمین نمیباشد'
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )


def status400response():
    return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    "msg": "شما نمیتوانید به عنوان ادمین وارد سایت شوید"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


def status204response():
    return Response(
            {
                "status": status.HTTP_204_NO_CONTENT,
                'msg': 'رویداد مورد نظر با موفقیت حذف شد'
            },
            status=status.HTTP_204_NO_CONTENT
        )
