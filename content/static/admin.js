// secret.js — JS for the secret grants detail page
// Author: Pito Salas and Claude Code
// Open Source Under MIT license

(function () {
  var ALL_ROWS = window.SECRET_ROWS;
  var YEARS = window.SECRET_YEARS;

  var select = document.getElementById("year-select");
  var summaryText = document.getElementById("summary-text");

  function formatAmount(n) {
    return "XCG\u00a0" + n.toLocaleString("en-US", { minimumFractionDigits: 0, maximumFractionDigits: 0 });
  }

  function fmt(n) {
    return n ? n.toLocaleString("en-US", { maximumFractionDigits: 0 }) : "";
  }

  function toGridRows(rows) {
    return rows.map(function (r) {
      return [r.date, r.nonprofit, formatAmount(r.amount), r.notes];
    });
  }

  function updateSummary(rows) {
    var total = rows.reduce(function (s, r) { return s + r.amount; }, 0);
    var orgs = new Set(rows.map(function (r) { return r.nonprofit; })).size;
    summaryText.textContent = rows.length + " grants to " + orgs + " different organizations for a total of " + formatAmount(total);
  }

  var currentRows = YEARS.length ? ALL_ROWS.filter(function (r) { return r.year === YEARS[0]; }) : ALL_ROWS;
  updateSummary(currentRows);

  var grid = new gridjs.Grid({
    columns: [
      { name: "Date", width: "10%" },
      { name: "Organization", width: "25%" },
      { name: "Amount", width: "12%" },
      { name: "Notes", width: "53%" },
    ],
    data: toGridRows(currentRows),
    search: true,
    sort: true,
    pagination: { limit: 50 },
  }).render(document.getElementById("grants-grid"));

  select.addEventListener("change", function () {
    var val = select.value;
    var rows = val === "all" ? ALL_ROWS : ALL_ROWS.filter(function (r) { return r.year === parseInt(val, 10); });
    updateSummary(rows);
    grid.updateConfig({ data: toGridRows(rows) }).forceRender();
  });

  // Org-by-year matrix
  var allYears = Array.from(new Set(ALL_ROWS.map(function (r) { return r.year; }))).sort().reverse();
  var allOrgs  = Array.from(new Set(ALL_ROWS.map(function (r) { return r.nonprofit; }))).sort();
  var sums = {};
  allOrgs.forEach(function (o) { sums[o] = {}; });
  ALL_ROWS.forEach(function (r) {
    sums[r.nonprofit][r.year] = (sums[r.nonprofit][r.year] || 0) + r.amount;
  });

  var gridCols = [{ name: "Organization", sort: false }].concat(
    allYears.map(function (y) { return { name: String(y), sort: false }; }),
    [{ name: "Total", sort: false }]
  );

  var gridData = allOrgs.map(function (o) {
    var rowTotal = 0;
    var cells = [o].concat(allYears.map(function (y) {
      var v = sums[o][y] || 0;
      rowTotal += v;
      return fmt(v);
    }));
    cells.push(fmt(rowTotal));
    return cells;
  });

  var grandTotal = 0;
  var totalsRow = ["Total"].concat(allYears.map(function (y) {
    var ct = allOrgs.reduce(function (s, o) { return s + (sums[o][y] || 0); }, 0);
    grandTotal += ct;
    return fmt(ct);
  }));
  totalsRow.push(fmt(grandTotal));
  gridData.push(totalsRow);

  new gridjs.Grid({
    columns: gridCols,
    data: gridData,
    sort: false,
    search: false,
    pagination: false,
  }).render(document.getElementById("org-year-grid"));
}());
