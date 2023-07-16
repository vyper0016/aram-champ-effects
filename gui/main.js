
eel.expose(updateTable)
function updateTable(data) {
  var existingTable = document.querySelector("table");

  if (existingTable) {
    // Clear existing table content
    while (existingTable.firstChild) {
      existingTable.firstChild.remove();
    }
    table = existingTable;
  } else {
    table = document.createElement("table");
  }

  var headerRow = document.createElement("tr");
  var headers = ["", "Champion", "Damage Dealt", "Damage Received", "Other Effects"];

  headers.forEach(function (header) {
    var th = document.createElement("th");
    th.textContent = header;
    headerRow.appendChild(th);
  });

  table.appendChild(headerRow);

  // Your Champ
  var champRow = document.createElement("tr");

  var yourChampCell = document.createElement("td");
  yourChampCell.textContent = "Your Champ";
  champRow.appendChild(yourChampCell);

  var champData = data.mine;

  var champNameCell = document.createElement("td");
  var champNameDiv = document.createElement("div");
  champNameDiv.className = "name";

  var champIcon = document.createElement("img");
  champIcon.className = "icon";
  champIcon.alt = champData.name;
  champIcon.src = champData.icon;
  champIcon.decoding = "async";
  champIcon.loading = "lazy";
  champIcon.width = 40;
  champIcon.height = 40;

  var champSpan = document.createElement("span");
  champSpan.textContent = champData.name;

  champNameDiv.appendChild(champIcon);
  champNameDiv.appendChild(champSpan);
  champNameCell.appendChild(champNameDiv);

  champRow.appendChild(champNameCell);

  var dmgDealtCell = document.createElement("td");
  dmgDealtCell.textContent = champData.dmg_dealt;
  champRow.appendChild(dmgDealtCell);

  var dmgReceivedCell = document.createElement("td");
  dmgReceivedCell.textContent = champData.dmg_received;
  champRow.appendChild(dmgReceivedCell);

  var otherCell = document.createElement("td");
  var otherList = document.createElement("ul");

  if (champData.other.length > 0) {
    champData.other.forEach(function (effect) {
      var effectItem = document.createElement("li");
      effectItem.textContent = effect;
      otherList.appendChild(effectItem);
    });
  }

  otherCell.appendChild(otherList);
  champRow.appendChild(otherCell);

  table.appendChild(champRow);

  // Tradable Champs
  var tradableHeaderCell = document.createElement("td");
  tradableHeaderCell.id = "tradable";
  tradableHeaderCell.className = "selected_champs";
  tradableHeaderCell.rowSpan = data.tradable.length;
  tradableHeaderCell.textContent = "Tradable Champs";

  var tradableRow = document.createElement("tr");
  tradableRow.appendChild(tradableHeaderCell);

  if (data.tradable.length === 0) {
    tradableHeaderCell.rowSpan = 1;
    var emptyCell = document.createElement("td");
    emptyCell.colSpan = 4;
    emptyCell.textContent = "No tradable champs";
    tradableRow.appendChild(emptyCell);
  } else {
    var firstTradable = data.tradable[0];

    var champNameCell = document.createElement("td");
    var champNameDiv = document.createElement("div");
    champNameDiv.className = "name";

    var champIcon = document.createElement("img");
    champIcon.className = "icon";
    champIcon.alt = firstTradable.name;
    champIcon.src = firstTradable.icon;
    champIcon.decoding = "async";
    champIcon.loading = "lazy";
    champIcon.width = 40;
    champIcon.height = 40;

    var champSpan = document.createElement("span");
    champSpan.textContent = firstTradable.name;

    champNameDiv.appendChild(champIcon);
    champNameDiv.appendChild(champSpan);
    champNameCell.appendChild(champNameDiv);

    var dmgDealtCell = document.createElement("td");
    dmgDealtCell.textContent = firstTradable.dmg_dealt;

    var dmgReceivedCell = document.createElement("td");
    dmgReceivedCell.textContent = firstTradable.dmg_received;

    var otherCell = document.createElement("td");
    otherCell.textContent = firstTradable.other;

    tradableRow.appendChild(champNameCell);
    tradableRow.appendChild(dmgDealtCell);
    tradableRow.appendChild(dmgReceivedCell);
    tradableRow.appendChild(otherCell);
  }

  table.appendChild(tradableRow);

  if (data.tradable.length > 1) {
    for (var i = 1; i < data.tradable.length; i++) {
      var tradable = data.tradable[i];

      var champRow = document.createElement("tr");

      var champNameCell = document.createElement("td");
      var champNameDiv = document.createElement("div");
      champNameDiv.className = "name";

      var champIcon = document.createElement("img");
      champIcon.className = "icon";
      champIcon.alt = tradable.name;
      champIcon.src = tradable.icon;
      champIcon.decoding = "async";
      champIcon.loading = "lazy";
      champIcon.width = 40;
      champIcon.height = 40;

      var champSpan = document.createElement("span");
      champSpan.textContent = tradable.name;

      champNameDiv.appendChild(champIcon);
      champNameDiv.appendChild(champSpan);
      champNameCell.appendChild(champNameDiv);

      var dmgDealtCell = document.createElement("td");
      dmgDealtCell.textContent = tradable.dmg_dealt;

      var dmgReceivedCell = document.createElement("td");
      dmgReceivedCell.textContent = tradable.dmg_received;

      var otherCell = document.createElement("td");
      otherCell.textContent = tradable.other;

      champRow.appendChild(champNameCell);
      champRow.appendChild(dmgDealtCell);
      champRow.appendChild(dmgReceivedCell);
      champRow.appendChild(otherCell);

      table.appendChild(champRow);
    }
  }

  // Bench Champs
  var benchHeaderCell = document.createElement("td");
  benchHeaderCell.id = "bench";
  benchHeaderCell.className = "selected_champs";
  benchHeaderCell.rowSpan = data.bench.length;
  benchHeaderCell.textContent = "Bench Champs";

  var benchRow = document.createElement("tr");
  benchRow.appendChild(benchHeaderCell);

  if (data.bench.length === 0) {
    benchHeaderCell.rowSpan = 1;
    var emptyCell = document.createElement("td");
    emptyCell.colSpan = 4;
    emptyCell.textContent = "No bench champs";
    benchRow.appendChild(emptyCell);
  } else {
    var firstBench = data.bench[0];

    var champNameCell = document.createElement("td");
    var champNameDiv = document.createElement("div");
    champNameDiv.className = "name";

    var champIcon = document.createElement("img");
    champIcon.className = "icon";
    champIcon.alt = firstBench.name;
    champIcon.src = firstBench.icon;
    champIcon.decoding = "async";
    champIcon.loading = "lazy";
    champIcon.width = 40;
    champIcon.height = 40;

    var champSpan = document.createElement("span");
    champSpan.textContent = firstBench.name;

    champNameDiv.appendChild(champIcon);
    champNameDiv.appendChild(champSpan);
    champNameCell.appendChild(champNameDiv);

    var dmgDealtCell = document.createElement("td");
    dmgDealtCell.textContent = firstBench.dmg_dealt;

    var dmgReceivedCell = document.createElement("td");
    dmgReceivedCell.textContent = firstBench.dmg_received;

    var otherCell = document.createElement("td");
    var otherList = document.createElement("ul");

    if (firstBench.other.length > 0) {
      firstBench.other.forEach(function (effect) {
        var effectItem = document.createElement("li");
        effectItem.textContent = effect;
        otherList.appendChild(effectItem);
      });
    }

    otherCell.appendChild(otherList);

    benchRow.appendChild(champNameCell);
    benchRow.appendChild(dmgDealtCell);
    benchRow.appendChild(dmgReceivedCell);
    benchRow.appendChild(otherCell);
  }

  table.appendChild(benchRow);

  if (data.bench.length > 1) {
    for (var i = 1; i < data.bench.length; i++) {
      var bench = data.bench[i];

      var champRow = document.createElement("tr");

      var champNameCell = document.createElement("td");
      var champNameDiv = document.createElement("div");
      champNameDiv.className = "name";

      var champIcon = document.createElement("img");
      champIcon.className = "icon";
      champIcon.alt = bench.name;
      champIcon.src = bench.icon;
      champIcon.decoding = "async";
      champIcon.loading = "lazy";
      champIcon.width = 40;
      champIcon.height = 40;

      var champSpan = document.createElement("span");
      champSpan.textContent = bench.name;

      champNameDiv.appendChild(champIcon);
      champNameDiv.appendChild(champSpan);
      champNameCell.appendChild(champNameDiv);

      var dmgDealtCell = document.createElement("td");
      dmgDealtCell.textContent = bench.dmg_dealt;

      var dmgReceivedCell = document.createElement("td");
      dmgReceivedCell.textContent = bench.dmg_received;

      var otherCell = document.createElement("td");
      var otherList = document.createElement("ul");

      if (bench.other.length > 0) {
        bench.other.forEach(function (effect) {
          var effectItem = document.createElement("li");
          effectItem.textContent = effect;
          otherList.appendChild(effectItem);
        });
      }

      otherCell.appendChild(otherList);

      champRow.appendChild(champNameCell);
      champRow.appendChild(dmgDealtCell);
      champRow.appendChild(dmgReceivedCell);
      champRow.appendChild(otherCell);

      table.appendChild(champRow);
    }
  }

  document.body.appendChild(table);
}
