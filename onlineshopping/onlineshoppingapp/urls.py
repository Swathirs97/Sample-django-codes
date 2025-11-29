from django.urls import path
from onlineshoppingapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('register', views.register, name='register'),
    path('list', views.productlist, name='list'),
    path('category/<int:id>/', views.category_detail, name='category_detail'),
    path('edit/<int:p_id>/', views.edit_product, name='edit'),
    path('delete/<int:p_id>/', views.delete_product, name='delete'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('search',views.search,name='search'),
    path('admin-panel', views.admin_panel, name='admin_panel'),
    path('add-category', views.add_category, name='add_category'),
    path('edit-category/<int:c_id>/', views.edit_category, name='edit_category'),
    path('delete-category/<int:c_id>/', views.delete_category, name='delete_category'),
    path('wishlist', views.view_wishlist, name='wishlist'),
    path('add-to-wishlist/<int:p_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:p_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('cart', views.view_cart, name='cart'),
    path('add-to-cart/<int:p_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:p_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart-quantity/<int:p_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('buy-now/<int:p_id>/', views.buy_now, name='buy_now'),
    path('bill/<int:order_id>/', views.bill, name='bill'),
    path('checkout/', views.checkout, name='checkout'),
    path('submit-review/<int:p_id>/', views.submit_review, name='submit_review'),
    path('reply-review/<int:review_id>/', views.reply_to_review, name='reply_to_review'),
    path('delete-review/<int:review_id>/', views.delete_review, name='delete_review')
]