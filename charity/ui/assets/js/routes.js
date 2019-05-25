const routes = [{
    path: "/",
    component: httpVueLoader("components/home.vue")
},
{
    path: "/login",
    component: httpVueLoader("components/login.vue")
},
{
    path: "/admin",
    component: httpVueLoader("components/admin.vue")
},
{
    path: "/admin/dashboard",
    component: httpVueLoader("components/admin.vue")
},
{
    path: "/admin/2fa",
    component: httpVueLoader("components/admin_components/2fa.vue")
},
{
    path: "/admin/dashboard/wallet-managment/:id",
    component: httpVueLoader("components/admin_components/walletManagement.vue")
},
{
    path: "/admin/dashboard/log-report",
    component: httpVueLoader("components/admin_components/logs.vue")
},
{
    path: "/admin/dashboard/login-report",
    component: httpVueLoader("components/admin_components/loginHistory.vue")
},
{
    path: "/admin/dashboard/role-managment",
    component: httpVueLoader("components/admin_components/roleManagment.vue")
},
{
    path: "/admin/dashboard/role-managment/:id",
    component: httpVueLoader("components/admin_components/roleManagment.vue")
},
{
    path: "/admin/dashboard/user-managment",
    component: httpVueLoader("components/admin_components/userManagment.vue")
},
{
    path: "/admin/dashboard/shutdown-api",
    component: httpVueLoader("components/admin_components/shutdownApi.vue")
},
{
    path: "/user/mail-verification",
    component: httpVueLoader("components/common/mailVerification.vue")
},
{
    path: "/user/change-password",
    component: httpVueLoader("components/common/changePassword.vue")
},
{
    path: "/payment",
    component: httpVueLoader("components/payment.vue")
},
{
    path: "/admin/base-category",
    component: httpVueLoader("components/admin_components/base-info/category.vue")
},
{
    path: "/admin/base-item/:id",
    component: httpVueLoader("components/admin_components/base-info/subCategory.vue")
},
];
