{% if referencefile %}
.. include:: {{ referencefile }}
{% endif %}

{{ objname }}
{{ underline }}

.. currentmodule:: {{ module }}

.. autoexception:: {{ objname }}
   :members:
   :show-inheritance:
   {% if noindex -%}
   :noindex:
   {%- endif %}
