<template type="text/x-template">
  <div>
    <nav aria-label="Page navigation" class="custom-pagination">
      <ul class="pagination pagination-circle pg-blue">
        <li class="page-item" :class="{'disabled': cp==1}">
          <a v-on:click="changePage(1)" class="page-link">First</a>
        </li>
        <li class="page-item" :class="{'disabled': cp==1}">
          <a v-on:click="changePage(cp-1)" class="page-link" aria-label="Previous">
            <span aria-hidden="true">&laquo;</span>
            <span class="sr-only">Previous</span>
          </a>
        </li>
        <li
          v-for="(page, index) in pages"
          v-bind:key="index"
          class="page-item"
          :class="{'active': page==cp}"
        >
          <a class="page-link" v-on:click="changePage(page)">{{page}}</a>
        </li>
        <li class="page-item" :class="{'disabled': cp==numbers}">
          <a v-on:click="changePage(cp+1)" class="page-link" aria-label="Next">
            <span aria-hidden="true">&raquo;</span>
            <span class="sr-only">Next</span>
          </a>
        </li>
        <li class="page-item" :class="{'disabled': cp==numbers}">
          <a v-on:click="changePage(numbers)" class="page-link">Last</a>
        </li>
        <li>
          <input
            type="text"
            class="page-entry"
            placeholder="Page number"
            v-if="numbers > 10"
            v-model="entery"
            @keyup.enter="changePage(entery)"
          >
        </li>
      </ul>
    </nav>
  </div>
</template>

<script>
module.exports = {
  components: {
    // "table-vue": httpVueLoader("components/common/table.vue")
  },
  data: function() {
    return {
      // cp: 1,
      entery: null
      // pages: []
    };
  },
  props: {
    numbers: Number, // Total Page Number
    callback: Function,
    cp: Number // Current Page
  },
  computed: {
    pages: function() {
      return this.paginationRange(this.cp, this.numbers);
    }
  },
  methods: {
    paginationRange(c, m) {
      var current = c,
        last = m,
        delta = 2,
        left = current - delta,
        right = current + delta + 1,
        range = [],
        rangeWithDots = [],
        l;
      for (let i = 1; i <= last; i++) {
        if (i == 1 || i == last || (i >= left && i < right)) {
          range.push(i);
        }
      }
      for (let i of range) {
        if (l) {
          if (i - l === 2) {
            rangeWithDots.push(l + 1);
          } else if (i - l !== 1) {
            rangeWithDots.push("...");
          }
        }
        rangeWithDots.push(i);
        l = i;
      }
      //   this.pages = rangeWithDots;
      return rangeWithDots;
    },
    changePage(page) {
      if (page == "...") return;
      page = parseInt(page);
      page = page < 1 ? 1 : page;
      page = page > this.numbers ? this.numbers : page;
      this.callback(page);
      this.cp = page;
    }
  },
  mounted() {}
};
</script>

<style lang="css" scoped>
.page-entry {
  padding: 10px;
  font-size: 18px;
  width: 130px;
  height: 15px;
  border: none;
  border-bottom: 1px black solid !important;
}
.custom-pagination {
  margin-top: 10px;
}
</style>