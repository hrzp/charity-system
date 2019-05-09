<template type="text/x-template">
  <div class>
    <div class="card-body">
      <div id="table" class="table-editable">
        <span class="table-add float-right mb-3 mr-2"></span>
        <input type="text">
        <table class="table table-bordered table-responsive-md table-striped text-center">
          <tr>
            <th class="text-center">ID</th>
            <th v-for="column in data.columns" class="text-center">{{column}}</th>
            <th class="text-center">Remove</th>
          </tr>
          <tr v-for="(item, index) in rows">
            <td v-for="(td, key) in item" class="pt-3-half" :contenteditable="checkId(key)">
              <div v-if="checkId(key)">{{td}}</div>
              <div v-else>{{index}}</div>
            </td>
            <td>
              <span class="table-remove">
                <button
                  type="button"
                  v-on:click="remove(index)"
                  class="btn btn-danger btn-rounded btn-sm my-0"
                >Remove</button>
              </span>
            </td>
          </tr>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
module.exports = {
  props: {
    data: {}
  },
  computed: {},
  data: function() {
    return {
      rows: null,
      f: false
    };
  },
  methods: {
    remove(index) {
      console.log(index);
    },
    checkId(key) {
      return key == "id" ? false : true;
    },
    init() {
      if (this.data.url) {
        this.$http.get("/api/" + this.data.url).then(
          function(response) {
            this.rows = response.body.objects;
          },
          function(response) {
            toastr.error(
              "Error in Connection - " + response.data.msg,
              "Error",
              {
                timeOut: 5000,
                closeButton: true
              }
            );
          }
        );
      }
    }
  },
  mounted() {
    this.init();
  },
  created() {}
};
</script>

<style lang="css">
</style>
