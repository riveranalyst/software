Dropzone.autoDiscover = false;

var myDropzone = new Dropzone("#my-dropzone",{
    url: "modify/upload/",
    maxFiles: 1,
    //in MB:
    maxFilesize: 2,
    acceptedFiles: ".csv",
})
