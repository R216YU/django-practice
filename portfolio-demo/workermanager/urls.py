from django.urls import path
from .views import index, signupFunc, loginFunc, logoutFunc, workerInfoFunc, addWorkingInfoFunc, workerListFunc, deleteWorkerFunc, adminWorkerInfoFunc

urlpatterns = [
    path('', index, name="index"),
    path('signup/', signupFunc, name="signup"),
    path('login/', loginFunc, name="login"),
    path('logout/', logoutFunc, name="logout"),
    path('worker_info/', workerInfoFunc, name="workerInfo"),
    path('worker_info/<int:id>', workerInfoFunc, name="adminWorkerInfo"),
    path('add_working_info/', addWorkingInfoFunc, name="addWorkingInfo"),
    path('manage/worker_list/', workerListFunc, name="workerList"),
    path('manage/worker_info/<int:id>', adminWorkerInfoFunc, name="adminWorkerInfo"),
    path('manage/worker_delete/<int:id>', deleteWorkerFunc, name="deleteWorker"),
]
