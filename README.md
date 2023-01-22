# `django-path-converters`

## Overview of the defined path converters

<!-- path converters -->
|    name    |                                                        regex                                                        |       examples        |                 type                  |                                      accepts                                      |
|------------|---------------------------------------------------------------------------------------------------------------------|-----------------------|---------------------------------------|-----------------------------------------------------------------------------------|
|`date`      |`[0-9]{4}[-](?:0?[1-9]\|1[0-2])-(?:0?[1-9]\|[12][0-9]\|3[01])`                                                          |`2023-01-21`           |`<class 'datetime.date'>`              |`<class 'datetime.date'>`                                                          |
|`month`     |`[0-9]{4}[-](?:0?[1-9]\|1[0-2])`                                                                                      |`2023-01`              |`<class 'datetime.date'>`              |`<class 'datetime.date'>`                                                          |
|`week`      |`[0-9]{4}[-]W(?:0?[1-9]\|[1-4][0-9]\|5[0-3])`                                                                          |`2023-W03`             |`<class 'datetime.date'>`              |`<class 'datetime.date'>`                                                          |
|`date_range`|`[0-9]{4}[-](?:0?[1-9]\|1[0-2])-(?:0?[1-9]\|[12][0-9]\|3[01])/[0-9]{4}[-](?:0?[1-9]\|1[0-2])-(?:0?[1-9]\|[12][0-9]\|3[01])`|`2023-01-21/2023-03-25`|`tuple[datetime.date, datetime.date]`  |`tuple[datetime.date, datetime.date]`                                              |
|`model`     |`[^/]+/[^/]+`                                                                                                        |`auth/user`            |`<class 'django.db.models.base.Model'>`|`<class 'django.db.models.base.Model'>` `<class 'django.db.models.base.ModelBase'>`|
|`object`    |`[^/]+/[^/]+/[^/]+`                                                                                                  |`auth/user/123`        |`<class 'django.db.models.base.Model'>`|`<class 'django.db.models.base.Model'>`
<!-- end path converters -->
