window.onload = (ev) => {
  $("#connect").submit((ev) => {
    ssid = ev.target[0].value;
    pass = ev.target[1].value;
    $.post("/api/connect", { ssid, pass })
      .done(() => {})
      .fail(() => {});
    return false;
  });
};
