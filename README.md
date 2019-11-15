<pre><code>Yb  dP    db    8b    d8 88     888888 88 888888 88     8888b.
 YbdP    dPYb   88b  d88 88     88__   88 88__   88      8I  Yb
  8P    dP__Yb  88YbdP88 88  .o 88""   88 88""   88  .o  8I  dY
 dP    dP""""Yb 88 YY 88 88ood8 88     88 888888 88ood8 8888Y"  </code></pre>

A Django database field for storing [YAML](http://en.wikipedia.org/wiki/YAML) data

[![Build Status](https://travis-ci.org/datadesk/django-yamlfield.png?branch=master)](https://travis-ci.org/datadesk/django-yamlfield)
[![PyPI version](https://badge.fury.io/py/django-yamlfield.png)](http://badge.fury.io/py/django-yamlfield)
[![Coverage Status](https://coveralls.io/repos/datadesk/django-yamlfield/badge.png?branch=master)](https://coveralls.io/r/datadesk/django-yamlfield?branch=master)

* Docs: [django-yamlfield.rtfd.org](https://django-yamlfield.rtfd.org)
* Issues: [github.com/datadesk/django-yamlfield/issues](https://github.com/datadesk/django-yamlfield/issues)
* Packaging: [pypi.python.org/pypi/django-yamlfield](https://pypi.python.org/pypi/django-yamlfield)
* Testing: [travis-ci.org/datadesk/django-yamlfield](https://travis-ci.org/datadesk/django-yamlfield)
* Coverage: [coveralls.io/r/datadesk/django-yamlfield](https://coveralls.io/r/datadesk/django-yamlfield)



YamlField in Templates
------------------------

By default, YamlField returns the contents as an OrderedDitc.  To display a yamlfield in a template as text, use the template filter as_text::

	{% load yamltags %}
	
	 <textarea name="settings">{{ object.settings|as_text }}</textarea>
	
To edit with the Ace Editor::


	<textarea name="settings" id="id_settings" style="display:none;">{{ object.settings|as_text }}</textarea>
	<div id="ace_settings"></div>
	
	
To setup Ace Editor (see more here: https://ace.c9.io/)::

	  <script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.6/ace.js" type="text/javascript" charset="utf-8"></script>
	  <script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.6/mode-yaml.js" type="text/javascript" charset="utf-8"></script>
	  <script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.6/theme-github.js" type="text/javascript" 
	  
	  <script>
        var options = {
          theme: "ace/theme/github",
          mode: "ace/mode/yaml",
          maxLines: 10,
          minLines: 6,
          wrap: true,
          autoScrollEditorIntoView: true
      };

      // setup ace editor to edit yaml contents
      // put editor in a div and sync changes in the div back to the hidden textarea

      var edit_settings = ace.edit("ace_settings",options);
      edit_settings.session.setValue($("#id_settings").val());
      edit_settings.getSession().on("change", function () {
          $("#id_settings").val(edit_settings.getSession().getValue());
      });
      
      
      // on submit make sure textarea is up to date
      $('form').on("submit", function() {

		   $("#id_settings").val(edit_settings.getSession().getValue());

	  });
	  
	</script>
	
	

