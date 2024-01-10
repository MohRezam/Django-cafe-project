from django.urls import path
from . import views


app_name = "accounts"

urlpatterns = [
    path('register/',views.StaffRegisterView.as_view(),name="staff-register"),
    path('profile/',views.StffProfileView.as_view(),name="staff-profile"),
    path('login/',views.StaffLoginView.as_view(),name="staff-login"),
    path('Logout/',views.StffLogoutView.as_view(),name="staff-logout"),
    path('profile-info/<int:staff_user_id>/',views.StaffProfileInfoView.as_view(),name="staff-profile-info"),
    path('profile-personal-info/',views.StaffProfilePersonalView.as_view(),name="staff-personal-info"),
    path('profile-categories/',views.StaffProfileCategoriesView.as_view(),name="staff-categories"),
    path('profile-category-delete/<int:id_category>/',views.StaffCategoryDeleteView.as_view(),name="staff-category-delete"),
    path('profile-category-update/<int:id_category>/',views.StaffCategoryUpdateView.as_view(),name="staff-category-update"),
    path('profile-add-category/',views.StaffAddCategoryView.as_view(),name="staff-add-category"),
    path('profile-items/',views.StaffProfileItemsView.as_view(),name="staff-items"),
    path('profile-item-delete/<int:id_item>/',views.StaffProfileDeleteItemView.as_view(),name="staff-delete-item"),
    path('profile-item-update/<int:id_item>/',views.StaffProfileUpdateItemView.as_view(),name="staff-update-item"),
    path('profile-add-item/',views.StaffProfileAddItemView.as_view(),name="staff-add-item"),
    path('profile-orders/',views.StaffProfileOrdersView.as_view(),name="staff-orders"),
    path('profile-order-uncomplete/',views.StaffProfileOrderUncompleteView.as_view(),name="staff-orders-uncomplete"),
    path('profile-order-complete/',views.StaffProfileOrdercompleteView.as_view(),name="staff-orders-complete"),
    path('profile-order-details/<int:id_order>/',views.StaffProfileOrderDetailView.as_view(),name="staff-order-detail"),
    path('profile-reports-and-insights/',views.StaffReportsInsightsView.as_view(),name="staff-reports-insights"),
    path('profile-edite-order/<int:id_order>/', views.StaffChangeOrderView.as_view(), name='staff-change-order'),
    path('profile-add-order/',views.StaffAddOrderView.as_view(),name="staff-add-order"),
    path('profile-delete-order/<int:order_id>/',views.StaffDeleteOrderView.as_view(),name="staff-delete-order"),
    path('profile-list-user/',views.StaffUserView.as_view(),name="staff-list-user"),
    path('profile-user-delete/<int:id_user>/',views.StaffUserDeleteView.as_view(),name="staff-delete-user"),
    path('profile-list-table/',views.StaffTablesView.as_view(),name="staff-list-table"),
    path('profile-table-delete/<int:id_table>/',views.StaffDeleteTableView.as_view(),name="staff-delete-table"),
    path('profile-edite-table/<int:id_table>',views.StaffTableFormView.as_view(),name="staff-edite-table"),
    path('csv-statics/',views.StatisticsView.as_view(),name="staff-csv-file")

]
