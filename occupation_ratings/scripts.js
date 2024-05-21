// Sample data
const data = [
    { occupation: 'Doctor', prestige: 86 },
    { occupation: 'Engineer', prestige: 76 },
    { occupation: 'Teacher', prestige: 66 },
    { occupation: 'Nurse', prestige: 70 },
    { occupation: 'Artist', prestige: 60 }
];

// Set dimensions and margins for the chart
const margin = {top: 20, right: 30, bottom: 40, left: 40},
      width = 800 - margin.left - margin.right,
      height = 500 - margin.top - margin.bottom;

// Append the SVG object to the chart div
const svg = d3.select("#chart")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

// Set the x scale
const x = d3.scaleBand()
    .domain(data.map(d => d.occupation))
    .range([0, width])
    .padding(0.1);

// Set the y scale
const y = d3.scaleLinear()
    .domain([0, 100])
    .range([height, 0]);

// Add the x Axis
svg.append("g")
    .attr("transform", `translate(0,${height})`)
    .call(d3.axisBottom(x));

// Add the y Axis
svg.append("g")
    .call(d3.axisLeft(y));

// Add the bars
svg.selectAll(".bar")
    .data(data)
    .enter()
    .append("rect")
    .attr("class", "bar")
    .attr("x", d => x(d.occupation))
    .attr("y", d => y(d.prestige))
    .attr("width", x.bandwidth())
    .attr("height", d => height - y(d.prestige))
    .attr("fill", "#69b3a2");