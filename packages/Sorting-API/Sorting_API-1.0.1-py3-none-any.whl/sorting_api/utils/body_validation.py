
import json
from fastapi import Request, HTTPException


async def validate_body(request: Request) -> list:

    try:
        data = await request.json()
        json.loads(await request.body())
    except json.decoder.JSONDecodeError:
        raise HTTPException(status_code=400, detail="JSON non valido") from None

    if not isinstance(data, list):
        raise HTTPException(
            status_code=400, 
            detail="L'elemento passato deve essere un array"
        ) from None

    return data


async def check_list_items_type(lst: list) -> bool:

    if not lst:
        return True

    first_type = type(lst[0])

    if first_type == str:
        return all(isinstance(item, str) for item in lst)

    if first_type in (int, float):
        return all(isinstance(item, (int, float)) for item in lst)

    return False