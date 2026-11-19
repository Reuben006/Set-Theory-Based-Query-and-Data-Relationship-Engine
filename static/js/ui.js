const Ui = {
  toast(message, type) {
    const box = document.querySelector("#toast");
    box.textContent = message;
    box.className = "toast-" + type;
    clearTimeout(this.timeout);
    this.timeout = setTimeout(() => {
      box.className = "";
    }, 3000);
  },
  clear(container) {
    container.innerHTML = "";
  },
  renderTable(container, columns, rows) {
    if (!rows.length) {
      container.textContent = "No rows";
      return;
    }
    const headers = columns.map((value) => `<th>${this.escape(value)}</th>`).join("");
    const body = rows
      .map(
        (row) =>
          `<tr>${row.map((value) => `<td${value === null ? ' class="missing"' : ""}>${value === null ? "-" : this.escape(value)}</td>`).join("")}</tr>`,
      )
      .join("");
    container.innerHTML = `<div class="table-wrap"><table><thead><tr>${headers}</tr></thead><tbody>${body}</tbody></table></div>`;
  },
  renderStats(container, stats) {
    this.renderTable(
      container,
      ["Item", "Value"],
      Object.entries(stats).map(([key, value]) => [
        key.replaceAll("_", " "),
        typeof value === "object" ? JSON.stringify(value) : value,
      ]),
    );
  },
  renderSummary(container, text) {
    container.innerHTML = `<p class="summary">${this.escape(text)}</p>`;
  },
  renderExportButton(container, resultId) {
    container.innerHTML = `<a class="button" href="${Api.exportUrl(resultId)}">Download CSV</a>`;
  },
  fillSelect(select, items, valueKey, labelKey) {
    select.innerHTML = `<option value="">-- choose --</option>${items.map((item) => `<option value="${this.escape(item[valueKey])}">${this.escape(item[labelKey])}</option>`).join("")}`;
  },
  setBusy(button, busy) {
    if (!button.dataset.text) button.dataset.text = button.textContent;
    button.disabled = busy;
    button.textContent = busy ? "Working..." : button.dataset.text;
  },
  createSetPicker(container, title) {
    container.innerHTML = `<h3>${title}</h3><select></select><div class="picker-columns"></div><button class="secondary" type="button">Use Datasets selection</button>`;
    const select = container.querySelector("select");
    const columns = container.querySelector(".picker-columns");
    let value = { dataset_id: "", columns: [] };
    const refreshColumns = async () => {
      columns.innerHTML = "";
      if (!select.value) return;
      try {
        const data = await Api.get(`/api/datasets/${select.value}/columns`);
        columns.innerHTML = data.columns
          .map(
            (item) =>
              `<label><input type="checkbox" value="${this.escape(item.name)}" ${value.columns.includes(item.name) ? "checked" : ""}> ${this.escape(item.name)}</label>`,
          )
          .join("");
      } catch (error) {
        this.toast(error.message, "error");
      }
    };
    const refresh = () => {
      const saved = select.value;
      select.innerHTML = `<option value="">-- choose --</option>${App.state.datasets.map((item) => `<option value="${item.dataset_id}">${this.escape(item.name)}</option>`).join("")}`;
      select.value = App.state.datasets.some((item) => item.dataset_id === saved)
        ? saved
        : value.dataset_id;
      refreshColumns();
    };
    select.addEventListener("change", () => {
      value = { dataset_id: select.value, columns: [] };
      refreshColumns();
    });
    container.querySelector("button").addEventListener("click", () => {
      value = {
        dataset_id: App.state.selection.datasetId || "",
        columns: App.state.selection.columns || [],
      };
      select.value = value.dataset_id;
      refreshColumns();
    });
    document.addEventListener("datasets-changed", refresh);
    return {
      getValue: () => ({
        dataset_id: select.value,
        columns: [...columns.querySelectorAll("input:checked")].map((item) => item.value),
      }),
      setValue: (next) => {
        value = next;
        select.value = next.dataset_id;
        refreshColumns();
      },
      refresh,
    };
  },
  escape(value) {
    const node = document.createElement("span");
    node.textContent = value;
    return node.innerHTML;
  },
};
