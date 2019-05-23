Alert = (function () {
  var self = {};

  self.loaderObj = null;

  self.animation = function () {
    let anims = [
      "https://media1.tenor.com/images/75643fee47adf65a46b50261be687697/tenor.gif?itemid=7830200",
      "https://cdn.dribbble.com/users/255512/screenshots/2192065/animation.gif",
      "https://cdn.dribbble.com/users/279765/screenshots/1918018/loadinganimation.gif",
      "https://cdn.dribbble.com/users/563824/screenshots/3633228/untitled-5.gif",
      "https://mir-s3-cdn-cf.behance.net/project_modules/disp/b6e0b072897469.5bf6e79950d23.gif",
      "https://createwebsite.net/wp-content/uploads/2015/09/Loader1.gif",
    ]
    return anims[Math.floor(Math.random() * anims.length)]
  }

  self.Loader = function () {
    let app = self;
    self.loaderObj = swal({
      title: "Please Wait",
      imageUrl: app.animation(),
      imageAlt: "Loader",
      backdrop: `
        rgba(23, 24, 33, 0.81)
      `,
      timer: 8000,
      allowOutsideClick: false,
      showConfirmButton: false
    }).catch(swal.noop);
  };

  self.StopLoader = function () {
    swal({
      timer: 0.1,
      showConfirmButton: false,
      allowOutsideClick: false
    }).catch(swal.noop);
  };

  self.Info = function (msg) {
    swal({
      title: "<strong>Info</strong>",
      type: "info",
      html: "<pre>" + msg + "</pre>"
    }).catch(swal.noop);
  };

  return self;
})();

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
];

const router = new VueRouter({
  routes
});

Vue.directive('init', {
  bind: function (el, binding, vnode) {
    vnode.context[binding.arg] = binding.value;
  }
});

const app = new Vue({
  router,
  data: {
    userInfo: {
      isLogin: false,
      fullName: "Guest",
      userType: "Guest",
      roles: []
    }
  },
  methods: {
    checkLoginStatus(neededRoles = []) {
      if (!this.userInfo.isLogin) {
        this.userInfo.isLogin = false;
        this.userInfo.userType = null;
        this.userInfo.roles = [];
        this.userInfo.fullName = "Guest";
        toastr.error("Your are not login.", "Error", {
          timeOut: 5000,
          closeButton: true
        });
        router.push("/");
        return;
      }
      if (neededRoles) {
        for (role in neededRoles) {
          if (this.userInfo.roles.indexOf(neededRoles[role]) != -1) {
            return true;
          }
        }
        return false;
      }
    },
    isSignIn(callBack) {
      this.$http.get("/user/is-signin").then(
        function (response) {
          this.userInfo = response.data;
        },
        function (response) {
          toastr.error("Error in Connection - " + response.data.msg, "Error", {
            timeOut: 5000,
            closeButton: true
          });
        }
      );
    },
    goToDashboard(userType) {
      switch (userType) {
        case "admin":
          router.push("/admin/dashboard");
          break;
        case "employee":
          router.push("/payment");
          break;
        case "Guest":
          router.push("/login");
          break;
        default:
          router.push("/login");
      }
    },
    singout() {
      this.$http.get("/user/signout").then(
        function (response) {
          this.userInfo = response.data;
          router.push("/");
        },
        function (response) {
          toastr.error("Error in Connection - " + response.data.msg, "Error", {
            timeOut: 5000,
            closeButton: true
          });
        }
      );
    }
  },
  computed: {},
  mounted() {
    this.isSignIn();
  }
}).$mount("#app");

$(document).ready(function () {
  $(".mdb-select").material_select();
});



jQuery.fn.putCursorAtEnd = function () {

  return this.each(function () {

    // Cache references
    var $el = $(this),
      el = this;

    // Only focus if input isn't already
    if (!$el.is(":focus")) {
      $el.focus();
    }

    // If this function exists... (IE 9+)
    if (el.setSelectionRange) {

      // Double the length because Opera is inconsistent about whether a carriage return is one character or two.
      var len = $el.val().length * 2;

      // Timeout seems to be required for Blink
      setTimeout(function () {
        el.setSelectionRange(len, len);
      }, 1);

    } else {

      // As a fallback, replace the contents with itself
      // Doesn't work in Chrome, but Chrome supports setSelectionRange
      $el.val($el.val());

    }

    // Scroll to the bottom, in case we're in a tall textarea
    // (Necessary for Firefox and Chrome)
    this.scrollTop = 999999;

  });

};