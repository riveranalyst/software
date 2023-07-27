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
        window.location.href="/riveranalyst/modify/upload/success_upload/"},
         2000)});
})
//var options = {
//    // the selector for the badge template
//    templateSelector: "#CodeBadgeTemplate",
//
//    // base content CSS selector that is searched for snippets
//    contentSelector: "body",
//
//    // Delay in ms used for `setTimeout` before badging is applied
//    // Use if you need to time highlighting and badge application
//    // since the badges need to be applied afterwards.
//    // 0 - direct execution (ie. you handle timing
//    loadDelay: 0,
//
//    // CSS class(es) used to render the copy icon.
//    copyIconClass: "fa fa-copy",
//    // optional content for icons class (<i class="fa fa-copy"></i> or <i class="material-icons">file_copy</i>)
//    copyIconContent: "",
//
//    // CSS class(es) used to render the done icon.
//    checkIconClass: "fa fa-check text-success",
//    checkIconContent: "",
//
//    // function called before code is placed on clipboard that allows you inspect and modify
//    // the text that goes onto the clipboard. Passes text and code root element (hljs).
//    // Example:  function(text, codeElement) { return text + " $$$"; }
//    onBeforeCodeCopied: null
//};