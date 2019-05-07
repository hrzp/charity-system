<template type="text/x-template">
  <div class>
    <hr>
    <!--Panel-->
    <div class="d-flex justify-content-center">
      <div class="card border-secondary mb-3" style="max-width: 100%;width: 70%;">
        <div class="card-body text-secondary">
          <h3>Your Mail Didnt Verify.Please enter the captcha and click send.</h3>
          <h2
            style="color: black"
          >We Will send an mail to your mail address and you have to click on activeated link in your mail</h2>
          <hr>
        </div>
        <div class="card-text">
          <div class="d-flex justify-content-center">
            <div class="row">
              <form class>
                <div class="col" v-if="msg.length == 0">
                  <div class>
                    <a class="icons-sm git-ic" @click="getCaptcha">
                      <i class="fa fa-refresh fa-2x"></i>
                    </a>
                    <img v-bind:src="'data:image/png;base64,'+captcha">
                  </div>
                  <hr>
                  <input type="text" name value v-model="captchaValue" placeholder="captch number">
                  <button type="submit" class="btn btn-primary" @click="sendMail">Send</button>
                </div>
              </form>
              <div class="col-12">
                <p class="mdb-color white-text">{{ msg }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!--/.Panel-->
  </div>
</template>

<script>
module.exports = {
  data: function() {
    return {
      captcha: null,
      captchaValue: null,
      msg: ""
    };
  },
  methods: {
    init() {
      this.getCaptcha();
    },
    getCaptcha() {
      this.$http.get("/general/new-captcha").then(
        function(response) {
          this.captcha = response.data.args.captcha;
        },
        function(response) {
          toastr.error("Error in Connection - " + response.data.msg, "Error", {
            timeOut: 5000,
            closeButton: true
          });
        }
      );
    },
    sendMail() {
      if (!this.captchaValue) {
        toastr.error("Please enter the captcha value", "Error", {
          timeOut: 5000,
          closeButton: true
        });
        return;
      }
      let data = {
        captcha_value: this.captchaValue
      };
      Alert.Loader();
      this.$http.post("/user/sendmailverifaction", data).then(
        function(response) {
          toastr.success(response.data.msg, "Successfuly", {
            timeOut: 5000,
            closeButton: true
          });
          this.msg =
            "Please check your mail and click on activate link, then Login again";
          this.signout();
          Alert.StopLoader();
        },
        function(response) {
          toastr.error("Error in Connection - " + response.data.msg, "Error", {
            timeOut: 5000,
            closeButton: true
          });
        }
      );
    },
    signout() {
      this.$http.get("/user/signout").then(
        function(response) {},
        function(response) {
          toastr.error("Error in Connection - " + response.data.msg, "Error", {
            timeOut: 5000,
            closeButton: true
          });
        }
      );
    }
  },
  updated() {
    if (!this.$root.checkLoginStatus(["admin", "employee"])) {
      toastr.error("Your are not allow to open this", "...", {
        timeOut: 5000,
        closeButton: true
      });
      router.push("/");
    }
  },
  created() {
    this.init();
  }
};
</script>

<style lang="css">
.input-info {
  margin-top: 10%;
}
</style>
