<template type="text/x-template">
  <div class>
    <hr>

    <!--Panel-->
    <div class="d-flex justify-content-center">
      <div class="card border-primary mb-3" style="max-width: 100%;width: 70%;">
        <div class="card-body text-secondary">
          <h3>User Roles List</h3>
        </div>
        <div class="card-text">
          <div class v-if="this.users.length > 0">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th scope="col">#</th>
                  <th scope="col">User</th>
                  <th scope="col">Full Name</th>
                  <th scope="col" v-for="role in roles">{{ role.label }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(user, index) in userRole">
                  <th scope="row">{{ index + 1 }}</th>
                  <td>{{ user.username }}</td>
                  <td>{{ user.name }}</td>
                  <td v-for="role in user.roles">
                    <div class="form-check">
                      <input
                        type="checkbox"
                        class="form-check-input"
                        v-bind:id="role.name+index"
                        :checked="role.value ? true : false"
                        v-on:change="changeRole(role.id, user.id)"
                      >
                      <label class="form-check-label" v-bind:for="role.name+index"></label>
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
  </div>
</template>

<script>
module.exports = {
  data: function() {
    return {
      roles: [],
      users: []
    };
  },
  methods: {
    init() {
      this.getUsersInfo();
      this.getRolesInfo();
    },

    getUsersInfo() {
      let url = "/api/user";
      if (this.$route.params.id) url = url + "/" + this.$route.params.id;
      this.$http.get(url).then(
        function(response) {
          if (response.data.num_results <= 0) {
            toastr.warn("There is no user", "Error", {
              timeOut: 5000,
              closeButton: true
            });
            return;
          }
          if (response.data.objects) {
            this.users = response.data.objects;
          } else {
            this.users = [response.data];
          }
        },
        function(response) {
          toastr.error("Error in Connection - " + response.data.msg, "Error", {
            timeOut: 5000,
            closeButton: true
          });
        }
      );
    },

    getRolesInfo() {
      this.$http.get("/api/role").then(
        function(response) {
          if (response.data.num_results <= 0) {
            toastr.warn("There is no roles", "Error", {
              timeOut: 5000,
              closeButton: true
            });
            return;
          }
          let data = response.data.objects;
          this.roles = [];
          for (let i in data) {
            if (!data[i].is_systemic) {
              this.roles.push(data[i]);
              // TODO: We have prevent this detail.it Should check from server
            }
          }
          // this.userRole = '';
        },
        function(response) {
          toastr.error("Error in Connection - " + response.data.msg, "Error", {
            timeOut: 5000,
            closeButton: true
          });
        }
      );
    },

    changeRole(id, userId) {
      let data = {
        id: id,
        user_id: userId
      };
      this.$http.post("/user/change-role", data).then(
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
    userRole: {
      // getter
      get: function() {
        // TODO: Be sure that all roles get in correct index
        let newObj = [];
        for (let i in this.users) {
          let tmp = {};
          let k = this.users[i].id;
          tmp["name"] = this.users[i].name;
          tmp["username"] = this.users[i].username;
          tmp["id"] = this.users[i].id;
          tmp["roles"] = [];
          for (let j in this.roles) {
            let key = this.roles[j].name;
            let id = this.roles[j].id;
            let tmpKey = {};
            tmpKey["name"] = key;
            tmpKey["id"] = id;
            for (role in this.users[i].roles) {
              if (this.users[i].roles[role].name == key) {
                tmpKey["value"] = true;
                break;
              }
            }
            if (!tmpKey.value) {
              tmpKey["value"] = false;
            }
            tmp["roles"].push(tmpKey);
          }
          newObj.push(tmp);
        }
        return newObj;
      },
      // setter
      set: function(arg) {
        return { user: this.users, role: this.roles };
      }
    }
  },
  watch: {
    $route(to, from) {
      this.init();
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
