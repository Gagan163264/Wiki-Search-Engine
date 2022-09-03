var residents = [{result: "RESULT 1", preview: "PREVIEW1"},{result: "RESULT 2", preview: "PREVIEW2"},{result: "RESULT 2", preview: "PREVIEW2"},{result: "RESULT 2", preview: "PREVIEW2"},{result: "RESULT 2", preview: "PREVIEW2"},{result: "RESULT 2", preview: "PREVIEW2"},{result: "RESULT 2", preview: "PREVIEW"}];

function people() {
    residents.forEach(function(resident) {
 document.write("<li>"+ resident.result + "<br> " + resident.preview + "</li>");
});

}
people();