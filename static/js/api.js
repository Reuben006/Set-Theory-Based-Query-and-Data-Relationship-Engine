const Api = {
  async request(url, options) {
    let response;
    try {
      response = await fetch(url, options);
    } catch (error) {
      throw new Error("Network error. Is the server running?");
    }
    const body = await response.json();
    if (!body.ok) throw new Error(body.error || "Request failed.");
    return body.data;
  },
  get(url) {
    return this.request(url);
  },
  post(url, body) {
    return this.request(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
  },
  del(url) {
    return this.request(url, { method: "DELETE" });
  },
  upload(url, file) {
    const data = new FormData();
    data.append("file", file);
    return this.request(url, { method: "POST", body: data });
  },
  exportUrl(resultId) {
    return "/api/export/" + resultId;
  },
};
