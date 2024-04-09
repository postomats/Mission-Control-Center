from fastapi import APIRouter


router = APIRouter()


@router.get('/', response_class=dict)
def index():
    return {
        'code': 200,
        'status': 'service is UP'
    }


@router.get('healcheck', response_class=dict)
def index():
    return {
        'code': 200,
        'status': 'OK'
    }
