from fastapi import APIRouter, Request, HTTPException
from sorting_techniques import pysort
from sorting_api.static.sorting_algo import algo_list
from sorting_api.utils.body_validation import validate_body, check_list_items_type

sort_router = APIRouter(prefix="/sort")


@sort_router.get(
    "/",
    summary="Array contenente algoritmi di ordinamento utilizzabili.",
    description="Restituisce un array contenente gli algoritmi " 
                "di ordinamento utilizzabili dall'utente.",
    response_model=list,
    responses={
        200: {
            "description": "Array degli algoritmi di ordinamento restituito con successo.",
            "content": {
                "application/json": {
                    "example": [
                        "bubblesort",
                        "insertionsort",
                        "selectionsort",
                        "mergesort"
                    ]
                }
            },
        }
    },
)
async def sort():
    return algo_list


@sort_router.post(
    "/{algo}/",
    summary="Ordina gli elementi di un array.",
    description=(
        "Prende in input un array di sole stringhe o soli numeri e lo restituisce "
        "ordinato in modo ascendente utilizzando "
        "l\'algoritmo di ordinamento scelto dall\'utente tra quelli disponibili"
    ),
    response_model=list,
    responses={
        200: {
            "description": "Array ordinato restituito con successo.",
            "content": {
                "application/json": {
                    "example": [2, 3, 5, 8, 9]
                }
            },
        },
        400: {
            "description": "JSON non valido o l'elemento passato non è un array "
            "o algoritmo di ordinamento non è valido",
            "content": {
                "application/json": {
                    "example": {"detail": "Algoritmo di sorting non valido"}
                }
            },
        },
    },
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {
                        "type": "array",
                        "example": [4, 6, 2]
                    }
                }
            }
        }
    },
)
async def sorting(algo: str, request: Request):

    data = await validate_body(request)

    if not await check_list_items_type(data):
        raise HTTPException(
            status_code=400, 
            detail="Gli elementi devono essere tutti numeri o tutte stringhe"
        )

    sorter = pysort.Sorting()

    algorithms = {
        "bubblesort": sorter.bubbleSort,
        "selectionsort": sorter.selectionSort,
        "insertionsort": sorter.insertionSort,
        "mergesort": sorter.mergeSort,
    }

    if algo not in algorithms:
        raise HTTPException(status_code=400, detail="Algoritmo di sorting non valido")

    return algorithms[algo](data)


@sort_router.post(
    "/{algo}/{order}",
    summary="Ordina gli elementi di un array in modo ascendente o discendente.",
    description=(
        "Prende in input un array di sole stringhe o soli numeri "
        "e lo restituisce ordinato in modo ascendente o discendente, "
        "in base alla scelta dell'utente, utilizzando "
        "l\'algoritmo di ordinamento scelto dall\'utente tra quelli disponibili"
    ),
    response_model=list,
    responses={
        200: {
            "description": "Array ordinato restituita con successo.",
            "content": {
                "application/json": {
                    "example": [9, 8, 5, 3, 2]
                }
            },
        },
        400: {
            "description": "JSON non valido o l'elemento passato non è un array "
            "o algoritmo di ordinamento non è valido o l'ordine non è valido",
            "content": {
                "application/json": {
                    "example": {"detail": "Ordine scelto non valido"}
                }
            },
        },
    },
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {
                        "type": "array",
                        "example": [4.4, 6.6, 2.2]
                    }
                }
            }
        }
    },
)
async def ordered_sorting(algo: str, order: str, request: Request):

    sorter = await sorting(algo, request)

    if isinstance(sorter, list):
        if order == "asc":
            return sorter
        if order == "desc":
            return sorter[::-1]
        raise HTTPException(status_code=400, detail="Ordine non valido")

    return sorter