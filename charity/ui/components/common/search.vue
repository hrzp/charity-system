<template type="text/x-template">
  <div>
    <label for="searchInp">Search</label>
    <input
      class="col-3 searchInput"
      type="text"
      v-on:keyup="queryMaker"
      v-model="textWord"
      id="searchInp"
    >
    <img v-show="send" src="assets/image/loading.gif" class="loader">
  </div>
</template>

<script>
module.exports = {
  components: {},
  data: function() {
    return {
      textWord: "",
      send: null
    };
  },
  props: {
    callback: Function,
    fileds: Array,
    currentPage: Number
  },
  computed: {},
  methods: {
    queryMaker() {
      let items = [];
      for (let i in this.fileds) {
        let filed = this.fileds[i];
        if (this.textWord.length == 0) continue;
        items.push({ name: filed, op: "like", val: `%${this.textWord}%` });
      }
      let q = {
        filters: [{ or: items }]
      };
      this.serach(q);
    },
    serach(query) {
      if (this.send) clearTimeout(this.send);
      let app = this;
      this.send = setTimeout(function() {
        app.callback(app.currentPage, query);
        app.send = null;
      }, 1000);
    }
  },
  mounted() {}
};
</script>

<style lang="css" scoped>
.searchInput {
  font-size: 15px;
  height: 20px;
  color: #000;
}
.loader {
  height: 45px;
}
</style>