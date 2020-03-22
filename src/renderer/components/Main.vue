<template>
  <div class="row  justify-content-start">
    <div class="col col-8">
      <b-form-file
        v-model="file"
        :state="Boolean(file)"
        @input="onFileChange"
        accept="image/*"
        placeholder="Choose an image or drop it here..."
        drop-placeholder="Drop image here..."
      ></b-form-file>
      <br> <br>
      <div class="form-inline">
        <button class="btn btn-outline-dark" @click="folderSelect"><font-awesome-icon icon="folder-open" ></font-awesome-icon>&nbsp; Video Folder</button>&nbsp;&nbsp;

        <div v-if="directory!=''" ><font-awesome-icon :icon="['far', 'folder']"></font-awesome-icon> {{directory}}</div>
      </div>

      <br>

      <b-list-group>
        <b-list-group-item>Cras justo odio</b-list-group-item>
        <b-list-group-item>Dapibus ac facilisis in</b-list-group-item>
        <b-list-group-item>Morbi leo risus</b-list-group-item>
        <b-list-group-item>Porta ac consectetur ac</b-list-group-item>
        <b-list-group-item>Vestibulum at eros</b-list-group-item>
      </b-list-group>
    </div>
    
    <!-- <input type="file" @change="onFileChange" /> -->
    <!-- <div>
      {{ file ? file.name : '' }}
    </div> -->
    <!-- <br> -->
    <div class="col">
      <div id="preview">
        <img v-if="url" :src="url" />

      </div>
    </div>
    
    
    
    
  </div>
</template>

<script>
const fs = require('fs');
const path = require('path');
const { remote } = require('electron')
const storage = require('electron-json-storage');

  export default {
    name: 'main',
    components: {  },
    data() {
      return {
        directory: "",
        file: null,
        url: path.join(__static, "placeholder.jpg"),
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
  max-width: 100%;
  max-height: auto;
}
</style>
