# _*_ coding: utf-8 _*_

from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from pyramid.i18n import (
    get_localizer,
    get_locale_name
)

#from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
)

import deform
import colander

from translationstring import TranslationStringFactory
_ = TranslationStringFactory('speedfunding')


@view_config(route_name='speedfund', renderer='templates/speedfunding.pt')
def speedfunding_view(request):
    """
    this view is the default view: the speedfunding form
    """
    DEBUG = True
    # if another language was chosen by clicking on a flag
    # the add_locale_to_cookie subscriber has planted an attr on the request

    if hasattr(request, '_REDIRECT_'):
        _query = request._REDIRECT_
        request.response.set_cookie('_LOCALE_', _query)
        request._LOCALE_ = locale_name = _query
        return HTTPFound(location=request.route_url('speedfund'),
                         headers=request.response.headers)
    else:
        locale_name = get_locale_name(request)

    # XXX TODO: i18n
    country_codes = [
        ('AT', _(u'Austria')),
        ('BE', _(u'Belgium')),
        ('BG', _(u'Bulgaria')),
        ('CH', _(u'Switzerland')),
        ('CZ', _(u'Czech Republic')),
        ('DE', _(u'Germany')),
        ('DK', _(u'Denmark')),
        ('ES', _(u'Spain')),
        ('EE', _(u'Estonia')),
        ('FI', _(u'Finland')),
        ('FR', _(u'France')),
        ('GB', _(u'United Kingdom')),
        ('GR', _(u'Greece')),
        ('HU', _(u'Hungary')),
        ('HR', _(u'Croatia')),
        ('IL', _(u'Israel')),
        ('IE', _(u'Ireland')),
        ('IT', _(u'Italy')),
        ('LT', _(u'Lithuania')),
        ('LV', _(u'Latvia')),
        ('LU', _(u'Luxembourg')),
        ('MT', _(u'Malta')),
        ('NL', _(u'Netherlands')),
        ('PL', _(u'Poland')),
        ('PT', _(u'Portugal')),
        ('SK', _(u'Slovakia')),
        ('SI', _(u'Slovenia')),
        ('SE', _(u'Sweden')),
        ('XX', _(u'other'))
    ]

    # set default of Country select widget according to locale
    LOCALE_COUNTRY_MAPPING = {
        'de': 'DE',
        #'da': 'DK',
        'en': 'GB',
        #'es': 'ES',
        #'fr': 'FR',
    }
    country_default = LOCALE_COUNTRY_MAPPING.get(locale_name)
    if DEBUG:  # pragma: no cover
        print("== locale is :" + str(locale_name))
        print("== choosing :" + str(country_default))

    # declare a form
    class SpeedfundingItem(colander.MappingSchema):
        """
        a class for the goodies or choices in our speedfunding
        """
        the_options = colander.SchemaNode(
            colander.String(),
            title=_('I choose...'),
            widget=deform.widget.RadioChoiceWidget(
                values=(
                    (u'thanks',
                     _(u'a Thanks! (5€ or more)')),
                    (u'shirt',
                     _(u'a T-Shirt! (35€)')),
                    (u'shares',
                     _(u'a Share! Or More... (50€ each)')),
                )
            )
        )
        the_amount = colander.SchemaNode(
            colander.String(),
            title=_(u'I want to say thanks with money. I donate €'),
            default=_(u'5'),
        )
        the_shirt = colander.SchemaNode(
            colander.String(),
            title=_(u"Yes, I'll have a T-Shirt please! Send Me"),
            widget=deform.widget.RadioChoiceWidget(
                values=(
                    (u'S',
                     _(u'Size S')),
                    (u'M',
                     _(u'Size M')),
                    (u'L',
                     _(u'Size L')),
                    (u'XL',
                     _(u'Size XL')),
                    (u'XXL',
                     _(u'Size XXL')),
                )
            )
        )
        address1 = colander.SchemaNode(
            colander.String(),
            title=_(u'Address Line 1')
        )
        address2 = colander.SchemaNode(
            colander.String(),
            missing=unicode(''),
            title=_(u"Address Line 2")
        )
        postcode = colander.SchemaNode(
            colander.String(),
            title=_(u'Post Code'),
            oid="postcode"
        )
        city = colander.SchemaNode(
            colander.String(),
            title=_(u'City'),
            oid="city",
        )
        #  region = colander.SchemaNode(
        #      colander.String(),
        #      title=_(u'Federal State / Province / County'),
        #      missing=unicode(''))
        country = colander.SchemaNode(
            colander.String(),
            title=_(u'Country'),
            default=country_default,
            widget=deform.widget.SelectWidget(
                values=country_codes),
            oid="country",
        )

    schema = SpeedfundingItem()
    form = deform.Form(
        schema,
        buttons=[
            deform.Button('submit', _(u'Submit')),
            deform.Button('reset', _(u'Reset')),
        ])

    # if the form has been used and SUBMITTED, check contents
    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
        except deform.ValidationFailure, e:
            print(e)
            request.session.flash(
                _(u"Please note: There were errors, "
                  "please check the form below."),
                'message_above_form',
                allow_duplicate=False)
            # if there were errors, present the form with error messages
            return{'form': e.render()}

        # if the form validated correctly, use the data given
        print("the appstruct: %s" % appstruct)
        return HTTPFound(
            location=request.route_url('success'),
        )

    # if not submitted: show form
    html = form.render()

    return {'form': html,
            'project': 'speedfunding'}
