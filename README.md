# `django-path-converters`

## Overview of the defined path converters

<!-- path converters -->
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>type</th>
      <th>examples</th>
      <th>regex</th>
      <th>also accepts</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>`&lt;autoslug:…&gt;`</td>
      <td>`&lt;class 'str'&gt;`</td>
      <td>this-is-a-slug\nslugifying-this-str</td>
      <td>`[-a-zA-Z0-9_]+`</td>
      <td></td>
    </tr>
    <tr>
      <th>2</th>
      <td>`&lt;date:…&gt;`</td>
      <td>`&lt;class 'datetime.date'&gt;`</td>
      <td>2023-01-21</td>
      <td>`[0-9]{4}[-](?:0?[1-9]|1[0-2])-(?:0?[1-9]|[12][0-9]|3[01])`</td>
      <td></td>
    </tr>
    <tr>
      <th>5</th>
      <td>`&lt;date_range:…&gt;`</td>
      <td>`tuple[datetime.date, datetime.date]`</td>
      <td>1958-3-25/2019-11-25</td>
      <td>`[0-9]{4}[-](?:0?[1-9]|1[0-2])-(?:0?[1-9]|[12][0-9]|3[01])/[0-9]{4}[-](?:0?[1-9]|1[0-2])-(?:0?[1-9]|[12][0-9]|3[01])`</td>
      <td></td>
    </tr>
    <tr>
      <th>1</th>
      <td>`&lt;datetime:…&gt;`</td>
      <td>`&lt;class 'datetime.datetime'&gt;`</td>
      <td>2023-01-24T19:21:18Z\n2023-01-24T19:21:18+00:00\n2023-01-24T19:47:58</td>
      <td>`[0-9]{4}[-](?:0?[1-9]|1[0-2])-(?:0?[1-9]|[12][0-9]|3[01])T(?:[0-1]\d|2[0-4])[:]?[0-5][0-9][:]?[0-5][0-9](?:Z|[+-](?:[0-1]\d|2[0-4])[:]?[0-5][0-9])?`</td>
      <td>&lt;class 'datetime.date'&gt;</td>
    </tr>
    <tr>
      <th>6</th>
      <td>`&lt;model:…&gt;`</td>
      <td>`&lt;class 'django.db.models.base.Model'&gt;`</td>
      <td>auth/user</td>
      <td>`[^/]+/[^/]+`</td>
      <td>&lt;class 'django.db.models.base.ModelBase'&gt;</td>
    </tr>
    <tr>
      <th>3</th>
      <td>`&lt;month:…&gt;`</td>
      <td>`&lt;class 'datetime.date'&gt;`</td>
      <td>2023-01</td>
      <td>`[0-9]{4}[-](?:0?[1-9]|1[0-2])`</td>
      <td></td>
    </tr>
    <tr>
      <th>7</th>
      <td>`&lt;object:…&gt;`</td>
      <td>`&lt;class 'django.db.models.base.Model'&gt;`</td>
      <td>auth/user/123\nauth/user/12</td>
      <td>`[^/]+/[^/]+/[^/]+`</td>
      <td></td>
    </tr>
    <tr>
      <th>4</th>
      <td>`&lt;week:…&gt;`</td>
      <td>`&lt;class 'datetime.date'&gt;`</td>
      <td>2023-W03</td>
      <td>`[0-9]{4}[-]W(?:0?[1-9]|[1-4][0-9]|5[0-3])`</td>
      <td></td>
    </tr>
  </tbody>
</table>
<!-- end path converters -->
