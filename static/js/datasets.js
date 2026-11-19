const DatasetsTab = {
  datasetId: null,
  page: 1,
  init() {
    document.querySelector("#datasets-upload").addEventListener("click", () => this.upload());
    document.querySelector("#datasets-prev").addEventListener("click", () => this.changePage(-1));
    document.querySelector("#datasets-next").addEventListener("click", () => this.changePage(1));
    document.addEventListener("datasets-changed", () => this.renderList());
  },
  async upload() {
    const input = document.querySelector("#datasets-file");
    const button = document.querySelector("#datasets-upload");
    if (!input.files[0]) return Ui.toast("Choose a CSV file first.", "error");
    try { Ui.setBusy(button, true); const data = await Api.upload("/api/datasets", input.files[0]); await App.loadDatasets(); await this.view(data.dataset_id); input.value = ""; Ui.toast("Dataset uploaded.", "success"); } catch (error) { Ui.toast(error.message, "error"); } finally { Ui.setBusy(button, false); }
  },
  renderList() {
    const rows = App.state.datasets.map(item => [item.name, item.rows, item.column_count, `<button data-view="${item.dataset_id}" class="secondary">View</button> <button data-delete="${item.dataset_id}" class="secondary">Delete</button>`]);
    const container = document.querySelector("#datasets-list");
    if (!rows.length) { container.textContent = "No datasets uploaded yet."; return; }
    container.innerHTML = `<div class="table-wrap"><table><thead><tr><th>Name</th><th>Rows</th><th>Columns</th><th>Actions</th></tr></thead><tbody>${rows.map(row => `<tr><td>${Ui.escape(row[0])}</td><td>${row[1]}</td><td>${row[2]}</td><td>${row[3]}</td></tr>`).join("")}</tbody></table></div>`;
    container.querySelectorAll("[data-view]").forEach(button => button.addEventListener("click", () => this.view(button.dataset.view)));
    container.querySelectorAll("[data-delete]").forEach(button => button.addEventListener("click", () => this.remove(button.dataset.delete)));
  },
  async view(datasetId) {
    this.datasetId = datasetId;
    this.page = 1;
    try { await Promise.all([this.loadPreview(), this.loadColumns(), this.loadQuality()]); document.querySelector("#datasets-view").classList.remove("hidden"); } catch (error) { Ui.toast(error.message, "error"); }
  },
  async loadPreview() {
    const data = await Api.get(`/api/datasets/${this.datasetId}?page=${this.page}`);
    document.querySelector("#datasets-info").textContent = `${data.name}: ${data.total_rows} rows, ${data.columns.length} columns`;
    Ui.renderTable(document.querySelector("#datasets-preview"), data.columns, data.rows);
    document.querySelector("#datasets-page").textContent = `Page ${data.page} of ${data.total_pages}`;
    document.querySelector("#datasets-prev").disabled = data.page <= 1;
    document.querySelector("#datasets-next").disabled = data.page >= data.total_pages;
  },
  async loadColumns() {
    const data = await Api.get(`/api/datasets/${this.datasetId}/columns`);
    const selected = App.state.selection.datasetId === this.datasetId ? App.state.selection.columns : [];
    const container = document.querySelector("#datasets-columns");
    container.innerHTML = data.columns.map(column => `<label><input type="checkbox" value="${Ui.escape(column.name)}" ${selected.includes(column.name) ? "checked" : ""}> ${Ui.escape(column.name)} <small>(${column.dtype}, ${column.missing} missing, ${column.unique} unique)</small></label>`).join("");
    container.querySelectorAll("input").forEach(input => input.addEventListener("change", () => this.saveSelection()));
  },
  saveSelection() { App.state.selection = { datasetId: this.datasetId, columns: [...document.querySelectorAll("#datasets-columns input:checked")].map(input => input.value) }; },
  async loadQuality() {
    const data = await Api.get(`/api/datasets/${this.datasetId}/quality`);
    const container = document.querySelector("#datasets-quality");
    container.innerHTML = `<p>${data.duplicate_rows} duplicate rows and ${data.missing_total} missing values.</p>`;
    Ui.renderTable(container, ["Column", "Missing", "Duplicate values"], data.columns.map(item => [item.name, item.missing, item.duplicate_values]));
  },
  async changePage(change) { this.page += change; await this.loadPreview(); },
  async remove(datasetId) {
    if (!confirm("Delete this dataset?")) return;
    try { await Api.del(`/api/datasets/${datasetId}`); if (this.datasetId === datasetId) document.querySelector("#datasets-view").classList.add("hidden"); await App.loadDatasets(); Ui.toast("Dataset deleted.", "success"); } catch (error) { Ui.toast(error.message, "error"); }
  }
};
