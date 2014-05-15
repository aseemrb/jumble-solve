function showAnas(response) {
	document.getElementById('response').innerHTML = "";
    document.getElementById('response').innerHTML += "<div class='row-fluid'>";
    for(var i=0;i<response.grams.length;i++)
    {
        var snipobj = response.grams[i];
        if(i%5==0)
            document.getElementById('response').innerHTML += "</div><br><br><div class='row-fluid'>";
        document.getElementById('response').innerHTML +=
                    "<div class='span3'>" + snipobj.gr + "</div>";
    }
    document.getElementById('response').innerHTML += '<br><br>';
    if(response.grams.length==0)
        document.getElementById('response').innerHTML = "<div class='row-fluid'><div class='span4'></div><div class='span6'><h3>No anagrams found in dictionary!</h3></div></div>";
}

function anagrams() {
    var xhr = new XMLHttpRequest();
    var word = document.getElementById('ana').value;    
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4)
        	showAnas(JSON.parse(xhr.responseText));
    }
    xhr.open("GET", "scrape/?word=" + word, false);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send();
    xmlDocument = xhr.responseText;
}