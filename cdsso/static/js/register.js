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

/* Side drawer */

/* Set the width of the sidebar to 250px and the left margin of the page content to 250px */
function openNav() {
    let drawer = document.getElementById("sideDrawer");
    let openbtn = document.getElementById("openbtn");
    if (drawer.style.width === "250px") {
        drawer.style.width = "0";
        openbtn.style.marginLeft = "0";
        openbtn.innerHTML = "Open Actions &uarr;";
        document.getElementsByTagName("main").item(0).style.marginLeft = "0";
        document.getElementsByTagName("footer").item(0).style.marginLeft = "0";
    } else {
        drawer.style.width = "250px";
        openbtn.style.marginLeft = "250px";
        openbtn.innerHTML = "Close Actions &darr;";
        document.getElementsByTagName("main").item(0).style.marginLeft = "270px";
        document.getElementsByTagName("footer").item(0).style.marginLeft = "270px";
    }
}

/* Set the width of the sidebar to 0 and the left margin of the page content to 0 */
function closeNav() {
    document.getElementById("sideDrawer").style.width = "0";
    document.getElementById("openbtn").style.marginLeft = "0";
    document.getElementById("openbtn").innerHTML = "Open Actions &uarr;";
    document.getElementById("main").style.marginLeft = "20px";
    document.getElementsByTagName("main").item(0).style.marginLeft = "0";
    document.getElementsByTagName("footer").item(0).style.marginLeft = "0";
}

/* Clipboard navigation */

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function () {
        /* clipboard successfully set */
        alert("Copied to clipboard");
    }, function () {
        /* clipboard write failed */
        alert("Could not copy to clipboard")
    });
}

/* buttons */

var slackCopyStudent = document.getElementById("slackCopyStudent");
var slackCopyAlumni = document.getElementById("slackCopyAlumni");
var slackConfirmStudent = document.getElementById("slackConfirmStudent");
var slackConfirmAlumni = document.getElementById("slackConfirmAlumni");
var sdsCopy = document.getElementById("sdsCopy");
var sdsConfirm = document.getElementById("sdsConfirm");

/* hidden value fields */

var slack_student_emails = document.getElementById("slack_student_emails");
var slack_alumni_emails = document.getElementById("slack_alumni_emails");
var sds_student_emails = document.getElementById("sds_student_emails");
var sds_alumni_emails = document.getElementById("sds_alumni_emails");

/* copyy operations */

slackCopyStudent.onclick = function () {
    var value = slack_student_emails.value;
    if (value === "") {
        alert("All students have been confirmed on Slack");
    } else {
        copyToClipboard(value);
    }
}

slackCopyAlumni.onclick = function () {
    var value = slack_alumni_emails.value;
    if (value === "") {
        alert("All alumni have been confirmed on Slack");
    } else {
        copyToClipboard(value);
    }
}

sdsCopy.onclick = function () {
    var value = sds_student_emails.value.replace(/,/g, "\n");
    if (value === "") {
        alert("All SunDevilSync Registrations have been confirmed on Slack");
    } else {
        copyToClipboard(value);
    }
}

/* confirmations */

slackConfirmStudent.onclick = function () {
    var value = slack_student_emails.value;
    if (value === "") {
        alert("All students have been confirmed on Slack");
    } else {
        var confirmStudent = confirm("Are you sure you want to confirm these students on Slack?");
        if (confirmStudent == true) {
            window.location.href = "/join/registrations/?slack_student_emails=" + value;
        }
    }
}

slackConfirmAlumni.onclick = function () {
    var value = slack_alumni_emails.value;
    if (value === "") {
        alert("All alumni have been confirmed on Slack");
    } else {
        var confirmStudent = confirm("Are you sure you want to confirm these alumni on Slack?");
        if (confirmStudent == true) {
            window.location.href = "/join/registrations/?slack_alumni_emails=" + value;
        }
    }
}

sdsConfirm.onclick = function () {
    var student_value = sds_student_emails.value
    var alumni_value = sds_alumni_emails.value
    if (student_value === "" && alumni_value === "") {
        alert("All members have been confirmed on SunDevilSync");
    } else {
        var confirmSds = confirm("Are you sure you want to confirm these members on SunDevilSync?");
        if (confirmSds == true) {
            let href_location = "/join/registrations/?"
            if (student_value !== "None") {
                href_location += "sds_student_emails=" + student_value;
            }

            if (alumni_value !== "None") {
                if (student_value !== "None") {
                    href_location += "&";
                }
                href_location += "&sds_alumni_emails=" + alumni_value;
            }
            window.location.href = href_location;
        }
    }
}
