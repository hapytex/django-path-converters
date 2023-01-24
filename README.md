# `django-path-converters`

## Overview of the defined path converters

<!-- path converters -->
|      name      |                                                                        regex                                                                        |                             examples                             |                 type                  |              also accepts               |
|----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------|---------------------------------------|-----------------------------------------|
|`<date:…>`      |`[0-9]{4}[-](?:0?[1-9]\|1[0-2])-(?:0?[1-9]\|[12][0-9]\|3[01])`                                                                                          |2023-01-21                                                        |`<class 'datetime.date'>`              |                                         |
|`<date_range:…>`|`[0-9]{4}[-](?:0?[1-9]\|1[0-2])-(?:0?[1-9]\|[12][0-9]\|3[01])/[0-9]{4}[-](?:0?[1-9]\|1[0-2])-(?:0?[1-9]\|[12][0-9]\|3[01])`                                |2023-01-21/2023-03-25                                             |`tuple[datetime.date, datetime.date]`  |                                         |
|`<datetime:…>`  |`[0-9]{4}[-](?:0?[1-9]\|1[0-2])-(?:0?[1-9]\|[12][0-9]\|3[01])T(?:[0-1]\d\|2[0-4])[:]?[0-5][0-9][:]?[0-5][0-9](?:Z\|[+-](?:[0-1]\d\|2[0-4])[:]?[0-5][0-9])?`|2023-01-24T19:21:18Z 2023-01-24T19:21:18+00:00 2023-01-24T19:47:58|`<class 'datetime.datetime'>`          |<class 'datetime.date'>                  |
|`<model:…>`     |`[^/]+/[^/]+`                                                                                                                                        |auth/user                                                         |`<class 'django.db.models.base.Model'>`|<class 'django.db.models.base.ModelBase'>|
|`<month:…>`     |`[0-9]{4}[-](?:0?[1-9]\|1[0-2])`                                                                                                                      |2023-01                                                           |`<class 'datetime.date'>`              |                                         |
|`<object:…>`    |`[^/]+/[^/]+/[^/]+`                                                                                                                                  |auth/user/123 auth/user/12                                        |`<class 'django.db.models.base.Model'>`|                                         |
|`<week:…>`      |`[0-9]{4}[-]W(?:0?[1-9]\|[1-4][0-9]\|5[0-3])`                                                                                                          |2023-W03                                                          |`<class 'datetime.date'>`              |                                         |
<!-- end path converters -->
