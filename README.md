# `django-path-converters`

An underestimated part of Django is its *path converters*: a way to define a certain pattern for a URL once, together with
mapping functions from and to that pattern.

These can then be plugged in into the URL paths one defines, and thus makes querying more convenient. The pattern can also
often be defined more restricted, since the work to define a pattern is done once, and is thus not very cumbersome.

This package aims to provide some general purpose path converters. Probably the most sophisticated one are lazy model
object loads: these will *not* evaluate an object, unless it is necessary, and thus therefore could save some queries.



## Overview of the defined path converters

<!-- path converters -->
C:\Users\willem.vanonsem\catalog\venv\Scripts\python.exe -m django converter_table --settings=settings 
System check identified some issues:

WARNINGS:
django_path_converters.Group: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the PathConvertersConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>name</th>
      <th>to_types</th>
      <th>examples</th>
      <th>regex</th>
      <th>from_types</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>&lt;auth.group:…&gt;</code></td>
      <td><code>&lt;class &#x27;django.contrib.auth.models.Group&#x27;&gt;</code></td>
      <td></td>
      <td><code>[0-9]+</code></td>
      <td><code>&lt;class &#x27;django.contrib.auth.models.Group&#x27;&gt;</code></td>
    </tr>
    <tr>
      <td><code>&lt;auth.group.id:…&gt;</code></td>
      <td><code>&lt;class &#x27;django.contrib.auth.models.Group&#x27;&gt;</code></td>
      <td></td>
      <td><code>[0-9]+</code></td>
      <td><code>&lt;class &#x27;django.contrib.auth.models.Group&#x27;&gt;</code></td>
    </tr>
    <tr>
      <td><code>&lt;auth.group.name:…&gt;</code></td>
      <td><code>&lt;class &#x27;django.contrib.auth.models.Group&#x27;&gt;</code></td>
      <td></td>
      <td><code>[^/]+</code></td>
      <td><code>&lt;class &#x27;django.contrib.auth.models.Group&#x27;&gt;</code></td>
    </tr>
    <tr>
      <td><code>&lt;auth.permission:…&gt;</code></td>
      <td><code>&lt;class &#x27;django.contrib.auth.models.Permission&#x27;&gt;</code></td>
      <td></td>
      <td><code>[0-9]+</code></td>
      <td><code>&lt;class &#x27;django.contrib.auth.models.Permission&#x27;&gt;</code></td>
    </tr>
    <tr>
      <td><code>&lt;auth.permission.id:…&gt;</code></td>
      <td><code>&lt;class &#x27;django.contrib.auth.models.Permission&#x27;&gt;</code></td>
      <td></td>
      <td><code>[0-9]+</code></td>
      <td><code>&lt;class &#x27;django.contrib.auth.models.Permission&#x27;&gt;</code></td>
    </tr>
    <tr>
      <td><code>&lt;auth.user:…&gt;</code></td>
      <td><code>&lt;class &#x27;django.contrib.auth.models.User&#x27;&gt;</code></td>
      <td></td>
      <td><code>[0-9]+</code></td>
      <td><code>&lt;class &#x27;django.contrib.auth.models.User&#x27;&gt;</code></td>
    </tr>
    <tr>
      <td><code>&lt;auth.user.id:…&gt;</code></td>
      <td><code>&lt;class &#x27;django.contrib.auth.models.User&#x27;&gt;</code></td>
      <td></td>
      <td><code>[0-9]+</code></td>
      <td><code>&lt;class &#x27;django.contrib.auth.models.User&#x27;&gt;</code></td>
    </tr>
    <tr>
      <td><code>&lt;auth.user.username:…&gt;</code></td>
      <td><code>&lt;class &#x27;django.contrib.auth.models.User&#x27;&gt;</code></td>
      <td></td>
      <td><code>[^/]+</code></td>
      <td><code>&lt;class &#x27;django.contrib.auth.models.User&#x27;&gt;</code></td>
    </tr>
    <tr>
      <td><code>&lt;autoslug:…&gt;</code></td>
      <td><code>&lt;class &#x27;str&#x27;&gt;</code></td>
      <td><code>this-is-a-slug</code><br/><code>slugifying-this-str</code></td>
      <td><code>[-a-zA-Z0-9_]+</code></td>
      <td><code>&lt;class &#x27;str&#x27;&gt;</code><br/><code>&lt;class &#x27;django.db.models.base.Model&#x27;&gt;</code></td>
    </tr>
    <tr>
      <td><code>&lt;autoslugunicode:…&gt;</code></td>
      <td><code>&lt;class &#x27;str&#x27;&gt;</code></td>
      <td><code>this-is-a-slug</code><br/><code>slugifying-this-str</code></td>
      <td><code>[-a-zA-Z0-9_]+</code></td>
      <td><code>&lt;class &#x27;str&#x27;&gt;</code><br/><code>&lt;class &#x27;django.db.models.base.Model&#x27;&gt;</code></td>
    </tr>
    <tr>
      <td><code>&lt;bool:…&gt;</code></td>
      <td><code>&lt;class &#x27;bool&#x27;&gt;</code></td>
      <td><code>True</code><br/><code>False</code><br/><code>1</code><br/><code>0</code><br/><code>T</code><br/><code>F</code><br/><code>on</code><br/><code>oFF</code><br/><code>yes</code><br/><code>NO</code></td>
      <td><code>[Yy]([Ee][Ss])?|[Tt]([Rr][Uu][Ee])?|[Oo][Nn]|1|[Ff]([Aa][Ll][Ss][Ee])?|[Nn][Oo]?|[Oo][Ff][Ff]|0</code></td>
      <td><code>&lt;class &#x27;object&#x27;&gt;</code></td>
    </tr>
    <tr>
      <td><code>&lt;contenttype:…&gt;</code></td>
      <td><code>&lt;class &#x27;django.contrib.contenttypes.models.ContentType&#x27;&gt;</code></td>
      <td></td>
      <td><code>[0-9]+</code></td>
      <td><code>&lt;class &#x27;django.contrib.contenttypes.models.ContentType&#x27;&gt;</code></td>
    </tr>
    <tr>
      <td><code>&lt;contenttype.id:…&gt;</code></td>
      <td><code>&lt;class &#x27;django.contrib.contenttypes.models.ContentType&#x27;&gt;</code></td>
      <td></td>
      <td><code>[0-9]+</code></td>
      <td><code>&lt;class &#x27;django.contrib.contenttypes.models.ContentType&#x27;&gt;</code></td>
    </tr>
    <tr>
      <td><code>&lt;contenttypes.contenttype:…&gt;</code></td>
      <td><code>&lt;class &#x27;django.contrib.contenttypes.models.ContentType&#x27;&gt;</code></td>
      <td></td>
      <td><code>[0-9]+</code></td>
      <td><code>&lt;class &#x27;django.contrib.contenttypes.models.ContentType&#x27;&gt;</code></td>
    </tr>
    <tr>
      <td><code>&lt;contenttypes.contenttype.id:…&gt;</code></td>
      <td><code>&lt;class &#x27;django.contrib.contenttypes.models.ContentType&#x27;&gt;</code></td>
      <td></td>
      <td><code>[0-9]+</code></td>
      <td><code>&lt;class &#x27;django.contrib.contenttypes.models.ContentType&#x27;&gt;</code></td>
    </tr>
    <tr>
      <td><code>&lt;date:…&gt;</code></td>
      <td><code>&lt;class &#x27;datetime.date&#x27;&gt;</code></td>
      <td><code>2023-01-21</code></td>
      <td><code>[0-9]{4}[-](?:0?[1-9]|1[0-2])-(?:0?[1-9]|[12][0-9]|3[01])</code></td>
      <td><code>&lt;class &#x27;datetime.datetime&#x27;&gt;</code><br/><code>&lt;class &#x27;datetime.date&#x27;&gt;</code></td>
    </tr>
    <tr>
      <td><code>&lt;daterange:…&gt;</code></td>
      <td><code>&lt;class &#x27;django_path_converters.converters.daterange&#x27;&gt;</code></td>
      <td><code>1958-3-25/2019-11-25</code></td>
      <td><code>(?P&lt;from_date&gt;[0-9]{4}[-](?:0?[1-9]|1[0-2])-(?:0?[1-9]|[12][0-9]|3[01]))/(?P&lt;to_date&gt;[0-9]{4}[-](?:0?[1-9]|1[0-2])-(?:0?[1-9]|[12][0-9]|3[01]))</code></td>
      <td><code>typing.Iterable</code></td>
    </tr>
    <tr>
      <td><code>&lt;datetime:…&gt;</code></td>
      <td><code>&lt;class &#x27;datetime.datetime&#x27;&gt;</code></td>
      <td><code>2023-01-24T19:21:18Z</code><br/><code>2023-01-24T19:21:18+00:00</code><br/><code>2023-01-24T19:47:58</code></td>
      <td><code>[0-9]{4}[-](?:0?[1-9]|1[0-2])-(?:0?[1-9]|[12][0-9]|3[01])T(?:[0-1]\d|2[0-4])[:]?[0-5][0-9][:]?[0-5][0-9](?:Z|[+-](?:[0-1]\d|2[0-4])[:]?[0-5][0-9])?</code></td>
      <td><code>&lt;class &#x27;datetime.datetime&#x27;&gt;</code><br/><code>&lt;class &#x27;datetime.date&#x27;&gt;</code></td>
    </tr>
    <tr>
      <td><code>&lt;django_path_converters.group:…&gt;</code></td>
      <td><code>&lt;class &#x27;django_path_converters.models.Group&#x27;&gt;</code></td>
      <td></td>
      <td><code>[0-9]+</code></td>
      <td><code>&lt;class &#x27;django_path_converters.models.Group&#x27;&gt;</code></td>
    </tr>
    <tr>
      <td><code>&lt;django_path_converters.group.id:…&gt;</code></td>
      <td><code>&lt;class &#x27;django_path_converters.models.Group&#x27;&gt;</code></td>
      <td></td>
      <td><code>[0-9]+</code></td>
      <td><code>&lt;class &#x27;django_path_converters.models.Group&#x27;&gt;</code></td>
    </tr>
    <tr>
      <td><code>&lt;django_path_converters.group.level:…&gt;</code></td>
      <td><code>&lt;class &#x27;django_path_converters.models.Group&#x27;&gt;</code></td>
      <td><code>-12</code><br/><code>14</code><br/><code>25</code></td>
      <td><code>[+-]?[0-9]+</code></td>
      <td><code>&lt;class &#x27;django_path_converters.models.Group&#x27;&gt;</code></td>
    </tr>
    <tr>
      <td><code>&lt;eager_auth.group:…&gt;</code></td>
      <td><code>&lt;class &#x27;django.contrib.auth.models.Group&#x27;&gt;</code></td>
      <td></td>
      <td><code>[0-9]+</code></td>
      <td><code>&lt;class &#x27;django.contrib.auth.models.Group&#x27;&gt;</code></td>
    </tr>
    <tr>
      <td><code>&lt;eager_auth.group.id:…&gt;</code></td>
      <td><code>&lt;class &#x27;django.contrib.auth.models.Group&#x27;&gt;</code></td>
      <td></td>
      <td><code>[0-9]+</code></td>
      <td><code>&lt;class &#x27;django.contrib.auth.models.Group&#x27;&gt;</code></td>
    </tr>
    <tr>
      <td><code>&lt;eager_auth.group.name:…&gt;</code></td>
      <td><code>&lt;class &#x27;django.contrib.auth.models.Group&#x27;&gt;</code></td>
      <td></td>
      <td><code>[^/]+</code></td>
      <td><code>&lt;class &#x27;django.contrib.auth.models.Group&#x27;&gt;</code></td>
    </tr>
    <tr>
      <td><code>&lt;eager_auth.permission:…&gt;</code></td>
      <td><code>&lt;class &#x27;django.contrib.auth.models.Permission&#x27;&gt;</code></td>
      <td></td>
      <td><code>[0-9]+</code></td>
      <td><code>&lt;class &#x27;django.contrib.auth.models.Permission&#x27;&gt;</code></td>
    </tr>
    <tr>
      <td><code>&lt;eager_auth.permission.id:…&gt;</code></td>
      <td><code>&lt;class &#x27;django.contrib.auth.models.Permission&#x27;&gt;</code></td>
      <td></td>
      <td><code>[0-9]+</code></td>
      <td><code>&lt;class &#x27;django.contrib.auth.models.Permission&#x27;&gt;</code></td>
    </tr>
	</tbody>
</table>
<!-- end path converters -->
