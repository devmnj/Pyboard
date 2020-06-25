Morris.Donut({
  element: 'm_donut_formatter',
  data: [
    {value: 70, label: 'foo', formatted: 'at least 70%' },
    {value: 15, label: 'bar', formatted: 'approx. 15%' },
    {value: 10, label: 'baz', formatted: 'approx. 10%' },
    {value: 5, label: 'A really really long label', formatted: 'at most 5%' }
  ],
  formatter: function (x, data) { return data.formatted; }
});

