;
(function() {
    function getQueryVariable(variable) {
        var query = window.location.search.substring(1);
        var vars = query.split("&");
        for (var i = 0; i < vars.length; i++) {
            var pair = vars[i].split("=");
            if (pair[0] == variable) {
                return pair[1];
            }
        }
        return (false);
    }

    function computeDistance(latitude_1, longitude_1) {
        if (sessionStorage.getItem("Latitude") === null) {
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
                //console.log('Request failed.  Returned status of', status);
            }
        );
    }

    // Returns a flattened hierarchy containing all leaf nodes under the root.
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

    // Initialise IP Geoloc

    ipLookUp();

    /*
    if (sessionStorage.getItem('Latitude')) {
        console.log('Latitude', sessionStorage.getItem('Latitude'));
        console.log('Longitude', sessionStorage.getItem('Longitude'));
    }
    */

    // Initialise Marquee

    $('.marquee')
        .bind('finished', function() {
            $(this).html(sessionStorage.getItem('news'))
            .marquee({duration: 5000, direction: 'left', pauseOnHover: 'true'})
        })
        .marquee({duration: 5000, direction: 'left', pauseOnHover: 'true'});

    // And continue...

    let generateChartTimeout = null;

    window.addEventListener('resize', function() {
        clearTimeout(generateChartTimeout);
        generateChartTimeout = setTimeout(function() {
            generateD3Charts(true);
        }, 200);
    });

    generateD3Charts();

    var inter = setInterval(function() {
        generateD3Charts(false);
    }, 750);

    var old_abstract = '';
    var old_news = '';
    var old_best = '';
    var old_activity = '';
    var old_last = '';
    var old_bubble = '';
    var old_all = '';
    var old_porteuse = '';
    var old_porteuse_extended = '';
    var old_node_extended = '';

    function generateD3Charts(redraw = false) {
        if (redraw === true) {
            console.log("rezise");
            old_abstract = '';
            old_news = '';
            old_best = '';
            old_activity = '';
            old_last = '';
            old_bubble = '';
            old_all = '';
            old_porteuse = '';
            old_porteuse_extended = '';
            old_node_extended = '';
        }

        const columnWidth = document.querySelector('.columns :first-child').clientWidth;

        // Set the dimensions of the canvas
        const margin = {
                top: 20,
                right: 20,
                bottom: 70,
                left: 40
            },
            width = columnWidth - margin.left - margin.right,
            height = Math.max(width / 3, 250) - margin.top - margin.bottom;

        // Set the ranges
        const x = d3.scale.ordinal().rangeRoundBands([0, width], .05);
        const y = d3.scale.linear().range([height, 0]);

        // Define the axis
        const xAxis = d3.svg.axis()
            .scale(x)
            .orient('bottom');

        const yAxis = d3.svg.axis()
            .scale(y)
            .orient('left')
            .ticks(10);

        // Tot
        // Load the data

        d3.json('transmit.json', function(error, data) {
            const containerSelector = '.tot-graph';

            var TOT = 0;
            var Indicatif = '';
            var Latitude = 0;
            var Longitude = 0;
            var Distance = 0;

            if (data !== undefined) {
                TOT = data[0].TOT;
                Indicatif = data[0].Indicatif;
                Latitude = parseFloat(data[0].Latitude);
                Longitude = parseFloat(data[0].Longitude);
            }

            if (Latitude !== 0) {
                Distance = computeDistance(Latitude, Longitude);
            }

            sessionStorage.setItem('Indicatif', Indicatif);

            if (TOT == 0) {
                title = 'Aucune émission';
            } else {
                //title = Indicatif + ' en émission';
                title = Indicatif;
                if (Distance !== 0) {
                    title += ' (~ ' + Distance + ' Km)';
                }
                else {
                    title += ' en émission';
                }
            }

            const containerTitle = title;
            const containerLegend = 'Affiche l\'indicatif du nœud en cours d\'émission, la distance approximative de ce nœud, ainsi que la durée de passage en émission.';

            d3.select(containerSelector).html('');
            d3.select(containerSelector).append('h2').text(containerTitle);

            var svg_tot = d3.select(containerSelector)
                .append('div')
                .attr('class', 'clock')

            var clock;
            // Instantiate a counter
            clock = new FlipClock($('.clock'), TOT, {
                clockFace: 'MinuteCounter',
                language: 'french',
                clockFaceOptions: {
                    autoPlay: false,
                    autoStart: false
                }
            });

            d3.select(containerSelector).append('span').text(containerLegend);
        });

        // Activity
        // Load the data
        d3.json('activity.json', function(error, data) {
            if (old_activity !== JSON.stringify(data)) {
                old_activity = JSON.stringify(data);
            } else {
                return 0;
            }

            //console.log("activity redraw");

            const containerSelector = '.activity-graph';
            const containerTitle = 'Activité heure par heure';
            const containerLegend = 'Cet histogramme représente le nombre de passages en émission, heure par heure. Seuls les passages en émission de plus de 3 secondes sont comptabilisés.';

            d3.select(containerSelector).html('');
            d3.select(containerSelector).append('h2').text(containerTitle);

            data.forEach(function(d) {
                d.Hour = d.Hour;
                d.TX = d.TX;
            });

            var color = "steelblue";
            var yMax = d3.max(data, function(d) {
                return d.TX
            });
            var yMin = d3.min(data, function(d) {
                return d.TX
            });
            var colorScale = d3.scale.linear()
                .domain([yMin, yMax])
                .range([d3.rgb(color).brighter(), d3.rgb(color).darker()]);

            // Scale the range of the data
            x.domain(data.map(function(d) {
                return d.Hour;
            }));
            y.domain([0, d3.max(data, function(d) {
                return d.TX;
            })]);

            var svg_activity = d3.select(containerSelector)
                .append('svg')
                .attr('width', width + margin.left + margin.right)
                .attr('height', height + margin.top + margin.bottom)
                .append('g')
                .attr('transform',
                    'translate(' + margin.left + ',' + margin.top + ')');

            // Add axis
            svg_activity.append('g')
                .attr('class', 'x axis')
                .attr('transform', 'translate(0,' + (height + 0.5) + ')')
                .call(xAxis)
                .selectAll('text')
                .style('text-anchor', 'end')
                .attr('dx', '-.8em')
                .attr('dy', '-.55em')
                .attr('transform', 'rotate(-45)');

            svg_activity.append('g')
                .attr('class', 'y axis')
                .call(yAxis)
                .append('text')
                .attr('transform', 'rotate(0)')
                .attr('y', -10)
                .attr('dy', '.71em')
                .style('text-anchor', 'end')
                .text('TX');

            // Add bar chart
            svg_activity.selectAll('bar')
                .data(data)
                .enter().append('rect')
                .attr('class', 'bar')
                .attr("fill", function(d) {
                    return colorScale(d.TX)
                })
                .attr('x', function(d) {
                    return x(d.Hour);
                })
                .attr('width', x.rangeBand())
                .attr('y', function(d) {
                    return y(d.TX);
                })
                .attr('height', function(d) {
                    return height - y(d.TX);
                });

            svg_activity.selectAll('text.bar')
                .data(data)
                .enter().append('text')
                .attr('class', 'value')
                .attr('text-anchor', 'middle')
                .attr("x", function(d) {
                    return x(d.Hour) + x.rangeBand() / 2;
                })
                .attr('y', function(d) {
                    return y(d.TX) - 5;
                })
                .text(function(d) {
                    return d.TX;
                });

            d3.select(containerSelector).append('span').text(containerLegend);
        });

        // Best
        // Load the data
        d3.json('best.json', function(error, data) {
            if (old_best !== JSON.stringify(data)) {
                old_best = JSON.stringify(data);
            } else {
                return 0;
            }

            //console.log("best redraw");

            const containerSelector = '.best-graph';
            const containerTitle = 'Top 20 des nœuds les plus actifs';
            const containerLegend = 'Cet histogramme représente le classement des 20 nœuds les plus actifs de la journée, en terme de passages en émission.';

            d3.select(containerSelector).html('');
            d3.select(containerSelector).append('h2').text(containerTitle);

            data.forEach(function(d) {
                d.Indicatif = d.Indicatif;
                d.TX = d.TX;
            });

            var color = "steelblue";
            var yMax = d3.max(data, function(d) {
                return d.TX
            });
            var yMin = d3.min(data, function(d) {
                return d.TX
            });
            var colorScale = d3.scale.linear()
                .domain([yMin, yMax])
                .range([d3.rgb(color).brighter(), d3.rgb(color).darker()]);

            const svg_best = d3.select(containerSelector)
                .append('svg')
                .attr('width', width + margin.left + margin.right)
                .attr('height', height + margin.top + margin.bottom)
                .append('g')
                .attr('transform',
                    'translate(' + margin.left + ',' + margin.top + ')');

            // Scale the range of the data
            x.domain(data.map(function(d) {
                return d.Indicatif;
            }));
            y.domain([0, d3.max(data, function(d) {
                return d.TX;
            })]);

            // Add axis
            svg_best.append('g')
                .attr('class', 'x axis')
                .attr('transform', 'translate(0,' + (height + 0.5) + ')')
                .call(xAxis)
                .selectAll('text')
                .style('text-anchor', 'end')
                .attr('dx', '-.8em')
                .attr('dy', '-.55em')
                .attr('transform', 'rotate(-45)');

            svg_best.append('g')
                .attr('class', 'y axis')
                .call(yAxis)
                .append('text')
                .attr('transform', 'rotate(0)')
                .attr('y', -10)
                .attr('dy', '.71em')
                .style('text-anchor', 'end')
                .text('TX');

            // Add bar chart
            svg_best.selectAll('bar')
                .data(data)
                .enter().append('rect')
                .attr('class', 'bar')
                .attr("fill", function(d) {
                    return colorScale(d.TX)
                })
                .attr('x', function(d) {
                    return x(d.Indicatif);
                })
                .attr('width', x.rangeBand())
                .attr('y', function(d) {
                    return y(d.TX);
                })
                .attr('height', function(d) {
                    return height - y(d.TX);
                })

            svg_best.selectAll('text.bar')
                .data(data)
                .enter().append('text')
                .attr('class', 'value')
                .attr('text-anchor', 'middle')
                .attr("x", function(d) {
                    return x(d.Indicatif) + x.rangeBand() / 2;
                })
                .attr('y', function(d) {
                    return y(d.TX) - 5;
                })
                .text(function(d) {
                    return d.TX;
                });

            d3.select(containerSelector).append('span').text(containerLegend);
        });

        // All
        // Load the data

        d3.json('all.json', function(error, data) {
            if (old_bubble !== JSON.stringify(data)) {
                old_bubble = JSON.stringify(data);
            } else {
                return 0;
            }

            //console.log("bubble redraw");

            Indicatif = sessionStorage.getItem('Indicatif');

            var diameter = width + margin.left + margin.right,
                format = d3.format(',d')
            color = d3.scale.category20c();

            var bubble = d3.layout.pack()
                .sort(null)
                .size([diameter, diameter])
                .padding(1);

            const containerSelector = '.all-bubble';
            const containerTitle = 'Classement des nœuds actifs par durée cumulée en émission';
            const containerLegend = 'Ce graph présente le classement par durée cumulée en émission, des nœuds actifs dans la journée.';

            d3.select(containerSelector).html('');
            d3.select(containerSelector).append('h2').text(containerTitle);

            const svg = d3.select(containerSelector)
                .append('svg')
                .attr('width', diameter)
                .attr('height', diameter);

            tmp = '{' +
                '"children":' + JSON.stringify(data) +
                '}';

            data = JSON.parse(tmp)

            var color = 'steelblue';

            data.children.forEach(function(d) {
                a = d.Durée;
                b = a.split(':');
                if (b.length === 3) {
                    s = (+b[0]) * 60 * 60 + (+b[1]) * 60 + (+b[2]); 
                }
                else {
                    s = (+b[0]) * 60 + (+b[1]); 
                }
                d.TX = s;
            });

            var yMax = d3.max(data.children, function(d) {
                return d.TX;
            });
            var yMin = d3.min(data.children, function(d) {
                return d.TX;
            });

            data.children.forEach(function(d) {
                if (d.Indicatif === Indicatif) {
                    d.TX = yMax;
                }
            });

            var colorScale = d3.scale.linear()
                .domain([yMin, yMax])
                .range([d3.rgb(color).brighter(), d3.rgb(color).darker()]);

            var node = svg.selectAll('.node')
                .data(bubble.nodes(classes(data))
                    .filter(function(d) {
                        return !d.children;
                    }))
                .enter().append('g')
                .attr('class', 'node')
                .attr('transform', function(d) {
                    return 'translate(' + d.x + ',' + d.y + ')';
                });

            node.append('circle')
                .attr('r', function(d) {
                    return (d.r);
                })
                //.style('fill', function(d) { return color; })
                .style('fill', function(d) {
                    if (d.className === Indicatif) {
                        return 'lightslategray';
                    }
                    return colorScale(d.value);
                });

            node.append('text')
                .attr('class', 'value')
                .attr('dy', '.3em')
                .style('fill', function(d) {
                    if (d.className === Indicatif) {
                        return 'white';
                    }
                    return 'white';
                })
                .style('font-family', 'Arial, Helvetica, sans-serif')
                .style('font-size', function(d) {
                    return (d.r) / 4 + 'px';
                })
                .style('text-anchor', 'middle')
                .style('pointer-events', 'none')
                .text(function(d) {
                    return d.className;
                });

            d3.select(self.frameElement).style('height', diameter + 'px');
            d3.select(containerSelector).append('span').text(containerLegend);

        });

        // Abstract
        // Load the data
        d3.json('abstract.json', function(error, data) {
            if (old_abstract !== JSON.stringify(data)) {
                old_abstract = JSON.stringify(data);
            } else {
                return 0;
            }

            //console.log("abstract redraw");

            const containerSelector = '.abstract-table';
            const containerTitle = 'Résumé de la journée' + data[0].Date;
            const containerLegend = 'Ce tableau présente le résumé de l\'activité du salon dans la journée: nombre de passages en émission total, durée cumulée en émission, nombre de nœuds actifs et connectés. ';
            const containerLegendBis = 'En complément, vous pouvez suivre les mouvements des nœuds entrants et sortants sur ce salon, ainsi que les éventuelles émissions sur les autres salons, en suivant le fil d\'informations défilant ci-dessous.';
    
            function tabulate(data, columns) {
                d3.select(containerSelector).html('');
                d3.select(containerSelector).append('h2').text(containerTitle);

                const table = d3.select(containerSelector)
                    .append('table')
                    .attr('width', width + margin.left + margin.right + 'px');
                const thead = table.append('thead');
                const tbody = table.append('tbody');

                // Append the header row
                thead.append('tr')
                    .selectAll('th')
                    .data(columns).enter()
                    .append('th')
                    .text(function(column) {
                        return column;
                    });

                // Create a row for each object in the data
                const rows = tbody.selectAll('tr')
                    .data(data)
                    .enter()
                    .append('tr');

                // Create a cell in each row for each column
                const cells = rows.selectAll('td')
                    .data(function(row) {
                        return columns.map(function(column) {
                            return {
                                column: column,
                                value: row[column]
                            };
                        });
                    })
                    .enter()
                    .append('td')
                    .html(function(d, i) {
                        url = window.location.href;
                        if (d.value === 'RRF') {
                            url = url.replace('RRF-', 'TEC-')
                            return '<a href="' + url + '">' + d.value + '</a>';
                        } else if (d.value === 'TEC') {
                            url = url.replace('TEC-', 'RRF-')
                            return '<a href="' + url + '">' + d.value + '</a>';
                        } else if (i === 4) {
                            return '<a onClick="sessionStorage.setItem(\'node_extended\', \'' + 'Node' + '\'); window.location.reload()">' + d.value + '</a>';
                        } else {
                            if (i > 4) {
                                return d.value.replace(/, /g, '<br/>');
                            } else {
                                return d.value;
                            }
                        }
                    });

                return table;
            }

            // Render the table(s)
            tabulate(data, ['Salon', 'TX total', 'Emission cumulée', 'Nœuds actifs', 'Nœuds connectés']); // 5 columns table
            d3.select(containerSelector).append('span').text(containerLegend + containerLegendBis);
        });
 
        // News
        // Load the data
        d3.json('news.json', function(error, data) {
            if (old_news !== JSON.stringify(data)) {
                old_news = JSON.stringify(data);
            } else {
                return 0;
            }
                        
            sessionStorage.setItem('news', data[0].Message);
        });

        // Last
        // Load the data
        d3.json('last.json', function(error, data) {
            if (old_last !== JSON.stringify(data)) {
                old_last = JSON.stringify(data);
            } else {
                return 0;
            }

            //console.log("last redraw");

            Indicatif = sessionStorage.getItem('Indicatif');

            const containerSelector = '.last-table';
            const containerTitle = 'Derniers passages en émission';
            const containerLegend = 'Ce tableau présente la liste des 10 derniers passages en émission: horodatage, indicatif du nœud et durée en émission.';

            function tabulate(data, columns) {
                d3.select(containerSelector).html('');
                d3.select(containerSelector).append('h2').text(containerTitle);

                var table = d3.select(containerSelector)
                    .append('table')
                    .attr('width', width + margin.left + margin.right + 'px');

                var thead = table.append('thead');
                var tbody = table.append('tbody');

                // Append the header row
                thead.append('tr')
                    .selectAll('th')
                    .data(columns).enter()
                    .append('th')
                    .text(function(column) {
                        return column;
                    });

                // Create a row for each object in the data
                var rows = tbody.selectAll('tr')
                    .data(data)
                    .enter()
                    .append('tr');

                // Create a cell in each row for each column
                var cells = rows.selectAll('td')
                    .data(function(row) {
                        return columns.map(function(column) {
                            return {
                                column: column,
                                value: row[column]
                            };
                        });
                    })
                    .enter()
                    .append('td')
                    .text(function(d) {
                        return d.value;
                    });
                    
                return table;
            }

            // Render the table(s)
            tabulate(data, ['Date', 'Indicatif', 'Durée']); // 3 columns table
            d3.select(containerSelector).append('span').text(containerLegend);
        });

        // All
        // Load the data
        d3.json('all.json', function(error, data) {
            if (old_all !== JSON.stringify(data)) {
                old_all = JSON.stringify(data);
            } else {
                return 0;
            }

            //console.log("all redraw");

            const containerSelector = '.all-table';
            const containerTitle = 'Classement des nœuds actifs par TX';
            const containerLegend = 'Ce tableau présente le classement complet des nœuds étant passés en émission dans la journée: position, indicatif du nœud, nombre de passages et durée cumulée en émission.';

            function tabulate(data, columns) {
                d3.select(containerSelector).html('');
                d3.select(containerSelector).append('h2').text(containerTitle);

                var table = d3.select(containerSelector)
                    .append('table')
                    .attr('width', width + margin.left + margin.right + 'px');

                var thead = table.append('thead');
                var tbody = table.append('tbody');

                // Append the header row
                thead.append('tr')
                    .selectAll('th')
                    .data(columns).enter()
                    .append('th')
                    .text(function(column) {
                        return column;
                    });

                // Create a row for each object in the data
                var rows = tbody.selectAll('tr')
                    .data(data)
                    .enter()
                    .append('tr');

                // Create a cell in each row for each column
                var cells = rows.selectAll('td')
                    .data(function(row) {
                        return columns.map(function(column) {
                            return {
                                column: column,
                                value: row[column]
                            };
                        });
                    })
                    .enter()
                    .append('td')
                    .text(function(d) {
                        return d.value;
                    });

                return table;
            }

            // Render the table(s)
            tabulate(data, ['Pos', 'Indicatif', 'TX', 'Durée']); // 4 columns table
            d3.select(containerSelector).append('span').text(containerLegend);
        });

        // Porteuse
        // Load the data
        d3.json('porteuse.json', function(error, data) {
            if (old_porteuse !== JSON.stringify(data)) {
                old_porteuse = JSON.stringify(data);
            } else {
                return 0;
            }

            //console.log("porteuse redraw");

            const containerSelector = '.porteuse-table';
            const containerTitle = 'Déclenchements intempestifs';
            const containerLegend = 'Ce tableau présente le classement complet des nœuds ayant fait l\'objet de passages en émission intempestifs ou suspects, d\'une durée de moins de 3 secondes: position, indicatif du nœud et nombre de passages en émission.';

            if (data !== undefined) {

                function tabulate(data, columns) {
                    d3.select(containerSelector).html('');
                    d3.select(containerSelector).append('h2').text(containerTitle);

                    var table = d3.select(containerSelector)
                        .append('table')
                        .attr('width', width + margin.left + margin.right + 'px');

                    var thead = table.append('thead');
                    var tbody = table.append('tbody');

                    // Append the header row
                    thead.append('tr')
                        .selectAll('th')
                        .data(columns).enter()
                        .append('th')
                        .text(function(column) {
                            return column;
                        });

                    // Create a row for each object in the data
                    var rows = tbody.selectAll('tr')
                        .data(data)
                        .enter()
                        .append('tr');

                    // Create a cell in each row for each column
                    var cells = rows.selectAll('td')
                        .data(function(row) {
                            return columns.map(function(column) {
                                return {
                                    column: column,
                                    value: row[column],
                                    id: row.Pos
                                };
                            });
                        })
                        .enter()
                        .append('td')
                        .html(function(d, i) {
                            if (i === 0) {
                                return '<a onClick="sessionStorage.setItem(\'porteuse_extended\', \'' + d.id + '\'); window.location.reload()">' + d.value + '</a>';
                            } else {
                                return d.value;
                            }
                        });

                    return table;
                }

                // Render the table(s)
                tabulate(data, ['Pos', 'Indicatif', 'TX']); // 3 columns table
                d3.select(containerSelector).append('span').text(containerLegend);
            }
        });

        node_extended = sessionStorage.getItem('node_extended');
        porteuse_extended = sessionStorage.getItem('porteuse_extended');

        if (porteuse_extended != null) {
            // Porteuse
            // Load the data
            d3.json('porteuse_extended.json', function(error, data) {
                if (old_porteuse_extended !== JSON.stringify(data)) {
                    old_porteuse_extended = JSON.stringify(data);
                } else {
                    return 0;
                }

                data = [data[parseInt(porteuse_extended) - 1]];

                const containerSelector = '#porteuse-extended-modal';
                const containerTitle = 'Heures des déclenchements intempestifs sur ' + data[0].Indicatif;
                const containerLegend = 'Ce tableau présente les heures de passages en émission intempestifs ou suspects, d\'une durée de moins de 3 secondes sur le nœud sélectionné.';

                if (data !== undefined) {

                    function tabulate(data, columns) {
                        d3.select(containerSelector).html('');
                        d3.select(containerSelector).append('h2').text(containerTitle);

                        var table = d3.select(containerSelector).append('table');
                        var thead = table.append('thead');
                        var tbody = table.append('tbody');

                        // Append the header row
                        thead.append('tr')
                            .selectAll('th')
                            .data(columns).enter()
                            .append('th')
                            .text(function(column) {
                                if (column === 'Date') {
                                    return 'Heure';
                                } else {
                                    return column;
                                }
                            });

                        // Create a row for each object in the data
                        var rows = tbody.selectAll('tr')
                            .data(data)
                            .enter()
                            .append('tr');

                        // Create a cell in each row for each column
                        var cells = rows.selectAll('td')
                            .data(function(row) {
                                return columns.map(function(column) {
                                    return {
                                        column: column,
                                        value: row[column]
                                    };
                                });
                            })
                            .enter()
                            .append('td')
                            .html(function(d, i) {
                                if (i === 1) {
                                    return d.value.replace(/, /g, '<br/>');
                                } else {
                                    return d.value;
                                }
                            });

                        return table;
                    }

                    // Render the table(s)                    
                    tabulate(data, ['Indicatif', 'Date', 'TX']); // 3 columns table
                    d3.select(containerSelector).append('span').text(containerLegend);

                    $('#porteuse-extended-modal').modal();
                    sessionStorage.removeItem('porteuse_extended');
                }
            });
        }

        if (node_extended != null) {
            // Porteuse
            // Load the data
            d3.json('node_extended.json', function(error, data) {
                if (old_node_extended !== JSON.stringify(data)) {
                    old_node_extended = JSON.stringify(data);
                } else {
                    return 0;
                }

                const containerSelector = '#node-extended-modal';
                const containerTitle = 'Liste des nœuds connectés';
                const containerLegend = 'Ce tableau présente la liste des nœuds actuellement connectés.';

                if (data !== undefined) {

                    function tabulate(data, columns) {
                        d3.select(containerSelector).html('');
                        d3.select(containerSelector).append('h2').text(containerTitle);

                        var table = d3.select(containerSelector).append('table');
                        var thead = table.append('thead');
                        var tbody = table.append('tbody');

                        // Create a row for each object in the data
                        var rows = tbody.selectAll('tr')
                            .data(data)
                            .enter()
                            .append('tr');

                        // Create a cell in each row for each column
                        var cells = rows.selectAll('td')
                            .data(function(row) {
                                return columns.map(function(column) {
                                    return {
                                        column: column,
                                        value: row[column]
                                    };
                                });
                            })
                            .enter()
                            .append('td')
                            .text(function(d) {
                                return d.value;
                            });

                        return table;
                    }

                    // Render the table(s)
                    tabulate(data, ['Node 0', 'Node 1', 'Node 2', 'Node 3']); // 8 columns table
                    d3.select(containerSelector).append('span').text(containerLegend);

                    $('#node-extended-modal').modal();
                    sessionStorage.removeItem('node_extended');
                }
            });
        }
    }

    const containerAuthor = 'RRFTracker est un projet Open Source, développé par F4HWN Armel, sous licence MIT.';
    const containerSelector = '.author-legend';
    d3.select(containerSelector).append('span')
        .attr('class', 'author')
        .text(containerAuthor);

})();