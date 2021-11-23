function rand() {
    return Math.random();
}
var plot1 = { y: [1,2,3].map(rand),
    mode: 'lines',
    line: {color: 'black'}
};

var plot2 = {
    y: [10,20,30].map(rand),
    mode: 'lines',
    line: {color: 'black'}
};
Plotly.newPlot('tester1', plot1)

var cnt = 0;

var interval = setInterval(function() {

    Plotly.extendTraces('tester1', {
        y: [[rand()]]
    }, [0])

    if(++cnt === 100) clearInterval(interval);
}, 300);

Plotly.newPlot('tester2', [{
    y: [1,2,3].map(rand),
    mode: 'lines',
    line: {color: 'black'}
}]);