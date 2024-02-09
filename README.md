# `django-path-converters`

An underestimated part of Django is its *path converters*: a way to define a certain pattern for a URL once, together with
mapping functions from and to that pattern.

These can then be plugged in into the URL paths one defines, and thus makes querying more convenient. The pattern can also
often be defined more restricted, since the work to define a pattern is done once, and is thus not very cumbersome.

This package aims to provide some general purpose path converters. Probably the most sophisticated one are lazy model
object loads: these will *not* evaluate an object, unless it is necessary, and thus therefore could save some queries.



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
      <td><code>str</code></td>
      <td><code>this-is-a-slug</code><br/><code>slugifying-this-str</code></td>
      <td><code>[-a-zA-Z0-9_]+</code></td>
      <td></td>
    </tr>
    <tr>
      <td><code>&lt;date:…&gt;</code></td>
      <td><code>datetime.date</code></td>
      <td><code>2023-01-21</code></td>
      <td><code>[0-9]{4}[-](?:0?[1-9]|1[0-2])-(?:0?[1-9]|[12][0-9]|3[01])</code></td>
      <td></td>
    </tr>
    <tr>
      <td><code>&lt;date_range:…&gt;</code></td>
      <td><code>tuple[datetime.date, datetime.date]</code></td>
      <td><code>1958-3-25/2019-11-25</code></td>
      <td><code>[0-9]{4}[-](?:0?[1-9]|1[0-2])-(?:0?[1-9]|[12][0-9]|3[01])/[0-9]{4}[-](?:0?[1-9]|1[0-2])-(?:0?[1-9]|[12][0-9]|3[01])</code></td>
      <td></td>
    </tr>
    <tr>
      <td><code>&lt;datetime:…&gt;</code></td>
      <td><code>datetime.datetime</code></td>
      <td><code>2023-01-24T19:21:18Z</code><br/><code>2023-01-24T19:21:18+00:00</code><br/><code>2023-01-24T19:47:58</code></td>
      <td><code>[0-9]{4}[-](?:0?[1-9]|1[0-2])-(?:0?[1-9]|[12][0-9]|3[01])T(?:[0-1]\d|2[0-4])[:]?[0-5][0-9][:]?[0-5][0-9](?:Z|[+-](?:[0-1]\d|2[0-4])[:]?[0-5][0-9])?</code></td>
      <td><code>&lt;class &#x27;datetime.date&#x27;&gt;</code></td>
    </tr>
    <tr>
      <td><code>&lt;eagerobject:…&gt;</code></td>
      <td><code>django.db.models.base.Model</code></td>
      <td><code>auth/user/123</code><br/><code>auth/user/12</code></td>
      <td><code>[^/]+/[^/]+/[^/]+</code></td>
      <td></td>
    </tr>
    <tr>
      <td><code>&lt;email:…&gt;</code></td>
      <td><code>str</code></td>
      <td><code>info@djangoproject.com</code><br/><code>test@foo.org</code></td>
      <td><code>.*</code></td>
      <td></td>
    </tr>
    <tr>
      <td><code>&lt;model:…&gt;</code></td>
      <td><code>django.db.models.base.Model</code></td>
      <td><code>auth/user</code></td>
      <td><code>[^/]+/[^/]+</code></td>
      <td><code>&lt;class &#x27;django.db.models.base.ModelBase&#x27;&gt;</code><br/><code>&lt;class &#x27;django.db.models.options.Options&#x27;&gt;</code></td>
    </tr>
    <tr>
      <td><code>&lt;month:…&gt;</code></td>
      <td><code>datetime.date</code></td>
      <td><code>2023-01</code></td>
      <td><code>[0-9]{4}[-](?:0?[1-9]|1[0-2])</code></td>
      <td></td>
    </tr>
    <tr>
      <td><code>&lt;object:…&gt;</code></td>
      <td><code>django.db.models.base.Model</code></td>
      <td><code>auth/user/123</code><br/><code>auth/user/12</code></td>
      <td><code>[^/]+/[^/]+/[^/]+</code></td>
      <td></td>
    </tr>
    <tr>
      <td><code>&lt;week:…&gt;</code></td>
      <td><code>datetime.date</code></td>
      <td><code>2023-W03</code></td>
      <td><code>[0-9]{4}[-]W(?:0?[1-9]|[1-4][0-9]|5[0-3])</code></td>
      <td></td>
    </tr>
  </tbody>
</table>
<!-- end path converters -->
