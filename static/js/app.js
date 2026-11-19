const App = {
  state: { datasets: [], selection: { datasetId: null, columns: [] } },
  async start() {
    await this.loadPartials();
    DatasetsTab.init();
    SetsTab.init();
    CartesianTab.init();
    RelationsTab.init();
    EquivalenceTab.init();
    JoinsTab.init();
    AnalysisTab.init();
    document.querySelectorAll("nav button").forEach(button => button.addEventListener("click", () => this.showTab(button.dataset.tab)));
    await this.loadDatasets();
    this.showTab("datasets");
  },
  async loadPartials() {
    await Promise.all(["datasets", "sets", "cartesian", "relations", "equivalence", "joins", "analysis"].map(async name => { document.querySelector("#tab-" + name).innerHTML = await (await fetch("/partials/" + name + ".html")).text(); }));
  },
  showTab(name) {
    document.querySelectorAll(".tab").forEach(tab => tab.classList.toggle("active", tab.id === "tab-" + name));
    document.querySelectorAll("nav button").forEach(button => button.classList.toggle("active", button.dataset.tab === name));
    if (name === "analysis") AnalysisTab.refresh();
    if (name === "equivalence") EquivalenceTab.refresh();
  },
  async loadDatasets() {
    const data = await Api.get("/api/datasets");
    this.state.datasets = data.datasets;
    document.dispatchEvent(new CustomEvent("datasets-changed"));
  }
};

document.addEventListener("DOMContentLoaded", () => App.start().catch(error => Ui.toast(error.message, "error")));
