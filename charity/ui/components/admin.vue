<template type="text/x-template">
  <div class>
    <hr>
    <!--Login history-->
    <div class="card mdb-color lighten-2 text-center z-depth-2">
      <div class="card-body">
        <div class="white-text row" style="float: left;width:100%;">
          <div class="col-2">
            <strong>Last Login Info:</strong>
          </div>
          <div class="col-2">
            <strong>Ip:</strong>
            {{ userInfo.history.ip }}
          </div>
          <div class="col-2">
            <strong>Time:</strong>
            {{ userInfo.history.lastLoginDate }}
          </div>
          <div class="col-3"></div>
          <div class="col-3">
            <a class="show-more" @click="setPanel('loginHistory')">Show More</a>
          </div>
        </div>
      </div>
    </div>
    <!--/.Login history-->

    <hr>

    <div class="row justify-content-center" v-if="panel!='loginHistory'">
      <div class="card-deck col-sm-3">
        <!-- Bitcoin Card -->
        <div class="card mb-4">
          <!--Card image-->
          <div class="view overlay">
            <img
              width="200"
              height="250"
              class="card-img-top"
              src="assets/image/btc.jpg"
              alt="Card image cap"
            >
            <a href="#">
              <div class="mask rgba-white-slight"></div>
            </a>
          </div>

          <!--Card content-->
          <div class="card-body">
            <!--Title-->
            <h4 class="card-title">Bitcoin</h4>
            <!--Text-->
            <p class="card-text"></p>
            <!-- Provides extra visual weight and identifies the primary action in a set of buttons -->
            <a
              type="button"
              class="btn btn-primary btn-md"
              href="#/admin/dashboard/wallet-managment/btc"
            >Open Wallet Managment</a>
          </div>
        </div>
      </div>

      <!-- Ethereum Card -->
      <div class="card-deck col-sm-3">
        <!-- Bitcoin Card -->
        <div class="card mb-4">
          <!--Card image-->
          <div class="view overlay">
            <img
              width="200"
              height="250"
              class="card-img-top"
              src="assets/image/eth.jpg"
              alt="Card image cap"
            >
            <a href="#">
              <div class="mask rgba-white-slight"></div>
            </a>
          </div>

          <!--Card content-->
          <div class="card-body">
            <!--Title-->
            <h4 class="card-title">Ethereum</h4>
            <!--Text-->
            <p class="card-text"></p>
            <!-- Provides extra visual weight and identifies the primary action in a set of buttons -->
            <a
              type="button"
              class="btn btn-primary btn-md"
              href="#/admin/dashboard/wallet-managment/eth"
            >Open Wallet Managment</a>
          </div>
        </div>
      </div>
      <!-- Ethereum Card -->

      <!-- Tether Card -->
      <div class="card-deck col-sm-3">
        <!-- Bitcoin Card -->
        <div class="card mb-4">
          <!--Card image-->
          <div class="view overlay">
            <img
              width="200"
              height="250"
              class="card-img-top"
              src="assets/image/teth.jpg"
              alt="Card image cap"
            >
            <a href="#">
              <div class="mask rgba-white-slight"></div>
            </a>
          </div>

          <!--Card content-->
          <div class="card-body">
            <!--Title-->
            <h4 class="card-title">Tether</h4>
            <!--Text-->
            <p class="card-text"></p>
            <!-- Provides extra visual weight and identifies the primary action in a set of buttons -->
            <a
              type="button"
              class="btn btn-primary btn-md"
              href="#/admin/dashboard/wallet-managment/tether"
            >Open Wallet Managment</a>
          </div>
        </div>
      </div>
      <!-- Tether Card -->
    </div>

    <!--/.Wallet Managment Panel-->

    <div v-if="panel=='loginHistory'">
      <login-history></login-history>
    </div>
  </div>
</template>

<script>
module.exports = {
  data: function() {
    return {
      panel: "home",
      userInfo: {
        history: {
          ip: null,
          lastLoginDate: null
        },
        username: null,
        fullName: null
      }
    };
  },
  watch: {
    $route(from, to) {
      this.$root.getLoginInfo();
    }
  },
  methods: {
    setPanel(panel) {
      this.panel = panel;
    }
  },
  components: {
    "login-history": httpVueLoader(
      "components/admin_components/loginHistory.vue"
    )
  },
  mounted() {
    this.$http.get("/user/info").then(
      function(response) {
        this.userInfo = response.data;
      },
      function(response) {
        toastr.error("Error in Connection - " + response.data.msg, "Error", {
          timeOut: 5000,
          closeButton: true
        });
      }
    );
  }
  // updated () {
  //   if ( !this.$root.checkLoginStatus(['admin']) ) {
  //     toastr.error('Your are not allow to open this', '...', {timeOut: 5000, closeButton: true});
  //     router.push('/');
  //   }
  // },
};
</script>

<style lang="css">
.show-more {
  float: right;
  font-weight: bold;
}
.show-more:hover {
  background-color: lightblue;
}
</style>
