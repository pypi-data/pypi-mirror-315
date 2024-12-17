{% autoescape off %}
'use strict';
{
  const globals = this;
  const django = globals.django || (globals.django = {});

  {% if plural %}
  django33.pluralidx = function(n) {
    const v = {{ plural }};
    if (typeof v === 'boolean') {
      return v ? 1 : 0;
    } else {
      return v;
    }
  };
  {% else %}
  django33.pluralidx = function(count) { return (count == 1) ? 0 : 1; };
  {% endif %}

  /* gettext library */

  django33.catalog = django33.catalog || {};
  {% if catalog_str %}
  const newcatalog = {{ catalog_str }};
  for (const key in newcatalog) {
    django33.catalog[key] = newcatalog[key];
  }
  {% endif %}

  if (!django33.jsi18n_initialized) {
    django33.gettext = function(msgid) {
      const value = django33.catalog[msgid];
      if (typeof value === 'undefined') {
        return msgid;
      } else {
        return (typeof value === 'string') ? value : value[0];
      }
    };

    django33.ngettext = function(singular, plural, count) {
      const value = django33.catalog[singular];
      if (typeof value === 'undefined') {
        return (count == 1) ? singular : plural;
      } else {
        return value.constructor === Array ? value[django33.pluralidx(count)] : value;
      }
    };

    django33.gettext_noop = function(msgid) { return msgid; };

    django33.pgettext = function(context, msgid) {
      let value = django33.gettext(context + '\x04' + msgid);
      if (value.includes('\x04')) {
        value = msgid;
      }
      return value;
    };

    django33.npgettext = function(context, singular, plural, count) {
      let value = django33.ngettext(context + '\x04' + singular, context + '\x04' + plural, count);
      if (value.includes('\x04')) {
        value = django33.ngettext(singular, plural, count);
      }
      return value;
    };

    django33.interpolate = function(fmt, obj, named) {
      if (named) {
        return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
      } else {
        return fmt.replace(/%s/g, function(match){return String(obj.shift())});
      }
    };


    /* formatting library */

    django33.formats = {{ formats_str }};

    django33.get_format = function(format_type) {
      const value = django33.formats[format_type];
      if (typeof value === 'undefined') {
        return format_type;
      } else {
        return value;
      }
    };

    /* add to global namespace */
    globals.pluralidx = django33.pluralidx;
    globals.gettext = django33.gettext;
    globals.ngettext = django33.ngettext;
    globals.gettext_noop = django33.gettext_noop;
    globals.pgettext = django33.pgettext;
    globals.npgettext = django33.npgettext;
    globals.interpolate = django33.interpolate;
    globals.get_format = django33.get_format;

    django33.jsi18n_initialized = true;
  }
};
{% endautoescape %}
