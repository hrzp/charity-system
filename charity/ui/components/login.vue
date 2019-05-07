<template>
  <div>
    <div class="wrapper fadeInDown">
      <div id="formContent">
        <!-- Tabs Titles -->
        <!-- Icon -->
        <div class="fadeIn first">
          <img src="assets/icon/icon.svg" id="icon" alt="User Icon">
        </div>
        <!-- Login Form -->
        <div>
          <input
            type="text"
            id="username"
            class="fadeIn second"
            placeholder="username"
            v-model="username"
          >
          <input
            type="password"
            id="password"
            class="fadeIn third"
            placeholder="password"
            v-model="password"
            v-on:keyup.enter="singin"
          >
          <input type="submit" class="fadeIn fourth" @click="singin" value="Log In">
        </div>
        <!-- Remind Passowrd -->
        <div id="formFooter">
          <div class="underlineHover">
            <div id="remember" class="checkbox">
              <label>
                <input type="checkbox" value="remember-me"> Remember me
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
module.exports = {
  data: function() {
    return {
      username: null,
      password: null,
      rememberMe: null
    };
  },
  components: {},
  methods: {
    singin() {
      if (!this.username) {
        toastr.error("Username is Empty", "Error", {
          timeOut: 5000,
          closeButton: true
        });
        return;
      }
      if (!this.password) {
        toastr.error("Passowrd is Empty", "Error", {
          timeOut: 5000,
          closeButton: true
        });
        return;
      }
      data = {
        username: this.username,
        password: this.password
      };
      this.$http.post("/user/login", data).then(
        function(response) {
          toastr.success("Wellcome Back: " + response.data.name, {
            timeOut: 5000,
            closeButton: true
          });
          this.doAction(response.data);
        },
        function(response) {
          toastr.error(response.data.msg, "Error in Connection", {
            timeOut: 5000,
            closeButton: true
          });
        }
      );
    },

    doAction(data) {
      this.$root.userInfo = data;
      if (!data.isLogin) {
        toastr.error(data.msg, "Error in Login", {
          timeOut: 5000,
          closeButton: true
        });
        return;
      }
      if (data.mailVerified == false) {
        router.push("/user/mail-verification");
        return;
      }
      if (data.ForceToChangePassword == true) {
        router.push("/user/change-password");
        return;
      }
      switch (data.userType) {
        case "admin":
          router.push("/admin/dashboard/login-report");
          break;
        case "employee":
          break;
        default:
          toastr.error(data.msg, "Error in Login", {
            timeOut: 5000,
            closeButton: true
          });
          return;
      }
      toastr.success("Welecome Back", "Login Successfuly Done", {
        timeOut: 5000,
        closeButton: true
      });
    }
  }
};
</script>

<style>
</style>
