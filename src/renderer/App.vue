<template>
  <div id="app">
    <div class="container-fluid">
          <Main></Main>
    </div>
  </div>
</template>

<script>
  import Main from '@/components/Main'
  import 'bootstrap/dist/css/bootstrap.css'
  import 'bootstrap-vue/dist/bootstrap-vue.css'

  export default {
    name: 'viraliq',
    components: {
      Main
    }
  }
</script>

<style>

#app {
  padding: 20px;
}
</style>
