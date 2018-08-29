var G = {};

function ue_loads(t){var retval={};var pairs=t.split('&');for(var i in pairs){var pair=pairs[i].split('=');if(pair[0] in retval){if(typeof retval[pair[0]]=='string'){retval[pair[0]]=[retval[pair[0]],decodeURIComponent(pair[1])];}else{retval[pair[0]].push(decodeURIComponent(pair[1]))}}else{retval[pair[0]]=decodeURIComponent(pair[1])}}return retval}

function isEditableType(mimetype){
    if(/(text|script)/.test(mimetype))
	return true;
    return false;
}

function request(method, url, data, callback){
	var req = new XMLHttpRequest();
	req.open(method, documentRoot + url);
	req.onreadystatechange = function(c){ return function(){
		if(this.readyState == XMLHttpRequest.DONE){
			c(this.responseText);
		}
	}
	}(callback);
    req.onerror = function(){
        globError('Failed to request server');
    }
	req.send(data);
}

function autoBind(){
    var binded = document.querySelectorAll('[data-bind]');
    Array.prototype.forEach.call(
        binded,
        function(x){
            if(x instanceof HTMLElement){
                window.G[x.getAttribute('data-bind')] = x;
            }
        }
    );
}

function humanizeSize(bytes){
    var i = 0;
    var prefixes = ['', 'K', 'M', 'G', 'T'];
    while(Math.pow(2, i * 10) < bytes) i++;
    return (bytes / (Math.pow(2, (i - 1) * 10))).toFixed(0) + prefixes[i - 1];
}

function renameShow(name){
    G['renameModal'].style.display = 'block';
    G['renameOld'].value = name;
    G['renameNew'].value = name;
}

function renameHide(){
    G['renameNew'].value = '';
    G['renameModal'].style.display = 'none';
}

function renameValidation(){
   if(G['renameNew'].value.trim() == '')
       return false;
   return true;
}

function updateFileListing(sortmode){
    if(typeof sortmode == 'undefined') sortmode = 'name';
    switch(sortmode){
    case 'size':
        var sortFunction = function(a, b){
            return a.size > b.size ? 1 : a.size == b.size ? 0 : -1;
        }
        break;
    case 'type':
        var sortFunction = function(a, b){
            return a.type.localeCompare(b.type);
        }
        break;
    default:
        var sortFunction = function(a, b){
            return a.name.localeCompare(b.name, {}, {sensitivity: 'case'});
        }
        break;
    }
    request(
        'GET',
        '/do/listing',
        null,
        function(sortfunc){
        return function(r){
            var resp = JSON.parse(r);
            if(resp.code == 0){
                var sorted = resp.result.sort(sortfunc);
                while(G.tabulator.rows.length > 1)
                    G.tabulator.deleteRow();
                for(var i in sorted){
                    var row = G.tabulator.insertRow(-1);
                    var rowContents = [
                        '<input type="checkbox" name="file" value="' + sorted[i].name + '">',
                        '<a href="/'+sorted[i].name+'" target="_blank">'+sorted[i].name+'</a>' + 
                        (isEditableType(sorted[i].type) ? ' <sup><a href="'+documentRoot+'/editor?file=' + sorted[i].name + '">edit</a></sup>' : ''),
                        sorted[i].type,
                        humanizeSize(sorted[i].size),
			'<button type="button" class="form-button form-button_regular form-button_compact" onclick="renameShow(\'' + sorted[i].name + '\')">RENAME</button>'
                    ];
                    for(var i in rowContents){
                        var cell = row.insertCell(-1);
                        cell.innerHTML = rowContents[i];
                    }
                }
            }
        }
        }(sortFunction)
    );
}
autoBind();
if(location.href.indexOf('?') != -1){
    var r = ue_loads(location.href.split('?')[1]);
    switch(r.sort){
    case 'size':
        updateFileListing('size');
        break;
    case 'type':
        updateFileListing('type');
        break;
    default:
        updateFileListing();
    }
} else {
    updateFileListing();
}
G.uploader.onchange = function(){
    G.upBtn.style.display = 'none';
    G.upList.style.display = 'inline-block';
    var files = [];
    for(var i in this.files){
        if(this.files[i] instanceof File)
        files.push(this.files[i].name);
    }
    console.log(files);
    G.upList.innerText = files.join(' ');
}

