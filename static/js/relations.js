const RelationsTab = {
  init() {
    this.pickerA = Ui.createSetPicker(document.querySelector("#relations-picker-a"), "Set A");
    this.pickerB = Ui.createSetPicker(document.querySelector("#relations-picker-b"), "Set B");
    this.manualA = Ui.createSetPicker(
      document.querySelector("#relations-manual-picker-a"),
      "Set A",
    );
    this.manualB = Ui.createSetPicker(
      document.querySelector("#relations-manual-picker-b"),
      "Set B",
    );
    document.querySelector("#relations-mode").addEventListener("change", () => this.showMode());
    document
      .querySelector("#relations-rows-dataset")
      .addEventListener("change", () => this.loadRowColumns());
    document.querySelector("#relations-build").addEventListener("click", () => this.build());
    document.querySelector("#relations-check").addEventListener("click", () => this.check());
    document.addEventListener("datasets-changed", () => this.refreshRows());
    this.refreshRows();
  },
  showMode() {
    const mode = document.querySelector("#relations-mode").value;
    ["rule", "manual", "rows"].forEach((name) =>
      document
        .querySelector(`#relations-${name}-block`)
        .classList.toggle("hidden", (name === "rows" ? "from_rows" : name) !== mode),
    );
  },
  refreshRows() {
    Ui.fillSelect(
      document.querySelector("#relations-rows-dataset"),
      App.state.datasets,
      "dataset_id",
      "name",
    );
    this.loadRowColumns();
  },
  async loadRowColumns() {
    const id = document.querySelector("#relations-rows-dataset").value;
    if (!id) return;
    try {
      const data = await Api.get(`/api/datasets/${id}/columns`);
      ["#relations-rows-col-a", "#relations-rows-col-b"].forEach((selector) =>
        Ui.fillSelect(document.querySelector(selector), data.columns, "name", "name"),
      );
    } catch (error) {
      Ui.toast(error.message, "error");
    }
  },
  async build() {
    const mode = document.querySelector("#relations-mode").value;
    let body = { mode };
    if (mode === "rule")
      body = {
        mode,
        set_a: this.pickerA.getValue(),
        set_b: this.pickerB.getValue(),
        rule: document.querySelector("#relations-rule").value,
      };
    if (mode === "manual")
      body = {
        mode,
        set_a: this.manualA.getValue(),
        set_b: this.manualB.getValue(),
        pairs: document
          .querySelector("#relations-manual-pairs")
          .value.split(/\r?\n/)
          .filter(Boolean)
          .map((line) => line.split(",").map((item) => item.trim())),
      };
    if (mode === "from_rows")
      body = {
        mode,
        dataset_id: document.querySelector("#relations-rows-dataset").value,
        column_a: document.querySelector("#relations-rows-col-a").value,
        column_b: document.querySelector("#relations-rows-col-b").value,
      };
    const button = document.querySelector("#relations-build");
    try {
      Ui.setBusy(button, true);
      const data = await Api.post("/api/relations/build", body);
      this.resultId = data.result_id;
      document.querySelector("#relations-check").disabled = false;
      Ui.renderSummary(document.querySelector("#relations-summary"), data.summary);
      Ui.renderStats(document.querySelector("#relations-stats"), data.stats);
      Ui.renderTable(document.querySelector("#relations-result"), ["A", "B"], data.pairs);
      Ui.renderExportButton(document.querySelector("#relations-export"), data.result_id);
    } catch (error) {
      Ui.toast(error.message, "error");
    } finally {
      Ui.setBusy(button, false);
    }
  },
  async check() {
    try {
      const data = await Api.post(`/api/relations/${this.resultId}/properties`, {});
      document.querySelector("#relations-props").innerHTML = this.propertyCards(data);
    } catch (error) {
      Ui.toast(error.message, "error");
    }
  },
  propertyCards(data) {
    const names = ["reflexive", "symmetric", "transitive"];
    return `<p>${Ui.escape(data.summary)}</p><div class="relations-props">${names.map((name) => this.propertyCard(name, data[name])).join("")}</div>`;
  },
  propertyCard(name, property) {
    const status = property.holds ? "YES" : "NO";
    const witnesses = property.witnesses.map((item) => item.join(" → ")).join(", ") || "None";
    return `<div><strong>${name}</strong><p class="${property.holds ? "yes" : "no"}">${status}</p><small>${Ui.escape(witnesses)}</small></div>`;
  },
};
