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
function computeDistance(latitude_1, longitude_1) {
    if (sessionStorage.getItem('Latitude') === null) {
        return 0
    }

    latitude_2 = parseFloat(sessionStorage.getItem('Latitude'));
    longitude_2 = parseFloat(sessionStorage.getItem('Longitude'));

    p = 0.017453292519943295 // Approximation Pi/180
    a = 0.5 - Math.cos((latitude_2 - latitude_1) * p) / 2 + Math.cos(latitude_1 * p) * Math.cos(latitude_2 * p) * (1 - Math.cos((longitude_2 - longitude_1) * p)) / 2
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
            sessionStorage.removeItem('Latitude');
            sessionStorage.setItem('Latitude', response.lat);
            sessionStorage.removeItem('Longitude');
            sessionStorage.setItem('Longitude', response.lon);
        },
        function fail(data, status) {
            sessionStorage.removeItem('Latitude');
            sessionStorage.removeItem('Longitude');
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
function color(selectedColor) {

    var newColor;

    if (selectedColor == 'SteelBlue') {
        newColor = 'ForestGreen';
    }
    else if (selectedColor == 'ForestGreen') {
        newColor = 'DarkOrange';
    }
    else if (selectedColor == 'DarkOrange') {
        newColor = 'DarkCyan';
    }
    else if (selectedColor == 'DarkCyan') {
        newColor = 'DarkMagenta';
    }
    else if (selectedColor == 'DarkMagenta') {
        newColor = 'DarkKhaki';
    }
    else if (selectedColor == 'DarkKhaki') {
        newColor = 'DimGray';
    }
    else if (selectedColor == 'DimGray') {
        newColor = 'Crimson';
    }
    else if (selectedColor == 'Crimson') {
        newColor = 'SteelBlue';
    }

    localStorage.setItem('Color', newColor);

    return 0;
}
