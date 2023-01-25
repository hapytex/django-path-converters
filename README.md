# `django-path-converters`

## Overview of the defined path converters

<!-- path converters -->
      name      |                 type                  |                             examples                             |                                                                        regex                                                                        |              also accepts               |
|----------------|---------------------------------------|------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------|
|`<autoslug:…>`  |`<class 'str'>`                        |this-is-a-slug slugifying-this-str                                |`[-a-zA-Z0-9_]+`                                                                                                                                     |                                         |
|`<date:…>`      |`<class 'datetime.date'>`              |2023-01-21                                                        |`[0-9]{4}[-](?:0?[1-9]\|1[0-2])-(?:0?[1-9]\|[12][0-9]\|3[01])`                                                                                          |                                         |
|`<date_range:…>`|`tuple[datetime.date, datetime.date]`  |1958-3-25/2019-11-25                                              |`[0-9]{4}[-](?:0?[1-9]\|1[0-2])-(?:0?[1-9]\|[12][0-9]\|3[01])/[0-9]{4}[-](?:0?[1-9]\|1[0-2])-(?:0?[1-9]\|[12][0-9]\|3[01])`                                |                                         |
|`<datetime:…>`  |`<class 'datetime.datetime'>`          |2023-01-24T19:21:18Z 2023-01-24T19:21:18+00:00 2023-01-24T19:47:58|`[0-9]{4}[-](?:0?[1-9]\|1[0-2])-(?:0?[1-9]\|[12][0-9]\|3[01])T(?:[0-1]\d\|2[0-4])[:]?[0-5][0-9][:]?[0-5][0-9](?:Z\|[+-](?:[0-1]\d\|2[0-4])[:]?[0-5][0-9])?`|<class 'datetime.date'>                  |
|`<model:…>`     |`<class 'django.db.models.base.Model'>`|auth/user                                                         |`[^/]+/[^/]+`                                                                                                                                        |<class 'django.db.models.base.ModelBase'>|
|`<month:…>`     |`<class 'datetime.date'>`              |2023-01                                                           |`[0-9]{4}[-](?:0?[1-9]\|1[0-2])`                                                                                                                      |                                         |
|`<object:…>`    |`<class 'django.db.models.base.Model'>`|auth/user/123 auth/user/12                                        |`[^/]+/[^/]+/[^/]+`                                                                                                                                  |                                         |
|`<week:…>`      |`<class 'datetime.date'>`              |2023-W03                                                          |`[0-9]{4}[-]W(?:0?[1-9]\|[1-4][0-9]\|5[0-3])`                                                                                                          |
<!-- end path converters -->
