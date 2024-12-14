# Alpine.js for Django

[Alpine.js](TODO) packaged in a Django reusable app.

This package includes the original JS files from the library.


## Installation

    pip install django-js-lib-alpinejs

## Usage

1. Add `"js_lib_alpinejs"` to your `INSTALLED_APPS` setting like this::

       INSTALLED_APPS = [
           ...
           "js_lib_alpinejs",
           ...
       ]

2. In your template use:
   
       {% load static %}
   
   ...
   
       <script src="{%static "js_lib_alpinejs/alpinejs.js" %}"></script>
