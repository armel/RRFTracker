;
(function() {
    // Initialise IP Geoloc
    ipLookUp();

    // Initialise Marquee
    $('.marquee')
        .bind('finished', function() {
            $(this).html(sessionStorage.getItem('news'))
            .marquee({duration: 5000, direction: 'left', pauseOnHover: 'true'})
        })
        .marquee({duration: 5000, direction: 'left', pauseOnHover: 'true'});

    // Initialise color

    if (localStorage.getItem('color') === null) {
        localStorage.setItem('color', 'ForestGreen');
    }
    
    var colorSelected = localStorage.getItem('color');

    // Initialise porteuse

    if (localStorage.getItem('porteuse') === null) {
        localStorage.setItem('porteuse', 10);
    }
    
    var porteuseSelected = localStorage.getItem('porteuse');

    // And continue...
    var generateChartTimeout = null;

    window.addEventListener('resize', function() {
        clearTimeout(generateChartTimeout);
        generateChartTimeout = setTimeout(function() {
            generateD3Charts(true);
        }, 250);
    });

    var abstract, abstractOld = '';
    var news, newsOld = '';
    var elsewhere, elsewhereOld = '';
    var activity, activityOld = '';
    var best, bestOld = '';
    var transmit, transmitOld = '';
    var last, lastOld = '';
    var allExtended, allExtendedOld = '';
    var bubbleOld = '';
    var porteuseExtended, porteuseExtendedOld = '';
    var nodeExtended, nodeExtendedOld = '';
    var totExtended, totExtendedOld = '';
    var colorSelectedOld = '';
    var porteuseSelectedOld = 10;
    var userCountOld = 0

    var inter = setInterval(function() {
        generateD3Charts(false);
    }, 250);

    function generateD3Charts(redraw = false) {
        if (redraw === true) {
            console.log("rezise");
            abstractOld = '';
            newsOld = '';
            elsewhereOld = '';
            activityOld = '';
            bestOld = '';
            transmitOld = '';
            lastOld = '';
            allOld = '';
            allExtendedOld = '';
            bubbleOld = '';
            porteuseOld = '';
            porteuseExtendedOld = '';
            nodeExtendedOld = '';
            totExtendedOld = '';
            colorSelectedOld = '';
            porteuseSelectedOld = 10;
            userCountOld = 0
        }

        colorSelected = localStorage.getItem('color');
        porteuseSelected = localStorage.getItem('porteuse');

        var bodyStyles = document.body.style;
        bodyStyles.setProperty('--color-theme', colorSelected);

        const noCache = new Date().getTime();
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

        // Other QSO
        var room = ['RRF', 'TECHNIQUE', 'INTERNATIONAL', 'BAVARDAGE', 'LOCAL', 'FON'];
        var roomOther = [];

        // Load the data
        //d3.json('rrf.json' + '?_=' + noCache, function(error, data) {
        d3.json('rrf.json', function(error, data) {
            if (error) {
                return console.warn('Erreur', error);
            }
            else {
                old = JSON.stringify(data).replace(/nœud/gi, 'link');
                data = JSON.parse(old);
                abstract = data['abstract'];
                news = data['news'];
                elsewhere = data['elsewhere'];
                activity = data['activity'];
                best = data['best'];
                transmit = data['transmit'];
                last = data['last'];
                allExtended = data['allExtended'];
                porteuseExtended = data['porteuseExtended'];
                nodeExtended = data['nodeExtended'];
                totExtended = data['totExtended'];
            }
        });

        nodeExtendedModal = sessionStorage.getItem('nodeExtendedModal');
        porteuseExtendedModal = sessionStorage.getItem('porteuseExtendedModal');
        totExtendedModal = sessionStorage.getItem('totExtendedModal');
        allExtendedModal = sessionStorage.getItem('allExtendedModal');

        // ---------------------------------
        // Abstract
        // ---------------------------------

        if (abstract !== undefined) {
            if (abstractOld !== JSON.stringify(abstract)) {
                abstractOld = JSON.stringify(abstract);

                //console.log(abstract[0].Date);
           
                sessionStorage.setItem('room', abstract[0].Salon);
                sessionStorage.setItem('user', abstract[0].User);

                url = window.location.href;
                if (url.indexOf('today') > 0) {
                    url = url.substring(0, url.lastIndexOf(sessionStorage.getItem('room') + '-'));
                    url += sessionStorage.getItem('room') + '-' + getYesterday();
                    
                    date = new Date(Date.now()).toLocaleString();
                    date = date.substring(0, date.lastIndexOf(':'));

                    var containerTitle = 'Résumé du ' + date + ' sur le salon ' + sessionStorage.getItem('room') + ' (<a href="' + url + '">archive d\'hier</a>)';
                }
                else {
                    url = url.substring(0, url.lastIndexOf(sessionStorage.getItem('room') + '-'));
                    url += sessionStorage.getItem('room') + '-today';

                    date = new Date(Date.now() - (1 * 24 * 3600 * 1000)).toLocaleString();
                    date = date.substring(0, date.indexOf(' '));

                    var containerTitle = 'Résumé de la journée du ' + date + ' sur le salon ' + sessionStorage.getItem('room') + ' (retour à <a href="' + url + '">aujourd\'hui</a>)';                }

                containerTitle = '<div class="icon"><i class="icofont-info-circle"></i></div> ' + containerTitle;

                const containerSelector = '.abstract-table';
                const containerLegend = 'Ce tableau présente le résumé de l\'activité du salon dans la journée : nombre de passages en émission total, durée cumulée en émission, nombre de links actifs et connectés. ';
                const containerLegendBis = 'En complément, vous pouvez suivre les mouvements des links entrants et sortants sur ce salon, en suivant le fil d\'informations défilant ci-dessous.';

                data = abstract;

                var roomCurrent = '';

                function tabulate(data, columns) {
                    d3.select(containerSelector).html('');
                    d3.select(containerSelector).append('h2').html(containerTitle);

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
                        .attr('width', '20%')
                        .html(function(d, i) {
                            if (i ===2 ) {
                                tmp = d.value.split(':');
                                if (d.value.length > 5) {
                                    d.value = tmp[0] + 'h ' + tmp[1] + 'm ' + tmp[2] + 's';
                                }
                                else {
                                    d.value = tmp[0] + 'm ' + tmp[1] + 's';
                                }
                            }

                            if (i === 4) {
                                return '<a onClick="sessionStorage.setItem(\'nodeExtendedModal\', \'' + 'Node' + '\');">' + d.value + '</a>';
                            } else {
                                return d.value;
                            }
                        });
                    return table;
                }

                // Render the table(s)
                tabulate(data, ['Salon', 'TX total', 'Emission cumulée', 'links actifs', 'links connectés']); // 5 columns table
                d3.select(containerSelector)
                    .append('span')
                    .attr('width', width + margin.left + margin.right + 'px')
                    .text(containerLegend + containerLegendBis);
            }
        }

        // ---------------------------------
        // News
        // ---------------------------------

        if (news !== undefined) {
            if (newsOld !== JSON.stringify(news)) {
                newsOld = JSON.stringify(news);

                sessionStorage.setItem('news', news[0].Message);
            }
        }

        // ---------------------------------
        // Elsewhere
        // ---------------------------------

        if (elsewhere !== undefined) {
            if (elsewhereOld !== JSON.stringify(elsewhere)) {
                elsewhereOld = JSON.stringify(elsewhere);

                const containerSelector = '.elsewhere-table';
                const containerTitle = '<div class="icon"><i class="icofont-dashboard-web"></i></div> ' + 'Activité sur les autres salons';
                const containerLegend = 'Ce tableau présente l\'activité éventuelle sur les autres salons : indicatif en cours d\'émission, nombre de passages en émission total, durée cumulée en émission, nombre de links actifs et connectés, ainsi qu\'un rappel des codes DTMF standards. ';

                data = elsewhere;

                room.forEach(function(d) {
                    if (d !== sessionStorage.getItem('room')) {
                        roomOther.push(d);
                    }
                });

                roomOther.unshift('Scanner RRF');

                var count = (elsewhereOld.match(/Aucune émission/g) || []).length;

                function tabulate(data, columns) {
                    d3.select(containerSelector).html('');
                    d3.select(containerSelector).append('h2').html(containerTitle);

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
                        .html(function(column) {
                            if (column != 'Scanner RRF') {
                                url = window.location.href;
                                url = url.replace('/' + sessionStorage.getItem('room') + '-', '/' + column + '-')
                                return '<a href="' + url + '">' + column + '</a>';
                            }
                            else {
                                if (count < 5) { // Fix me after migration with 5
                                    return ('<div class="blink"><div class="icon"><i class="icofont-headphone-alt-1"></i></div></div>');
                                }
                                else {
                                    return ('<div class="icon"><i class="icofont-headphone-alt-3"></i></div>');
                                }
                            }
                        });

                    // Create a row for each object in the data
                    const rows = tbody.selectAll('tr')
                        .data(data)
                        .enter()
                        .append('tr');

                    // Create a cell in each row for each column

                    j = 0;

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
                        .attr('width', function(d, i) {
                            if (i === 0) {
                                return '20%';
                            }
                            else {
                                return '16%';
                                // return '16%';
                            }
                        })
                        .html(function(d, i) {
                            if (i == 0) {
                                j += 1;
                            }
                            if (i > 0 && j == 4) {
                                tmp = d.value.split(':');
                                if (d.value.length > 5) {
                                    d.value = tmp[0] + 'h ' + tmp[1] + 'm ' + tmp[2] + 's';
                                }
                                else {
                                    d.value = tmp[0] + 'm ' + tmp[1] + 's';
                                }
                            }
                            if (d.column == 'Scanner RRF') {
                                return '<b>' + d.value + '</b>';
                            }
                            else {
                                return d.value;
                            }
                        });
                        
                    return table;
                }

                // Render the table(s)
                tabulate(data, roomOther); // 5 columns table
                d3.select(containerSelector).append('span').text(containerLegend);
            }
        }

        // ---------------------------------
        // Activity
        // ---------------------------------

        if (activity !== undefined && activity.length != 0) {
            if (activityOld !== JSON.stringify(activity)) {
                activityOld = JSON.stringify(activity);

                const containerSelector = '.activity-graph';
                const containerTitle = '<div class="icon"><i class="icofont-spreadsheet"></i></div> ' +'Activité heure par heure par TX';
                const containerLegend = 'Cet histogramme représente le nombre de passages en émission, heure par heure. Seuls les passages en émission de plus de 3 secondes sont comptabilisés.';

                d3.select(containerSelector).html('');
                d3.select(containerSelector).append('h2').html(containerTitle);

                data = activity;

                data.forEach(function(d) {
                    d.Hour = d.Hour;
                    d.TX = d.TX;
                });

                var color = colorSelected;
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

                var svgActivity = d3.select(containerSelector)
                    .append('svg')
                    .attr('width', width + margin.left + margin.right)
                    .attr('height', height + margin.top + margin.bottom)
                    .append('g')
                    .attr('transform',
                        'translate(' + margin.left + ',' + margin.top + ')');

                // Add axis
                svgActivity.append('g')
                    .attr('class', 'x axis')
                    .attr('transform', 'translate(0,' + (height + 0.5) + ')')
                    .call(xAxis)
                    .selectAll('text')
                    .style('text-anchor', 'end')
                    .attr('dx', '-.8em')
                    .attr('dy', '-.55em')
                    .attr('transform', 'rotate(-45)');

                svgActivity.append('g')
                    .attr('class', 'y axis')
                    .call(yAxis)
                    .append('text')
                    .attr('transform', 'rotate(0)')
                    .attr('y', -10)
                    .attr('dy', '.71em')
                    .style('text-anchor', 'end')
                    .text('TX');

                // Add bar chart
                svgActivity.selectAll('bar')
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

                svgActivity.selectAll('text.bar')
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
            }
        }

        // ---------------------------------
        // Best
        // ---------------------------------

        if (best !== undefined && best.length != 0) {
            if (bestOld !== JSON.stringify(best)) {
                bestOld = JSON.stringify(best);

                const containerSelector = '.best-graph';
                const containerTitle = '<div class="icon"><i class="icofont-spreadsheet"></i></div> ' + 'Top 20 des links les plus actifs par TX';
                const containerLegend = 'Cet histogramme représente le classement des 20 links les plus actifs de la journée, en terme de passages en émission.';

                d3.select(containerSelector).html('');
                d3.select(containerSelector).append('h2').html(containerTitle);

                data = best;

                data.forEach(function(d) {
                    d.Indicatif = d.Indicatif;
                    d.TX = d.TX;
                });

                var color = colorSelected;
                var yMax = d3.max(data, function(d) {
                    return d.TX
                });
                var yMin = d3.min(data, function(d) {
                    return d.TX
                });
                var colorScale = d3.scale.linear()
                    .domain([yMin, yMax])
                    .range([d3.rgb(color).brighter(), d3.rgb(color).darker()]);

                const svgBest = d3.select(containerSelector)
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
                svgBest.append('g')
                    .attr('class', 'x axis')
                    .attr('transform', 'translate(0,' + (height + 0.5) + ')')
                    .call(xAxis)
                    .selectAll('text')
                    .style('text-anchor', 'end')
                    .attr('dx', '-.8em')
                    .attr('dy', '-.55em')
                    .attr('transform', 'rotate(-45)');

                svgBest.append('g')
                    .attr('class', 'y axis')
                    .call(yAxis)
                    .append('text')
                    .attr('transform', 'rotate(0)')
                    .attr('y', -10)
                    .attr('dy', '.71em')
                    .style('text-anchor', 'end')
                    .text('TX');

                // Add bar chart
                svgBest.selectAll('bar')
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

                svgBest.selectAll('text.bar')
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

            }
        }

        // ---------------------------------
        // Bubble
        // ---------------------------------

        if (allExtended !== undefined && allExtended.length != 0) {
            if (bubbleOld !== JSON.stringify(allExtended)) {
                bubbleOld = JSON.stringify(allExtended);

                indicatif = sessionStorage.getItem('indicatif');

                var diameter = width + margin.left + margin.right,
                    format = d3.format(',d')
                color = d3.scale.category20c();

                var bubble = d3.layout.pack()
                    .sort(null)
                    .size([diameter, diameter])
                    .padding(1);

                const containerSelector = '.all-bubble';
                const containerTitle = '<div class="icon"><i class="icofont-badge"></i></div> ' + 'Classement des links par durée cumulée en émission';
                const containerLegend = 'Ce graphe présente le classement par durée cumulée en émission, des links actifs dans la journée.';

                d3.select(containerSelector).html('');
                d3.select(containerSelector).append('h2').html(containerTitle);

                data = allExtended;

                const svg = d3.select(containerSelector)
                    .append('svg')
                    .attr('width', diameter)
                    .attr('height', diameter);

                tmp = '{' +
                    '"children":' + JSON.stringify(data) +
                    '}';

                data = JSON.parse(tmp)

                var color = colorSelected;

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
                    if (d.Indicatif === indicatif) {
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
                        if (d.className === indicatif) {
                            return 'lightslategray';
                        }
                        return colorScale(d.value);
                    });

                node.append('text')
                    .attr('class', 'value')
                    .attr('dy', '.3em')
                    .style('fill', function(d) {
                        if (d.className === indicatif) {
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
            }
        }

        // ---------------------------------
        // Transmit
        // ---------------------------------

        if (transmit !== undefined) {
            if (transmitOld !== JSON.stringify(transmit)) {
                transmitOld = JSON.stringify(transmit);

                data = transmit;

                var tot = data[0].TOT;
                var indicatif = data[0].Indicatif;
                var latitude = parseFloat(data[0].Latitude);
                var longitude = parseFloat(data[0].Longitude);
                var distance = 0;

                if (latitude !== 0) {
                    distance = computeDistance(latitude, longitude);
                }

                sessionStorage.setItem('indicatif', indicatif);

                if (tot == 0) {
                    title = '<div class="icon"><i class="icofont-mic-mute"></i></div> ' + 'Aucune émission';
                    
                } else {
                    //title = Indicatif + ' en émission';
                    title = '<div class="icon"><i class="icofont-mic"></i></div> ' + indicatif;
                    if (distance !== 0) {
                        title += ' (~ ' + distance + ' Km)';
                    }
                    else {
                        title += ' en émission';
                    }
                }

                const containerSelector = '.tot-graph';
                const containerTitle = title;
                const containerLegend = 'Affiche l\'indicatif du link en cours d\'émission, la distance approximative de ce link, ainsi que la durée de passage en émission.';

                d3.select(containerSelector).html('');
                d3.select(containerSelector).append('h2').html(containerTitle);

                var svgTot = d3.select(containerSelector)
                    .append('div')
                    .attr('class', 'clock')

                clock = new FlipClock($('.clock'), tot, {
                    clockFace: 'MinuteCounter',
                    language: 'french',
                    clockFaceOptions: {
                        autoPlay: false,
                        autoStart: false
                    }
                });

                d3.select(containerSelector).append('span').text(containerLegend);
            }
            else {
                clock.stop(function() {});
            }
        }

        // ---------------------------------
        // Last
        // ---------------------------------

        if (last !== undefined && last.length != 0) {
            if (lastOld !== JSON.stringify(last)) {
                lastOld = JSON.stringify(last);

                const containerSelector = '.last-table';
                const containerTitle = '<div class="icon"><i class="icofont-wall-clock"></i></div> ' + 'Derniers passages en émission';
                const containerLegend = 'Ce tableau présente la liste des 10 derniers passages en émission : horodatage, indicatif du link, durée en émission et éventuellement durée des blancs si infèrieure à 5 secondes. Les durées en émission de moins de 3 secondes sont grisées et comptabilisées comme déclenchements intempestifs.';

                data = last;

                data.forEach(function(d) {
                    d.Durée = d.Durée.replace(':', 'm ');
                    d.Durée += 's';

                    if (d.Durée < '00m 03s') {
                        d.Durée = '<h3>' + d.Durée + '</h3>';
                    }

                    if (d.Blanc.length == 5) {
                        tmp = d.Blanc;
                        if (tmp.slice(0, 2) == '00' && tmp.slice(-2) <= '05') {
                            d.Blanc = '<h3>' +  tmp.slice(-2) + 's</h3>';
                        }
                        else {
                            d.Blanc = ' ✓ ';
                        }
                    }
                    else {
                        d.Blanc = ' ✓ '; 
                    }
                });

                function tabulate(data, columns) {
                    d3.select(containerSelector).html('');
                    d3.select(containerSelector).append('h2').html(containerTitle);

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
                        .html(function(d) {
                            return d.value;
                        });
                        
                    return table;
                }

                // Render the table(s)
                tabulate(data, ['Heure', 'Indicatif', 'Blanc', 'Durée']); // 4 columns table
                d3.select(containerSelector).append('span').text(containerLegend);
            }
        }

        // ---------------------------------
        // All
        // ---------------------------------

        if (allExtended !== undefined && allExtended.length != 0) {
            if (allExtendedOld !== JSON.stringify(allExtended)) {
                allExtendedOld = JSON.stringify(allExtended);

                const containerSelector = '.all-table';
                const containerTitle = '<div class="icon"><i class="icofont-badge"></i></div> ' + 'Classement des links par durée';
                const containerLegend = 'Ce tableau présente le classement complet par durée des links étant passés en émission dans la journée : position, indicatif du link, nombre de passages et durée cumulée en émission.';

                data = allExtended;

                function tabulate(data, columns) {
                    d3.select(containerSelector).html('');
                    d3.select(containerSelector).append('h2').html(containerTitle);

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
                            if (d.column == 'Durée') {
                                tmp = d.value.split(':');
                                if (d.value.length > 5) {
                                    d.value = tmp[0] + 'h ' + tmp[1] + 'm ' + tmp[2] + 's';
                                }
                                else {
                                    d.value = tmp[0] + 'm ' + tmp[1] + 's';
                                }
                            }
                            if (i === 0) {
                                return '<a onClick="sessionStorage.setItem(\'allExtendedModal\', \'' + d.id + '\');">' + d.value + '</a>';
                            } else {
                                return d.value;
                            }
                        });

                    return table;
                }

                // Render the table(s)
                tabulate(data, ['Pos', 'Indicatif', 'TX', 'Durée']); // 4 columns table
                d3.select(containerSelector).append('span').text(containerLegend);
            }
        }

        // ---------------------------------
        // Porteuse
        // ---------------------------------

        if (porteuseExtended !== undefined && porteuseExtended.length != 0) {
            if (porteuseExtendedOld !== JSON.stringify(porteuseExtended)) {
                porteuseExtendedOld = JSON.stringify(porteuseExtended);

                data = porteuseExtended;

                var porteuseTotal = 0;
                var porteuseView = false;
                var linkTotal = 0;

                data.forEach(function(d) {
                    if (d.TX >= porteuseSelected) {
                        porteuseView = true;
                    }
                    porteuseTotal += d.TX;
                    linkTotal += 1;
                });


                const containerSelector = '.porteuse-table';
                const containerTitle = '<div class="icon"><i class="icofont-bug"></i></div> ' + 'Déclenchements intempestifs';
                
                if (porteuseSelected == 1) {
                    var containerLegend = 'Ce tableau présente le classement des links ayant fait l\'objet d\'au moins <a onClick="porteuse(\'' + porteuseSelected + '\');">' + porteuseSelected + '</a> déclenchement intempestif ou suspects, d\'une durée de moins de 3 secondes : position, indicatif du link et nombre de déclenchement.';
                }
                else {
                    var containerLegend = 'Ce tableau présente le classement des links ayant fait l\'objet d\'au moins <a onClick="porteuse(\'' + porteuseSelected + '\');">' + porteuseSelected + '</a> déclenchements intempestifs ou suspects, d\'une durée de moins de 3 secondes : position, indicatif du link et nombre de déclenchement.';                    
                }

                if (linkTotal == 1) {
                    var containerTotal = 'Aujourd\'hui, il y a eu un total de 1 déclenchement, en provenance de 1 link.';
                }
                else if (linkTotal > 1) {
                    var containerTotal = 'Aujourd\'hui, il y a eu un total de ' + porteuseTotal + ' déclenchements, en provenance de ' + linkTotal + ' links distincts.';
                } 

                function tabulate(data, columns) {
                    d3.select(containerSelector).html('');
                    d3.select(containerSelector).append('h2').html(containerTitle);

                    d3.select(containerSelector).append('span').text(containerTotal);

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
                            if (column === 'TX') {
                                return 'Nb';
                            } 
                            else {
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
                            if(row.TX < porteuseSelected) {
                                return 0;
                            }
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
                                return '<a onClick="sessionStorage.setItem(\'porteuseExtendedModal\', \'' + d.id + '\');">' + d.value + '</a>';
                            } else {
                                return d.value;
                            }
                        });

                    return table;
                }

                // Render the table(s)
                if (porteuseView == true) {
                    tabulate(data, ['Pos', 'Indicatif', 'TX']); // 3 columns table
                    d3.select(containerSelector).append('span').html(containerLegend);
                }
                else {
                    d3.select(containerSelector).html('');
                }
            }
        }

        // ---------------------------------
        // Tot
        // ---------------------------------

        if (totExtended !== undefined && totExtended.length != 0) {
            if (totExtendedOld !== JSON.stringify(totExtended)) {
                totExtendedOld = JSON.stringify(totExtended);

                data = totExtended;

                var totTotal = 0;
                var totView = true;
                var linkTotal = 0;

                data.forEach(function(d) {
                    totTotal += d.TX;
                    linkTotal += 1;
                });

                const containerSelector = '.tot-table';
                const containerTitle = '<div class="icon"><i class="icofont-not-allowed"></i></div> ' + 'Time Out Timer (TOT)';
                const containerLegend = 'Ce tableau présente le classement des links ayant fait l\'objet d\'au moins 1 TOT : position, indicatif du link et nombre de TOT.';
                

                if (totTotal == 1) {
                    var containerTotal = 'Aujourd\'hui, il y a eu un total de 1 TOT, en provenance de 1 link.';
                }
                else if (totTotal > 1) {
                    var containerTotal = 'Aujourd\'hui, il y a eu un total de ' + totTotal + ' TOT, en provenance de ';
                    if(linkTotal == 1) {
                        containerTotal += '1 link.';
                    }
                    else {
                        containerTotal += linkTotal + ' links distincts.';
                    }
                } 

                function tabulate(data, columns) {
                    d3.select(containerSelector).html('');
                    d3.select(containerSelector).append('h2').html(containerTitle);

                    d3.select(containerSelector).append('span').text(containerTotal);

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
                            if (column === 'TX') {
                                return 'Nb';
                            } 
                            else {
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
                                    value: row[column],
                                    id: row.Pos
                                };
                            });
                        })
                        .enter()
                        .append('td')
                        .html(function(d, i) {
                            if (i === 0) {
                                return '<a onClick="sessionStorage.setItem(\'totExtendedModal\', \'' + d.id + '\');">' + d.value + '</a>';
                            } else {
                                return d.value;
                            }
                        });

                    return table;
                }

                // Render the table(s)
                if (totView == true) {
                    tabulate(data, ['Pos', 'Indicatif', 'TX']); // 3 columns table
                    d3.select(containerSelector).append('span').html(containerLegend);
                }
                else {
                    d3.select(containerSelector).html('');
                }
            }
        }

        // ---------------------------------
        // Node extended
        // ---------------------------------

        if (nodeExtendedModal != null) {
            if (nodeExtended !== undefined) {

                const containerSelector = '#node-extended-modal';
                const containerTitle = '<div class="icon"><i class="icofont-info-circle"></i></div> ' + 'Liste des links connectés';
                const containerLegend = 'Ce tableau présente la liste des links actuellement connectés.';

                data = nodeExtended;

                function tabulate(data, columns) {
                    d3.select(containerSelector).html('');
                    d3.select(containerSelector).append('h2').html(containerTitle);

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
                        .attr('width', '25%')
                        .text(function(d) {
                            return d.value;
                        });

                    return table;
                }

                // Render the table(s)
                tabulate(data, ['Node 0', 'Node 1', 'Node 2', 'Node 3']); // 8 columns table
                d3.select(containerSelector).append('span').text(containerLegend);

                $('#node-extended-modal').modal();
                sessionStorage.removeItem('nodeExtendedModal');
            }
        }

        // ---------------------------------
        // Porteuse extended
        // ---------------------------------

        if (porteuseExtendedModal != null) {
            if (porteuseExtended !== undefined) {

                data = [porteuseExtended[parseInt(porteuseExtendedModal) - 1]];

                const containerSelector = '#porteuse-extended-modal';
                const containerTitle = '<div class="icon"><i class="icofont-info-circle"></i></div> ' + 'Déclenchements intempestifs sur ' + data[0].Indicatif;
                const containerLegend = 'Ce tableau présente les heures de passages en émission intempestifs ou suspects, d\'une durée de moins de 3 secondes sur le link sélectionné.';

                function tabulate(data, columns) {
                    d3.select(containerSelector).html('');
                    d3.select(containerSelector).append('h2').html(containerTitle);

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
                            } 
                            else if (column === 'TX') {
                                return 'Nb';
                            }
                            else {
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
                sessionStorage.removeItem('porteuseExtendedModal');

            }
        }

        // ---------------------------------
        // Tot extended
        // ---------------------------------

        if (totExtendedModal != null) {
            if (totExtended !== undefined) {

                data = [totExtended[parseInt(totExtendedModal) - 1]];

                const containerSelector = '#tot-extended-modal';
                const containerTitle = '<div class="icon"><i class="icofont-info-circle"></i></div> ' + 'Time Out Timer sur ' + data[0].Indicatif;
                const containerLegend = 'Ce tableau présente les heures de TOT sur le link sélectionné.';

                function tabulate(data, columns) {
                    d3.select(containerSelector).html('');
                    d3.select(containerSelector).append('h2').html(containerTitle);

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
                            } 
                            else if (column === 'TX') {
                                return 'Nb';
                            }
                            else {
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

                $('#tot-extended-modal').modal();
                sessionStorage.removeItem('totExtendedModal');

            }
        }

        // ---------------------------------
        // All extended
        // ---------------------------------

        if (allExtendedModal != null) {
            if (allExtended !== undefined) {

                data = [allExtended[parseInt(allExtendedModal) - 1]];

                const containerSelector = '#all-extended-modal';
                const containerTitle = '<div class="icon"><i class="icofont-wall-cloc"></i></div> ' + 'Détail des passages en émission sur ' + data[0].Indicatif;
                const containerLegend = 'Ce tableau présente les heures et durées en émission sur le link sélectionné, ainsi que le nombre de passages en émission.';

                function tabulate(data, columns) {
                    d3.select(containerSelector).html('');
                    d3.select(containerSelector).append('h2').html(containerTitle);

                    var table = d3.select(containerSelector).append('table');
                    var thead = table.append('thead');
                    var tbody = table.append('tbody');

                    // Append the header row
                    thead.append('tr')
                        .selectAll('th')
                        .data(columns).enter()
                        .append('th')
                        .text(function(column) {
                            if (column === 'TX') {
                                return 'Nb';
                            }
                            else if (column === 'Chrono') {
                                return 'Durée';
                            }
                            else {
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
                            if (i === 2) {
                                list = d.value.split(', ')
                                value_new = '';

                                list.forEach(function(element) {
                                    tmp = element.split(':');
                                    if (element.length > 5) {
                                        value_new += tmp[0] + 'h ' + tmp[1] + 'm ' + tmp[2] + 's, ';
                                    }
                                    else {
                                        value_new += tmp[0] + 'm ' + tmp[1] + 's, ';
                                    }
                                });
                                d.value = value_new;
                            }
                            if (i === 1 || i === 2) {
                                return d.value.replace(/, /g, '<br/>');
                            } else {
                                return d.value;
                            }
                        });

                    return table;
                }

                // Render the table(s)                    
                tabulate(data, ['Indicatif', 'Heure', 'Chrono', 'TX']); // 4 columns table
                d3.select(containerSelector).append('span').text(containerLegend);

                $('#all-extended-modal').modal();
                sessionStorage.removeItem('allExtendedModal');

            }
        }

        // ---------------------------------
        // Author and Color
        // ---------------------------------

        if (userCountOld != sessionStorage.getItem('user') || colorSelectedOld != localStorage.getItem('color') || porteuseSelectedOld != localStorage.getItem('porteuse')) {
            userCountOld = sessionStorage.getItem('user');

            if(colorSelectedOld != localStorage.getItem('color')) {
                colorSelectedOld = localStorage.getItem('color');

                activityOld = '';
                bestOld = '';
                bubbleOld = '';
            }

            if(porteuseSelectedOld != localStorage.getItem('porteuse')) {
                porteuseSelectedOld = localStorage.getItem('porteuse');

                porteuseExtendedOld = '';
            }

            const containerSelector = '.author-legend';
            var containerAuthor = '<a href="https://github.com/armel/RRFTracker_Web">RRFTracker</a> est un projet Open Source, développé par <a href="https://www.qrz.com/db/F4HWN">F4HWN Armel</a>, sous licence MIT. ';

            containerAuthor += '<br>Couleur actuelle du thème <a onClick="color(\'' + colorSelected + '\');">' + colorSelected + '</a>.';

            if (userCountOld > 1)
                containerAuthor += ' Actuellement ' + userCountOld + ' utilisateurs sont en ligne.';
            else if(userCountOld == 1)
                containerAuthor += ' Actuellement ' + userCountOld + ' utilisateur est en ligne.';

            d3.select(containerSelector).html('');
            d3.select(containerSelector).append('span')
                .attr('class', 'author')
                .html(containerAuthor);

        }
    }

})();
