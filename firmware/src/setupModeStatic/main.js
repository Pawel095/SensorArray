window.onload = (ev) => {
  $("#connect").submit((ev) => {
    ssid = ev.target[0].value;
    pass = ev.target[1].value;
    $.post("/api/connect", JSON.stringify({ ssid, pass }))
      .done(() => {
        let self = setInterval(() => {
          $.get("/api/connect").done((data) => {
            console.log(data);
            switch (data) {
              case "0":
                $("#result").text("Idle; check ssid and password");
                setTimeout(() => {
                  clearInterval(self);
                }, 100);
                break;
              case "1":
                $("#result").text("Connecting");
                break;
              case "2":
                $("#result").text("Wrong Password");
                setTimeout(() => {
                  clearInterval(self);
                }, 100);
                break;
              case "3":
                $("#result").text("Wrong SSID");
                setTimeout(() => {
                  clearInterval(self);
                }, 100);
                break;
              case "4":
                $("#result").text("Unknown error");
                setTimeout(() => {
                  clearInterval(self);
                }, 100);
                break;
              case "5":
                $("#result").text("Connected!");
                setTimeout(() => {
                  clearInterval(self);
                }, 100);
                
                break;
              default:
                break;
            }
          });
        }, 500);
      })
      .fail(() => {});
    return false;
  });
};
