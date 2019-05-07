<template type="text/x-template">
  <div class>
    <hr>
    <!--Search Panel-->
    <div class="d-flex justify-content-center">
      <div class="card border-primary" style="width: 85%;">
        <div class="card-header">Search Log History</div>
        <div class="card-body text-primary">
          <div class="card-text">
            <div class>
              <div>
                <div class="row">
                  <div class="col-sm" style="padding-top: 2.5%">
                    <!-- <label for="user-select">User</label>
                    <select id="user-select" class="browser-default" v-model="selectedUser">
                      <option value disabled selected>Choose your user</option>
                      <option
                        v-for="user in userList"
                        v-bind:value="user.id"
                      >{{ user.userType + ': ' + user.fullName }}</option>
                    </select>-->
                    <select
                      style="width: 100%;font-size:4em;"
                      class="js-example-basic-single js-states form-control user"
                      id="mySelect2"
                      v-model="users"
                      v-on:click="selectedUser = 3;"
                    ></select>
                  </div>
                  <div class="col-sm">
                    <label for="from-date">From Date</label>
                    <input type="text" to="from-date" class="from-date">
                  </div>
                  <div class="col-sm">
                    <label for="to-date">To Date</label>
                    <input type="text" to="to-date" class="to-date">
                  </div>
                  <div class="col-sm" style="padding-top: 2%">
                    <button class="btn btn-primary" @click="search">
                      <i class="fa fa-search mr-2"></i> Search
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!--/.Search Panel-->

    <div v-show="reports.length > 0">
      <hr>
      <!--Result Panel-->
      <div class="d-flex justify-content-center">
        <div class="card border-secondary table-responsive" style="width: 85%;">
          <div class="card-header">Result</div>
          <div class="card-body text-primary">
            <div class="card-text">
              <div class>
                <table class="table table-bordered">
                  <thead>
                    <tr>
                      <th scope="col">#</th>
                      <th scope="col">Time</th>
                      <th scope="col">Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(report, index) in reports">
                      <th scope="row">{{ index + 1 }}</th>
                      <td>{{ report.time }}</td>
                      <td>{{ report.msg }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!--/.Result Panel-->
    </div>
  </div>
</template>

<script>
module.exports = {
  data: function() {
    return {
      fromDate: null,
      toDate: null,
      userList: [],
      selectedUser: null,
      reports: [],
      users: []
    };
  },

  methods: {
    fixDateZero(number) {
      return number < 10 ? "0" + String(number) : String(number);
    },
    search() {
      if (!this.selectedUser) {
        toastr.warning("Please select a user", "Error", {
          timeOut: 5000,
          closeButton: true
        });
        return;
      }
      if (!this.fromDate) {
        toastr.warning("Please choose from data", "Error", {
          timeOut: 5000,
          closeButton: true
        });
        return;
      }
      if (!this.toDate) {
        toastr.warning("Please choose from data", "Error", {
          timeOut: 5000,
          closeButton: true
        });
        return;
      }
      let data = {
        id: this.selectedUser,
        from_date: this.fromDate,
        to_date: this.toDate
      };
      this.$http.post("/user/log-report", data).then(
        function(response) {
          this.reports = response.data.args;
          for (let i in this.reports) {
            let item = this.reports[i];
            let date = persianDate.unix(item.time);
            item.time =
              date.year() +
              "-" +
              this.fixDateZero(date.month()) +
              "-" +
              this.fixDateZero(date.day()) +
              " " +
              this.fixDateZero(date.hour()) +
              ":" +
              this.fixDateZero(date.minute()) +
              ":" +
              this.fixDateZero(date.second());
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

    getUserList() {
      this.$http.get("/user/list").then(
        function(response) {
          this.userList = response.data.args;
        },
        function(response) {
          toastr.error("Error in Connection - " + response.data.msg, "Error", {
            timeOut: 5000,
            closeButton: true
          });
        }
      );
    },

    showMoreInfo(info) {
      Alert.Info(info);
    },
    cleanUnixValue(uni) {
      let u = String(uni);
      return u.substr(0, u.length - 3);
    }
  },
  mounted() {
    var vm = this;
    $(".from-date").persianDatepicker({
      initialValue: false,
      // calendarType: 'gregorian',
      toolbox: {
        calendarSwitch: {
          enabled: true
        }
      },
      navigator: {
        scroll: {
          enabled: false
        }
      },
      timePicker: {
        enabled: true,
        meridiem: {
          enabled: true
        }
      },
      onSelect: function functionName(unix) {
        vm.fromDate = vm.cleanUnixValue(unix);
      },
      onShow: function functionName() {
        console.log("onShow");
      }
    });

    $(".to-date").persianDatepicker({
      initialValue: false,
      // calendarType: "gregorian",
      toolbox: {
        calendarSwitch: {
          enabled: true
        }
      },
      navigator: {
        scroll: {
          enabled: false
        }
      },
      timePicker: {
        enabled: true,
        meridiem: {
          enabled: true
        }
      },
      onSelect: function functionName(unix) {
        vm.toDate = vm.cleanUnixValue(unix);
      }
    });
    $("select.user").change(function() {
      let id = $(this)
        .children("option:selected")
        .val();
      for (let i in vm.userList) {
        let user = vm.userList[i];
        if (id == user.id) {
          vm.selectedUser = user.id;
          break;
        }
      }
    });
    $("#mySelect2").select2({
      ajax: {
        url: "http://127.0.0.1:5000/user/list",
        data: function(params) {
          var query = {};
          // Query parameters will be ?search=[term]&type=public
          return query;
        },
        processResults: function(data) {
          let newList = [];
          data = data.args;
          vm.userList = data;
          for (let i in data) {
            let item = data[i];
            newList.push({
              id: item.id,
              text: item.name + ": " + item.userType
            });
          }
          // Tranforms the top-level key of the response object from 'items' to 'results'
          return {
            results: newList
          };
        }
      }
    });
  }
};
</script>

<style lang="css">
.input-group.md-form.form-sm.form-1 input {
  border: 1px solid #bdbdbd;
  border-top-right-radius: 0.25rem;
  border-bottom-right-radius: 0.25rem;
}
.input-group.md-form.form-sm.form-2 input {
  border: 1px solid #bdbdbd;
  border-top-left-radius: 0.25rem;
  border-bottom-left-radius: 0.25rem;
}
.input-group.md-form.form-sm.form-2 input.red-border {
  border: 1px solid #ef9a9a;
}
.input-group.md-form.form-sm.form-2 input.lime-border {
  border: 1px solid #cddc39;
}
.input-group.md-form.form-sm.form-2 input.amber-border {
  border: 1px solid #ffca28;
}
</style>
