function status() {

}

function run() {
  fetch('http://127.0.0.1:9000/run', {
    method: "POST"
  }).then((resp) => resp.json()).then((data) => {
    console.log(data);
    document.getElementById('output').innerHTML = '<pre>' + data['output'] + '</pre>';
    for (let i of data['logs']) {
      document.getElementById('logs').innerHTML += '<pre>' + '<div onclick="get(\''+i+'\')">' + i + '</div></pre>'
    }
  })
}

function get(filename) {
  console.log(filename)
  fetch('http://127.0.0.1:9000/trace', {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({"name": filename})
  }).then(response => response.blob())
  .then(blob => {
    console.log(blob);
    const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.style.display = "none";
        a.href = url;
        // the filename you want
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);   
  });
}

function pass_json() {
  j = document.getElementById('dzejsn').value
  console.log(j)

  fetch('http://127.0.0.1:9000/tracejson', {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(j)
  }).then((resp) => resp.json()).then((data) => {
    console.log(data);
    document.getElementById('output').innerHTML = '<pre>' + data['output'] + '</pre>';
    for (let i of data['logs']) {
      document.getElementById('logs').innerHTML += '<pre>' + '<div onclick="get(\''+i+'\')">' + i + '</div></pre>'
    }
  })
}