
import random
from fastapi import APIRouter, Request
from sorting_api.utils.body_validation import validate_body

random_router = APIRouter(prefix="/randomize")


@random_router.post(
    "/",
    summary="Randomizza gli elementi di un array.",
    description="Prende un array come input e restituisce lo stesso "
                "array con gli elementi mescolati in ordine casuale.",
    response_model=list,
    responses={
        200: {
            "description": "Array mescolato restituito con successo.",
            "content": {
                "application/json": {
                    "example": [
                        "test",
                        42,
                        2.4,
                        "foo",
                        17
                    ]
                }
            },          
        },
        400: {"description": "JSON non valido o l'elemento passato non è un array."},
    },
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {
                        "type": "array",
                        "example": ["4.4", 6.6, 2.2, "foo"]
                    }
                }
            }
        }
    },
)
async def randomize(request: Request) -> list:

    print(request)

    req_list = await validate_body(request)

    random.shuffle(req_list)

    return req_list