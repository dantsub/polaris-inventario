$(document).ready(function () {
  var colors = [
    "#1abc9c",
    "#2ecc71",
    "#3498db",
    "#9b59b6",
    "#34495e",
    "#16a085",
    "#27ae60",
    "#2980b9",
    "#8e44ad",
    "#2c3e50",
    "#f1c40f",
    "#e67e22",
    "#e74c3c",
    "#95a5a6",
    "#f39c12",
    "#d35400",
    "#c0392b",
    "#bdc3c7",
    "#7f8c8d",
    "#7367f0",
  ];

  var avatarElement = $(".avatar-initials"),
    avatarWidth = avatarElement.attr("width"),
    avatarHeight = avatarElement.attr("height"),
    name = avatarElement.data("name"),
    initials =
      name.split(" ")[0].charAt(0).toUpperCase() +
      name.split(" ")[1].charAt(0).toUpperCase(),
    charIndex = initials.charCodeAt(0) - 65,
    colorIndex = charIndex % 19;

  avatarElement
    .css({
      "background-color": colors[19],
      width: avatarWidth,
      height: avatarHeight,
      font: avatarWidth / 2 + "px Arial",
      color: "#FFF",
      textAlign: "center",
      lineHeight: avatarHeight + "px",
      borderRadius: "50%",
    })
    .html(initials);
});
