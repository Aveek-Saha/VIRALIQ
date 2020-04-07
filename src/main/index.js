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

var filename = path.join(__static, 'scripts', 'test.py');
// console.log(filename);

ipcMain.on('run-script', (event, arg) => {
  console.log(arg)
  let options = {
    mode: 'json',
    args: [arg.videoDir, arg.imgPath]
  };

  PythonShell.run(filename, options, function (err, results) {
    if (err) throw err;
    // results is an array consisting of messages collected during execution
    // console.log('results: %j', results);
    
    event.sender.send('data', results[0])

  });

})

var vidEmb = path.join(__static, 'scripts', 'create_video_embeddings.py');


ipcMain.on('create-emb', (event, arg) => {
  console.log(arg)
  let options = {
    mode: 'text',
    args: [arg.videoDir, arg.imgPath]
  };

  // PythonShell.run(vidEmb, options, function (err, results) {
  //   if (err) throw err;
  //   // results is an array consisting of messages collected during execution
  //   // console.log('results: %j', results);

  //   event.sender.send('emb-made', results[0])

  // });

  var myPythonScript = path.join(__static, 'scripts', 'create_video_embeddings.py');
  // Provide the path of the python executable, if python is available as environment variable then you can use only "python"
  var pythonExecutable = "python";

  // Function to convert an Uint8Array to a string
  var uint8arrayToString = function (data) {
    return String.fromCharCode.apply(null, data);
  };

  const spawn = require('child_process').spawn;
  const scriptExecution = spawn(pythonExecutable, [myPythonScript, arg.videoDir, arg.imgPath]);

  // Handle normal output
  scriptExecution.stdout.on('data', (data) => {
    var out = uint8arrayToString(data)
    // if (out.startsWith("Total"))
    //   console.log(out.split(',')[1]);
    // else if (out.startsWith("Finished"))
    //   console.log(out.split(',')[1]);
    console.log(out);
    
  });

  // Handle error output
  scriptExecution.stderr.on('data', (data) => {
    // As said before, convert the Uint8Array to a readable string.
    // console.log(uint8arrayToString(data));
  });

  scriptExecution.on('exit', (code) => {
    console.log("Process quit with code : " + code);
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
