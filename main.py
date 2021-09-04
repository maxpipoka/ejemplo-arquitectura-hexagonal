from app.adapter import JsonError, NotRequestOkError
from app.domain.auxiliar_classes import DebtProcessed
import json
from typing import Dict, List
from app.domain.service import ProcessDebtsService
from app.adapter.api_repository import ApiRepository


def output(to_print: str) ->  None:
    print(to_print)

def convert_service_to_string(to_convert: List[DebtProcessed]) -> List[Dict]:
    return [dp.convert_to_dict() for dp in to_convert]


def main() -> None:
    repository = ApiRepository()

    service = ProcessDebtsService(repository=repository)
    
    try:
        main_proccess = service.analize_debt()
        package_message = {
            "status": "ok",
            "message": convert_service_to_string(main_proccess)
        }
    except (NotRequestOkError, JsonError, KeyError):
        package_message = {
            "status": "error",
            "message": ""
        }
    
    output(json.dumps(package_message))

if __name__ == '__main__':
    main()