<template type="text/x-template">
  <div class="component-body animated fadeInUp">
    <hr>

    <!--Search Panel-->
    <div class="d-flex justify-content-center">
      <div class="card border-primary" style="width: 85%;">
        <div class="card-header custome-head">Login History</div>
        <div class="card-body text-primary">
          <div class="card-text">
            <div class>
              <form v-on:keyup.enter="search">
                <div class="row">
                  <div class="col-sm" style="padding-top: 2.5%">
                    <!-- <label for="user-select">User</label>
                    <select id="user-select" class="browser-default" v-model="selectedUser">
                      <option value disabled selected>Choose your user</option>
                      <option
                        v-for="user in userList"
                        v-bind:value="user.id"
                      >{{ user.userType + ': ' + user.name }}</option>
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
              </form>
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
                      <th scope="col">Ip</th>
                      <th scope="col">Browser</th>
                      <th scope="col">More Info</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(report, index) in reports">
                      <th scope="row">{{ index + 1 }}</th>
                      <td>{{ report.time }}</td>
                      <td>{{ report.ip }}</td>
                      <td>{{ report.browser }}</td>
                      <td>
                        <button
                          type="button"
                          class="btn btn-info"
                          @click="showMoreInfo(report.fullBrowserInfo)"
                        >Show More Info</button>
                      </td>
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
      users: [],
      selectedUser: null,
      reports: []
    };
  },
  methods: {
    init() {
      this.selectedUser = 0;
      var vm = this;
      $(".from-date").persianDatepicker({
        initialValue: false,
        // calendarType: "gregorian",r
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
        onShow: function functionName() {}
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
          headers: {
            Authorization: getHeaders(true)
          },
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
      let app = this;
      API.post("/user/login-report", data).then(function(response) {
        app.reports = response.data.args;
        app.convertDate(app.reports);
      });
    },
    showMoreInfo(info) {
      Alert.Info(info);
    },
    fixDateZero(number) {
      return number < 10 ? "0" + String(number) : String(number);
    },
    convertDate(reports) {
      for (let i in reports) {
        let item = reports[i];
        let d = new Date(item.time);
        var date = new persianDate(d);
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
    cleanUnixValue(uni) {
      let u = String(uni);
      return u.substr(0, u.length - 3);
    }
  },
  mounted() {
    this.$root.isSignin();
    this.init();
  }
};
</script>

<style lang="css" scoped>
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
.note {
  padding: 10px;
  border-left: 6px solid;
  -webkit-border-radius: 5px;
  border-radius: 5px;
}
.note.note-primary {
  background-color: #dfeefd;
  border-color: #176ac4;
}
p {
  margin-top: 0;
  margin-bottom: 0;
  text-align: center;
}
</style>
