from django.urls import path
from .views.main_page import MainPage
from .views.about_page import AboutPage
from .views.cart_page import CartPage
from .views.historyorder_page import HistoryorderPage
from .views.catalog_page import CatalogPage
from .views.order_details_page import OrderDetailsPage
from .views.order_page import OrderPage
from .views.payment_page import PaymentPage
from .views.payment_someone_page import PaymentSomeonePage
from .views.product_page import ProductPage
from .views.registration_page import RegistrationPage
from .views.authenticate_page import AuthenticatePage, LogOutView
from .views.profile_avatar_page import ProfileAvatarPage
from .views.progress_payment_page import ProgressPaymentPage
from .views.account_page import AccountPage
from .views.sale_page import SalePage


urlpatterns = [
    path('', MainPage.as_view(), name='index'),
    path('about', AboutPage.as_view(), name='about'),
    path('cart', CartPage.as_view(), name='cart'),
    path('history', HistoryorderPage.as_view(), name='history'),
    path('catalog/<int:pk>', CatalogPage.as_view(), name='catalog'),
    path('order-details', OrderDetailsPage.as_view(), name='order-details'),
    path('order', OrderPage.as_view(), name='order'),
    path('payment', PaymentPage.as_view(), name='payment'),

    path('payment-someone', PaymentSomeonePage.as_view(), name='payment-someone'),
    path('product/<int:pk>', ProductPage.as_view(), name='product'),
    path('registration', RegistrationPage.as_view(), name='registration'),
    path('authenticate', AuthenticatePage.as_view(), name='authenticate'),
    path('logout', LogOutView.as_view(), name='logout'),
    path('profile-avatar', ProfileAvatarPage.as_view(), name='profile-avatar'),
    path('progress-payment', ProgressPaymentPage.as_view(), name='progress-payment'),
    path('account', AccountPage.as_view(), name='account'),
    path('sale', SalePage.as_view(), name='sale'),
]