<template type="text/x-template">
  <div class>
    <hr>

    <!--Panel-->
    <div class="d-flex justify-content-center">
      <div class="card border-success mb-3" style="max-width: 100%;width: 70%;">
        <div class="card-body text-success">
          <h3>Users List</h3>
          <div class>
            <button
              type="button"
              class="btn btn-primary"
              data-toggle="modal"
              data-target="#new-user"
            >Create New User</button>
          </div>
        </div>
        <div class="card-text">
          <div class v-if="this.users.length > 0">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th scope="col">#</th>
                  <th scope="col">Username</th>
                  <th scope="col">Full Name</th>
                  <th scope="col">User Type</th>
                  <th scope="col">Roles</th>
                  <th scope="col">Active</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(user, index) in users">
                  <th scope="row">{{ index + 1 }}</th>
                  <td>{{ user.username }}</td>
                  <td>{{ user.name }}</td>
                  <td>{{ user.user_type }}</td>
                  <td>
                    <button
                      type="button"
                      class="btn btn-info"
                      @click="gotoRoles(user.id)"
                    >Click To Change Roles</button>
                  </td>
                  <td>
                    <div class="form-check">
                      <input
                        type="checkbox"
                        class="form-check-input"
                        v-bind:id="index"
                        :checked="user.active ? true : false"
                        v-on:change="changeActivation(user.id)"
                      >
                      <label class="form-check-label" v-bind:for="index"></label>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    <!--/.Panel-->

    <!-- New User Modals -->
    <div
      class="modal fade"
      id="new-user"
      tabindex="-1"
      role="dialog"
      aria-labelledby="myModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-lg" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="modal-title w-100" id="myModalLabel">New User</h4>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <h2>User Type:</h2>
            <div class="row">
              <div class="col-12">
                <div class="form-check form-check-inline">
                  <input
                    type="radio"
                    class="form-check-input"
                    value="admin"
                    id="admin"
                    v-model="userType"
                    name="userType"
                  >
                  <label class="form-check-label" for="admin">Admin</label>
                </div>
                <div class="form-check form-check-inline">
                  <input
                    type="radio"
                    class="form-check-input"
                    value="employee"
                    id="employe"
                    v-model="userType"
                    name="userType"
                  >
                  <label class="form-check-label" for="employe">Employee</label>
                </div>
              </div>
              <div class="col-12">
                <hr>
              </div>
              <div class="col-12">
                <form class="row">
                  <div class="col">
                    <div class="md-form">
                      <i class="fa fa-user-circle-o prefix"></i>
                      <input type="text" id="inputIconEx1" class="form-control" v-model="username">
                      <label for="inputIconEx1">Username</label>
                    </div>
                  </div>
                  <div class="col">
                    <div class="md-form">
                      <i class="fa fa-lock prefix"></i>
                      <input
                        disabled
                        type="password"
                        id="pass1"
                        class="form-control"
                        v-bind:class="{validate: passValidate}"
                        v-model="password"
                      >
                      <label for="pass1">Type a password</label>
                    </div>
                  </div>
                  <div class="col">
                    <div class="md-form">
                      <i class="fa fa-lock prefix"></i>
                      <input
                        disabled
                        type="password"
                        id="pass2"
                        class="form-control"
                        v-bind:class="{validate: passValidate}"
                        v-model="confirmPassword"
                      >
                      <label for="pass2">Type password again</label>
                    </div>
                  </div>
                  <div class="col-12">
                    <hr>
                  </div>
                  <div class="col">
                    <div class="md-form">
                      <i class="fa fa-address-card prefix"></i>
                      <input type="text" id="full-name" class="form-control" v-model="name">
                      <label for="full-name">Full Name</label>
                    </div>
                  </div>
                  <div class="col">
                    <div class="md-form">
                      <i class="fa fa-envelope prefix"></i>
                      <input type="text" id="mail" class="form-control" v-model="mail">
                      <label for="mail">Mail Address</label>
                    </div>
                  </div>
                </form>
              </div>
              <div class="col-12">
                <hr>
              </div>
              <div class="col">
                <div class="form-check">
                  <input
                    type="checkbox"
                    class="form-check-input"
                    id="active-user"
                    v-model="activeUser"
                  >
                  <label class="form-check-label" for="active-user">Active</label>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary btn-sm" data-dismiss="modal">Close</button>
            <button
              type="button"
              class="btn btn-primary btn-sm"
              data-dismiss="modal"
              @click="newUser"
            >Create</button>
          </div>
        </div>
      </div>
    </div>
    <!-- New User Modals -->
  </div>
</template>

<script>
module.exports = {
  data: function() {
    return {
      roles: [],
      users: [],
      activeUser: false,
      userType: "employee",
      username: null,
      name: null,
      password: null,
      mail: null,
      confirmPassword: null
    };
  },
  methods: {
    init() {
      this.getUsersInfo();
    },

    getUsersInfo() {
      this.$http.get("/api/user").then(
        function(response) {
          if (response.data.num_results <= 0) {
            toastr.warn("There is no user", "Error", {
              timeOut: 5000,
              closeButton: true
            });
            return;
          }
          this.users = response.data.objects;
        },
        function(response) {
          toastr.error("Error in Connection - " + response.data.msg, "Error", {
            timeOut: 5000,
            closeButton: true
          });
        }
      );
    },

    gotoRoles(userId) {
      router.push("/admin/dashboard/role-managment/" + userId);
    },

    validateEmail(email) {
      var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(String(email).toLowerCase());
    },

    newUser() {
      if (!this.username) {
        toastr.error("Please Enter Username", "Error", {
          timeOut: 5000,
          closeButton: true
        });
        return;
      }
      // if ( !this.password ) {
      //   toastr.error('Please Enter Password', 'Error', {timeOut: 5000, closeButton: true})
      //   return;
      // }
      if (!this.name) {
        toastr.error("Please Enter Full Name", "Error", {
          timeOut: 5000,
          closeButton: true
        });
        return;
      }
      if (!this.mail) {
        toastr.error("Please Enter Valid Mail", "Error", {
          timeOut: 5000,
          closeButton: true
        });
        return;
      } else if (!this.validateEmail(this.mail)) {
        toastr.error("Mail Not Valid", "Error", {
          timeOut: 5000,
          closeButton: true
        });
        return;
      }
      Alert.Loader();
      // if ( this.password != this.confirmPassword ) {
      //   toastr.error('Passwords Are Diffrent', 'Error', {timeOut: 5000, closeButton: true})
      //   return;
      // }
      let data = {
        username: this.username,
        password: this.password,
        name: this.name,
        user_type: this.userType,
        mail: this.mail,
        active: this.activeUser
      };
      this.$http.post("/user/new", data).then(
        function(response) {
          toastr.success(response.data.msg, "", {
            timeOut: 5000,
            closeButton: true
          });

          this.init();
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

    changeActivation(userId) {
      let data = {
        user_id: userId
      };
      this.$http.post("/user/changeactivation", data).then(
        function(response) {
          toastr.success(response.data.msg, "", {
            timeOut: 5000,
            closeButton: true
          });

          this.init();
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
  computed: {
    passValidate() {
      if (this.password == this.confirmPassword) {
        return true;
      }
      return false;
    }
  },
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
