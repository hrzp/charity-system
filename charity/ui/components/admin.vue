<template type="text/x-template">
  <div class>
    <hr>
  </div>
</template>

<script>
module.exports = {
  data: function() {
    return {};
  },
  mounted() {
    this.$root.isSignin();
  }
};
</script>

<style lang="css" scoped>
</style>
