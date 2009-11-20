django-admin-histograms
=======================

To use this app simple have your ``ModelAdmin`` subclass 
``django_histograms.admin.HistogramAdmin`` and give it a ``date_hierarchy``
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
	{% histogram_for appname.Model 'date_hierarchy' 1 1 %}

Heres a sample `change_list.html` which shows the latest activity::

    {% extends "admin/change_list.html" %}
    {% load adminmedia admin_list i18n %}
    {% load histograms %}

    {% block content %}
    <div id="content-main">
        {% histogram_for activities.Activity 'creation_date' 1 1 %}
        <br/>
        {% block object-tools %}
        {% if has_add_permission %}
            <ul class="object-tools">
            <li>
                <a href="add/{% if is_popup %}?_popup=1{% endif %}" class="addlink">
                {% blocktrans with cl.opts.verbose_name as name %}Add {{ name }}{% endblocktrans %}
                </a>
            </li>
            <li>
                <a href="/admin/activities/activity/report/{% if is_popup %}?_popup=1{% endif %}" class="link">
                    {% trans "View histogram for other months" %}
                </a>
            </li>
            </ul>
        {% endif %}
        {% endblock %}
        {% if cl.formset.errors %}
            <p class="errornote">
            {% blocktrans count cl.formset.errors|length as counter %}Please correct the error below.{% plural %}Please correct the errors below.{% endblocktrans %}
            </p>
            <ul class="errorlist">{% for error in cl.formset.non_field_errors %}<li>{{ error }}</li>{% endfor %}</ul>
        {% endif %}
        <div class="module{% if cl.has_filters %} filtered{% endif %}" id="changelist">
        {% block search %}{% search_form cl %}{% endblock %}
        {% block date_hierarchy %}{% date_hierarchy cl %}{% endblock %}

        {% block filters %}
            {% if cl.has_filters %}
            <div id="changelist-filter">
                <h2>{% trans 'Filter' %}</h2>
                {% for spec in cl.filter_specs %}{% admin_list_filter cl spec %}{% endfor %}
            </div>
            {% endif %}
        {% endblock %}
        
        <form action="" method="post"{% if cl.formset.is_multipart %} enctype="multipart/form-data"{% endif %}>
        {% if cl.formset %}
            {{ cl.formset.management_form }}
        {% endif %}

        {% block result_list %}
            {% if action_form and actions_on_top and cl.full_result_count %}{% admin_actions %}{% endif %}
            {% result_list cl %}
            {% if action_form and actions_on_bottom and cl.full_result_count %}{% admin_actions %}{% endif %}
        {% endblock %}
        {% block pagination %}{% pagination cl %}{% endblock %}
        </form>
        </div>
    </div>
    {% endblock %}
