# Описание REST API

## Описание запросов
...

### REST API structure
`<protocol>://<hostname>/<api_version>/<application>/<resource>/<id>/<action|resource>?<query_params>`

 - __api_version__: `api/v1` or `api/v2`. Note same apps/resources can have different API versions, ex. `data_model/series`.
 - __application__ is app name from [core of project](../gateway/) or [external plugins](configuration.md#plugins): `data_model`, `data_storage`, `plugins/<plugin_name>` etc. In some cases app name does not equal rest app name: `gateway.rules_v2` - `api/v2/rule_service/`  
 - __resource__ is plural form of model (see `models.py`): `rules`, `equipment` and so on. Some resources are nested for another resource: `series/:id/nodes`, `users/:id/permissions` or `equipment/:id/events/data`. 
 - __id__ is unique identifier of resource object: `1` or any integer number.
 - __action__ is action over resource or its object or their additional property: `data`, `run`, `:id/progress`
 - __query_params__ are different: 
   - pagination: `limit=25&offset=50` or `page_size=25&page=3`
   - filtration: `ids=1,2,3&name=isubstr&context={"1":"any"}`
   - sorting: `ordering=name,-id`
   - flexibility of response: `expand=*&fields=id,name&omit=name`
   - format of response: `format=yaml`
   - or just query params.

### CRUD operations over resources (models, entities)
- request: `POST /resource/` - create an object or sometime objects.

  response: created json-object with auto-generated id, `HTTP 201 Created` or sometime `HTTP 200 OK`

- request: `GET /resource/` - receive list of all objects.

  response: list of json-objects, usually with pagination, `HTTP 200 OK`.

- request: `GET /resource/<id>/` - receive the object.

  response: json-object, `HTTP 200 OK`.

- request: `PUT или PATCH /resource/<id>/` - change the object. PUT - all fields, PATCH - part of fields.

  response: updated json-object, `HTTP 200 OK`.

- request: `DELETE /resource/<id>/` - removing the object.

  response: `HTTP 204 No Content` or sometime `HTTP 200 OK` with meta.

- request: `DELETE /resource/?ids=1,2,3` - removing the objects with ids.

  response: `HTTP 204 No Content` or sometime `HTTP 200 OK` with meta.


## Описание ответов

### I. Успешные ответы, 2xx
...

### II. Ответы с ошибкой, 4xx-5xx

1. Пользовательские ошибки валидации формы переданной с клиента `4xx` (ошибки поднятые в serializers, либо в models при сохранении объектов):

    1. Ошибки по конкретным полям (`name`, `code` - названия полей):
 
            [Example code]
            class SomeSerializer(...):
                name = srlz.CharField(...)
                code = srlz.CharField(max_length=100)
                
                def validate_name(self, value: str) -> str:
                    if len(value) > 300:
                        raise ValidationError("Убедитесь, что в этом поле не больше 300 символов.")
            
            or       
            
            class SomeModel(...):
                ...
                
                def save(self, ...):
                    if len(self.name) > 300:
                        raise ValidationError({"name": "Убедитесь, что в этом поле не больше 300 символов."})
            
            
            [Example response]      
            {
                "name": [
                   "Убедитесь, что в этом поле не больше 300 символов."
                ],
                "code": [
                   "Убедитесь, что в этом поле не больше 100 символов."
                ]
            }
            
            or
            
            {
                "name": "Убедитесь, что в этом поле не больше 300 символов.",
                "code": "Убедитесь, что в этом поле не больше 100 символов."
            }

    2. Общая ошибка формы, которую нельзя связать с конкретным полем (`non_field_errors` - константа в DRF, ее можно заменить на `detail`):
            
            [Example code]
            class SomeSerializer(...):
                ...
                
                def validate(self, attrs):
                    if ...:
                        raise ValidationError("Кастомная ошибка.")
            
            [Example response]
            {
                "non_field_errors": [
                   "Кастомная ошибка."
                ]
            }

    3. Эти ошибки не могут указываться вместе, из-за особенностей DRF, т.к. сначала валидируются поля, а потом идет общая валидация этих полей.

2. Остальные ошибки, не связанные с валидации формы (ошибки поднятые на уровне viewset или любом другом уровне, кроме serializer).

    1. Указывается просто строка c текстом пользовательской ошибки `4xx` (строка оборачивается в список - особенность DRF, этого можно избежать только пожертвовав добавлением лишнего кода):
            
            [Example code]
            raise ValidationError("Кастомная ошибка.")
            
            [Example response]
            [
                "Кастомная ошибка."
            ]
            
            or
            
            "Кастомная ошибка."

    2. Другие случаи когда указывается строка, но возвращается объект (ключ `detail` - захордкоженное значение в DRF, которое сложно поменять и лучше оставить).
        
        В основном это серверная ошибка `500` и некоторые другие пользовательские ошибки `401, 403, 404, 405, 429`.
        
            [Example code]
            raise APIException("Кастомная ошибка.")
            
            or 
            
            raise NotFound("Кастомная ошибка.")
            
            [Example response]
            {
                "detail": "Кастомная ошибка."
            }

    3. Указывается определенная структуру с информацией об ошибке (таких случаев очень мало и они должны быть преведены к предыдущему формату):
    
        **TODO:** обязать наличие ключа `detail`, как в предыдущем пункте или рассмотреть другие варианты. Просьба сообщать от таких эндпоинтах или создавать задачу с типом ошибка.
                    
            [Example code]
            raise ValidationError({"custom_key": "Кастомная структура ошибки."})
            
            [Example response]
            {
                "custom_key": "Кастомная структура ошибки."
            }

            or example TSP error format 
            
            {
                "errorCode": null,
                "message": "Custom platform error. ConnectionError: ...",
                "errors": [
                   "Traceback ..."
                ]
            }


Итого, все форматы можно свести к __двум типам__:
1. Ошибки формы: `{"field1": ["error text"], "field2": ["error text"]}` или `{"non_field_errors": ["error text"]}`  
2. Прочие ошибки: `{"detail": "error text"}` или `["error text"]`

При этом все ошибки могут быть:
 - не обернуты в список - `"error text"`
 - обернуты в список - `["error text"]` 
 - иметь несколько строк в списке - `["error text", "error text2"]`. Тогда нужно отобразить каждую с новой строки
 
 
## Статусы ответов

1. Часть ответов возвращаются на уровне фреймворка: `201, 3хх, 401, 403, 404, 405, 429` и возможно некоторые другие статусы.
2. Основная часть ответов регулируется разработчиками: `200, 400, 500` и иногда `201, 204, 404`.
3. Если разработчиком не была предусмотрена серверная ошибка, то вернется **`500` ошибка в виде html-страницы**. Такие эндпоинты нужно возвращать на доработку или ставить новую задачу с ошибкой.


