django-admin-histograms
=======================

To use this app simple have your ``ModelAdmin`` subclass 
``django_histograms.admin.HistogramAdmin`` and give it a ``histogram_field``
attribute with the name of a ``DateField`` or ``DateTimeField`` to create the
histogram over.  Then you can pull up 
``localhost:8000/your_app/your_model/report/`` to see the histogram (adjust the
URL as necessary).

The designs came from Wilson Miner's article on data visualization for A List
Apart.


Using histograms in other pages
===============================

You can use the built-in ``histogram_for`` template tag::

	{% load histograms %}
	{% histogram_for appname.Model 'histogram_field' 1 1 %}
