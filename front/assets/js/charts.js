;
(function() {
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
    }, 500);

    var old_abstract = '';
    var old_best = '';
    var old_activity = '';
    var old_last = '';
    var old_all = '';
    var old_porteuse = '';

    console.log(old_abstract);


    function generateD3Charts(redraw = false) {
        if (redraw === true) {
            console.log("rezise");
            old_abstract = '';
            old_best = '';
            old_activity = '';
            old_last = '';
            old_all = '';
            old_porteuse = '';
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

            if (data !== undefined) {
                TOT = data[0].TOT;
                Indicatif = data[0].Indicatif;
            }

            if (TOT == 0) {
                title = 'Aucune émission';
            } else {
                title = Indicatif + ' en émission';
            }

            const containerTitle = title;
            const containerLegend = 'Affiche l\'indicatif du nœud en cours d\'émission ainsi que la durée de passage en émission.';

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
            }
            else {
                return 0;
            }

            console.log("activity redraw");

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
            }
            else {
                return 0;
            }

            console.log("best redraw");

            const containerSelector = '.best-graph';
            const containerTitle = 'Top 20 des nœuds les plus actifs';
            const containerLegend = 'Cet histogramme représente le classement des 20 nœuds les plus actifs de la journée, en terme de passages en émission.';
            const containerAuthor = 'RRFTracker est un projet Open Source, développé par F4HWN Armel, sous licence MIT.';

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
            d3.select(containerSelector).append('span')
                                        .attr('class', 'author')
                                        .text(containerAuthor);
        });

        // Abstract
        // Load the data
        d3.json('abstract.json', function(error, data) {
            if (old_abstract !== JSON.stringify(data)) {
                old_abstract = JSON.stringify(data);
            }
            else {
                return 0;
            }

            console.log("abstract redraw");

            const containerSelector = '.abstract-graph';
            const containerTitle = 'Résumé de la journée';
            const containerLegend = 'Ce tableau présente le résumé de l\'activité du salon dans la journée: nombre de passages en émission total, durée cumulée en émission, nombre de nœuds actifs, total, max et min.';

            function tabulate(data, columns) {
                d3.select(containerSelector).html('');
                d3.select(containerSelector).append('h2').text(containerTitle);

                const table = d3.select(containerSelector).append('table');
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
                    .text(function(d) {
                        return d.value;
                    });

                return table;
            }

            // Render the table(s)
            tabulate(data, ['Salon', 'Date', 'TX total', 'Emission cumulée', 'Nœuds actifs', 'Nœuds total', 'Nœuds max / min']); // 7 columns table
            d3.select(containerSelector).append('span').text(containerLegend);
        });

        // Last
        // Load the data
        d3.json('last.json', function(error, data) {
            if (old_last !== JSON.stringify(data)) {
                old_last = JSON.stringify(data);
            }
            else {
                return 0;
            }

            console.log("last redraw");

            const containerSelector = '.last-graph';
            const containerTitle = 'Derniers passages en émission';
            const containerLegend = 'Ce tableau présente la liste des 10 derniers passages en émission: horodatage, indicatif du nœud et durée en émission.';

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
            }
            else {
                return 0;
            }

            console.log("all redraw");

            const containerSelector = '.all-graph';
            const containerTitle = 'Classement des nœuds actifs';
            const containerLegend = 'Ce tableau présente le classement complet des nœuds étant passés en émission dans la journée: position, indicatif du nœud, nombre de passages et durée cumulée en émission.';

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
            }
            else {
                return 0;
            }

            console.log("porteuse redraw");

            const containerSelector = '.porteuse-graph';
            const containerTitle = 'Déclenchements intempestifs';
            const containerLegend = 'Ce tableau présente le classement complet des nœuds ayant fait l\'objet de passages en émission intempestifs ou suspects, d\'une durée de moins de 3 secondes: position, indicatif du nœud et nombre de passages en émission.';

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
                tabulate(data, ['Pos', 'Indicatif', 'TX']); // 3 columns table
                d3.select(containerSelector).append('span').text(containerLegend);
            }
        });
    }
})();