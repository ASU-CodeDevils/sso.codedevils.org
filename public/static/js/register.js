// Get the modal
var modal = document.getElementById("modal");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

function filterByColumn(col, input) {
    // Declare variables
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById(input);
    filter = input.value.toUpperCase();
    table = document.getElementById("registerTable");
    tr = table.getElementsByTagName("tr");

    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[col];
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

$("#registerTable tr.record").click(function () {
    $(this).addClass('selected').siblings().removeClass('selected');
    let lang = document.documentElement.lang;
    let value = $(this).find('td:first').html();
    window.location = lang + "/join/registrations/" + value + "/";
});

// modal info

// Get the modal
var slackModal = document.getElementById("slackModal");
var slackInstructions = document.getElementById("slackInstructions");
var sdsModal = document.getElementById("sdsModal");
var sdsInstructions = document.getElementById("sdsInstructions");

// Get the <span> element that closes the modal
var slackInstructionsSpan = document.getElementById("slackInstructionsLink");
var slackSpan = document.getElementById("slackClose");
var sdsInstructionsSpan = document.getElementById("sdsInstructionsLink");
var sdsSpan = document.getElementById("sdsClose");

// Get the button that opens the modal
var slackBtn = document.getElementById("slackBtn");
var sdsBtn = document.getElementById("sdsBtn");
slackBtn.onclick = function() {
    slackModal.style.display = "block";
}
sdsBtn.onclick = function() {
    sdsModal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
slackSpan.onclick = function() {
  slackModal.style.display = "none";
}
slackInstructionsSpan.onclick = function() {
    if(slackInstructions.style.display !== "none") {
        slackInstructions.style.display = "none";
        slackInstructionsSpan.innerHTML = "Show instructions";
    } else {
        slackInstructions.style.display = "block";
        slackInstructionsSpan.innerHTML = "Hide instructions";
    }
}
sdsSpan.onclick = function() {
  sdsModal.style.display = "none";
}
sdsInstructionsSpan.onclick = function() {
    if(sdsInstructions.style.display !== "none") {
        sdsInstructions.style.display = "none";
        sdsInstructionsSpan.innerHTML = "Show instructions";
    } else {
        sdsInstructions.style.display = "block";
        sdsInstructionsSpan.innerHTML = "Hide instructions";
    }
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == slackModal) {
    slackModal.style.display = "none";
  }
  if (event.target == sdsModal) {
    sdsModal.style.display = "none";
  }
}