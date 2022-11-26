const WEB_URL = `http://127.0.0.1:9000`

function run() {
  fetch(`${WEB_URL}/run`, {
    method: "POST"
  }).then((resp) => resp.json()).then((data) => {
    document.getElementById('output').innerHTML = '<pre>' + data['output'] + '</pre>';

    let log_cont = document.getElementById('logs').innerHTML
    log_cont += '<pre>'
    for (let i of data['logs']) {
      let name = i.name;
      let size = i.size;
      log_cont +=`<div onclick="get(\''${name}'\')"> ${name} (${size} bytes)</div></pre>`
    }
    log_cont += '</pre>'
  })
}

function get(filename) {
  console.log(filename)
  fetch(`${WEB_URL}/trace?name=${filename}`, {
    method: "GET",
    headers: {
      'Content-Type': 'application/json'
    }
  }).then(response => response.blob())
  .then(blob => {
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

  fetch(`${WEB_URL}/tracejson`, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(j)
  }).then((resp) => resp.json()).then((data) => {
    let elem_output = document.getElementById('output')
    elem_output.innerHTML = '<pre>' 
    for (let msg of data['output']) {
      elem_output.innerHTML += `${msg}<br>`;
    }
    elem_output +=  '</pre>';
    let elem_log = document.getElementById('logs')
    elem_log.innerHTML = '<pre>'
    for (let i of data['logs']) {
      let name = i.name;
      let size = i.size;
      elem_log.innerHTML +=`<div onclick="get(\''${name}'\')"> ${name} (${size} bytes)</div></pre>`
    }
    elem_log.innerHTML += '</pre>'
  })
}