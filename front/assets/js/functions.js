// Compute Yesterday date
function getYesterday() {
    var todayTimeStamp = +new Date; // Unix timestamp in milliseconds
    var oneDayTimeStamp = 1000 * 60 * 60 * 24; // Milliseconds in a day
    var diff = todayTimeStamp - oneDayTimeStamp;
    var yesterdayDate = new Date(diff);
    var result = yesterdayDate.getFullYear() + '-'
    if ((yesterdayDate.getMonth() + 1) < 10) {
        result += '0';
    }
    result += yesterdayDate.getMonth() + 1 + '-'
    if (yesterdayDate.getDate() < 10) {
        result += '0';
    }
    result += yesterdayDate.getDate();
    return result;
}

// Compute Distance
function computeDistance(latitudeLink, longitudeLink) {
    if (sessionStorage.getItem('latitude') === null) {
        return 0
    }

    latitudeUser = parseFloat(sessionStorage.getItem('latitude'));
    longitudeUser = parseFloat(sessionStorage.getItem('longitude'));

    p = 0.017453292519943295 // Approximation Pi/180
    a = 0.5 - Math.cos((latitudeUser - latitudeLink) * p) / 2 + Math.cos(latitudeLink * p) * Math.cos(latitudeUser * p) * (1 - Math.cos((longitudeUser - longitudeLink) * p)) / 2
    r = (12742 * Math.asin(Math.sqrt(a)))
    if (r < 100) {
        r = Math.round((12742 * Math.asin(Math.sqrt(a))), 1)
    }
    else {
        r = Math.ceil(12742 * Math.asin(Math.sqrt(a)))
    }

    return r;
}

// Get IP Location
function ipLookUp () {
    $.ajax('http://ip-api.com/json')
    .then(
        function success(response) {
            sessionStorage.removeItem('latitude');
            sessionStorage.setItem('latitude', response.lat);
            sessionStorage.removeItem('longitude');
            sessionStorage.setItem('longitude', response.lon);
        },
        function fail(data, status) {
            sessionStorage.removeItem('latitude');
            sessionStorage.removeItem('longitude');
        }
    );
}

// Returns a flattened hierarchy containing all leaf nodes under the root
function classes(data) {
    var classes = [];

    function recurse(name, node) {
        if (node.children) node.children.forEach(function(child) {
            recurse(node.name, child);
        });
        else classes.push({
            packageName: name,
            className: node.Indicatif,
            value: node.TX
        });
    }

    recurse(null, data);
    return {
        children: classes
    };
}

// Change color
function color(colorSelected) {

    var newColor;

    if (colorSelected == 'SteelBlue') {
        newColor = 'ForestGreen';
    }
    else if (colorSelected == 'ForestGreen') {
        newColor = 'DarkOrange';
    }
    else if (colorSelected == 'DarkOrange') {
        newColor = 'DarkCyan';
    }
    else if (colorSelected == 'DarkCyan') {
        newColor = 'DarkMagenta';
    }
    else if (colorSelected == 'DarkMagenta') {
        newColor = 'DarkKhaki';
    }
    else if (colorSelected == 'DarkKhaki') {
        newColor = 'DimGray';
    }
    else if (colorSelected == 'DimGray') {
        newColor = 'Crimson';
    }
    else if (colorSelected == 'Crimson') {
        newColor = 'SteelBlue';
    }

    localStorage.setItem('color', newColor);

    return 0;
}

// Change porteuse
function porteuse(porteuseSelected) {

    var newPorteuse;

    if (porteuseSelected == 1) {
        newPorteuse = 5;
    }
    else if (porteuseSelected == 5) {
        newPorteuse = 10;
    }
    else {
        newPorteuse = 1;
    }
    
    localStorage.setItem('porteuse', newPorteuse);

    return 0;
}
