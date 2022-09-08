Dropzone.autoDiscover = false;

$(function() {
    // initialize the dropzone
    var myDropzone = new Dropzone("#my-dropzone",{
        url: "modify/upload/",
        maxFiles: 1,
        //in MB:
        maxFilesize: 2,
        acceptedFiles: ".csv",
        });
        // custom functionality for redirecting
        myDropzone.on("success", function(file){
        window.setTimeout(function(){
        window.location.href="/flussdata/modify/upload/success_upload/"},
         2000)});
})

$('code').on('click', function(e){
  var sel = window.getSelection()
  var r = document.createRange()
  r.selectNodeContents(e.target.closest('code'))
  sel.removeAllRanges()
  sel.addRange(r)
  document.execCommand('copy')
})
