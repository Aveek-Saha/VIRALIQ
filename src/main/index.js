import { app, BrowserWindow, ipcMain } from 'electron'
let { PythonShell } = require('python-shell')
const path = require('path');

/**
 * Set `__static` path to static files in production
 * https://simulatedgreg.gitbooks.io/electron-vue/content/en/using-static-assets.html
 */
if (process.env.NODE_ENV !== 'development') {
  global.__static = require('path').join(__dirname, '/static').replace(/\\/g, '\\\\')
}

let mainWindow
const winURL = process.env.NODE_ENV === 'development'
  ? `http://localhost:9080`
  : `file://${__dirname}/index.html`

function createWindow () {
  /**
   * Initial window options
   */
  mainWindow = new BrowserWindow({
    height: 563,
    useContentSize: true,
    width: 1000,
    webPreferences: {
      nodeIntegration: true,
      webSecurity: false
    }
  })

  mainWindow.loadURL(winURL)

  mainWindow.on('closed', () => {
    mainWindow = null
  })
}

app.on('ready', createWindow)

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow()
  }
})

const spawn = require('child_process').spawn;

var pythonExecutable = "python";
var vidSearch = path.join(__static, 'scripts', 'retrieve_videos.py');
var vidEmb = path.join(__static, 'scripts', 'create_video_embeddings.py');
var test = path.join(__static, 'scripts', 'test.py');

// Function to convert an Uint8Array to a string
var uint8arrayToString = function (data) {
  return String.fromCharCode.apply(null, data);
};

ipcMain.on('run-script', (event, arg) => {
  console.log(arg)

  const scriptExecution = spawn(pythonExecutable, [vidSearch, arg.imgPath]);

  // Handle normal output
  scriptExecution.stdout.on('data', (data) => {
    var out = uint8arrayToString(data)
    if (out.startsWith("ranks ")){
      var arr = out.slice("ranks ".length).replace(/[\n\r]/g, '').split(',')
      var res = []
      arr.forEach(ele => {
        var e = ele.split(':')
        // res[e[0]] = parseFloat(e[1])
        res.push({
          "name": e[0], 
          "rank": parseFloat(e[1]).toFixed(3),
          "file": "null"
        })
      });
      res.sort((a, b) => { return b.rank - a.rank; })
      console.log(res);

      event.sender.send('data', {
        "ranks": res
      })
      
    }
    // else if (out.startsWith("Finished"))
    //   console.log(out.split(',')[1]);
    console.log(out);

  });

  // Handle error output
  scriptExecution.stderr.on('data', (data) => {
    // As said before, convert the Uint8Array to a readable string.
    console.log(uint8arrayToString(data));
  });

  scriptExecution.on('exit', (code) => {
    console.log(event);
    
    console.log("Process quit with code : " + code);
    // event.sender.send('data', {
    //   'status': 'Finished',
    //   'code': code
    // })

  })

  });
  
  
ipcMain.on('create-emb', (event, arg) => {
  console.log(arg)

  const scriptExecution = spawn(pythonExecutable, [vidEmb, arg.videoDir]);

  // Handle normal output
  scriptExecution.stdout.on('data', (data) => {
    var out = uint8arrayToString(data)
    if (out.startsWith("Finished")){
      var done = parseFloat(out.split(',')[1].replace(/[\n\r]/g, '')) * 100;
      event.sender.send('progress', {
        'status': done.toFixed(3)
      })
    }
    // console.log(out);
  });

  // Handle error output
  scriptExecution.stderr.on('data', (data) => {
    // As said before, convert the Uint8Array to a readable string.
    // console.log(uint8arrayToString(data));
  });

  scriptExecution.on('exit', (code) => {
    console.log("Process quit with code : " + code);
    event.sender.send('emb-made', {
      'status': 'Finished',
      'code': code
    })
  });

})


/**
 * Auto Updater
 *
 * Uncomment the following code below and install `electron-updater` to
 * support auto updating. Code Signing with a valid certificate is required.
 * https://simulatedgreg.gitbooks.io/electron-vue/content/en/using-electron-builder.html#auto-updating
 */

/*
import { autoUpdater } from 'electron-updater'

autoUpdater.on('update-downloaded', () => {
  autoUpdater.quitAndInstall()
})

app.on('ready', () => {
  if (process.env.NODE_ENV === 'production') autoUpdater.checkForUpdates()
})
 */
