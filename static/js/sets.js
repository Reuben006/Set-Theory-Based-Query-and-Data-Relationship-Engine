const SetsTab = {
  init() { this.pickerA = Ui.createSetPicker(document.querySelector("#sets-picker-a"), "Set A"); this.pickerB = Ui.createSetPicker(document.querySelector("#sets-picker-b"), "Set B"); document.querySelector("#sets-run").addEventListener("click", () => this.run()); document.querySelector("#sets-swap").addEventListener("click", () => { const a = this.pickerA.getValue(); this.pickerA.setValue(this.pickerB.getValue()); this.pickerB.setValue(a); }); },
  async run() {
    const button = document.querySelector("#sets-run");
    try { Ui.setBusy(button, true); const data = await Api.post("/api/sets/operate", { operation: document.querySelector("#sets-operation").value, set_a: this.pickerA.getValue(), set_b: this.pickerB.getValue() }); Ui.renderSummary(document.querySelector("#sets-summary"), data.summary); Ui.renderStats(document.querySelector("#sets-stats"), data.stats); Ui.renderTable(document.querySelector("#sets-result"), ["Element"], data.elements.map(item => [item])); Ui.renderExportButton(document.querySelector("#sets-export"), data.result_id); if (data.truncated) Ui.toast("Showing the first 1000 elements. Export has all elements.", "success"); } catch (error) { Ui.toast(error.message, "error"); } finally { Ui.setBusy(button, false); }
  }
};
