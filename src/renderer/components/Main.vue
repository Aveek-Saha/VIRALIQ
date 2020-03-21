<template>
  <div id="wrapper">
    <b-form-file
      v-model="file"
      :state="Boolean(file)"
      accept="image/*"
      placeholder="Choose a file or drop it here..."
      drop-placeholder="Drop file here..."
    ></b-form-file>
    <!-- <input type="file" @change="onFileChange" /> -->
    <div>
      {{ file ? file.name : '' }}
    </div>
    <div id="preview">
      <img v-if="url" :src="url" />
    </div>
  </div>
</template>

<script>

  export default {
    name: 'main',
    components: {  },
    data() {
      return {
        url: null,
        file: null,
        filePath: null
      }
    },
    methods: {
      // onFileChange(e) {
      //   const file = e.target.files[0];
      //   this.filePath = file.path
      //   console.log(this.filePath);
        
      //   this.url = URL.createObjectURL(file);
      // }
    }
  }
</script>

<style>
/* body {
  background-color: #e2e2e2;
} */

#preview {
  display: flex;
  justify-content: center;
  align-items: center;
}

#preview img {
  max-width: 20vw;
  max-height: 20vh;
}
</style>
