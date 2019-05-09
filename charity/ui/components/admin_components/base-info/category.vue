<template type="text/x-template">
  <div class>
    <hr>
    <h2>Base Categories</h2>

    <div class="d-flex justify-content-center">
      <div class="card border-secondary table-responsive" style="width: 85%;">
        <div class="card-header">Result</div>
        <div class="card-body text-primary">
          <div class="card-text">
            <!-- Editable table -->
            <div class="card">
              <div id="table" class="table-editable">
                <span class="table-add float-right mb-3 mr-2"></span>
                <input type="text">
                <table class="table table-bordered table-responsive-md table-striped text-center">
                  <tr>
                    <th class="text-center">ID</th>
                    <th class="text-center">Item</th>
                    <th class="text-center">Remove</th>
                  </tr>
                  <tr v-for="(item, index) in rows">
                    <td class="pt-3-half" contenteditable="false">{{index}}</td>
                    <td
                      class="pt-3-half"
                      :id="assginId()"
                      @focus="editElement($event)"
                      @blur="leave($event)"
                      contenteditable="true"
                    >{{item.item}}</td>
                    <td>
                      <span class="table-remove">
                        <button
                          type="button"
                          v-on:click="remove(item.id)"
                          class="btn btn-danger btn-rounded btn-sm my-0"
                        >Remove</button>
                      </span>
                    </td>
                  </tr>
                </table>
              </div>
            </div>
            <!-- Editable table -->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
module.exports = {
  components: {
    "table-vue": httpVueLoader("components/common/table.vue")
  },
  data: function() {
    return {
      rows: null,
      myvar: null
    };
  },
  methods: {
    leave(index) {},
    editElement(id) {
      console.log(id);
    },
    assginId() {
      let id = Math.random();
      return id.toString(36).substring(2);
    },
    remove(index) {
      console.log(index);
    },
    checkId(key) {
      return key == "id" ? false : true;
    },
    getData() {
      this.$http.get("/api/base-category").then(
        function(response) {
          this.rows = response.body.objects;
        },
        function(response) {
          toastr.error("Error in Connection - " + response.data.msg, "Error", {
            timeOut: 5000,
            closeButton: true
          });
        }
      );
    },
    init() {
      this.getData();
    }
  },
  mounted() {
    this.init();
  }
};
</script>

<style lang="css">
.pt-3-half {
  padding-top: 1.4rem;
}
</style>