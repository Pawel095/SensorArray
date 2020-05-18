function getSensorData() {
  $.get("/api/getReading")
    .done((data) => {
      d = JSON.parse(data);
      $("#temp").text(d.temperature);
      $("#humi").text(d.humidity);
      $("#error").text("");
    })
    .fail(() => {
      $("#temp").text("");
      $("#humi").text("");
      $("#error").text("Błąd wczytywania danych");
    });
}
window.onload = (ev) => {
  getSensorData()
  setInterval(getSensorData, 10000);
};
