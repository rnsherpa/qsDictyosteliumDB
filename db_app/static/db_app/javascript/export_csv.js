function downloadCSV(csv, filename) {
    var csvFile;
    var downloadLink;

    csvFile = new Blob([csv], {type: "text/csv"});

    downloadLink = document.createElement("a");

    downloadLink.download = filename;

    downloadLink.href = window.URL.createObjectURL(csvFile);

    downloadLink.style.display = "none";

    document.body.appendChild(downloadLink);

    downloadLink.click();
}

function tableToCSV(filename) {
    var csv = [];
    var allRows = document.querySelectorAll("table tr");

    for (var i=0; i<allRows.length; i++) {
        var row = []
        var cols = allRows[i].querySelectorAll("td,th");

        for (var j=0; j<cols.length; j++) {
            row.push(cols[j].innerText);
        }
    
        csv.push(row.join(","));
    }

    downloadCSV(csv.join("\n"), filename);
}