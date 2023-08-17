{% if referencefile %}
.. include:: {{ referencefile }}
{% endif %}

{{ objname }}
{{ underline }}

.. currentmodule:: {{ module }}

.. auto{{ objtype }}:: {{ objname }}
   :inherited-members: BaseModel
