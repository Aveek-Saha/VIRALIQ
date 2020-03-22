<template>
  <div id="app">
    <div class="container-fluid">
          <primary></primary>
    </div>
  </div>
</template>

<script>
  import Primary from '@/components/Primary'
  import 'bootstrap/dist/css/bootstrap.css'
  import 'bootstrap-vue/dist/bootstrap-vue.css'

  export default {
    name: 'viraliq',
    components: {
      Primary
    }
  }
</script>

<style>

#app {
  padding: 20px;
}
</style>
