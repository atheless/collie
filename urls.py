"""
Routing urls.
"""


from routing import Router
from security.basic.authentication import basic_auth_handler, loginPage, logout_handler
from views import home_handler, about_handler, UserModelView, some_handler

router = Router()

# Examples
router.add_route("/", 'GET', home_handler)
router.add_route("/about", 'GET', about_handler)
router.add_route("/api", 'GET', UserModelView.as_view())
router.add_route("/auth", 'POST', basic_auth_handler)
router.add_route("/login", 'GET', loginPage)
router.add_route("/logout", 'GET', logout_handler)
router.add_route('/api/<pk>', 'GET', UserModelView.as_view())
router.add_route('/test/<pk>/', 'GET', some_handler)