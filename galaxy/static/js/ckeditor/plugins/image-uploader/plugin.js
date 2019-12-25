class ImageUploader {
    constructor(loader) {
        this.loader = loader
        this.url = '/api/upload'
        this.xhr = null
    }

    upload() {
        return this.loader.file.then(file => {
            this.xhr = new XMLHttpRequest()
            this.xhr.responseType = 'json'
            this.xhr.onprogress = (event) => {
                this.loader.uploadTotal = event.total
                this.loader.uploaded = event.uploaded
            }
            this.xhr.open('POST', this.url)
            return new Promise((resolve, reject) => {
                this._initRequest()
                this._initListeners(resolve, reject, file)
                this._sendRequest(file)
            })
        })
    }

    _initRequest() {
        const xhr = this.xhr = new XMLHttpRequest()
        xhr.open('POST', this.url, true)
        xhr.responseType = 'json'
    }

    _initListeners(resolve, reject, file) {
        const xhr = this.xhr
        const loader = this.loader
        const genericErrorText = `Couldn't upload file: ${file.name}.`

        xhr.addEventListener('error', () => reject(genericErrorText))
        xhr.addEventListener('abort', () => reject())

        xhr.addEventListener('load', () => {
            const response = xhr.response
            if (!response || response.error) {
                return reject(response && response.error ? response.error.message : genericErrorText)
            }
            resolve({
                default: response.data.url
            })
        })

        if (xhr.upload) {
            xhr.upload.addEventListener('progress', evt => {
                if (evt.lengthComputable) {
                    loader.uploadTotal = evt.total
                    loader.uploaded = evt.loaded
                }
            })
        }
    }

    _sendRequest(file) {
        const data = new FormData();
        data.append( 'file', file );
        this.xhr.send( data );
    }

    abort() {
        this.xhr.abort()
    }
}