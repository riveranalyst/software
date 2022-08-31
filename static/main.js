Dropzone.autoDiscover = false;

const myDropzone = new Dropzone("#my-dropzone",{
    url: "modify/upload/",
    maxFiles: 1,
    //in MB:
    maxFilesize: 2,
    acceptedFiles: '.csv'
})
