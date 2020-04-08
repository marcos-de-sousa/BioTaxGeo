window.addEventListener("load", function () {

  const loader = document.querySelector(".loader");
  setTimeout(() => {loader.className += " hidden";}, 500);
  
 }
);

// window.addEventListener("loadstart", function () {

//   const loader = document.querySelector(".loader hidden");
//   loader.className == " loader";
// });

// window.addEventListener("progress", function () {

//   const loader = document.querySelector(".loader hidden");
//   loader.className == " loader";
// });