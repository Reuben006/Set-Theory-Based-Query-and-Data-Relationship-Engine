const AnalysisTab = {
  init() { document.querySelector("#analysis-refresh").addEventListener("click", () => this.refresh()); },
  async refresh() {
    try { const [overview, results] = await Promise.all([Api.get("/api/results/overview"), Api.get("/api/results")]); Ui.renderStats(document.querySelector("#analysis-overview"), overview); const container = document.querySelector("#analysis-results"); if (!results.results.length) { container.textContent = "No saved results yet."; return; } container.innerHTML = `<div class="table-wrap"><table><thead><tr><th>Id</th><th>Kind</th><th>Label</th><th>Created</th><th></th></tr></thead><tbody>${results.results.map(item => `<tr><td>${Ui.escape(item.result_id)}</td><td>${Ui.escape(item.kind)}</td><td>${Ui.escape(item.label)}</td><td>${Ui.escape(item.created_at)}</td><td><button data-result="${item.result_id}" class="secondary">Details</button></td></tr>`).join("")}</tbody></table></div>`; container.querySelectorAll("[data-result]").forEach(button => button.addEventListener("click", () => this.details(button.dataset.result))); } catch (error) { Ui.toast(error.message, "error"); }
  },
  async details(resultId) {
    try { const data = await Api.get(`/api/results/${resultId}`); const container = document.querySelector("#analysis-detail"); container.innerHTML = ""; Ui.renderSummary(container, data.summary); const stats = document.createElement("div"); Ui.renderStats(stats, data.stats); container.append(stats); Ui.renderExportButton(container, resultId); } catch (error) { Ui.toast(error.message, "error"); }
  }
};
