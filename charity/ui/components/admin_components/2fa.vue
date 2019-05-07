<template type="text/x-template">
  <div class>
    <hr>

    <!--Panel-->
    <div class="d-flex justify-content-center">
      <div class="card border-secondary mb-3" style="max-width: 100%;width: 70%;">
        <div class="card-body text-secondary">
          <h3>Please save this code to your google authenticateor</h3>
        </div>
        <div class="card-text">
          <div class="d-flex justify-content-center">
            <div class="row">
              <div class="col-sm-12 col-md-12 col-lg-12 d-flex justify-content-center">
                <strong>URI:</strong>
                {{ secret }}
              </div>
              <div class="col-sm-12 col-md-12 col-lg-12 d-flex justify-content-center">
                <div class id="2fa-uri"></div>
              </div>
              <div class="col-sm-12 col-md-12 col-lg-12 row input-info">
                <div class="col">Please enter key to authenticate your device</div>
                <div class="col">
                  <input type="text" name value v-model="key">
                </div>
                <div class="col">
                  <button type="button" class="btn btn-primary" name="button" @click="sendKey">Send</button>
                </div>
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
      secret: null,
      key: null
    };
  },
  methods: {
    init() {
      this.get2faKey();
    },

    get2faKey() {
      Alert.Loader();
      this.$http.get("/user/2fa").then(
        function(response) {
          if (!response.data.status) {
            toastr.error("Somthing Wrong", "Error", {
              timeOut: 5000,
              closeButton: true
            });
            return;
          }
          var qrcode = new QRCode("2fa-uri", {
            text: "Nothing",
            width: 255,
            height: 255,
            colorDark: "#000000",
            colorLight: "#ffffff",
            correctLevel: QRCode.CorrectLevel.H
          });
          qrcode.clear();
          qrcode.makeCode(response.data.uri);
          this.secret = response.data.secret;
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

    sendKey() {
      Alert.Loader();
      if (!this.key) {
        toastr.error("Please enter the key", "Error", {
          timeOut: 5000,
          closeButton: true
        });
        return;
      }
      let data = {
        key: this.key
      };
      this.$http.post("/user/2favalidate", data).then(
        function(response) {
          toastr.success(response.data.msg, "Successfuly", {
            timeOut: 5000,
            closeButton: true
          });
          router.push("/admin/dashboard");
          Alert.StopLoader();
        },
        function(response) {
          toastr.error("Error in Connection - " + response.data.msg, "Error", {
            timeOut: 5000,
            closeButton: true
          });
        }
      );
    }
  },
  // components: {

  // },
  mounted() {},
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
