const router = new VueRouter({
  routes // from routes.jsloader: true,
});

Vue.directive('init', {
  bind: function (el, binding, vnode) {
    vnode.context[binding.arg] = binding.value;
  }
});


const app = new Vue({
  router,
  data: function () {
    return {
      loader: true,
      userInfo: {
        isLogin: false,
        fullName: "Guest",
        userType: "Guest",
        roles: []
      }
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
    isSignin(callBack) {
      let app = this;
      API.get("/user/is-signin").then(function (response) {
        app.userInfo = response.data;
        if (!app.userInfo.isLogin) {
          router.push('/login');
          toastr.info('You are not login', { timeOut: 8000 })
        }
      });
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
      let app = this;
      API.get("/user/signout").then(
        function (response) {
          setHeaders('', '')
          app.userInfo = response.data;
          router.push("/");
          toastr.success("Logout successfully", "Success", {
            timeOut: 10000,
            closeButton: true
          })
        });
    }
  },
  mounted() {
    setTimeout(function () {
      $('.lds-parent').hide(); // user jquery, because out of app
    }, 2000)
  }
}).$mount("#app");

$(document).ready(function () {
  $(".mdb-select").material_select();
});

function getHeaders(forAxios = false) {
  let access_token = refresh_token = '';
  if (localStorage.access_token) {
    access_token = localStorage.getItem('access_token');
  }
  if (forAxios) {
    return 'Bearer ' + access_token
  }
  return {
    headers: {
      'Authorization': 'Bearer ' + access_token
    }
  }
}

function setHeaders(access_token, refresh_token) {
  localStorage.access_token = access_token;
  localStorage.refresh_token = refresh_token;
  API.defaults.headers.Authorization = 'Bearer ' + access_token;
}

function msgHandler(response) {

}
function pr() {
  console.log.apply(console, arguments);
}

var API = axios.create({
  timeout: 10000,
  headers: { 'Authorization': getHeaders(true) }
});


// Api call error handling
API.interceptors.response.use(null, function (error) {
  let msg = '';
  if (error.request.status == 0) {
    msg = "Please check your internt conection or call site manager"
  }
  if (error.response && (error.response.status === 401 || error.response.status === 422)) {
    if (error.response.data.msg == "Token has expired") {
      msg = "your session has expired. Please login again"
    }
    else {
      msg = "You are not login"
    }
  }
  if (error.response && error.response.status === 400) {
    msg = error.response.data.msg;
  }
  toastr.error(msg, "Error", {
    timeOut: 15000,
    closeButton: true
  })

  return Promise.reject(error);
});

