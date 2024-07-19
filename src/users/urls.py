from django .urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage' ),
    path('productpage/', views.productpage, name='productpage'),
    path('productdetail/<int:product_id>', views.product_detail, name='productdetail'),    
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout,name='logout'),
    path('addtocart/<int:product_id>',views.add_to_cart,name='addtocart'),
    path('cart/',views.viewcart,name='cart')
]
