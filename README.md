# `django-path-converters`

## Overview of the defined path converters

<!-- path converters -->
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>name</th>
      <th>type</th>
      <th>examples</th>
      <th>regex</th>
      <th>also accepts</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>&lt;autoslug:…&gt;</code></td>
      <td><code>&lt;class &#x27;str&#x27;&gt;</code></td>
      <td>this-is-a-slug\nslugifying-this-str</td>
      <td><code>[-a-zA-Z0-9_]+</code></td>
      <td></td>
    </tr>
    <tr>
      <td><code>&lt;date:…&gt;</code></td>
      <td><code>&lt;class &#x27;datetime.date&#x27;&gt;</code></td>
      <td>2023-01-21</td>
      <td><code>[0-9]{4}[-](?:0?[1-9]|1[0-2])-(?:0?[1-9]|[12][0-9]|3[01])</code></td>
      <td></td>
    </tr>
    <tr>
      <td><code>&lt;date_range:…&gt;</code></td>
      <td><code>tuple[datetime.date, datetime.date]</code></td>
      <td>1958-3-25/2019-11-25</td>
      <td><code>[0-9]{4}[-](?:0?[1-9]|1[0-2])-(?:0?[1-9]|[12][0-9]|3[01])/[0-9]{4}[-](?:0?[1-9]|1[0-2])-(?:0?[1-9]|[12][0-9]|3[01])</code></td>
      <td></td>
    </tr>
    <tr>
      <td><code>&lt;datetime:…&gt;</code></td>
      <td><code>&lt;class &#x27;datetime.datetime&#x27;&gt;</code></td>
      <td>2023-01-24T19:21:18Z\n2023-01-24T19:21:18+00:00\n2023-01-24T19:47:58</td>
      <td><code>[0-9]{4}[-](?:0?[1-9]|1[0-2])-(?:0?[1-9]|[12][0-9]|3[01])T(?:[0-1]\d|2[0-4])[:]?[0-5][0-9][:]?[0-5][0-9](?:Z|[+-](?:[0-1]\d|2[0-4])[:]?[0-5][0-9])?</code></td>
      <td><class 'datetime.date'></td>
    </tr>
    <tr>
      <td><code>&lt;model:…&gt;</code></td>
      <td><code>&lt;class &#x27;django.db.models.base.Model&#x27;&gt;</code></td>
      <td>auth/user</td>
      <td><code>[^/]+/[^/]+</code></td>
      <td><class 'django.db.models.base.ModelBase'></td>
    </tr>
    <tr>
      <td><code>&lt;month:…&gt;</code></td>
      <td><code>&lt;class &#x27;datetime.date&#x27;&gt;</code></td>
      <td>2023-01</td>
      <td><code>[0-9]{4}[-](?:0?[1-9]|1[0-2])</code></td>
      <td></td>
    </tr>
    <tr>
      <td><code>&lt;object:…&gt;</code></td>
      <td><code>&lt;class &#x27;django.db.models.base.Model&#x27;&gt;</code></td>
      <td>auth/user/123\nauth/user/12</td>
      <td><code>[^/]+/[^/]+/[^/]+</code></td>
      <td></td>
    </tr>
    <tr>
      <td><code>&lt;week:…&gt;</code></td>
      <td><code>&lt;class &#x27;datetime.date&#x27;&gt;</code></td>
      <td>2023-W03</td>
      <td><code>[0-9]{4}[-]W(?:0?[1-9]|[1-4][0-9]|5[0-3])</code></td>
      <td></td>
    </tr>
  </tbody>
</table>
<!-- end path converters -->
