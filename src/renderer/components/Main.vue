<template>
  <div id="wrapper">
    <b-form-file
      v-model="file"
      :state="Boolean(file)"
      @input="onFileChange"
      accept="image/*"
      placeholder="Choose a file or drop it here..."
      drop-placeholder="Drop file here..."
    ></b-form-file>
    <!-- <input type="file" @change="onFileChange" /> -->
    <div>
      {{ file ? file.name : '' }}
    </div>
    <br>
    
    <div id="preview">
      <img v-if="url" :src="url" />
    </div>
    
     <div class="form-inline">
      <div v-if="directory!=''" ><font-awesome-icon :icon="['far', 'folder']"></font-awesome-icon> {{directory}}</div>&nbsp;&nbsp;

      <button class="btn btn-outline-dark" @click="folderSelect"><font-awesome-icon icon="folder-open" ></font-awesome-icon>&nbsp; Video Folder</button>

     </div>
  </div>
</template>

<script>
const fs = require('fs');
const { remote } = require('electron')
const storage = require('electron-json-storage');

  export default {
    name: 'main',
    components: {  },
    data() {
      return {
        directory: "",
        file: null,
        url: null,
        filePath: null
      }
    },
    created() {
      this.checkDir()
    },
    methods: {
      folderSelect () {
        remote.dialog.showOpenDialog({
          properties: ['openDirectory'],
          // defaultPath: current
        }, names => {
          console.log('selected directory:' + names[0]);
          this.directory = names[0]
          storage.set('directory', { dir: this.directory }, function(error) {
            if (error) throw error;
          });
        });
      },
      onFileChange(file) {
        this.filePath = file.path
        console.log(this.filePath);
        
        this.url = URL.createObjectURL(file);
      },
      checkDir() {
        const that = this
        storage.has('directory', function(error, hasKey) {
          if (error) throw error;
          if (hasKey) {
            storage.get('directory', function(error, data) {
              if (error) throw error;
              console.log(data.dir);
              that.directory = data.dir
            });
          }
        });
      }
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
