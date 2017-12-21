from twisted.internet.defer import inlineCallbacks

from yombo.core.exceptions import YomboWarning
from yombo.core.log import get_logger
from yombo.lib.webinterface.auth import require_auth

logger = get_logger("modules.homebridge.web_routes")

def module_homebridge_routes(webapp):
    """
    Adds routes to the webinterface module.

    :param webapp: A pointer to the webapp, it's used to setup routes.
    :return:
    """
    with webapp.subroute("/modules_settings") as webapp:

        def root_breadcrumb(webinterface, request):
            webinterface.add_breadcrumb(request, "/?", "Home")
            webinterface.add_breadcrumb(request, "/modules/index", "Modules")
            webinterface.add_breadcrumb(request, "/modules_settings/homebridge/index", "Homebridge")

        @webapp.route("/homebridge", methods=['GET'])
        @require_auth()
        def page_module_homebridge_get(webinterface, request, session):
            return webinterface.redirect(request, '/modules/homebridge/index')

        @webapp.route("/homebridge/index", methods=['GET'])
        @require_auth()
        def page_module_homebridge_index_get(webinterface, request, session):
            homebridge = webinterface._Modules['HomeBridge']

            page = webinterface.webapp.templates.get_template('modules/homebridge/web/index.html')
            root_breadcrumb(webinterface, request)

            return page.render(alerts=webinterface.get_alerts(),
                               homebridge=homebridge,
                               )

        @webapp.route("/homebridge/rotate_username", methods=['GET'])
        @require_auth()
        def page_module_homebridge_rotate_username_get(webinterface, request, session):
            homebridge = webinterface._Modules['HomeBridge']

            page = webinterface.webapp.templates.get_template('modules/homebridge/web/rotate_username.html')
            root_breadcrumb(webinterface, request)
            webinterface.add_breadcrumb(request, "/modules_settings/homebridge/rotate_username", "Rotate Username & Pin")
            return page.render(alerts=webinterface.get_alerts(),
                               homebridge=homebridge,
                               )

        @webapp.route('/homebridge/rotate_username', methods=['POST'])
        @require_auth()
        @inlineCallbacks
        def page_module_homebridge_rotate_username_post(webinterface, request, session):
            homebridge = webinterface._Modules['HomeBridge']

            try:
                confirm = request.args.get('confirm')[0]
            except Exception:
                confirm = None
            if confirm != "rotate":
                page = webinterface.webapp.templates.get_template('modules/homebridge/web/rotate_username.html')
                webinterface.add_alert('Must enter "rotate" in the confirmation box.', 'warning')
                webinterface.add_breadcrumb(request, "/modules_settings/homebridge/rotate_username",
                                            "Rotate Username & Pin")
                return page.render(alerts=webinterface.get_alerts(),
                                   homebridge=homebridge,
                                   )
            try:
                yield homebridge.rotate_username()
            except YomboWarning as e:
                webinterface.add_alert(e.message, 'warning')
            else:
                webinterface.add_alert('Restarting Homebridge.', 'warning')

            return webinterface.redirect(request, '/modules_settings/homebridge/index')

        @webapp.route("/homebridge/restart_homebridge", methods=['GET'])
        @require_auth()
        def page_module_homebridge_restart_homebridge_get(webinterface, request, session):
            homebridge = webinterface._Modules['HomeBridge']

            page = webinterface.webapp.templates.get_template('modules/homebridge/web/restart_homebridge.html')
            root_breadcrumb(webinterface, request)
            webinterface.add_breadcrumb(request, "/modules_settings/homebridge/restart_homebridge", "Restart Homebridge")
            return page.render(alerts=webinterface.get_alerts(),
                               homebridge=homebridge,
                               )

        @webapp.route('/homebridge/restart_homebridge', methods=['POST'])
        @require_auth()
        @inlineCallbacks
        def page_module_homebridge_restart_homebridge_post(webinterface, request, session):
            homebridge = webinterface._Modules['HomeBridge']

            try:
                yield homebridge.restart_homebridge()
            except YomboWarning as e:
                webinterface.add_alert(e.message, 'warning')
            else:
                webinterface.add_alert('Restarting Homebridge.', 'warning')

            return webinterface.redirect(request, '/modules_settings/homebridge/index')
