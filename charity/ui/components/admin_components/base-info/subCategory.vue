<template type="text/x-template">
  <div class>
    <hr>
    <div class="d-flex justify-content-center cp-head">
      <p class="center" style="color: black">Sub Categories: {{catName}}</p>
      <button class="btn btn-mdb-color back-btn btn-sm btn-rounded" v-on:click="back">
        <i class="fa fa-arrow-circle-left"></i> Back
      </button>
    </div>
    <div class="d-flex justify-content-center input-box">
      <div class="card form-box">
        <form class="form-group">
          <input
            v-model="item"
            placeholder="Item name"
            type="text"
            class="form-control col-3"
            @keyup.enter="save"
          >
          <button
            type="button"
            @keyup.enter="save"
            v-on:click="save"
            class="btn btn-primary btn-rounded save-btn"
          >Save</button>
        </form>
      </div>
    </div>

    <div class="d-flex justify-content-center">
      <div class="card border-secondary table-responsive" style="width: 85%;">
        <div class="card-header">Result</div>
        <div class="card-body text-primary">
          <div class="card-text">
            <div class="card">
              <div>
                <search :callback="getData" :fileds="['item']"></search>
              </div>
              <div id="table" class="table-editable">
                <table class="table table-bordered table-responsive-md table-striped text-center">
                  <tr>
                    <th class="text-center">ID</th>
                    <th class="text-center">Item</th>
                    <th class="text-center">Remove</th>
                  </tr>
                  <tr v-for="(item, index) in rows" v-bind:key="index">
                    <td class="pt-3-half" contenteditable="false">{{index+1}}</td>
                    <td
                      class="pt-3-half editable"
                      :id="'ele-'+(index+1)"
                      @focus="editElement($event)"
                      @blur="leave($event, item.id)"
                      @keyup.enter="leave($event, item.id, true)"
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
            <pagination :callback="getData" :numbers="totalPages" :cp="currentPage"></pagination>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
module.exports = {
  components: {
    pagination: httpVueLoader("components/common/customPaginate.vue"),
    search: httpVueLoader("components/common/search.vue")
  },

  data: function() {
    return {
      catName: "",
      id: null,
      rows: null,
      item: null,
      tmpValue: null,
      currentPage: 1,
      totalPages: 1,
      query: null
    };
  },
  methods: {
    nextEle(event) {
      let currentID = event.target.id;
      let nextID = parseInt(currentID.split("-")[1]) + 1;
      $("#ele-" + nextID).focus();
    },
    back() {
      router.push("/admin/base-category");
    },
    leave(event, id, byEnter = false) {
      event.target.textContent = event.target.textContent.trim();
      let newValue = event.target.textContent.trim();
      if (byEnter == true) {
        this.nextEle(event);
        return;
      }
      if (this.tmpValue.trim() == newValue) {
        return;
      }
      data = {
        item: event.target.textContent
      };
      let app = this;
      API.put("/api/base-item/" + id, data).then(function(response) {
        toastr.info("Edit successfully", {
          timeOut: 6000,
          closeButton: true
        });
        app.getData(app.currentPage);
        app.item = null;
      });
    },
    editElement(event) {
      this.tmpValue = event.target.textContent;
    },
    assginID(id) {
      return "ele-" + id;
    },
    remove(id) {
      let app = this;
      API.delete("/api/base-item/" + id).then(function(response) {
        toastr.success("Deleted successfully", {
          timeOut: 5000,
          closeButton: true
        });
        app.getData(app.currentPage);
        app.item = null;
      });
    },
    checkId(key) {
      return key == "id" ? false : true;
    },
    save() {
      if (!this.item) {
        toastr.info("Enter an item name", {
          timeOut: 8000,
          closeButton: true
        });
        return;
      }
      let app = this;
      API.post("/api/base-item", {
        item: app.item,
        category: { id: app.id }
      }).then(function(response) {
        toastr.success("Saved successfully", {
          timeOut: 5000,
          closeButton: true
        });
        app.currentPage = 1;
        app.getData(1);
        app.item = null;
      });
    },
    preventEnter() {
      // setTimeout(function() {
      //   $(".editable")
      //     .on("paste", function(e) {
      //       var $self = $(this);
      //       setTimeout(function() {
      //         $self.html($self.text());
      //       }, 0);
      //     })
      //     .on("keypress", function(e) {
      //       return e.which != 13;
      //     });
      // }, 2);
    },
    initGetData(page, query) {
      if (!page) {
        page = 1; // If called form search component
      } else {
        if (this.query) {
          query = this.query;
        }
      }
      if (!query) {
        query = { filters: [] };
      } else {
        this.query = query;
      }
      this.currentPage = page;
      return { page: page, query: query };
    },
    getData(page, query) {
      let res = this.initGetData(page, query);
      page = res.page;
      query = res.query;
      query.filters.push({ name: "category_id", op: "eq", val: this.id });
      let app = this;
      QUERY = Object.assign(
        { order_by: [{ field: "id", direction: "desc" }] },
        query
      );
      API.get("/api/base-item?page=" + page, {
        params: { q: QUERY }
      }).then(function(response) {
        app.totalPages = response.data.total_pages;
        app.rows = response.data.objects;
        app.preventEnter();
      });
    },
    getCatInfo() {
      let app = this;
      API.get("/api/base-category/" + this.id).then(function(response) {
        console.log(response);
        app.catName = response.data.item;
      });
    },
    init() {
      this.getData(1);
      this.getCatInfo();
    }
  },
  mounted() {
    if (!this.$route.params.id) {
      toastr.error("Worong url", "Error", { timeOut: 8000 });
      return;
    }
    this.id = this.$route.params.id;
    this.$root.isSignin();
    this.init();
  }
};
</script>

<style lang="css" scoped>
.input-text {
  background-color: white !important;
  border-bottom: 1px black solid !important;
  border: 1px rgb(51, 72, 105) solid !important;
}
.input-box {
  border: none;
  margin-bottom: 20px;
  height: 100px;
}
.form-box {
  padding: 1%;
  overflow: hidden;
  width: 85%;
}
.save-btn {
  font-size: 10px;
}
input {
  background-color: rgb(255, 255, 255) !important;
  text-align: left !important;
  color: black !important;
  border-bottom-color: rgb(153, 188, 253) !important;
}
th {
  white-space: nowrap;
}
td {
  color: black !important;
  white-space: nowrap;
}
.editable:hover {
  cursor: text;
  background-color: ghostwhite;
}
.pt-3-half {
  padding-top: 1.4rem;
}
.page-entry {
  padding: 10px;
  font-size: 18px;
  width: 130px;
  height: 15px;
  border: none;
}
.back-btn {
  float: right;
  font-size: 12px !important;
  height: 35px;
  margin-top: 13px;
}
.back-btn i {
  float: left !important;
  font-size: 18px !important;
  margin-right: 10px;
}
</style>