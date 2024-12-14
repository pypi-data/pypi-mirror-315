Silence chosen exceptions.
----


`stfu` is a replacement for the idiom:

```python
try:
    may_raise_exception()
except Exception:
    pass
```

Just write:

```python
with stfu:
    may_raise_exception()
```

```python
with stfu(TypeError, ValueError):
    may_raise_type_or_value_error()
```


To catch *everything* (even KeyboardInterrup and StopIteration):

```python
with stfu_all:
    may_raise_any_exception()
```

Remember to import it:

```python
from stfu import stfu
from stfu import stfu_all
```

----


> Errors should never pass silently.  
> Unless explicitly silenced.

