# -*- coding: utf-8 -*-

from speedfunding.models import (
    Speedfundings,
    C3sStaff,
    TheTotal,
    DBSession,
)

from pkg_resources import resource_filename
import colander
import deform
from deform import ValidationFailure

from pyramid.i18n import (
    get_localizer,
)
from pyramid.view import view_config
from pyramid.threadlocal import get_current_request
from pyramid.httpexceptions import HTTPFound
from pyramid.security import (
    remember,
    forget,
    authenticated_userid,
)
from pyramid.url import route_url
from translationstring import TranslationStringFactory

from datetime import datetime

deform_templates = resource_filename('deform', 'templates')
speedfunding_templates = resource_filename('speedfunding', 'templates')

my_search_path = (deform_templates, speedfunding_templates)

_ = TranslationStringFactory('speedfunding')


def translator(term):
    return get_localizer(get_current_request()).translate(term)

my_template_dir = resource_filename('speedfunding', 'templates/')
deform_template_dir = resource_filename('deform', 'templates/')

zpt_renderer = deform.ZPTRendererFactory(
    [
        my_template_dir,
        deform_template_dir,
    ],
    translator=translator,
)
# the zpt_renderer above is referred to within the demo.ini file by dotted name

DEBUG = False
LOGGING = True

if LOGGING:  # pragma: no cover
    import logging
    log = logging.getLogger(__name__)


@view_config(renderer='templates/total.pt',
             permission='manage',
             route_name='total')
def new_total(request):
    """
    This view lets accountants set the amount collected:
    """

    class NewTotal(colander.MappingSchema):
        """
        colander schema for setting the collected sum
        """
        amount_collected = colander.SchemaNode(
            colander.Int(),
            title=_(u"sum collected"),
            validator=colander.Range(0, 200000),
            oid="sum",
        )
        amount_promised = colander.SchemaNode(
            colander.Int(),
            title=_(u"promised"),
            oid="promised",
        )
        num_shirts = colander.SchemaNode(
            colander.Int(),
            title=_(u"shirts"),
            oid="shirts",
        )

    schema = NewTotal()

    form = deform.Form(
        schema,
        buttons=[
            deform.Button('submit', _(u'Submit')),
            deform.Button('reset', _(u'Reset'))
        ],
        #use_ajax=True,
        #renderer=zpt_renderer
    )

    # get and show the former totals
    _totals = TheTotal.get_listing(
        TheTotal.id.asc())

    # if the form has been used and SUBMITTED, check contents
    if 'submit' in request.POST:
        print("the form was submitted")
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
            print("the appstruct: %s" % appstruct)

            # time to save the data to the DB
            #{
            #    'num_shirts': 123,
            #    'amount_collected': 12345,
            #    'amount_promised': 23456
            #}

            _new_total = TheTotal(
                amount_actual=appstruct['amount_collected'],
                amount_promised=appstruct['amount_promised'],
                num_shirts=appstruct['num_shirts'],
            )
            try:
                DBSession.add(_new_total)
                DBSession.flush()
            except:
                print("could not write to DB. Error: ")

        except ValidationFailure, e:
            print(e)

            request.session.flash(
                _(u"Please note: There were errors, "
                  "please check the form below."),
                'message_above_form',
                allow_duplicate=False)
            return{'form': e.render(),
                   'totals': {}}

    html = form.render()

    return {
        'form': html,
        'totals': _totals,
    }


@view_config(renderer='templates/login.pt',
             route_name='login')
def accountants_login(request):
    """
    This view lets accountants log in
    """
    logged_in = authenticated_userid(request)
    #print("authenticated_userid: " + str(logged_in))

    log.info("login by %s" % logged_in)

    if logged_in is not None:  # if user is already authenticated
        return HTTPFound(  # redirect her to the dashboard
            request.route_url('dashboard',
                              number=0,))

    class AccountantLogin(colander.MappingSchema):
        """
        colander schema for login form
        """
        login = colander.SchemaNode(
            colander.String(),
            title=_(u"login"),
            oid="login",
        )
        password = colander.SchemaNode(
            colander.String(),
            validator=colander.Length(min=5, max=100),
            widget=deform.widget.PasswordWidget(size=20),
            title=_(u"password"),
            oid="password",
        )

    schema = AccountantLogin()

    form = deform.Form(
        schema,
        buttons=[
            deform.Button('submit', _(u'Submit')),
            deform.Button('reset', _(u'Reset'))
        ],
        #use_ajax=True,
        #renderer=zpt_renderer
    )

    # if the form has been used and SUBMITTED, check contents
    if 'submit' in request.POST:
        #print("the form was submitted")
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
        except ValidationFailure, e:
            print(e)

            request.session.flash(
                _(u"Please note: There were errors, "
                  "please check the form below."),
                'message_above_form',
                allow_duplicate=False)
            return{'form': e.render()}

        # get user and check pw...
        login = appstruct['login']
        password = appstruct['password']

        try:
            checked = C3sStaff.check_password(login, password)
        except AttributeError:  # pragma: no cover
            checked = False
        if checked:
            log.info("password check for %s: good!" % login)
            headers = remember(request, login)
            log.info("logging in %s" % login)
            return HTTPFound(  # redirect to accountants dashboard
                location=route_url(  # after successful login
                    'dashboard',
                    number=0,
                    request=request),
                headers=headers)
        else:
            log.info("password check: failed.")

    html = form.render()
    return {'form': html, }


@view_config(renderer='templates/dashboard.pt',
             permission='manage',
             route_name='dashboard')
def accountants_desk(request):
    """
    This view lets accountants view applications and set their status:
    has their signature arrived? how about the payment?
    """
    _number_of_datasets = Speedfundings.get_number()
    #print("request.matchdict['number']: %s" % request.matchdict['number'])
    try:  # check if
        # a page number was supplied with the URL
        _page_to_show = int(request.matchdict['number'])
        #print("page to show: %s" % _page_to_show)
    except:
        _page_to_show = 0
    # is it a number? yes, cast above
    #if not isinstance(_page_to_show, type(1)):
    #    _page_to_show = 0
    #print("_page_to_show: %s" % _page_to_show)

    # check for input from "find dataset by confirm code" form
    if 'code_to_show' in request.POST:
        #print("found code_to_show in POST")
        try:
            _code = request.POST['code_to_show']
            #print(_code)
            _entry = Speedfundings.get_by_code(_code)
            #print(_entry)

            return HTTPFound(
                location=request.route_url(
                    'detail',
                    speed_id=_entry.id)
            )
        except:
            # choose default
            #print("barf!")
            pass

    # how many to display on one page?
    """
    num_display determines how many items are to be shown on one page
    """
    #print request.POST
    if 'num_to_show' in request.POST:
        #print("found it in POST")
        try:
            _num = int(request.POST['num_to_show'])
            if isinstance(_num, type(1)):
                num_display = _num
        except:
            # choose default
            num_display = 20
    elif 'num_display' in request.cookies:
        #print("found it in cookie")
        num_display = int(request.cookies['num_display'])
    else:
        #print("setting default")
        num_display = request.registry.settings[
            'speedfunding.dashboard_number']
    #print("num_display: %s " % num_display)

    """
    base_offset helps us to minimize impact on the database
    when querying for results.
    we can choose just those results we need for the page to show
    """
    #try:
    base_offset = int(_page_to_show) * int(num_display)
    #print("base offset: %s" % base_offset)
    #except:
    #    base_offset = 0
    #    if 'base_offset' in request.session:
    #        base_offset = request.session['base_offset']
    #    else:
    #        base_offset = request.registry.settings['speedfunding.offset']

    # get data sets from DB
    _speedfundings = Speedfundings.speed_listing(
        Speedfundings.id.desc(), how_many=num_display, offset=base_offset)

    # calculate next-previous-navi
    next_page = (int(_page_to_show) + 1)
    if (int(_page_to_show) > 0):
        previous_page = int(_page_to_show) - 1
    else:
        previous_page = int(_page_to_show)

    # store info about current page in cookie
    request.response.set_cookie('on_page', value=str(_page_to_show))
    #print("num_display: %s" % num_display)
    request.response.set_cookie('num_display', value=str(num_display))

    return {'_number_of_datasets': _number_of_datasets,
            'speedfundings': _speedfundings,
            'num_display': num_display,
            'next': next_page,
            'previous': previous_page,
            }


# @view_config(permission='manage',
#              route_name='switch_sig')
# def switch_sig(request):
#     """
#     This view lets accountants switch member signature info
#     has their signature arrived?
#     """
#     memberid = request.matchdict['memberid']
#     #log.info("the id: %s" % memberid)

#     # store the dashboard page the admin came from
#     dashboard_page = request.cookies['on_page']

#     _member = C3sMember.get_by_id(memberid)
#     if _member.signature_received is True:
#         _member.signature_received = False
#         _member.signature_received_date = datetime(1970, 1, 1)
#     elif _member.signature_received is False:
#         _member.signature_received = True
#         _member.signature_received_date = datetime.now()

#     log.info(
#         "signature status of member.id %s changed by %s to %s" % (
#             _member.id,
#             request.user.login,
#             _member.signature_received
#         )
#     )

#     return HTTPFound(
#         request.route_url('dashboard',
#                           number=dashboard_page,))


@view_config(permission='manage',
             route_name='delete_entry')
def delete_entry(request):
    """
    This view lets accountants delete entries (doublettes)
    """
    _id = request.matchdict['speed_id']
    dashboard_page = request.cookies['on_page']
    _entry = Speedfundings.get_by_id(_id)

    Speedfundings.delete_by_id(_entry.id)
    #log.info(
    #    "entry.id %s was deleted by %s" % (
    #        _entry.id,
    #        request.user.login,
    #    )
    #)

    return HTTPFound(
        request.route_url('dashboard',
                          number=dashboard_page,))


@view_config(permission='manage',
             route_name='switch_pay')
def switch_pay(request):
    """
    This view lets accountants switch member signature info
    has their signature arrived?
    """
    speed_id = request.matchdict['speed_id']
    dashboard_page = request.cookies['on_page']
    _entry = Speedfundings.get_by_id(speed_id)

    if _entry.payment_received is True:  # change to NOT SET
        _entry.payment_received = False
        _entry.payment_received_date = datetime(1970, 1, 1)
    elif _entry.payment_received is False:  # set to NOW
        _entry.payment_received = True
        _entry.payment_received_date = datetime.now()

#    log.info(
#        "payment info of speedfunding.id %s changed by %s to %s" % (
#            _entry.id,
#            request.user.login,
#            _entry.payment_received
#        )
#    )
    return HTTPFound(
        request.route_url('dashboard',
                          number=dashboard_page,))


@view_config(renderer='templates/detail.pt',
             permission='manage',
             route_name='detail')
def speedfunding_detail(request):
    """
    This view lets accountants view speedfunding details
    has their signature arrived? how about the payment?
    """
    #logged_in = authenticated_userid(request)
    #log.info("detail view.................................................")
    #print("---- authenticated_userid: " + str(logged_in))

    speedfundingid = request.matchdict['speed_id']
    #log.info("the id: %s" % speedfundingid)

    _speedfunding = Speedfundings.get_by_id(speedfundingid)

    #print(_speedfunding)
    if _speedfunding is None:  # that speed_id did not produce good results
        return HTTPFound(  # back to base
            request.route_url('dashboard',
                              number=0,))

    class ChangeDetails(colander.MappingSchema):
        """
        colander schema (form) to change details of speedfunding
        """
        payment_received = colander.SchemaNode(
            colander.Bool(),
            title=_(u"Have we received payment for the funding item??")
        )

    schema = ChangeDetails()
    form = deform.Form(
        schema,
        buttons=[
            deform.Button('submit', _(u'Submit')),
            deform.Button('reset', _(u'Reset'))
        ],
        use_ajax=True,
        renderer=zpt_renderer
    )

    # if the form has been used and SUBMITTED, check contents
    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
        except ValidationFailure, e:  # pragma: no cover
            log.info(e)
            #print("the appstruct from the form: %s \n") % appstruct
            #for thing in appstruct:
            #    print("the thing: %s") % thing
            #    print("type: %s") % type(thing)
            print(e)
            #message.append(
            request.session.flash(
                _(u"Please note: There were errors, "
                  "please check the form below."),
                'message_above_form',
                allow_duplicate=False)
            return{'form': e.render()}

        # change info about speedfunding in database

        test1 = (  # changed value through form (different from db)?
            appstruct[
                'signature_received'
            ] == _speedfunding.signature_received)
        if not test1:
            log.info(
                "info about signature of %s changed by %s to %s" % (
                    _speedfunding.id,
                    request.user.login,
                    appstruct['signature_received']))
            _speedfunding.signature_received = appstruct['signature_received']
        test2 = (  # changed value through form (different from db)?
            appstruct['payment_received'] == _speedfunding.payment_received)
        if not test2:
            log.info(
                "info about payment of %s changed by %s to %s" % (
                    _speedfunding.id,
                    request.user.login,
                    appstruct['payment_received']))
            _speedfunding.payment_received = appstruct['payment_received']
        # store appstruct in session
        request.session['appstruct'] = appstruct

        # show the updated details
        HTTPFound(route_url('detail', request, speedfundingid=speedfundingid))

    # else: form was not submitted: just show speedfunding info and form
    else:
        appstruct = {  # populate form with values from DB
            #'signature_received': _speedfunding.signature_received,
            'payment_received': _speedfunding.payment_received}
        form.set_appstruct(appstruct)
        #print("the appstruct: %s") % appstruct
    html = form.render()

    return {'speedfunding': _speedfunding,
            'form': html}


@view_config(permission='view',
             route_name='logout')
def logout_view(request):
    """
    can be used to log a user/staffer off. "forget"
    """
    request.session.invalidate()
    request.session.flash(u'Logged out successfully.')
    headers = forget(request)
    return HTTPFound(location=route_url('login', request),
                     headers=headers)
