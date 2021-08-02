<script>
    const { ipcRenderer } = require("electron");
    
    function folderselect() {
        console.log(ipcRenderer.sendSync('folder-select', 'ping'))
    }
</script>

<div class="container p-3">
    <div class="row">
        <div class="col-8">
            <div class="mb-3">
                <button
                    type="button"
                    class="btn btn-outline-primary m-3 align-center"
                    on:click={folderselect}>Select video folder</button
                >
            </div>
            <div class="card">
                <div class="card-header">
                    <h5 class="card-title">Matches</h5>
                </div>
                <ul class="list-group list-group-flush">
                    <li class="list-group-item">An item</li>
                    <li class="list-group-item">A second item</li>
                    <li class="list-group-item">A third item</li>
                </ul>
            </div>
        </div>
        <div class="col-4 text-center">
            <img
                src="assets/placeholder.jpg"
                class="img-thumbnail"
                alt="placeholder"
            />
            <button
                type="button"
                class="btn btn-outline-primary m-3 align-center"
                >Select image</button
            >
        </div>
    </div>
</div>

<style>
</style>
