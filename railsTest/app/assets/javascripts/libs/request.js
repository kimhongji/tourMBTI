(function() {
    window.get_default_url = function (){
        const regex = /(https?:\/\/)([a-zA-Z0-9:._-]+)/
        let current_url = window.location.href
        return current_url.match(regex)[0]
    }

    window.get_current_url = function (){
        const regex = /(https?:\/\/)([a-zA-Z0-9:._\-\/]+)/
        let current_url = window.location.href
        return current_url.match(regex)[0]
    }

    window.get_csrf = function (){
        return document.querySelector("meta[name='csrf-token']").getAttribute("content");
    }

    window.download_file = function (datafile, title){
        datafile = [datafile];
        let blob = new Blob(datafile, {type: "text/json;charset=utf-8"});
        let isIE = false || !!document.documentMode;
        if (isIE) {
            window.navigator.msSaveBlob(blob, title);
        } else {
            let url = window.URL || window.webkitURL;
            let link = url.createObjectURL(blob);
            let a = $("<a />");
            a.attr("download", title);
            a.attr("href", link);
            $("body").append(a);
            a[0].click();
            $("body").remove(a);
        }
    }

    window.post_file = function (file, url){
        // FILE READ
        const reader = new FileReader();
        reader.readAsText(file);
        reader.onload = function () {
            // POST FILE TO SERVER
            const result = reader.result;
            axios.post(url, result, {
                headers: {
                    "Content-Type": 'application/json',
                    "Accept": "application/json",
                    'X-CSRF-Token': get_csrf()
                }
            }).then((res) => {
                alert(res.data.message);
                location.href = url;
            }).catch(error => {
                console.log('failed', error)
            })
        }
    }

    window.addCommas = function(nStr){
        nStr += '';
        var x = nStr.split('.');
        var x1 = x[0];
        var x2 = x.length > 1 ? '.' + x[1] : '';
        var rgx = /(\d+)(\d{3})/;
        while (rgx.test(x1)) {
            x1 = x1.replace(rgx, '$1' + ',' + '$2');
        }
        return x1 + x2;
    }
})();