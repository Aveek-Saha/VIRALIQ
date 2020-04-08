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
        <button class="btn btn-outline-dark" @click="folderSelect"><font-awesome-icon icon="video" ></font-awesome-icon>&nbsp; Video Folder</button>&nbsp;&nbsp;

        <div v-if="directory!=''" ><font-awesome-icon :icon="['far', 'folder']"></font-awesome-icon> {{directory}}</div>
      </div>

      <br>
      <div class="card" >
        <div class="card-header">
          <h5> 
            Best matches &nbsp; 
            <!-- <span class="align-middle"><font-awesome-icon icon="sort-down" size="lg"></font-awesome-icon></span> -->
          </h5>
        </div>
          <div class="list-group list-group-flush">
            <div v-if="waiting" class="list-group-item list-group-item-action d-flex justify-content-center">
              <div class="spinner-border" role="status">
                <span class="sr-only">Loading...</span>
              </div>
            </div>
            <button type="button" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center"
            v-for="(item , index) in list" :key="index"
            @click="showVideo(item.file)">
              {{ item.name }} 
              <span class="badge badge-primary badge-pill"> {{ item.rank }} </span>
            </button>
          </div>
      </div>
    </div>
    
    <!-- <input type="file" @change="onFileChange" /> -->
    <!-- <div>
      {{ file ? file.name : '' }}
    </div> -->
    <!-- <br> -->
    <div class="col text-center">
      <div id="preview">
        <img v-if="url" :src="url" />
      </div>

      <br>

      <button class="btn btn-outline-success" 
      :disabled="filePath == null || directory == ''"
      @click="runScript"
      >Start Search <font-awesome-icon icon="search" ></font-awesome-icon></button>
    </div>
    
    
    
    
  </div>
</template>

<script>
const fs = require('fs');
const path = require('path');
const { remote, ipcRenderer } = require('electron')
const storage = require('electron-json-storage');
const shell = remote.shell;

  export default {
    name: 'primary',
    components: {  },
    data() {
      return {
        directory: "",
        file: null,
        url: path.join(__static, "placeholder.jpg"),
        filePath: null,
        list: [],
        waiting: false
      }
    },
    created() {
      this.checkDir(),
      this.setListener()
      // this.dummyData()
    },
    methods: {
      setListener () {
        var that = this
        ipcRenderer.on('data', (event, arg) => {
          console.log(arg)
          that.waiting = false
          // this.arg = arg
        })

        ipcRenderer.on('emb-made', (event, arg) => {
          console.log(arg)
          // that.waiting = false
          // this.arg = arg
        })
      },
      runScript () {
        this.waiting = true
        ipcRenderer.send('run-script', {
          videoDir: this.directory,
          imgPath: this.filePath
        })
      },
      showVideo (file) {
        shell.showItemInFolder(path.join(this.directory, file))
        // console.log(filepath)
      },
      dummyData () {
        for(var i=0; i<5; i++){
          // var fp = path.join(this.directory, "text.txt")
          this.list.push({
            name: "Video" + i,
            rank: Math.floor((Math.random() * 10) + 1),
            file: "text.txt"
          })
        }

        this.list.sort((a, b) => { return b.rank - a.rank; })
        // this
        
      },
      folderSelect () {
        remote.dialog.showOpenDialog({
          properties: ['openDirectory'],
          // defaultPath: current
        }, names => {
          console.log('selected directory:' + names[0]);
          this.directory = names[0]
          ipcRenderer.send('create-emb', {
            videoDir: this.directory,
            imgPath: this.url
          })
          // this.waiting = true
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
font-awesome-icon {
  vertical-align: middle;
}
</style>
