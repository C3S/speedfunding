The Slider in the donate form is built with jQuery.

You need to patch your local deform widgets.py
and add a slider named `selectslider.pt`.

To widgets.py add a class **SelectSliderWidget** similar to
**SelectWidget**.

Depending on your setup, you find (and need to add to or put) the files under::

   env/lib/python2.7/site-packages/deform- ... -py2.7.egg/deform/widget.py
   env/lib/python2.7/site-packages/deform- ... -py2.7.egg/deform/templates/
